from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import BibleModule
from .rtf import mybible_text_to_rtf
from .utils import ensure_parent_dir, today_iso


def export_bblx(module: BibleModule, output_path: Path, force: bool = False) -> Path:
    if output_path.exists() and not force:
        raise FileExistsError(f"El archivo de salida ya existe: {output_path}")
    ensure_parent_dir(output_path)
    if output_path.exists():
        output_path.unlink()

    has_ot = any(verse.book_number <= 390 for verse in module.verses)
    has_nt = any(verse.book_number >= 470 for verse in module.verses)
    with sqlite3.connect(output_path) as conn:
        conn.execute(
            """CREATE TABLE Details (
                Description NVARCHAR(255),
                Abbreviation NVARCHAR(50),
                Comments TEXT,
                Version TEXT,
                VersionDate DATETIME,
                PublishDate DATETIME,
                RightToLeft BOOL,
                OT BOOL,
                NT BOOL,
                Strong BOOL,
                CustomCSS TEXT
            )"""
        )
        conn.execute(
            """CREATE TABLE Bible (
                Book INT,
                Chapter INT,
                Verse INT,
                Scripture TEXT,
                PRIMARY KEY(Book, Chapter, Verse)
            )"""
        )
        conn.execute("CREATE INDEX IF NOT EXISTS BibleIndex ON Bible(Book, Chapter, Verse)")
        conn.execute(
            "INSERT INTO Details VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                module.metadata.description or module.metadata.name or module.source_path.stem,
                module.metadata.abbreviation or module.source_path.stem[:16],
                module.metadata.author or module.metadata.publisher or "",
                module.metadata.version or "1.0",
                today_iso(),
                module.metadata.publish_date or today_iso(),
                False,
                has_ot,
                has_nt,
                False,
                "",
            ),
        )
        conn.executemany(
            "INSERT INTO Bible(Book, Chapter, Verse, Scripture) VALUES (?, ?, ?, ?)",
            (
                (
                    verse.book_number,
                    verse.chapter,
                    verse.verse,
                    mybible_text_to_rtf(verse.text),
                )
                for verse in module.verses
            ),
        )
        conn.commit()
    return output_path
