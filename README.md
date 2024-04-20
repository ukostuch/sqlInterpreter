# SQL Interpreter
# Autorzy: Urszula Kostuch, Wojciech Łabędź

## Opis
Projekt ten zawiera prosty interpreter dla języka SQL, który rozpoznaje i analizuje różne rodzaje instrukcji SQL. Projekt został podzielony na dwa pliki:

- `my_token.py`: Zawiera definicje tokenów dla analizatora leksykalnego
- `grammar.py`: Zawiera definicje gramatyki oraz analizatora składniowego

## Wymagania
Aby uruchomić ten projekt, wymagane jest środowisko Python 3 oraz biblioteka Ply (Python Lex-Yacc).

## Instalacja
1. Pobierz zawartość repozytorium na swój lokalny komputer.
2. Upewnij się, że masz zainstalowanego Pythona 3
3. Zainstaluj bibliotekę Ply, jeśli nie masz jej jeszcze zainstalowanej:
   
pip install ply

## Uruchamianie
1. Upewnij się, że oba pliki `my_token.py` i `grammar.py` są w tym samym katalogu.
2. Uruchom plik `grammar.py` za pomocą Pythona:

python grammar.py

## Użycie
Uruchom `grammar.py` po ustawieniu zawartości zmiennej 'results' przechowującej instrukcje SQL do analizy. 
Program wyświetli zidentyfikowane tokeny oraz wynik analizy składniowej.

## Przykładowe zapytania SQL
Poniżej znajdują się przykładowe zapytania SQL, które możesz użyć do testowania parsera:

- `SELECT id, name FROM users WHERE id = 1 AND age > 18 ORDER BY name ASC LIMIT 10;`
- `INSERT INTO table_name (column1, column2, column3) VALUES (value1, value2, value3);`
- `UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition;`
- `DELETE FROM table_name WHERE condition;`
- `CREATE TABLE table_name (column1 datatype, column2 datatype, column3 datatype);`
- `ALTER TABLE table_name ADD column_name datatype;`
- `DROP TABLE table_name;`
- `SELECT column1 FROM table1 UNION SELECT column1 FROM table2;`
- `SELECT column1 FROM table1 UNION ALL SELECT column1 FROM table2;`
- `SELECT column1 FROM table1 INTERSECT SELECT column1 FROM table2;`
- `SELECT column1 FROM table1 EXCEPT SELECT column1 FROM table2;`

