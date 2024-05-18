import ply.yacc as yacc
from grammar import *
import pandas as pd
import os


def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list

def save_data_to_file(data):
    with open('database.txt', 'w') as f:
        for row in data:
            f.write(','.join([str(value) for value in row.values()]) + '\n')


def read_data_from_file(path):
    data = pd.read_csv(path)
    return data


def write_data_to_file(df, file_path):
    df.to_csv(file_path, index=False)

# Funkcja wykonująca zapytanie SELECT
def execute_select_statement(statement):
    distinct = False
    column_count = 0
    column_names = []
    star = False
    table_name = ''
    done = False
    left_table = None
    table = None
    columns_to_group = []
    agg_cols = {}
    coalesce = {}
    order = None
    limit = 0
    i = 1
    while i < len(statement):
        if statement[i].lower() == 'distinct':
            distinct = True
            i += 1
            continue
        while statement[i].lower() != 'from' and done is False:
            if statement[i] == ',':
                i += 1
                continue
            if statement[i] == '*':
                star = True
                i += 1
                break
            if statement[i].lower() == 'avg' or statement[i].lower() == 'min' or statement[i].lower() == 'max' or \
                    statement[i].lower() == 'count' or statement[i].lower() == 'sum':
                i += 2
                column_count += 1
                column_names.append(statement[i].lower())
                agg_cols[statement[i].lower()] = statement[i - 2].lower()
                agg_cols[statement[i].lower()] = statement[i - 2].lower()
                i += 1
            elif statement[i].lower() == 'coalesce':
                i += 2
                column_count += 1
                column_names.append(statement[i].lower())
                coalesce[statement[i].lower()] = statement[i + 2]
                i += 3
            else:
                column_count += 1
                column_names.append(statement[i].lower())
            i += 1
        if statement[i].lower() == 'from':
            done = True
            i += 1
            table_name = statement[i]
            i += 1
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, table_name + '.csv')
            if not os.path.exists(file_path):
                return "Bledna nazwa tabeli"
            table = read_data_from_file(file_path)

        if statement[i].lower() == 'join':
            if left_table is None:
                current_directory = os.getcwd()
                file_path = os.path.join(current_directory, table_name + '.csv')
                if not os.path.exists(file_path):
                    return "Bledna nazwa tabeli"
                left_table = read_data_from_file(file_path)

            pom = statement[i - 1].lower()
            if not (pom == 'right' or pom == 'left' or pom == 'outer' or pom == 'inner' or pom == 'full'):
                pom = ''
            i += 1
            right_table_name = statement[i]
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, right_table_name + '.csv')
            if not os.path.exists(file_path):
                return "Bledna nazwa tabeli"
            right_table = read_data_from_file(file_path)

            i += 4
            left_column = statement[i]
            try:
                left_table[left_column]
            except:
                return "Wybranej kolumny nie ma w tabeli"
            i += 2
            if statement[i] != right_table_name:
                return "Niekomatybilna nazwa tabeli"
            i += 2
            right_column = statement[i]
            try:
                right_table[right_column]
            except:
                return "Wybranej kolumny nie ma w tabeli"

            if (pom == ''):
                left_table = pd.merge(left_table, right_table, left_on=left_column, right_on=right_column)
            else:
                left_table = pd.merge(left_table, right_table, how=pom, left_on=left_column, right_on=right_column)
            table = left_table

        if statement[i].lower() == 'where':
            logic = []
            df_table = []
            if left_table is not None: table = left_table
            i += 1
            i_p = i
            while (statement[i] != 'group' and statement[i] != 'order' and statement[i] != ';'):
                if statement[i] == 'and' or statement[i] == 'or':
                    substatement = statement[i_p:i]
                    logic.append(statement[i])
                    try:
                        substatement[2] = float(substatement[2])
                    except:
                        if table[substatement[0]].dtype == 'object':
                            pass
                        else:
                            return "Operacja arytmetyczna na błędnym typie"

                    if substatement[1] == '<':
                        df_table.append(table[table[substatement[0]] < substatement[2]])
                    elif substatement[1] == '<=':
                        df_table.append(table[table[substatement[0]] <= substatement[2]])
                    elif substatement[1] == '>':
                        df_table.append(table[table[substatement[0]] > substatement[2]])
                    elif substatement[1] == '>=':
                        df_table.append(table[table[substatement[0]] >= substatement[2]])
                    elif substatement[1] == '=':
                        df_table.append(table[table[substatement[0]] == substatement[2]])
                    i_p = i + 1
                i += 1

            if statement[i] == ';' or statement[i] == 'order':
                substatement = statement[i_p:i]
                try:
                    substatement[2] = float(substatement[2])
                except:
                    if table[substatement[0]].dtype == 'object':
                        pass
                    else:
                        return "Operacja arytmetyczna na błędnym typie"
                if substatement[1] == '<':
                    df_table.append(table[table[substatement[0]] < substatement[2]])
                elif substatement[1] == '<=':
                    df_table.append(table[table[substatement[0]] <= substatement[2]])
                elif substatement[1] == '>':
                    df_table.append(table[table[substatement[0]] > int(substatement[2])])
                elif substatement[1] == '>=':
                    df_table.append(table[table[substatement[0]] >= substatement[2]])
                elif substatement[1] == '=':
                    df_table.append(table[table[substatement[0]] == substatement[2]])

            result_table = df_table[0]
            count = 1
            for element in logic:
                if element.lower() == 'and':
                    result_table = pd.merge(result_table, df_table[count], how='inner')
                elif element.lower() == 'or':
                    result_table = pd.concat([result_table, df_table[count]])
                count += 1
            table = result_table

        if statement[i].lower() == 'group':
            i += 2
            while statement[i] != ';' and statement[i].lower() != 'having' and statement[i].lower() != 'order':
                if statement[i] == ',':
                    i += 1
                    continue
                columns_to_group.append(statement[i])
                i += 1
            try:
                for coln in column_names:
                    if coln not in columns_to_group and coln not in agg_cols.keys():
                        return "You cannot group like that"
                if len(agg_cols) == 0:
                    table = table.groupby(columns_to_group).first().reset_index()
                else:
                    for dicts in agg_cols.keys():
                        if agg_cols[dicts] == 'avg':
                            agg_cols[dicts] = 'mean'
                    table = table.groupby(columns_to_group).agg(agg_cols).reset_index()
            except:
                return "You cannot group like that"

        if statement[i].lower() == 'having':
            i += 1
            logic = []
            df_table = []
            i_p = i
            while statement[i] != ';' and statement[i] != 'order' and statement[i] != 'ORDER':
                if not isinstance(statement[i], int) and not isinstance(statement[i], float) and (
                        statement[i].lower() == 'count' or statement[i].lower() == 'avg' or statement[
                    i].lower() == 'min' or statement[i].lower() == 'max' or statement[i].lower() == 'sum'):
                    i += 2
                    if statement[i] in agg_cols.keys():
                        if agg_cols[statement[i]] == statement[i - 2].lower():
                            i += 2
                        else:
                            return "Błędne użycie w klauzuli Having"
                    else:
                        return "Błęne użycie w klauzuli Having"

                if statement[i] == 'and' or statement[i] == 'or':
                    substatement = statement[i_p:i]
                    logic.append(statement[i])

                    if substatement[0].lower() == 'count' or substatement[0].lower() == 'avg' or substatement[
                        0].lower() == 'sum' or substatement[0].lower() == 'min' or substatement[0].lower() == 'max':
                        i += 3
                        col_pod = substatement[2]
                        try:
                            substatement[5] = float(substatement[5])
                        except:
                            if table[substatement[2]].dtype == 'object':
                                pass
                            else:
                                return "Operacja arytmetyczna na błędnym typie"
                    else:
                        col_pod = substatement[0]
                        try:
                            substatement[2] = float(substatement[2])
                        except:
                            if table[substatement[0]].dtype == 'object':
                                pass
                            else:
                                return "Operacja arytmetyczna na błędnym typie"
                    try:
                        f = table[col_pod]
                    except:
                        return "Błędnie dobrane kolumny w klauzuli having";
                    if substatement[-2] == '<':
                        df_table.append(table[table[col_pod] < substatement[-1]])
                    elif substatement[-2] == '<=':
                        df_table.append(table[table[col_pod] <= substatement[-1]])
                    elif substatement[-2] == '>':
                        df_table.append(table[table[col_pod] > substatement[-1]])
                    elif substatement[-2] == '>=':
                        df_table.append(table[table[col_pod] >= substatement[-1]])
                    elif substatement[-2] == '=':
                        df_table.append(table[table[col_pod] == substatement[-1]])
                    i_p = i + 1
                i += 1

            if statement[i] == ';':
                substatement = statement[i_p:i]
                logic.append(statement[i])
                if substatement[0].lower() == 'count' or substatement[0].lower() == 'avg' \
                        or substatement[0].lower() == 'sum' or substatement[0].lower() == 'min' \
                        or substatement[0].lower() == 'max':
                    col_pod = substatement[2]
                    try:
                        substatement[5] = float(substatement[5])
                    except:
                        if table[substatement[2]].dtype == 'object':
                            pass
                        else:
                            return "Operacja arytmetyczna na błędnym typie"
                else:
                    col_pod = substatement[0]
                    try:
                        substatement[2] = float(substatement[2])
                    except:
                        if table[substatement[0]].dtype == 'object':
                            pass
                        else:
                            return "Operacja arytmetyczna na błędnym typie"
                try:
                    f = table[col_pod]
                except:
                    return "Błędnie dobrane kolumny w klauzuli having";
                if substatement[-2] == '<':
                    df_table.append(table[table[col_pod] < substatement[-1]])
                elif substatement[-2] == '<=':
                    df_table.append(table[table[col_pod] <= substatement[-1]])
                elif substatement[-2] == '>':
                    df_table.append(table[table[col_pod] > substatement[-1]])
                elif substatement[-2] == '>=':
                    df_table.append(table[table[col_pod] >= substatement[-1]])
                elif substatement[-2] == '=':
                    df_table.append(table[table[col_pod] == substatement[-1]])

            result_table = df_table[0]
            count = 1
            for element in logic:
                if element.lower() == 'and':
                    result_table = pd.merge(result_table, df_table[count], how='inner')
                elif element.lower() == 'or':
                    result_table = pd.concat([result_table, df_table[count]])
                count += 1
            table = result_table

        if statement[i].lower() == 'order':
            i += 2
            while statement[i].lower() != 'limit' and statement[i] != "LIMIT" and statement[i] != ';':
                if statement[i] == ',' or statement[i] == ')':
                    i += 1
                elif statement[i] == 'count' or statement[i] == 'COUNT' or statement[i] == 'avg' \
                        or statement[i] == 'AVG' or statement[i] == 'MAX' or statement[i] == 'max' \
                        or statement[i] == 'MIN' or statement[i] == 'min' or statement[i] == 'SUM' or statement[
                    i] == 'sum':
                    i += 2
                else:
                    try:
                        f = table[statement[i]]
                        if order is None:
                            order = []
                        order.append(statement[i])
                        i += 1
                    except:
                        return "Błędna kolumna w klauzuli order by"

        if statement[i] == 'limit' or statement[i] == 'LIMIT':
            i += 1
            if statement[i] <= 0:
                return "Błąd w klazuli limit"
            else:
                limit = statement[i]
            i += 1

        if statement[i] == ';':
            try:
                if star is True:
                    selected_columns = table
                    if order is not None:
                        selected_columns = selected_columns.sort_values(by=order)
                    if distinct:
                        selected_columns = selected_columns.drop_duplicates()
                    if limit != 0:
                        selected_columns = selected_columns.iloc[:limit]
                else:
                    selected_columns = table
                    if len(column_names) == 1 and len(agg_cols) == 1 and len(columns_to_group) == 0:
                        selected_columns = table[column_names]
                        if list(agg_cols.values())[0].lower() == 'avg':
                            selected_columns = selected_columns.mean()
                        elif list(agg_cols.values())[0].lower() == 'sum':
                            selected_columns = selected_columns.sum()
                        elif list(agg_cols.values())[0].lower() == 'count':
                            selected_columns = selected_columns.count()
                        elif list(agg_cols.values())[0].lower() == 'min':
                            selected_columns = selected_columns.min()
                        elif list(agg_cols.values())[0].lower() == 'max':
                            selected_columns = selected_columns.max()
                    elif len(columns_to_group) == 0 and (len(agg_cols) == 1 and len(agg_cols) != len(column_names)):
                        return "Nie mozna uzyc funkcji agregacyjnej gdy nie używamy grupowania po kolumnach z SELECT"
                    if len(coalesce) != 0:
                        for col in coalesce.keys():
                            if coalesce[col].startswith('\'') or coalesce[col].startswith('\"'):
                                coalesce[col] = coalesce[col][1:len(coalesce[col]) - 1]
                            selected_columns.loc[:, col] = selected_columns[col].fillna(coalesce[col])
                    if order is not None:
                        selected_columns = selected_columns.sort_values(by=order)
                    selected_columns = selected_columns[column_names]
                    if distinct:
                        selected_columns = selected_columns.drop_duplicates()
                    if limit != 0:
                        selected_columns = selected_columns.iloc[:limit]
            except:
                return "Błędne nazwy kolumn"
            if isinstance(selected_columns, pd.Series):
                selected_columns = selected_columns.to_frame()
            return selected_columns
        i += 1

    # Funkcja wykonująca zapytanie INSERT
def execute_insert_statement(statement):
    table_name = statement[2]
    columns = []
    values = []
    table = None
    status = False
    i = 4
    while i < len(statement):
        while i < len(statement) and statement[i] != ')' and not status:
            if statement[i] != ',':
                columns.append(statement[i])
            i += 1
        status = True
        i += 3
        while i < len(statement) and statement[i] != ')' and status:
            if statement[i] != ',':
                values.append(statement[i])
            i += 1
        i += 1
    #print(columns)
    #print(values)
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, table_name + '.csv')
    if not os.path.exists(file_path):
            return "Bledna nazwa tabeli"
    table = read_data_from_file(file_path)
    if len(columns) != len(values):
        return "Mismatch between column names and values"
    
    #new_row = dict(zip(columns, values))
    new_data = pd.DataFrame([dict(zip(columns, values))])
    #table = table.append(new_row, ignore_index=True)
    table = pd.concat([table, new_data], ignore_index=True)
    write_data_to_file(table, file_path)
    
    return "Inserted successfully."


# Funkcja wykonująca zapytanie CREATE
def execute_create_statement(statement):
    table_name = statement[2]
    i = 4
    i_p = i
    constraint_list = []
    df = pd.DataFrame()
    while i < len(statement) - 1:
        while statement[i] != ',' and (statement[i:i+2] != [')',';']):
            i += 1
        substatement = statement[i_p:i]
        #print(substatement)
        col_name = substatement[0]
        if substatement[1].lower() == 'int':
            df[col_name] = pd.Series(dtype=int)
            constraint_list = substatement[2:]
        elif substatement[1].lower() == 'float':
            df[col_name] = pd.Series(dtype=float)
            df[col_name] = df[col_name].round(substatement[3])
            constraint_list = substatement[5:]
        elif substatement[1].lower() == 'varchar':
            df[col_name] = pd.Series(dtype=str)
            df[col_name] = df[col_name].str.slice(0, 255)
            constraint_list = substatement[5:]

        i+=1
        i_p = i

    df.to_csv(os.path.join(table_name+'.csv'),index=False)

    return f"Table {table_name} created successfully."



# Przykładowe zapytania
# create_query = parser.parse("create table database4 (id int, name varchar(5));")
# select_query = parser.parse("select comment_id, name from database3 order by name limit 2;")
# select_query = parser.parse("select comment_id, name from database3 order by name;")
# select_query = parser.parse("select name, count(comment_id) from database3 group by name having name = alice;")
# select_query = parser.parse("select coalesce(name, 'name') from database3 left join database2 on database3.name = database2.name where comment_id > 2;")
# select_query = parser.parse("select distinct coalesce(name, 'name') from database3 left join database2 on database3.name = database2.name where comment_id > 2;")
# select_query = parser.parse("select priority from database3 order by comment_id limit 3;")
# select_query = parser.parse("select priority from database3 order by comment_id;")
# select_query= parser.parse("select count(name) from database3;")
# insert_query= parser.parse("INSERT INTO database3 (comment_id, name, priority) VALUES (30, kasia, 29);")

def return_results(my_query):
    queries = my_query.split(';')  
    results = []
    for i, query in enumerate(queries):
        query = query.strip()
        parser = yacc.yacc()
        if i < len(queries) - 1: 
            query += ';'
        if query:
            try:
                select_query = parser.parse(query)
                select_query = flatten(select_query)
                try:
                    result = execute_select_statement(select_query)
                except:
                    try:
                        result = execute_create_statement(select_query)
                    except:
                        try:
                            result = execute_insert_statement(select_query)
                        except:
                            return "Błędny typ zapytania"
                results.append(result)
            except SyntaxError as e:
                results.append(e.__str__())
    return results

#results = return_results("select priority from database3 order by comment_id;")
#for result in results:
#    print(result)

    