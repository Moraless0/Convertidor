# Ejemplos

## sample_mybible.sql

Ejemplo mínimo de estructura MyBible para pruebas y documentación.

## Uso

```bash
sqlite3 sample.SQLite3 < sample_mybible.sql
python convert.py sample.SQLite3 sample.bblx --validate --verbose
```
