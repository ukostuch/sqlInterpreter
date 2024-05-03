from my_token import tokens
from grammar import *
import ply.yacc as yacc
import numpy as np

parser = yacc.yacc()


# Funkcja do zapisu danych do pliku
def save_data_to_file(data):
    with open('database.txt', 'w') as f:
        for row in data:
            f.write(','.join([str(value) for value in row.values()]) + '\n')

# Funkcja do odczytu danych z pliku
def read_data_from_file():
    with open('database.txt', 'r') as f:
        data = []
        for line in f:
            values = line.strip().split(',')
            data.append({'ID': int(values[0]), 'Name': values[1], 'Age': int(values[2])})
        return data

# Funkcja wykonująca zapytanie SELECT
def execute_select_statement(statement):
    data = read_data_from_file()
    if statement[0] == '*':
        return data
    else:
        selected_columns = statement[0]
        return [{column: row[column] for column in selected_columns} for row in data]

# Funkcja wykonująca zapytanie INSERT
def execute_insert_statement(statement):
    columns = statement[5]
    values = statement[9]

    data = read_data_from_file()

    new_id = len(data) + 1
    new_record = {'ID': new_id}
    for i in range(len(columns)):
        new_record[columns[i]] = values[i]

    data.append(new_record)
    save_data_to_file(data)
    return "Inserted successfully."

# Funkcja wykonująca zapytanie UPDATE
def execute_update_statement(statement):
    set_list = statement[4]
    where_clause = statement[5]

    data = read_data_from_file()

    for row in data:
        if where_clause and row.get(where_clause[2]) == where_clause[4]:
            for i in range(0, len(set_list), 3):
                column = set_list[i]
                new_value = set_list[i+2]
                row[column] = new_value
    save_data_to_file(data)
    return f"Updated successfully."

# Funkcja wykonująca zapytanie DELETE
def execute_delete_statement(statement):
    where_clause = statement[3]

    data = read_data_from_file()

    if where_clause:
        data[:] = [row for row in data if row.get(where_clause[1]) != where_clause[3]]
    else:
        data.clear()
    save_data_to_file(data)
    return f"Deleted successfully."

# Funkcja wykonująca zapytanie ALTER
def execute_alter_statement(statement):
    alter_actions = statement[4]

    data = read_data_from_file()

    for action in alter_actions:
        if action[1] == 'ADD':
            # Obsługa dodawania kolumny
            column_name = action[3]
            data[:] = [{**row, column_name: None} for row in data]
        elif action[1] == 'DROP':
            # Obsługa usuwania kolumny
            column_name = action[3]
            for row in data:
                row.pop(column_name, None)
    save_data_to_file(data)
    return f"Altered successfully."

# Funkcja wykonująca zapytanie CREATE
def execute_create_statement(statement):
    # Obsługa tworzenia tabeli - tutaj można dodać obsługę tworzenia schematu, funkcji, itp.
    table_name = statement[3]
    column_def_list = statement[6]

    data = read_data_from_file()

    # Przygotowanie struktury nowej tabeli
    new_table_data = []
    for row in data:
        new_row = {}
        for column_def in column_def_list:
            column_name = column_def[0]
            new_row[column_name] = None
        new_table_data.append(new_row)

    # Zapisanie nowej tabeli do pliku
    save_data_to_file(new_table_data)
    return f"Table {table_name} created successfully."

# Funkcja wykonująca zapytanie DROP
def execute_drop_statement(statement):
    object_type = statement[1]
    object_name = statement[3]

    if object_type == 'TABLE':
        # Obsługa usuwania tabeli
        save_data_to_file([])
        return f"Table {object_name} dropped successfully."
    elif object_type == 'COLUMN':
        # Obsługa usuwania kolumny - można zaimplementować w razie potrzeby
        pass
    else:
        return f"Invalid DROP operation."

# Przykładowe zapytania
select_query = parser.parse("SELECT * FROM table;")
insert_query = parser.parse("INSERT INTO table (Name, Age) VALUES ('John', 30);")
update_query = parser.parse("UPDATE table SET Age = 35 WHERE Name = 'John';")
delete_query = parser.parse("DELETE FROM table WHERE Name = 'John';")
alter_query = parser.parse("ALTER TABLE table ADD COLUMN new_column INT;")
create_query = parser.parse("CREATE TABLE new_table (ID INT, Name VARCHAR);")
drop_query = parser.parse("DROP TABLE table;")


print(select_query)
# Wykonanie zapytań
#select_result = execute_select_statement(select_query)
#insert_result = execute_insert_statement(insert_query)
#update_result = execute_update_statement(update_query)
#delete_result = execute_delete_statement(delete_query)
#alter_result = execute_alter_statement(alter_query)
#create_result = execute_create_statement(create_query)
#drop_result = execute_drop_statement(drop_query)

# Wyświetlenie wyników
#print("SELECT result:", select_result)
#print("INSERT result:", insert_result)
#print("UPDATE result:", update_result)
#print("DELETE result:", delete_result)
#print("ALTER result:", alter_result)
#print("CREATE result:", create_result)
#print("DROP result:", drop_result)