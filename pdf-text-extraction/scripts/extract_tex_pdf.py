#!/usr/bin/env python3

import argparse
import re
import zlib
from pathlib import Path


SPACE_THRESHOLD = -235.0
LINE_BREAK_THRESHOLD = 12.0
PDF_DELIMS = b"()<>[]{}/%"
PDF_WS = b"\x00\t\n\x0c\r "


class Name(str):
    pass


class Operator(str):
    pass


def parse_pdf_objects(pdf_bytes: bytes) -> dict[int, bytes]:
    objects: dict[int, bytes] = {}
    for match in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", pdf_bytes, re.S):
        objects[int(match.group(1))] = match.group(2)
    return objects


def stream_data(body: bytes) -> bytes | None:
    marker = re.search(rb"stream\r?\n", body)
    if not marker:
        return None
    length_match = re.search(rb"/Length\s+(\d+)", body)
    if not length_match:
        return None
    length = int(length_match.group(1))
    raw = body[marker.end() : marker.end() + length]
    return zlib.decompress(raw)


def decode_cmap_target(hex_text: str) -> str:
    raw = bytes.fromhex(hex_text)
    if len(raw) % 2 == 0:
        try:
            return raw.decode("utf-16-be")
        except UnicodeDecodeError:
            pass
    return "".join(chr(b) for b in raw)


def parse_cmap(data: bytes) -> dict[int, str]:
    lines = [line.strip() for line in data.decode("latin1").splitlines()]
    mapping: dict[int, str] = {}
    i = 0
    while i < len(lines):
        bfchar = re.match(r"(\d+)\s+beginbfchar", lines[i])
        if bfchar:
            count = int(bfchar.group(1))
            for offset in range(1, count + 1):
                src, dst = re.findall(r"<([^>]+)>", lines[i + offset])
                mapping[int(src, 16)] = decode_cmap_target(dst)
            i += count + 1
            continue

        bfrange = re.match(r"(\d+)\s+beginbfrange", lines[i])
        if bfrange:
            count = int(bfrange.group(1))
            for offset in range(1, count + 1):
                line = lines[i + offset]
                parts = re.findall(r"<([^>]+)>", line)
                if "[" in line:
                    start = int(parts[0], 16)
                    for arr_offset, dst in enumerate(parts[2:]):
                        mapping[start + arr_offset] = decode_cmap_target(dst)
                else:
                    start = int(parts[0], 16)
                    end = int(parts[1], 16)
                    dst0 = int(parts[2], 16)
                    for code in range(start, end + 1):
                        mapping[code] = chr(dst0 + (code - start))
            i += count + 1
            continue

        i += 1
    return mapping


def parse_literal(data: bytes, idx: int) -> tuple[bytes, int]:
    idx += 1
    depth = 1
    out = bytearray()
    while idx < len(data):
        char = data[idx]
        if char == 0x5C:
            idx += 1
            if idx >= len(data):
                break
            esc = data[idx]
            escapes = {
                ord("n"): 10,
                ord("r"): 13,
                ord("t"): 9,
                ord("b"): 8,
                ord("f"): 12,
                ord("("): 40,
                ord(")"): 41,
                ord("\\"): 92,
            }
            if esc in escapes:
                out.append(escapes[esc])
                idx += 1
                continue
            if esc in b"\n\r":
                if esc == ord("\r") and idx + 1 < len(data) and data[idx + 1] == ord("\n"):
                    idx += 2
                else:
                    idx += 1
                continue
            if 48 <= esc <= 55:
                octal = bytes([esc])
                idx += 1
                for _ in range(2):
                    if idx < len(data) and 48 <= data[idx] <= 55:
                        octal += bytes([data[idx]])
                        idx += 1
                    else:
                        break
                out.append(int(octal, 8))
                continue
            out.append(esc)
            idx += 1
            continue
        if char == 0x28:
            depth += 1
            out.append(char)
            idx += 1
            continue
        if char == 0x29:
            depth -= 1
            if depth == 0:
                return bytes(out), idx + 1
            out.append(char)
            idx += 1
            continue
        out.append(char)
        idx += 1
    return bytes(out), idx


def parse_hex(data: bytes, idx: int) -> tuple[bytes, int]:
    idx += 1
    out = bytearray()
    while idx < len(data) and data[idx] != 0x3E:
        if chr(data[idx]).isspace():
            idx += 1
            continue
        out.append(data[idx])
        idx += 1
    if len(out) % 2:
        out.append(ord("0"))
    return bytes.fromhex(out.decode()), idx + 1


def parse_name(data: bytes, idx: int) -> tuple[Name, int]:
    idx += 1
    start = idx
    while idx < len(data) and data[idx] not in PDF_WS + PDF_DELIMS:
        idx += 1
    return Name(data[start:idx].decode("latin1")), idx


def parse_number(data: bytes, idx: int) -> tuple[float, int]:
    start = idx
    while idx < len(data) and data[idx] not in PDF_WS + PDF_DELIMS:
        idx += 1
    return float(data[start:idx]), idx


def parse_word(data: bytes, idx: int) -> tuple[Operator, int]:
    start = idx
    while idx < len(data) and data[idx] not in PDF_WS + PDF_DELIMS:
        idx += 1
    return Operator(data[start:idx].decode("latin1")), idx


def parse_array(data: bytes, idx: int) -> tuple[list[object], int]:
    arr: list[object] = []
    idx += 1
    while idx < len(data):
        char = data[idx]
        if char in PDF_WS:
            idx += 1
            continue
        if char == 0x5D:
            return arr, idx + 1
        if char == 0x28:
            value, idx = parse_literal(data, idx)
            arr.append(value)
            continue
        if char == 0x3C:
            value, idx = parse_hex(data, idx)
            arr.append(value)
            continue
        if char == 0x5B:
            value, idx = parse_array(data, idx)
            arr.append(value)
            continue
        if char == 0x2F:
            value, idx = parse_name(data, idx)
            arr.append(value)
            continue
        if char in b"+-.0123456789":
            value, idx = parse_number(data, idx)
            arr.append(value)
            continue
        value, idx = parse_word(data, idx)
        arr.append(value)
    return arr, idx


def tokenize_content_stream(data: bytes):
    idx = 0
    while idx < len(data):
        char = data[idx]
        if char in PDF_WS:
            idx += 1
            continue
        if char == 0x25:
            while idx < len(data) and data[idx] not in b"\r\n":
                idx += 1
            continue
        if char == 0x28:
            value, idx = parse_literal(data, idx)
            yield value
            continue
        if char == 0x3C:
            if idx + 1 < len(data) and data[idx + 1] == 0x3C:
                idx += 2
                continue
            value, idx = parse_hex(data, idx)
            yield value
            continue
        if char == 0x3E and idx + 1 < len(data) and data[idx + 1] == 0x3E:
            idx += 2
            continue
        if char == 0x5B:
            value, idx = parse_array(data, idx)
            yield value
            continue
        if char == 0x5D:
            idx += 1
            continue
        if char == 0x2F:
            value, idx = parse_name(data, idx)
            yield value
            continue
        if char in b"+-.0123456789":
            value, idx = parse_number(data, idx)
            yield value
            continue
        value, idx = parse_word(data, idx)
        yield value


def decode_bytes(raw: bytes, cmap: dict[int, str]) -> str:
    pieces = []
    for byte in raw:
        if byte in cmap:
            pieces.append(cmap[byte])
        elif 32 <= byte < 127:
            pieces.append(chr(byte))
    return "".join(pieces)


def decode_tj_array(items: list[object], cmap: dict[int, str]) -> str:
    pieces = []
    for item in items:
        if isinstance(item, (bytes, bytearray)):
            pieces.append(decode_bytes(item, cmap))
        elif isinstance(item, float) and item <= SPACE_THRESHOLD:
            pieces.append(" ")
    return "".join(pieces)


def extract_page_lines(content: bytes, fonts: dict[str, int], font_cmaps: dict[int, dict[int, str]]) -> list[str]:
    current_cmap: dict[int, str] | None = None
    current_line = ""
    lines: list[str] = []
    operands: list[object] = []

    for token in tokenize_content_stream(content):
        if isinstance(token, Operator):
            if token == "BT":
                current_line = ""
            elif token == "ET":
                if current_line.strip():
                    lines.append(current_line.rstrip())
                current_line = ""
            elif token == "Tf":
                if len(operands) >= 2 and isinstance(operands[-2], Name):
                    font_name = str(operands[-2])
                    current_cmap = font_cmaps.get(fonts[font_name], {})
            elif token == "Td":
                if len(operands) >= 2:
                    ty = float(operands[-1])
                    if current_line.strip() and abs(ty) >= LINE_BREAK_THRESHOLD:
                        lines.append(current_line.rstrip())
                        current_line = ""
            elif token == "TJ" and operands:
                current_line += decode_tj_array(operands[-1], current_cmap or {})
            elif token == "Tj" and operands:
                current_line += decode_bytes(operands[-1], current_cmap or {})
            operands = []
            continue

        operands.append(token)

    cleaned = []
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"\d+", stripped):
            continue
        cleaned.append(stripped)
    return cleaned


def extract_text(pdf_path: Path) -> str:
    objects = parse_pdf_objects(pdf_path.read_bytes())

    font_cmaps: dict[int, dict[int, str]] = {}
    for objnum, body in objects.items():
        match = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", body)
        if not match:
            continue
        cmap_stream = stream_data(objects[int(match.group(1))])
        if cmap_stream is not None:
            font_cmaps[objnum] = parse_cmap(cmap_stream)

    pages_body = next(body for body in objects.values() if b"/Type /Pages" in body)
    page_numbers = [int(ref) for ref in re.findall(rb"(\d+)\s+0\s+R", re.search(rb"/Kids\s*\[(.*?)\]", pages_body, re.S).group(1))]

    all_lines: list[str] = []
    for page_num in page_numbers:
        page_body = objects[page_num]
        contents_obj = int(re.search(rb"/Contents\s+(\d+)\s+0\s+R", page_body).group(1))
        resources_obj = int(re.search(rb"/Resources\s+(\d+)\s+0\s+R", page_body).group(1))
        fonts = {
            name.decode(): int(ref)
            for name, ref in re.findall(rb"/(F\d+)\s+(\d+)\s+0\s+R", objects[resources_obj])
        }
        content_stream = stream_data(objects[contents_obj])
        if content_stream is None:
            continue
        page_lines = extract_page_lines(content_stream, fonts, font_cmaps)
        if all_lines and page_lines:
            all_lines.append("")
        all_lines.extend(page_lines)

    return "\n".join(all_lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from TeX-style PDFs with ToUnicode maps.")
    parser.add_argument("pdf", type=Path, help="Path to the source PDF")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output path. Defaults to <pdf stem>_extracted.txt next to the PDF.",
    )
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    output_path = args.output or pdf_path.with_name(f"{pdf_path.stem}_extracted.txt")
    output_path.write_text(extract_text(pdf_path), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
