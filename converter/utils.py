from __future__ import annotations

from pathlib import Path


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def normalize_whitespace(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"))


def coerce_text(value: bytes | str | int | float | None, encoding: str = "utf-8") -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)


def coerce_text_lossy(value: bytes | str | int | float | None, encoding: str = "utf-8") -> tuple[str, bool]:
    if value is None:
        return "", False
    if isinstance(value, bytes):
        try:
            return value.decode(encoding), False
        except UnicodeDecodeError:
            return value.decode(encoding, errors="replace"), True
    return str(value), False


def is_nonempty(value: str) -> bool:
    return bool(value.strip())


def today_iso() -> str:
    from datetime import date

    return date.today().isoformat()
