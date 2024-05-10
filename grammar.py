import ply.yacc as yacc
from my_token import tokens
import pandas as pd
import os


#reguly gramatyki
def p_statement(p):
    '''statement : statement2
                | statement statement2'''
    p[0] = p[1:]


def p_statement2(p):
    '''statement2 : select_statement SEMICOLON
                 | insert_statement
                 | update_statement
                 | delete_statement
                 | create_statement
                 | alter_statement
                 | drop_statement
                 | select_statement UNION select_statement SEMICOLON
                 | select_statement UNION ALL select_statement SEMICOLON
                 | select_statement INTERSECT select_statement SEMICOLON
                 | select_statement EXCEPT select_statement SEMICOLON'''

    p[0] = p[1:]



def p_select_statement(p):
    '''
    select_statement : SELECT dist_list select_list FROM table_expr join_expr where_clause group_by_clause having_clause order_by_clause limit_clause
                     | SELECT dist_list select_list FROM table_expr join_expr where_clause order_by_clause
                     | SELECT dist_list select_list FROM table_expr join_expr where_clause group_by_clause having_clause
                     | SELECT dist_list select_list FROM table_expr join_expr where_clause group_by_clause order_by_clause limit_clause
                     | SELECT dist_list select_list FROM table_expr join_expr where_clause group_by_clause
                     | SELECT dist_list select_list FROM table_expr join_expr where_clause order_by_clause limit_clause
                     | SELECT dist_list select_list FROM table_expr join_expr where_clause
                     | SELECT dist_list select_list FROM table_expr join_expr
                     | SELECT dist_list select_list FROM table_expr where_clause group_by_clause having_clause order_by_clause limit_clause
                     | SELECT dist_list select_list FROM table_expr where_clause order_by_clause
                     | SELECT dist_list select_list FROM table_expr where_clause group_by_clause having_clause
                     | SELECT dist_list select_list FROM table_expr where_clause group_by_clause order_by_clause limit_clause
                     | SELECT dist_list select_list FROM table_expr where_clause group_by_clause
                     | SELECT dist_list select_list FROM table_expr where_clause order_by_clause limit_clause
                     | SELECT dist_list select_list FROM table_expr where_clause
                     | SELECT dist_list select_list FROM table_expr
                     | SELECT select_list FROM table_expr join_expr where_clause group_by_clause having_clause order_by_clause limit_clause
                     | SELECT select_list FROM table_expr join_expr where_clause order_by_clause
                     | SELECT select_list FROM table_expr join_expr where_clause group_by_clause having_clause
                     | SELECT select_list FROM table_expr join_expr where_clause group_by_clause order_by_clause limit_clause
                     | SELECT select_list FROM table_expr join_expr where_clause group_by_clause
                     | SELECT select_list FROM table_expr join_expr where_clause order_by_clause limit_clause
                     | SELECT select_list FROM table_expr join_expr where_clause
                     | SELECT select_list FROM table_expr join_expr
                     | SELECT select_list FROM table_expr where_clause group_by_clause having_clause order_by_clause limit_clause
                     | SELECT select_list FROM table_expr where_clause order_by_clause
                     | SELECT select_list FROM table_expr where_clause group_by_clause having_clause
                     | SELECT select_list FROM table_expr where_clause group_by_clause order_by_clause limit_clause
                     | SELECT select_list FROM table_expr where_clause group_by_clause
                     | SELECT select_list FROM table_expr where_clause order_by_clause limit_clause
                     | SELECT select_list FROM table_expr where_clause
                     | SELECT select_list FROM table_expr
    '''
    p[0] = p[1:]

def p_select_list(p):
    '''select_list : select_list COMMA select_item
                   | select_item
                   | TIMES
                   | conditional_expr'''
    p[0] = p[1:]


def p_dist_list(p):
    '''dist_list : DISTINCT'''
    p[0] = p[1:]      

def p_select_item(p):
    '''select_item : expression AS ID
                   | expression
                   | COALESCE LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                   | conditional_expr AS ID'''

    p[0] = p[1:]

def p_table_expr(p):
    '''table_expr : ID DOT ID
                  | ID'''

    p[0] = p[1:]

def p_where_clause(p):
    '''where_clause : 
                    | WHERE expression
                    | WHERE ID BETWEEN between_expr AND between_expr
                    | WHERE ID NOT BETWEEN between_expr AND between_expr
                    | WHERE ID IN LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                    | WHERE ID NOT IN LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                    | WHERE ID IN LEFT_PARENTHESIS select_statement RIGHT_PARENTHESIS
                    | WHERE ID NOT IN LEFT_PARENTHESIS select_statement RIGHT_PARENTHESIS
                    | WHERE ID LIKE STRING
                    '''
    p[0] = p[1:]

def p_between_expr(p):
    '''between_expr : ID
                  | ID DOT ID
                  | NUMBER
                  | ABS LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                  | ABS LEFT_PARENTHESIS NUMBER RIGHT_PARENTHESIS
                  | STRING
'''
    
    p[0] = p[1:]
    


def p_group_by_clause(p):
    '''group_by_clause : GROUP BY expression_list'''
    p[0] = p[1:]

def p_having_clause(p):
    '''having_clause : HAVING expression'''
    p[0] = p[1:]

def p_order_by_clause(p):
    '''order_by_clause : ORDER BY order_list'''
    p[0] = p[1:]

def p_order_item(p):
    '''order_item : expression ASC
                  | expression DESC
                  | expression'''
    p[0] = p[1:]

def p_order_list(p):
    '''order_list : order_list COMMA order_item
                  | order_item'''

    p[0] = p[1:]

def p_limit_clause(p):
    '''limit_clause : LIMIT NUMBER'''
    p[0] = p[1:]

def p_expression_list(p):
    '''expression_list : expression_list COMMA expression
                       | expression'''
    p[0] = p[1:]

def p_expression(p):
    '''expression : ID
                  | ID DOT ID
                  | NUMBER
                  | ABS LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                  | ABS LEFT_PARENTHESIS NUMBER RIGHT_PARENTHESIS
                  | STRING
                  | NULL
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUALS expression
                  | expression LESS_OR_EQUAL expression
                  | expression LESS_THAN expression
                  | expression GREATER_THAN expression
                  | expression GREATER_OR_EQUAL expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression
                  | DATEPART LEFT_PARENTHESIS ID COMMA STRING RIGHT_PARENTHESIS
                  | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
                  | COUNT LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                  | AVG LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                  | MIN LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                  | MAX LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                  | SUM LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                  | conditional_expr'''

    p[0] = p[1:]


def p_insert_statement(p):
    '''insert_statement : INSERT INTO ID LEFT_PARENTHESIS column_list RIGHT_PARENTHESIS VALUES LEFT_PARENTHESIS value_list RIGHT_PARENTHESIS SEMICOLON'''
    p[0] = p[1:]

def p_column_list(p):
    '''column_list : column_list COMMA ID
                   | ID'''
    p[0] = p[1:]

def p_value_list(p):
    '''value_list : value_list COMMA value
                  | value'''
    p[0] = p[1:]

def p_value(p):
    '''value : NUMBER
             | STRING
             | ID
             | NULL'''
    p[0] = p[1:]

def p_update_statement(p):
    '''update_statement : UPDATE ID SET set_list where_clause SEMICOLON'''
    p[0] = p[1:]

def p_conditional_expr(p):
    '''conditional_expr : IF expression THEN expression END
                        | IF expression THEN expression ELSE expression
                        | IF  expression THEN expression elsif_list ELSE expression END
                        | CASE case_expr END
                        '''
    p[0] = p[1:]

def p_elsif_list(p):
    '''elsif_list : ELSIF LEFT_PARENTHESIS expression THEN expression
                  | elsif_list ELSIF LEFT_PARENTHESIS expression THEN expression'''

    p[0] = p[1:]

def p_case_expr(p):
    '''case_expr : WHEN expression THEN expression
                 | WHEN expression THEN  expression case_expr'''
    p[0] = p[1:]

def p_set_list(p):
    '''set_list : set_list COMMA ID EQUALS value
                | ID EQUALS value'''

    p[0] = p[1:]

def p_delete_statement(p):
    '''delete_statement : DELETE FROM ID where_clause SEMICOLON'''
    p[0] = p[1:]

def p_create_statement(p):
    '''create_statement : CREATE TABLE ID LEFT_PARENTHESIS column_def_list RIGHT_PARENTHESIS SEMICOLON
                        | CREATE SCHEMA ID SEMICOLON
                        | CREATE FUNCTION ID LEFT_PARENTHESIS parameter_list RIGHT_PARENTHESIS RETURNS data_type LANGUAGE ID AS function_body
                        | CREATE OR REPLACE FUNCTION ID LEFT_PARENTHESIS parameter_list RIGHT_PARENTHESIS RETURNS data_type LANGUAGE ID AS function_body'''
    p[0] = p[1:]

def p_column_def_list(p):
    '''column_def_list : column_def_list COMMA column_def
                       | column_def'''
    p[0] = p[1:]

def p_column_def(p):
    '''column_def : ID data_type
                  | ID data_type column_constraints'''
    p[0] = p[1:]

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    p[0] = p[1:]

def p_parameter(p):
    '''parameter : ID data_type'''
    p[0] = p[1:]

def p_function_body(p):
    '''function_body : DOLARS DECLARE parameter_list SEMICOLON BEGIN STRING END SEMICOLON DOLARS SEMICOLON
    '''
    p[0] = p[1:]

def p_data_type(p):
    '''data_type : INT
                 | VARCHAR LEFT_PARENTHESIS NUMBER RIGHT_PARENTHESIS
                 | FLOAT LEFT_PARENTHESIS NUMBER RIGHT_PARENTHESIS'''

    p[0] = p[1:]

def p_column_constraints(p):
    '''column_constraints : column_constraints column_constraint
                          | column_constraint'''
    p[0] = p[1:]

def p_column_constraint(p):
    '''column_constraint : NOT NULL
                         | UNIQUE
                         | PRIMARY_KEY
                         | FOREIGN_KEY LEFT_PARENTHESIS ID RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                         | CHECK LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
                         | DEFAULT value'''
    p[0] = p[1:]


def p_join_expr(p):
    '''join_expr : join_type table_expr ON expression
                 | join_expr join_type table_expr ON expression'''

    p[0] = p[1:]

def p_join_type(p):
    '''join_type : INNER JOIN
                 | LEFT JOIN
                 | RIGHT JOIN
                 | FULL JOIN
                 | OUTER JOIN
                 | JOIN'''
    p[0] = p[1:]

def p_alter_statement(p):
    '''alter_statement : ALTER TABLE ID alter_actions SEMICOLON'''
    p[0] = p[1:]

def p_alter_actions(p):
    '''alter_actions : alter_actions alter_action
                     | alter_action'''
    p[0] = p[1:]

def p_alter_action(p):
    '''alter_action : ADD COLUMN column_def
                    | ADD CONSTRAINT ID constraint_def
                    | DROP COLUMN ID
                    | DROP CONSTRAINT ID'''
    p[0] = p[1:]


def p_constraint_def(p):
    '''constraint_def : UNIQUE LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                      | PRIMARY_KEY LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                      | FOREIGN_KEY LEFT_PARENTHESIS ID RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                      | CHECK LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
                      | DEFAULT value'''
    p[0] = p[1:]

def p_drop_statement(p):
    '''drop_statement : DROP TABLE ID SEMICOLON
                      | DROP COLUMN ID DOT ID SEMICOLON'''
    p[0] = p[1:]

def p_error(p):
    print("Syntax error in input!")

#budowanie parsera
parser = yacc.yacc()

#przykładowe zapytania:
#result = parser.parse("select a from b where a ~ 'm.*';")
#result = parser.parse("select datepart(year, '2017-12-03') from a;")
#result = parser.parse("select productid from q where q>0;")
#result = parser.parse("select distinct id from a intersect select id from b;")
#result = parser.parse("SELECT * from customers where a NOT IN (select customerid from orders);")
#result = parser.parse("SELECT x from a where a between a and abs(-6);")
#result = parser.parse("SELECT COALESCE(NULL, NULL, NULL, 'W3Schools.com', NULL, 'Example.com') from a;")
#result = parser.parse("SELECT CASE WHEN Quantity > 30 THEN x WHEN Quantity = 30 THEN 'The quantity is 30' END FROM OrderDetails;")
#result = parser.parse("CREATE FUNCTION a (arg1 int) returns int language plpgsql as $$ declare x int; begin 'aaa' end; $$;")
#result = parser.parse("create schema employee;")
#result = parser.parse("select distinct a from b;")
#result = parser.parse("DELETE FROM table_name WHERE x>y;")
#result = parser.parse("SELECT column1 FROM table1 EXCEPT SELECT column1 FROM table2;")
#result = parser.parse("ALTER TABLE table_name ADD COLUMN column_name int;")

#result = parser.parse("SELECT * from customers where a NOT IN (select customerid from orders);\nSELECT * from customers where a NOT IN (select customerid from orders);")
#print(result)








def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


# Funkcja do zapisu danych do pliku
def save_data_to_file(data):
    with open('database.txt', 'w') as f:
        for row in data:
            f.write(','.join([str(value) for value in row.values()]) + '\n')

# Funkcja do odczytu danych z pliku
def read_data_from_file(path):
    data = pd.read_csv(path)
    return data

# Funkcja wykonująca zapytanie SELECT
def execute_select_statement(statement):
    distinct=False
    join = False
    column_count=0
    column_names=[]
    star=False
    table_name=''
    done=False
    left_table = None
    right_table = None
    table=None
    result_table= None
    columns_to_group = []
    agg_cols = {}
    coalesce = {}
    order = None
    i=1
    #data = read_data_from_file()
    while i<len(statement):
        if statement[i].lower() == 'distinct':
            distinct=True
            i+=1
            continue
        while statement[i].lower()!='from' and done is False:
            if statement[i] ==',':
                i+=1
                continue
            if statement[i]=='*':
                star=True
                i+=1
                break
            if statement[i].lower() == 'avg' or statement[i].lower() == 'min' or statement[i].lower() == 'max' or statement[i].lower() == 'count' or statement[i].lower() == 'sum':
                i += 2
                column_count += 1
                column_names.append(statement[i].lower())
                agg_cols[statement[i].lower()] = statement[i-2].lower()
                agg_cols[statement[i].lower()] = statement[i-2].lower()
                i += 1
            elif statement[i].lower() == 'coalesce':
                i += 2
                column_count += 1
                column_names.append(statement[i].lower())
                coalesce[statement[i].lower()] = statement[i+2]
                i += 3
            else:
                column_count+=1
                column_names.append(statement[i].lower())
            i+=1
        if statement[i].lower()=='from':
            done = True
            i+=1
            table_name = statement[i]
            i+=1
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, table_name +'.csv')
            if not os.path.exists(file_path):
                return "Bledna nazwa tabeli"
            table = read_data_from_file(file_path)
    
        if statement[i].lower()=='join':
            #print('Jestem w joinie')
            if left_table is None:
                current_directory = os.getcwd()
                file_path = os.path.join(current_directory, table_name +'.csv')
                if not os.path.exists(file_path):
                    return "Bledna nazwa tabeli"
                left_table = read_data_from_file(file_path)

            pom = statement[i-1].lower()
            if not(pom =='right' or pom =='left' or pom=='outer' or pom =='inner' or pom == 'full'):
                pom=''
            i+=1
            right_table_name = statement[i]
            current_directory = os.getcwd()
            file_path = os.path.join(current_directory, right_table_name +'.csv')
            if not os.path.exists(file_path):
                return "Bledna nazwa tabeli"
            right_table = read_data_from_file(file_path)

            i+=4
            left_column=statement[i]
            try:
                left_table[left_column]
            except:
               return "Wybranej kolumny nie ma w tabeli"    
            i+=2
            if statement[i]!= right_table_name:
                return "Niekomatybilna nazwa tabeli"  
            i+=2
            right_column = statement[i]
            try:
                right_table[right_column]
            except:
               return "Wybranej kolumny nie ma w tabeli"
            
            if(pom==''): left_table = pd.merge(left_table, right_table, left_on = left_column, right_on = right_column)
            else: left_table = pd.merge(left_table, right_table, how=pom,left_on = left_column, right_on = right_column)
            table = left_table

        if statement[i].lower() =='where':
            logic=[]
            df_table = []
            if left_table is not None: table = left_table
            i+=1
            i_p = i
            while(statement[i]!='group' and statement[i]!='order' and statement[i]!=';'):
                if statement[i]=='and' or statement[i]=='or':
                    substatement = statement[i_p:i]
                    logic.append(statement[i])
                    try:
                        substatement[2]=float(substatement[2])
                    except: 
                        if table[substatement[0]].dtype == 'object':
                            pass
                        else:
                            return "Operacja arytmetyczna na błędnym typie"

                    if substatement[1]=='<':
                        df_table.append(table[table[substatement[0]]<substatement[2]])
                    elif substatement[1]=='<=':
                        df_table.append(table[table[substatement[0]]<=substatement[2]]) 
                    elif substatement[1]=='>':
                        df_table.append(table[table[substatement[0]]>substatement[2]]) 
                    elif substatement[1]=='>=':
                        df_table.append(table[table[substatement[0]]>=substatement[2]]) 
                    elif substatement[1]=='=':
                        df_table.append(table[table[substatement[0]]==substatement[2]])               
                    i_p =i+1
                i+=1

            if statement[i]==';' or statement[i] == 'order':
                substatement = statement[i_p:i]
                try:
                        substatement[2]=float(substatement[2])
                except: 
                        if table[substatement[0]].dtype == 'object':
                            pass
                        else:
                            return "Operacja arytmetyczna na błędnym typie"
                if substatement[1] == '<':
                    df_table.append(table[table[substatement[0]]<substatement[2]])
                elif substatement[1] == '<=':
                    df_table.append(table[table[substatement[0]]<=substatement[2]]) 
                elif substatement[1] == '>':
                    df_table.append(table[table[substatement[0]]>int(substatement[2])]) 
                elif substatement[1] == '>=':
                    df_table.append(table[table[substatement[0]]>=substatement[2]]) 
                elif substatement[1] == '=':
                    df_table.append(table[table[substatement[0]]==substatement[2]])

            result_table=df_table[0]
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
                if statement[i] ==',':
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
                if not isinstance(statement[i],int) and not isinstance(statement[i],float) and (statement[i].lower() == 'count' or statement[i].lower() == 'avg' or statement[i].lower() == 'min' or statement[i].lower() == 'max' or statement[i].lower() == 'sum'):
                    i += 2
                    if statement[i] in agg_cols.keys():
                        if agg_cols[statement[i]] == statement[i-2].lower():
                            i += 2
                        else:
                            return "Błędne użycie w klauzuli Having"
                    else:
                        return "Błęne użycie w klauzuli Having"

                if statement[i] == 'and' or statement[i] == 'or':
                    substatement = statement[i_p:i]
                    logic.append(statement[i])

                    if substatement[0].lower() == 'count' or substatement[0].lower() == 'avg' or substatement[0].lower() == 'sum' or substatement[0].lower() == 'min' or substatement[0].lower() == 'max':
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
                    i+=1
                elif statement[i] == 'count' or statement[i] == 'COUNT' or statement[i] == 'avg' \
                        or statement[i] == 'AVG' or statement[i] == 'MAX' or statement[i] == 'max' \
                        or statement[i] == 'MIN' or statement[i] == 'min' or statement[i] == 'SUM' or statement[i] == 'sum':
                    i+=2
                else:
                    try:
                        f = table[statement[i]]
                        if order is None:
                            order = []
                        order.append(statement[i])
                        i += 1
                    except:
                        return "Błędna kolumna w klauzuli order by"

        if statement[i] == ';':
            try:
               if star is True:
                   selected_columns = table
               else:
                   selected_columns = table[column_names]
                   if len(column_names) == 1 and len(agg_cols) == 1 and len(columns_to_group) == 0:
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
                               coalesce[col] = coalesce[col][1:len(coalesce[col])-1]
                           selected_columns.loc[:, col] = selected_columns[col].fillna(coalesce[col])
                   if order is not None:
                        selected_columns = selected_columns.sort_values(by=order)
                   if distinct:
                       selected_columns = selected_columns.drop_duplicates()
            except:
               return "Błędne nazwy kolumn"  
            return selected_columns
        i+=1       
    
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
#select_query = parser.parse("select comment_id, name from database3 order by name;")
#select_query = parser.parse("select name, count(comment_id) from database3 group by name having name = alice;")
#select_query = parser.parse("select coalesce(name, 'name') from database3 left join database2 on database3.name = database2.name where comment_id > 2;")
#insert_query = parser.parse("INSERT INTO table (Name, Age) VALUES ('John', 30);")
#update_query = parser.parse("UPDATE table SET Age = 35 WHERE Name = 'John';")
#delete_query = parser.parse("DELETE FROM table WHERE Name = 'John';")
#alter_query = parser.parse("ALTER TABLE table ADD COLUMN new_column INT;")
#create_query = parser.parse("CREATE TABLE new_table (ID INT, Name VARCHAR);")
#drop_query = parser.parse("DROP TABLE table;")



select_query = flatten(select_query)
print(select_query)

# Wykonanie zapytań
select_result = execute_select_statement(select_query)
#insert_result = execute_insert_statement(insert_query)
#update_result = execute_update_statement(update_query)
#delete_result = execute_delete_statement(delete_query)
#alter_result = execute_alter_statement(alter_query)
#create_result = execute_create_statement(create_query)
#drop_result = execute_drop_statement(drop_query)

# Wyświetlenie wyników
print(select_result)
#print("INSERT result:", insert_result)
#print("UPDATE result:", update_result)
#print("DELETE result:", delete_result)
#print("ALTER result:", alter_result)
#print("CREATE result:", create_result)
#print("DROP result:", drop_result)