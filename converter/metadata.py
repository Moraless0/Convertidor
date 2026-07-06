from __future__ import annotations

from pathlib import Path

from .models import Metadata, ParsedSchema


def enrich_metadata(metadata: Metadata, path: Path, schema: ParsedSchema, books: list) -> Metadata:
    raw = dict(metadata.raw)
    name = metadata.name or raw.get("description") or raw.get("name") or path.stem
    abbreviation = metadata.abbreviation or raw.get("abbreviation") or raw.get("abbr") or path.stem[:16]
    language = metadata.language or raw.get("language") or raw.get("lang") or infer_language_from_name(name)
    description = metadata.description or raw.get("description") or name
    version = metadata.version or raw.get("version") or raw.get("module_version") or ""
    author = metadata.author or raw.get("author") or raw.get("creator") or ""
    publisher = metadata.publisher or raw.get("publisher") or ""
    publish_date = metadata.publish_date or raw.get("date") or raw.get("publish_date") or ""
    encoding = metadata.encoding or raw.get("encoding") or "UTF-8"
    return Metadata(
        name=name.strip(),
        abbreviation=abbreviation.strip(),
        language=language.strip(),
        description=description.strip(),
        version=version.strip(),
        author=author.strip(),
        publisher=publisher.strip(),
        publish_date=publish_date.strip(),
        encoding=encoding.strip() or "UTF-8",
        source=str(path),
        raw=raw,
    )


def infer_language_from_name(name: str) -> str:
    lowered = name.lower()
    if any(token in lowered for token in ("españ", "biblia", "reina valera", "rvr")):
        return "es"
    if any(token in lowered for token in ("english", "kjv", "niv", "nasb")):
        return "en"
    if any(token in lowered for token in ("portugu", "arc")):
        return "pt"
    return ""
