CREATE TABLE info (name TEXT, value TEXT);
CREATE TABLE books (book_number INTEGER, short_name TEXT, long_name TEXT, book_color TEXT, is_present INTEGER);
CREATE TABLE verses (book_number INTEGER, chapter INTEGER, verse INTEGER, text TEXT);

INSERT INTO info VALUES
  ('language', 'es'),
  ('description', 'Biblia de ejemplo'),
  ('abbreviation', 'EJEMPLO'),
  ('version', '1.0'),
  ('author', 'Devin');

INSERT INTO books VALUES
  (10, 'Gn', 'Génesis', '#ccccff', 1),
  (470, 'Mt', 'Mateo', '#ffff99', 1);

INSERT INTO verses VALUES
  (10, 1, 1, '<b>En el principio</b> creó Dios los cielos y la tierra.'),
  (10, 1, 2, 'Y la tierra estaba desordenada y vacía.'),
  (470, 1, 1, 'Libro de la genealogía de Jesucristo.');
