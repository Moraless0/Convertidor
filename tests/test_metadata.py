from __future__ import annotations

from pathlib import Path

from converter.metadata import enrich_metadata, infer_language_from_name
from converter.models import Metadata, ParsedSchema, ModuleType


def test_metadata_fallbacks(tmp_path):
    metadata = Metadata(raw={})
    enriched = enrich_metadata(metadata, tmp_path / "BibliaDemo.SQLite3", ParsedSchema(tables={}, module_type=ModuleType.BIBLE), [])

    assert enriched.name == "BibliaDemo.SQLite3".replace(".SQLite3", "")
    assert enriched.abbreviation.startswith("BibliaDemo")
    assert enriched.encoding == "UTF-8"


def test_language_inference():
    assert infer_language_from_name("Biblia Reina Valera") == "es"
