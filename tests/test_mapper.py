from __future__ import annotations

from converter.books import build_book_entry
from converter.mapper import map_books, map_verses
from converter.models import BookEntry, VerseEntry


def test_mapper_maps_canonical_books():
    books = [build_book_entry(10), build_book_entry(470)]
    result = map_books([book for book in books if book is not None])

    assert result.books[0].esword_number == 1
    assert result.books[1].esword_number == 40


def test_mapper_sorts_verses():
    verses = [
        VerseEntry(470, 2, 1, "b"),
        VerseEntry(10, 1, 2, "c"),
        VerseEntry(10, 1, 1, "a"),
    ]

    mapped = map_verses(verses)
    assert [(verse.book_number, verse.chapter, verse.verse) for verse in mapped] == [(1, 1, 1), (1, 1, 2), (40, 2, 1)]
