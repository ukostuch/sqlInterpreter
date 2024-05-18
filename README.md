# SQL Interpreter

**Autorzy:** Urszula Kostuch, Wojciech Łabędź

## Opis

Projekt ten zawiera prosty interpreter dla języka SQL, który rozpoznaje i analizuje różne rodzaje instrukcji SQL. Projekt został podzielony na cztery pliki:

- **my_token.py**: Zawiera definicje tokenów dla analizatora leksykalnego.
- **grammar.py**: Zawiera definicje gramatyki oraz analizatora składniowego.
- **functions.py**: Zawiera implementację funkcji do wykonywania instrukcji SQL.
- **app.py**: Zawiera interfejs graficzny oparty na Flasku, umożliwiający użytkownikowi interakcję z interpreterem SQL przez przeglądarkę.

## Wymagania

Aby uruchomić ten projekt, wymagane jest środowisko Python 3 oraz biblioteka Ply (Python Lex-Yacc).

## Instalacja

1. Pobierz zawartość repozytorium na swój lokalny komputer.
2. Upewnij się, że masz zainstalowanego Pythona 3.
3. Zainstaluj bibliotekę Ply, jeśli nie masz jej jeszcze zainstalowanej:

    ```bash
    pip install ply
    ```

4. Zainstaluj dodatkowe wymagania:

    ```bash
    pip install flask pandas
    ```

## Uruchamianie

Upewnij się, że wszystkie pliki `my_token.py`, `grammar.py`, `functions.py`, i `app.py` są w tym samym katalogu.

1. Uruchom aplikację Flask:

    ```bash
    python app.py
    ```

2. Otwórz przeglądarkę i przejdź do adresu:

    ```
    http://127.0.0.1:5000/
    ```

## Użycie

1. Uruchom `app.py`, aby wyświetlić interfejs graficzny w przeglądarce.
2. W interfejsie graficznym możesz wprowadzać zapytania SQL w celu analizy plików CSV.

## Przykładowe zapytania SQL

Poniżej znajdują się przykładowe zapytania SQL, które możesz użyć do testowania parsera:

```sql
select coalesce(name,'brak') from database2;
select name from database2;

select comment_id, name from database3 order by name;

select comment_id, name from database3 order by name limit 2;

select name, count(comment_id) from database3 group by name;
select name, count(comment_id) from database3 group by name having name = alice;

select name from database3 left join database2 on database3.name = database2.name where comment_id > 2;
select distinct name from database3 left join database2 on database3.name = database2.name where comment_id > 2;


select comment_id,priority from database3 order by priority;
select comment_id,priority from database3 order by priority limit 3;

select name,avg(comment_id) from database3 group by name;

select count(name) from database3;


create table database5 (id int, name varchar(5));
insert into database5 (id,name) values (2,kasia);
select * from database5;
