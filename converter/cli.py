from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import logging
from pathlib import Path

from .exporter import export_bblx
from .mapper import map_books, map_verses
from .metadata import enrich_metadata
from .models import BibleModule
from .parser import parse_module
from .validator import validate_module


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convierte módulos MyBible SQLite a e-Sword BBLX.")
    parser.add_argument("entrada", type=Path, help="Archivo MyBible SQLite (.SQLite3/.db/.sqlite)")
    parser.add_argument("salida", type=Path, nargs="?", help="Archivo de salida .bblx")
    parser.add_argument("--output", dest="output", type=Path, help="Sobrescribe la ruta de salida")
    parser.add_argument("--verbose", action="store_true", help="Registro detallado")
    parser.add_argument("--debug", action="store_true", help="Registro de depuración")
    parser.add_argument("--log", dest="log_path", type=Path, help="Archivo de log")
    parser.add_argument("--force", action="store_true", help="Sobrescribe el archivo de salida")
    parser.add_argument("--metadata", action="store_true", help="Guarda un informe de metadata en JSON")
    parser.add_argument("--validate", action="store_true", help="Ejecuta validaciones antes de exportar")
    return parser


def _configure_logging(verbose: bool, debug: bool, log_path: Path | None) -> None:
    level = logging.INFO if verbose else logging.WARNING
    if debug:
        level = logging.DEBUG
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _configure_logging(args.verbose, args.debug, args.log_path)
    logger = logging.getLogger("convertidor")

    output = args.output or args.salida
    if output is None:
        output = args.entrada.with_suffix(".bblx")

    logger.info("Leyendo metadata...")
    schema, metadata, books, verses, warnings = parse_module(args.entrada)
    metadata = enrich_metadata(metadata, args.entrada, schema, books)

    logger.info("Detectando tablas...")
    logger.debug("Tablas detectadas: %s", ", ".join(sorted(schema.tables)))
    for warning in warnings:
        logger.warning(warning)

    logger.info("Mapeando libros...")
    mapped_books = map_books(books)
    for warning in mapped_books.warnings:
        logger.warning(warning)

    logger.info("Convirtiendo versículos...")
    mapped_verses = map_verses(verses)

    module = BibleModule(
        source_path=args.entrada,
        schema=schema,
        metadata=metadata,
        books=mapped_books.books,
        verses=mapped_verses,
        warnings=warnings + mapped_books.warnings,
    )

    if args.validate:
        logger.info("Validando...")
        report = validate_module(module)
        for issue in report.issues:
            logger.log(logging.ERROR if issue.severity.value == "error" else logging.WARNING, "%s: %s", issue.code, issue.message)
        if report.has_errors:
            logger.warning("La validación encontró errores, pero la exportación continuará.")

    logger.info("Exportando...")
    export_bblx(module, output, force=args.force)
    if args.metadata:
        metadata_path = output.with_suffix(output.suffix + ".metadata.json")
        metadata_path.write_text(json.dumps(asdict(metadata), ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Informe de metadata guardado en %s", metadata_path)

    logger.info("Conversión finalizada.")
    return 0
