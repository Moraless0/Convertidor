from __future__ import annotations

import sqlite3
from pathlib import Path


def write_sample_mybible_db(path: Path, *, renamed: bool = False, duplicate: bool = False, empty: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        if renamed:
            conn.execute("CREATE TABLE module_info (name TEXT, value TEXT)")
            conn.execute(
                "CREATE TABLE book_rows (book_id INTEGER, short_name TEXT, long_name TEXT, book_color TEXT, is_present INTEGER)"
            )
            conn.execute(
                "CREATE TABLE verse_rows (book_id INTEGER, chapter_no INTEGER, verse_no INTEGER, verse_text TEXT)"
            )
            info_table = "module_info"
            books_table = "book_rows"
            verses_table = "verse_rows"
        else:
            conn.execute("CREATE TABLE info (name TEXT, value TEXT)")
            conn.execute("CREATE TABLE books (book_number INTEGER, short_name TEXT, long_name TEXT, book_color TEXT, is_present INTEGER)")
            conn.execute("CREATE TABLE verses (book_number INTEGER, chapter INTEGER, verse INTEGER, text TEXT)")
            info_table = "info"
            books_table = "books"
            verses_table = "verses"

        conn.executemany(
            f'INSERT INTO "{info_table}" (name, value) VALUES (?, ?)',
            [
                ("language", "es"),
                ("description", "Biblia de prueba"),
                ("abbreviation", "PRUEBA"),
                ("version", "1.0"),
                ("author", "Equipo de prueba"),
                ("encoding", "UTF-8"),
            ],
        )
        conn.executemany(
            f'INSERT INTO "{books_table}" (book_id, short_name, long_name, book_color, is_present) VALUES (?, ?, ?, ?, ?)'
            if renamed
            else f'INSERT INTO "{books_table}" (book_number, short_name, long_name, book_color, is_present) VALUES (?, ?, ?, ?, ?)',
            [
                (10, "Gn", "Génesis", "#ccccff", 1),
                (470, "Mt", "Mateo", "#ffff99", 1),
            ],
        )
        verses = [
            (10, 1, 1, "<b>En el principio</b> creó Dios los cielos y la tierra."),
            (10, 1, 2, "Y la tierra estaba desordenada y vacía."),
            (470, 1, 1, "Libro de la genealogía de Jesucristo."),
        ]
        if empty:
            verses.append((470, 1, 2, ""))
        if duplicate:
            verses.append((10, 1, 1, "Texto duplicado"))
        conn.executemany(
            f'INSERT INTO "{verses_table}" (book_id, chapter_no, verse_no, verse_text) VALUES (?, ?, ?, ?)'
            if renamed
            else f'INSERT INTO "{verses_table}" (book_number, chapter, verse, text) VALUES (?, ?, ?, ?)',
            verses,
        )
        conn.commit()
    return path
