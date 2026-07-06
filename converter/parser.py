from __future__ import annotations

import sqlite3
from dataclasses import replace
from pathlib import Path
from typing import Iterable

from .books import build_book_entry
from .models import BookEntry, ColumnInfo, IndexInfo, Metadata, ModuleType, ParsedSchema, TableInfo, VerseEntry
from .utils import coerce_text_lossy, normalize_whitespace

_COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "book_number": ("book_number", "book", "book_id", "book_no", "booknum"),
    "chapter": ("chapter", "chapter_number", "chapter_no", "chap"),
    "verse": ("verse", "verse_number", "verse_no", "vers", "v"),
    "text": ("text", "scripture", "verse_text", "content", "body", "html"),
    "name": ("name", "key", "item", "setting"),
    "value": ("value", "val", "data", "setting_value"),
    "short_name": ("short_name", "abbr", "abbreviation", "short", "book_short"),
    "long_name": ("long_name", "name_long", "full_name", "book_name", "title"),
}


def _decode(value: bytes | str | int | float | None) -> str:
    text, _ = coerce_text_lossy(value)
    return text


def _coerce_bool(value: object) -> bool:
    if isinstance(value, bytes):
        value = _decode(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        return lowered in {"1", "true", "yes", "y", "on"}
    return bool(value)


def _table_info(conn: sqlite3.Connection, table_name: str) -> TableInfo:
    cursor = conn.execute(f'PRAGMA table_info("{table_name}")')
    columns = tuple(
        ColumnInfo(
            name=_decode(row[1]),
            data_type=_decode(row[2]),
            notnull=bool(row[3]),
            default_value=_decode(row[4]) if row[4] is not None else None,
            primary_key=int(row[5]),
        )
        for row in cursor.fetchall()
    )
    index_rows = conn.execute(f'PRAGMA index_list("{table_name}")').fetchall()
    indexes: list[IndexInfo] = []
    for row in index_rows:
        index_name = _decode(row[1])
        unique = bool(row[2])
        index_columns = tuple(
            _decode(col_row[2])
            for col_row in conn.execute(f'PRAGMA index_info("{index_name}")').fetchall()
        )
        indexes.append(IndexInfo(index_name, unique, index_columns))
    foreign_keys = tuple(
        (_decode(row[3]), _decode(row[2]), _decode(row[4]))
        for row in conn.execute(f'PRAGMA foreign_key_list("{table_name}")').fetchall()
    )
    sql_row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND lower(name)=lower(?)",
        (table_name,),
    ).fetchone()
    sql = _decode(sql_row[0]) if sql_row and sql_row[0] is not None else None
    return TableInfo(name=table_name, sql=sql, columns=columns, indexes=tuple(indexes), foreign_keys=foreign_keys)


def _column_names(table: TableInfo) -> set[str]:
    return {column.name.lower() for column in table.columns}


def _matches_aliases(names: set[str], aliases: Iterable[str]) -> bool:
    return any(alias.lower() in names for alias in aliases)


def _find_table(tables: dict[str, TableInfo], required: Iterable[Iterable[str]], optional: Iterable[str] = ()) -> str | None:
    required_groups = tuple(required)
    optional_set = {item.lower() for item in optional}
    best_name: str | None = None
    best_score = 0
    for name, table in tables.items():
        names = _column_names(table)
        if not all(_matches_aliases(names, alias_group) for alias_group in required_groups):
            continue
        score = len(required_groups) * 10 + len(names & optional_set)
        if score > best_score:
            best_name = name
            best_score = score
    return best_name


def _find_column(table: TableInfo, aliases: tuple[str, ...], required: bool = True) -> str | None:
    names = {column.name.lower(): column.name for column in table.columns}
    for alias in aliases:
        if alias.lower() in names:
            return names[alias.lower()]
    if required:
        raise KeyError(f"No se encontró una columna compatible con {aliases!r} en la tabla {table.name!r}")
    return None


def inspect_schema(path: Path) -> ParsedSchema:
    with sqlite3.connect(path) as conn:
        conn.text_factory = bytes
        master_rows = conn.execute(
            "SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
        ).fetchall()
        tables: dict[str, TableInfo] = {}
        warnings: list[str] = []
        for row in master_rows:
            kind = _decode(row[0])
            if kind != "table":
                continue
            table_name = _decode(row[1])
            tables[table_name] = _table_info(conn, table_name)

        info_table = _find_table(tables, (("name", "key", "item"), ("value", "data", "setting_value")), optional={"data"})
        books_table = _find_table(
            tables,
            (("book_number", "book", "book_id", "book_no"),),
            optional={"short_name", "long_name", "book_color", "is_present"},
        )
        verses_table = _find_table(
            tables,
            (
                ("book_number", "book", "book_id", "book_no"),
                ("chapter", "chapter_number", "chapter_no", "chap"),
                ("verse", "verse_number", "verse_no", "vers"),
            ),
            optional={"text", "scripture", "verse_text", "content"},
        )

        module_type = ModuleType.UNKNOWN
        if verses_table:
            module_type = ModuleType.BIBLE
        elif _find_table(tables, (("reference",),), optional={"text", "content"}):
            module_type = ModuleType.COMMENTARY
        elif _find_table(tables, (("entry",),), optional={"definition", "text", "body"}):
            module_type = ModuleType.DICTIONARY

        return ParsedSchema(
            tables=tables,
            module_type=module_type,
            info_table=info_table,
            books_table=books_table,
            verses_table=verses_table,
            warnings=warnings,
        )


def _read_key_value_rows(conn: sqlite3.Connection, table_name: str) -> dict[str, str]:
    table = conn.execute(f'SELECT * FROM "{table_name}"').fetchall()
    table_info = conn.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    columns = [str(row[1], "utf-8") if isinstance(row[1], bytes) else str(row[1]) for row in table_info]
    name_column = next((col for col in columns if col.lower() in _COLUMN_ALIASES["name"]), columns[0])
    value_column = next((col for col in columns if col.lower() in _COLUMN_ALIASES["value"]), columns[1] if len(columns) > 1 else columns[0])
    result: dict[str, str] = {}
    for row in table:
        row_map = dict(zip(columns, row))
        key, key_warn = coerce_text_lossy(row_map.get(name_column))
        value, value_warn = coerce_text_lossy(row_map.get(value_column))
        if key:
            result[key.strip().lower()] = normalize_whitespace(value).strip()
        if key_warn or value_warn:
            result.setdefault("__decode_warning__", "true")
    result.pop("__decode_warning__", None)
    return result


def parse_module(path: Path) -> tuple[ParsedSchema, Metadata, list, list[VerseEntry], list[str]]:
    schema = inspect_schema(path)
    warnings = list(schema.warnings)
    metadata = Metadata(source=str(path))
    books: list = []
    verses: list[VerseEntry] = []
    with sqlite3.connect(path) as conn:
        conn.text_factory = bytes
        if schema.info_table:
            info = _read_key_value_rows(conn, schema.info_table)
            metadata.raw = dict(info)
        else:
            info = {}
        if schema.books_table:
            table = schema.tables[schema.books_table]
            columns = {column.name.lower(): column.name for column in table.columns}
            book_number_col = _find_column(table, _COLUMN_ALIASES["book_number"])
            short_name_col = _find_column(table, _COLUMN_ALIASES["short_name"], required=False)
            long_name_col = _find_column(table, _COLUMN_ALIASES["long_name"], required=False)
            color_col = next((columns[name] for name in columns if "color" in name), None)
            present_col = next((columns[name] for name in columns if name in {"is_present", "present"}), None)
            rows = conn.execute(f'SELECT * FROM "{schema.books_table}"').fetchall()
            all_columns = [column.name for column in table.columns]
            for row in rows:
                row_map = dict(zip(all_columns, row))
                source_number_text, _ = coerce_text_lossy(row_map.get(book_number_col))
                if not source_number_text.strip().isdigit():
                    warnings.append(f"Libro con identificador inválido en {schema.books_table}: {source_number_text!r}")
                    continue
                source_number = int(source_number_text)
                entry = build_book_entry(source_number)
                if entry is None:
                    short_name, _ = coerce_text_lossy(row_map.get(short_name_col)) if short_name_col else ("", False)
                    long_name, _ = coerce_text_lossy(row_map.get(long_name_col)) if long_name_col else ("", False)
                    entry = BookEntry(
                        source_number=source_number,
                        esword_number=None,
                        osis_id=f"Book{source_number}",
                        short_name=short_name or f"Bk{source_number}",
                        long_name=long_name or short_name or f"Book {source_number}",
                        category="unknown",
                        color=None,
                        is_present=_coerce_bool(row_map.get(present_col, True)) if present_col else True,
                    )
                else:
                    if short_name_col:
                        short_name, _ = coerce_text_lossy(row_map.get(short_name_col))
                        entry = replace(entry, short_name=short_name or entry.short_name)
                    if long_name_col:
                        long_name, _ = coerce_text_lossy(row_map.get(long_name_col))
                        entry = replace(entry, long_name=long_name or entry.long_name)
                    if color_col:
                        color, _ = coerce_text_lossy(row_map.get(color_col))
                        entry = replace(entry, color=color or entry.color)
                    if present_col:
                        entry = replace(entry, is_present=_coerce_bool(row_map.get(present_col)))
                books.append(entry)

        if schema.verses_table:
            table = schema.tables[schema.verses_table]
            columns = {column.name.lower(): column.name for column in table.columns}
            book_col = _find_column(table, _COLUMN_ALIASES["book_number"])
            chapter_col = _find_column(table, _COLUMN_ALIASES["chapter"])
            verse_col = _find_column(table, _COLUMN_ALIASES["verse"])
            text_col = _find_column(table, _COLUMN_ALIASES["text"])
            rows = conn.execute(f'SELECT * FROM "{schema.verses_table}"').fetchall()
            all_columns = [column.name for column in table.columns]
            for row in rows:
                row_map = dict(zip(all_columns, row))
                book_text, book_warn = coerce_text_lossy(row_map.get(book_col))
                chapter_text, chapter_warn = coerce_text_lossy(row_map.get(chapter_col))
                verse_text, verse_warn = coerce_text_lossy(row_map.get(verse_col))
                text_value, text_warn = coerce_text_lossy(row_map.get(text_col))
                if not (book_text.strip().isdigit() and chapter_text.strip().isdigit() and verse_text.strip().isdigit()):
                    warnings.append(f"Verso omitido por referencia inválida: {book_text!r} {chapter_text!r} {verse_text!r}")
                    continue
                if book_warn or chapter_warn or verse_warn or text_warn:
                    warnings.append(
                        f"Decodificación con reemplazo en {schema.verses_table} {book_text}:{chapter_text}:{verse_text}"
                    )
                verses.append(
                    VerseEntry(
                        book_number=int(book_text),
                        chapter=int(chapter_text),
                        verse=int(verse_text),
                        text=normalize_whitespace(text_value),
                    )
                )

    if not books and verses:
        source_numbers = sorted({verse.book_number for verse in verses})
        for source_number in source_numbers:
            entry = build_book_entry(source_number)
            if entry is not None:
                books.append(entry)
            else:
                warnings.append(f"Libro no reconocido: {source_number}")

    metadata = infer_metadata(metadata, path, schema, books)
    return schema, metadata, books, verses, warnings


def infer_metadata(metadata: Metadata, path: Path, schema: ParsedSchema, books: list) -> Metadata:
    raw = dict(metadata.raw)
    name = raw.get("description") or raw.get("name") or path.stem
    abbreviation = raw.get("abbreviation") or raw.get("abbr") or path.stem[:16]
    language = raw.get("language") or raw.get("lang") or ""
    description = raw.get("description") or name
    version = raw.get("version") or raw.get("module_version") or ""
    author = raw.get("author") or raw.get("creator") or ""
    publisher = raw.get("publisher") or raw.get("publishers") or ""
    publish_date = raw.get("date") or raw.get("publish_date") or ""
    encoding = raw.get("encoding") or "UTF-8"
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
