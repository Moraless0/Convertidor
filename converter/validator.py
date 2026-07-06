from __future__ import annotations

from collections import defaultdict

from .models import BibleModule, Severity, ValidationReport


def validate_module(module: BibleModule) -> ValidationReport:
    report = ValidationReport()
    seen: set[tuple[int, int, int]] = set()
    by_book: dict[int, dict[int, list[int]]] = defaultdict(lambda: defaultdict(list))

    for verse in module.verses:
        ref = (verse.book_number, verse.chapter, verse.verse)
        if ref in seen:
            report.add(Severity.ERROR, "duplicate-verse", "Versículo duplicado", f"{verse.book_number}:{verse.chapter}:{verse.verse}")
        else:
            seen.add(ref)
        if not verse.text.strip():
            report.add(Severity.WARNING, "empty-verse", "Versículo sin texto", f"{verse.book_number}:{verse.chapter}:{verse.verse}")
        by_book[verse.book_number][verse.chapter].append(verse.verse)

    for book_number, chapters in by_book.items():
        chapter_numbers = sorted(chapters)
        if not chapter_numbers:
            report.add(Severity.ERROR, "empty-book", "Libro sin versículos", str(book_number))
            continue
        expected_chapters = list(range(chapter_numbers[0], chapter_numbers[-1] + 1))
        missing_chapters = sorted(set(expected_chapters) - set(chapter_numbers))
        for chapter in missing_chapters:
            report.add(Severity.WARNING, "missing-chapter", "Capítulo faltante", f"{book_number}:{chapter}")
        for chapter, verses in chapters.items():
            verse_numbers = sorted(set(verses))
            expected_verses = list(range(verse_numbers[0], verse_numbers[-1] + 1))
            missing_verses = sorted(set(expected_verses) - set(verse_numbers))
            for verse in missing_verses:
                report.add(Severity.WARNING, "missing-verse", "Versículo faltante", f"{book_number}:{chapter}:{verse}")
            if len(verses) != len(verse_numbers):
                report.add(Severity.ERROR, "duplicate-verse-number", "Números de versículo repetidos en el capítulo", f"{book_number}:{chapter}")

    if not module.books:
        report.add(Severity.WARNING, "no-books-table", "No se detectó tabla de libros compatible", None)
    if not module.verses:
        report.add(Severity.ERROR, "no-verses", "No se detectó tabla de versículos compatible", None)
    return report
