from __future__ import annotations

import sqlite3
from pathlib import Path

from converter.exporter import export_bblx
from converter.mapper import map_books, map_verses
from converter.metadata import enrich_metadata
from converter.models import BibleModule
from converter.parser import parse_module

from .conftest import write_sample_mybible_db


def test_exporter_writes_bblx_sqlite(tmp_path):
    source = write_sample_mybible_db(tmp_path / "input.db")
    schema, metadata, books, verses, _ = parse_module(source)
    module = BibleModule(
        source_path=source,
        schema=schema,
        metadata=enrich_metadata(metadata, source, schema, books),
        books=map_books(books).books,
        verses=map_verses(verses),
    )
    output = export_bblx(module, tmp_path / "output.bblx", force=True)

    with sqlite3.connect(output) as conn:
        details = conn.execute("SELECT Description, Abbreviation, OT, NT FROM Details").fetchone()
        bible_rows = conn.execute("SELECT Book, Chapter, Verse, Scripture FROM Bible ORDER BY Book, Chapter, Verse").fetchall()

    assert details[0] == "Biblia de prueba"
    assert details[1] == "PRUEBA"
    assert bible_rows[0][0] == 1
    assert bible_rows[-1][0] == 40
    assert bible_rows[0][3].startswith("{\\rtf1")
    assert len(bible_rows) == 3
