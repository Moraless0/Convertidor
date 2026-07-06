# Comparación de formatos

## MyBible

- Contenedor SQLite.
- Tablas frecuentes: `info`, `books` / `books_all`, `verses`.
- Metadata como pares `name/value`.
- El texto puede incluir marcado embebido.
- El esquema puede variar ligeramente entre versiones o tipos de módulo.

## e-Sword BBLX

- Contenedor SQLite.
- Tablas mínimas útiles: `Details`, `Bible`.
- `Bible` usa claves lógicas de libro/capítulo/versículo.
- `Scripture` se guarda como RTF en la práctica comunitaria.

## Transformaciones aplicadas

| MyBible | e-Sword | Motivo |
| --- | --- | --- |
| `info` | `Details` | Normalizar metadata en un esquema esperado por e-Sword |
| `books` / `books_all` | catálogo interno | Mapear numeración legacy de MyBible al catálogo objetivo |
| `verses.text` | `Bible.Scripture` | Exportar texto compatible con e-Sword |
| Tags embebidos | RTF mínimo | Conservar negritas, cursivas y saltos de línea |
