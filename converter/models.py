from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ModuleType(str, Enum):
    BIBLE = "bible"
    COMMENTARY = "commentary"
    DICTIONARY = "dictionary"
    DEVOTIONAL = "devotional"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class ColumnInfo:
    name: str
    data_type: str
    notnull: bool
    default_value: str | None
    primary_key: int


@dataclass(frozen=True, slots=True)
class IndexInfo:
    name: str
    unique: bool
    columns: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TableInfo:
    name: str
    sql: str | None
    columns: tuple[ColumnInfo, ...]
    indexes: tuple[IndexInfo, ...] = ()
    foreign_keys: tuple[tuple[str, str, str], ...] = ()


@dataclass(slots=True)
class ParsedSchema:
    tables: dict[str, TableInfo]
    module_type: ModuleType
    info_table: str | None = None
    books_table: str | None = None
    verses_table: str | None = None
    module_hints: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Metadata:
    name: str = ""
    abbreviation: str = ""
    language: str = ""
    description: str = ""
    version: str = ""
    author: str = ""
    publisher: str = ""
    publish_date: str = ""
    encoding: str = "UTF-8"
    source: str = ""
    raw: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class BookEntry:
    source_number: int
    esword_number: int | None
    osis_id: str
    short_name: str
    long_name: str
    category: str = "protestant"
    color: str | None = None
    is_present: bool = True


@dataclass(frozen=True, slots=True)
class VerseEntry:
    book_number: int
    chapter: int
    verse: int
    text: str


@dataclass(slots=True)
class BibleModule:
    source_path: Path
    schema: ParsedSchema
    metadata: Metadata
    books: list[BookEntry]
    verses: list[VerseEntry]
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    severity: Severity
    code: str
    message: str
    location: str | None = None


@dataclass(slots=True)
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(issue.severity is Severity.ERROR for issue in self.issues)

    def add(self, severity: Severity, code: str, message: str, location: str | None = None) -> None:
        self.issues.append(ValidationIssue(severity, code, message, location))
