from __future__ import annotations

from dataclasses import dataclass

from .books import BOOK_LOOKUP, PROTESTANT_BOOKS
from .models import BookEntry, VerseEntry


@dataclass(frozen=True, slots=True)
class MappingResult:
    books: list[BookEntry]
    verses: list[VerseEntry]
    warnings: list[str]


def map_books(books: list[BookEntry]) -> MappingResult:
    mapped_books: list[BookEntry] = []
    warnings: list[str] = []
    for book in books:
        definition = BOOK_LOOKUP.get(book.source_number)
        if definition is None:
            warnings.append(f"Libro MyBible no soportado todavía: {book.source_number}")
            mapped_books.append(book)
            continue
        mapped_books.append(
            BookEntry(
                source_number=book.source_number,
                esword_number=definition.esword_number,
                osis_id=definition.osis_id,
                short_name=book.short_name or definition.short_name,
                long_name=book.long_name or definition.long_name,
                category=definition.category,
                color=book.color or definition.color,
                is_present=book.is_present,
            )
        )
    mapped_books.sort(key=lambda item: (item.esword_number is None, item.esword_number or 999, item.source_number))
    return MappingResult(mapped_books, [], warnings)


def map_verses(verses: list[VerseEntry]) -> list[VerseEntry]:
    mapped_verses: list[VerseEntry] = []
    for verse in verses:
        definition = BOOK_LOOKUP.get(verse.book_number)
        if definition is not None and definition.esword_number is not None:
            mapped_verses.append(
                VerseEntry(
                    book_number=definition.esword_number,
                    chapter=verse.chapter,
                    verse=verse.verse,
                    text=verse.text,
                )
            )
        else:
            mapped_verses.append(verse)
    return sorted(mapped_verses, key=lambda verse: (verse.book_number, verse.chapter, verse.verse))
