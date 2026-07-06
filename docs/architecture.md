# Arquitectura

```mermaid
flowchart TD
    Input[MyBible SQLite] --> Parser[parser.py]
    Parser --> Schema[ParsedSchema]
    Parser --> Metadata[metadata.py]
    Parser --> Books[mapper.py]
    Parser --> Verses[validator.py]
    Validator --> Exporter[exporter.py]
    Exporter --> Output[e-Sword BBLX]
```

## Objetivos de diseño

- separar lectura, mapeo, validación y exportación;
- facilitar la extensión a otros tipos de módulos;
- mantener el código pequeño y testeable;
- registrar toda anomalía sin perder el flujo cuando sea posible.
