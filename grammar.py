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
    '''create_statement : CREATE TABLE ID LEFT_PARENTHESIS column_def_list RIGHT_PARENTHESIS SEMICOLON'''
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





