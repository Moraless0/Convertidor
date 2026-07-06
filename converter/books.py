from __future__ import annotations

from dataclasses import dataclass

from .models import BookEntry


@dataclass(frozen=True, slots=True)
class BookDefinition:
    source_number: int
    esword_number: int | None
    osis_id: str
    short_name: str
    long_name: str
    category: str = "protestant"
    color: str | None = None


PROTESTANT_BOOKS: tuple[BookDefinition, ...] = (
    BookDefinition(10, 1, "Gen", "Gen", "Génesis", "protestant", "#ccccff"),
    BookDefinition(20, 2, "Exod", "Exod", "Éxodo", "protestant", "#ccccff"),
    BookDefinition(30, 3, "Lev", "Lev", "Levítico", "protestant", "#ccccff"),
    BookDefinition(40, 4, "Num", "Num", "Números", "protestant", "#ccccff"),
    BookDefinition(50, 5, "Deut", "Deut", "Deuteronomio", "protestant", "#ccccff"),
    BookDefinition(60, 6, "Josh", "Jos", "Josué", "protestant", "#ffcc99"),
    BookDefinition(70, 7, "Judg", "Jue", "Jueces", "protestant", "#ffcc99"),
    BookDefinition(80, 8, "Ruth", "Rut", "Rut", "protestant", "#ffcc99"),
    BookDefinition(90, 9, "1Sam", "1Sa", "1 Samuel", "protestant", "#ffcc99"),
    BookDefinition(100, 10, "2Sam", "2Sa", "2 Samuel", "protestant", "#ffcc99"),
    BookDefinition(110, 11, "1Kgs", "1Re", "1 Reyes", "protestant", "#ffcc99"),
    BookDefinition(120, 12, "2Kgs", "2Re", "2 Reyes", "protestant", "#ffcc99"),
    BookDefinition(130, 13, "1Chr", "1Cr", "1 Crónicas", "protestant", "#ffcc99"),
    BookDefinition(140, 14, "2Chr", "2Cr", "2 Crónicas", "protestant", "#ffcc99"),
    BookDefinition(150, 15, "Ezra", "Esd", "Esdras", "protestant", "#ffcc99"),
    BookDefinition(160, 16, "Neh", "Neh", "Nehemías", "protestant", "#ffcc99"),
    BookDefinition(190, 17, "Esth", "Est", "Ester", "protestant", "#ffcc99"),
    BookDefinition(220, 18, "Job", "Job", "Job", "protestant", "#66ff99"),
    BookDefinition(230, 19, "Ps", "Sal", "Salmos", "protestant", "#66ff99"),
    BookDefinition(240, 20, "Prov", "Pro", "Proverbios", "protestant", "#66ff99"),
    BookDefinition(250, 21, "Eccl", "Ecl", "Eclesiastés", "protestant", "#66ff99"),
    BookDefinition(260, 22, "Song", "Cnt", "Cantares", "protestant", "#66ff99"),
    BookDefinition(290, 23, "Isa", "Isa", "Isaías", "protestant", "#ff9fb4"),
    BookDefinition(300, 24, "Jer", "Jer", "Jeremías", "protestant", "#ff9fb4"),
    BookDefinition(310, 25, "Lam", "Lam", "Lamentaciones", "protestant", "#ff9fb4"),
    BookDefinition(330, 26, "Ezek", "Eze", "Ezequiel", "protestant", "#ff9fb4"),
    BookDefinition(340, 27, "Dan", "Dan", "Daniel", "protestant", "#ff9fb4"),
    BookDefinition(350, 28, "Hos", "Os", "Oseas", "protestant", "#99ccff"),
    BookDefinition(360, 29, "Joel", "Jl", "Joel", "protestant", "#99ccff"),
    BookDefinition(370, 30, "Amos", "Am", "Amós", "protestant", "#99ccff"),
    BookDefinition(380, 31, "Obad", "Abd", "Abdías", "protestant", "#99ccff"),
    BookDefinition(390, 32, "Jonah", "Jon", "Jonás", "protestant", "#99ccff"),
    BookDefinition(400, 33, "Mic", "Mi", "Miqueas", "protestant", "#99ccff"),
    BookDefinition(410, 34, "Nah", "Nah", "Nahúm", "protestant", "#99ccff"),
    BookDefinition(420, 35, "Hab", "Hab", "Habacuc", "protestant", "#99ccff"),
    BookDefinition(430, 36, "Zeph", "Sof", "Sofonías", "protestant", "#99ccff"),
    BookDefinition(440, 37, "Hag", "Hag", "Hageo", "protestant", "#99ccff"),
    BookDefinition(450, 38, "Zech", "Zac", "Zacarías", "protestant", "#99ccff"),
    BookDefinition(460, 39, "Mal", "Mal", "Malaquías", "protestant", "#99ccff"),
    BookDefinition(470, 40, "Matt", "Mat", "Mateo", "protestant", "#ffff99"),
    BookDefinition(480, 41, "Mark", "Mar", "Marcos", "protestant", "#ffff99"),
    BookDefinition(490, 42, "Luke", "Luc", "Lucas", "protestant", "#ffff99"),
    BookDefinition(500, 43, "John", "Jua", "Juan", "protestant", "#ffff99"),
    BookDefinition(510, 44, "Acts", "Hch", "Hechos", "protestant", "#ffff99"),
    BookDefinition(520, 45, "Rom", "Rom", "Romanos", "protestant", "#ffff99"),
    BookDefinition(530, 46, "1Cor", "1Co", "1 Corintios", "protestant", "#ffff99"),
    BookDefinition(540, 47, "2Cor", "2Co", "2 Corintios", "protestant", "#ffff99"),
    BookDefinition(550, 48, "Gal", "Gál", "Gálatas", "protestant", "#ffff99"),
    BookDefinition(560, 49, "Eph", "Efe", "Efesios", "protestant", "#ffff99"),
    BookDefinition(570, 50, "Phil", "Fil", "Filipenses", "protestant", "#ffff99"),
    BookDefinition(580, 51, "Col", "Col", "Colosenses", "protestant", "#ffff99"),
    BookDefinition(590, 52, "1Thess", "1Ts", "1 Tesalonicenses", "protestant", "#ffff99"),
    BookDefinition(600, 53, "2Thess", "2Ts", "2 Tesalonicenses", "protestant", "#ffff99"),
    BookDefinition(610, 54, "1Tim", "1Ti", "1 Timoteo", "protestant", "#ffff99"),
    BookDefinition(620, 55, "2Tim", "2Ti", "2 Timoteo", "protestant", "#ffff99"),
    BookDefinition(630, 56, "Titus", "Tit", "Tito", "protestant", "#ffff99"),
    BookDefinition(640, 57, "Phlm", "Flm", "Filemón", "protestant", "#ffff99"),
    BookDefinition(650, 58, "Heb", "Heb", "Hebreos", "protestant", "#ffff99"),
    BookDefinition(660, 59, "Jas", "Stg", "Santiago", "protestant", "#ffff99"),
    BookDefinition(670, 60, "1Pet", "1Pe", "1 Pedro", "protestant", "#ffff99"),
    BookDefinition(680, 61, "2Pet", "2Pe", "2 Pedro", "protestant", "#ffff99"),
    BookDefinition(690, 62, "1John", "1Jn", "1 Juan", "protestant", "#ffff99"),
    BookDefinition(700, 63, "2John", "2Jn", "2 Juan", "protestant", "#ffff99"),
    BookDefinition(710, 64, "3John", "3Jn", "3 Juan", "protestant", "#ffff99"),
    BookDefinition(720, 65, "Jude", "Jud", "Judas", "protestant", "#ffff99"),
    BookDefinition(730, 66, "Rev", "Apo", "Apocalipsis", "protestant", "#ffff99"),
)

APOCRYPHA_BOOKS: tuple[BookDefinition, ...] = (
    BookDefinition(170, None, "Tob", "Tob", "Tobit", "apocrypha", "#ffcc99"),
    BookDefinition(180, None, "Jdt", "Jdt", "Judit", "apocrypha", "#ffcc99"),
    BookDefinition(192, None, "AddEsth", "AddEsth", "Adiciones a Ester", "apocrypha", "#c0c0c0"),
    BookDefinition(165, None, "2Esd", "2Esd", "2 Esdras", "apocrypha", "#ffcc99"),
    BookDefinition(270, None, "Wis", "Sab", "Sabiduría", "apocrypha", "#66ff99"),
    BookDefinition(280, None, "Sir", "Eclo", "Eclesiástico", "apocrypha", "#66ff99"),
)

ORTHODOX_BOOKS: tuple[BookDefinition, ...] = (
    BookDefinition(145, None, "PrMan", "OrMan", "Oración de Manasés", "orthodox", "#66ff99"),
    BookDefinition(305, None, "PrAzar", "OrAz", "Oración de Azarías", "orthodox", "#c0c0c0"),
    BookDefinition(315, None, "EpJer", "EpJer", "Carta de Jeremías", "orthodox", "#ff9fb4"),
    BookDefinition(323, None, "AddDan", "AddDan", "Adiciones a Daniel", "orthodox", "#c0c0c0"),
    BookDefinition(325, None, "Sus", "Sus", "Susana", "orthodox", "#c0c0c0"),
    BookDefinition(341, None, "DanGr", "DanGr", "Daniel griego", "orthodox", "#c0c0c0"),
    BookDefinition(345, None, "Bel", "Bel", "Bel y el dragón", "orthodox", "#c0c0c0"),
)

BOOK_LOOKUP = {book.source_number: book for book in PROTESTANT_BOOKS + APOCRYPHA_BOOKS + ORTHODOX_BOOKS}


def build_book_entry(source_number: int) -> BookEntry | None:
    definition = BOOK_LOOKUP.get(source_number)
    if definition is None:
        return None
    return BookEntry(
        source_number=definition.source_number,
        esword_number=definition.esword_number,
        osis_id=definition.osis_id,
        short_name=definition.short_name,
        long_name=definition.long_name,
        category=definition.category,
        color=definition.color,
    )
