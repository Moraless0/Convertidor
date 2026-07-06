from __future__ import annotations

from pathlib import Path

from converter.models import BibleModule, Metadata, ParsedSchema
from converter.validator import validate_module
from converter.models import BookEntry, ModuleType, Severity, VerseEntry


def test_validator_detects_duplicates_and_empty_text():
    module = BibleModule(
        source_path=Path("sample.db"),
        schema=ParsedSchema(tables={}, module_type=ModuleType.BIBLE),
        metadata=Metadata(name="Prueba"),
        books=[BookEntry(10, 1, "Gen", "Gn", "Génesis")],
        verses=[
            VerseEntry(10, 1, 1, "texto"),
            VerseEntry(10, 1, 1, "duplicado"),
            VerseEntry(10, 1, 3, ""),
        ],
    )

    report = validate_module(module)
    assert report.has_errors
    assert any(issue.code == "duplicate-verse" for issue in report.issues)
    assert any(issue.code == "empty-verse" for issue in report.issues)
