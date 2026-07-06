# Registro de decisiones técnicas

1. **Python 3.12+**: alineado con el requisito del proyecto.
2. **Solo biblioteca estándar + pytest**: evita dependencias innecesarias.
3. **Catálogo de libros separado**: facilita agregar canónicos extendidos más adelante.
4. **Salida SQLite nueva**: no se copia la base original; se genera un módulo nuevo.
5. **RTF mínimo**: suficiente para representar texto enriquecido sin destruir contenido.
6. **Validación no bloqueante por defecto**: útil para módulos incompletos o imperfectos.
