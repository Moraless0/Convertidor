from __future__ import annotations

from html import unescape
from html.parser import HTMLParser


def _escape_rtf_text(text: str) -> str:
    chunks: list[str] = []
    for char in text:
        if char == "\\":
            chunks.append(r"\\")
        elif char == "{":
            chunks.append(r"\{")
        elif char == "}":
            chunks.append(r"\}")
        elif char == "\n":
            chunks.append(r"\line ")
        elif ord(char) > 127:
            code = ord(char)
            if code > 32767:
                code -= 65536
            chunks.append(f"\\u{code}?")
        else:
            chunks.append(char)
    return "".join(chunks)


class _RtfHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: list[str] = [r"{\rtf1\ansi\deff0 "]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"b", "strong"}:
            self.parts.append(r"\b ")
        elif tag in {"i", "em"}:
            self.parts.append(r"\i ")
        elif tag == "u":
            self.parts.append(r"\ul ")
        elif tag == "sup":
            self.parts.append(r"\super ")
        elif tag == "sub":
            self.parts.append(r"\sub ")
        elif tag in {"br", "hr"}:
            self.parts.append(r"\line ")
        elif tag in {"p", "div"}:
            self.parts.append(r"\par ")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"b", "strong"}:
            self.parts.append(r"\b0 ")
        elif tag in {"i", "em"}:
            self.parts.append(r"\i0 ")
        elif tag == "u":
            self.parts.append(r"\ul0 ")
        elif tag == "sup":
            self.parts.append(r"\nosupersub ")
        elif tag == "sub":
            self.parts.append(r"\nosupersub ")

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(_escape_rtf_text(unescape(data)))

    def getvalue(self) -> str:
        return "".join(self.parts) + "}"


def mybible_text_to_rtf(text: str) -> str:
    parser = _RtfHTMLParser()
    parser.feed(text)
    parser.close()
    return parser.getvalue()
