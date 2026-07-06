from __future__ import annotations

from converter.parser import parse_module

from .conftest import write_sample_mybible_db


def test_parser_detects_renamed_schema(tmp_path):
    source = write_sample_mybible_db(tmp_path / "sample.db", renamed=True)
    schema, metadata, books, verses, warnings = parse_module(source)

    assert schema.module_type.value == "bible"
    assert schema.info_table == "module_info"
    assert schema.books_table == "book_rows"
    assert schema.verses_table == "verse_rows"
    assert metadata.language == "es"
    assert metadata.abbreviation == "PRUEBA"
    assert len(books) == 2
    assert len(verses) == 3
    assert not warnings


def test_parser_preserves_text_and_accents(tmp_path):
    source = write_sample_mybible_db(tmp_path / "sample.db")
    _, _, _, verses, _ = parse_module(source)

    assert verses[0].text.startswith("<b>En el principio</b>")
    assert "Génesis" not in verses[0].text
