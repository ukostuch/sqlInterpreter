import ply.lex as lex
import ply.yacc as yacc
import re

keywords = [
    'select','from', 'where', 'and', 'or','function', 'language', 'float','update', 'elsif', 'begin','declare','returns','dolars','delete', 'group', 'having', 'insert', 'values', 'order', 'by', 'asc', 'desc', 'join', 'left', 'right', 'inner', 'outer', 'on', 'limit', 'distinct', 'union', 'all', 'as', 'case', 'when', 'then', 'else', 'end', 'except', 'intersect', 'sum', 'avg', 'max', 'min', 'count', 'coalesce', 'unique', 'null', 'if', 'create', 'replace', 'abs', 'datepart', 'alter', 'table', 'column', 'drop', 'between', 'database', 'schema', 'exists', 'any', 'in', 'into', 'full','check', 'default', 'primary key', 'foreign key', 'constraint', 'not', 'set', 'add', 'references','int', 'varchar'
]

tokens = (
    'SELECT',
    'FROM',
    'WHERE',
    'BEGIN',
    'RETURNS',
    'DECLARE',
    'DOLARS',
    'LANGUAGE',
    'ID',
    'DOT',
    'ELSIF',
    'NUMBER',
    'COMMA',
    'EQUALS',
    'AND',
    'OR',
    'FUNCTION',  #
    'REFERENCES',
    'UPDATE',
    'DELETE',
    'FLOAT',
    'GROUP',
    'HAVING',
    'INSERT',
    'VALUES',
    'ORDER',
    'BY',
    'ASC',
    'DESC',
    'JOIN',
    'LEFT',
    'RIGHT',
    'INNER',
    'OUTER',
    'ON',
    'LIMIT',
    'DISTINCT', 
    'UNION',    
    'AS',       
    'CASE',      
    'WHEN',     
    'ELSE',    
    'END',    
    'EXCEPT', 
    'INTERSECT', 
    'SUM',
    'AVG',
    'MAX',
    'MIN',
    'COUNT',
    'COALESCE',  
    'UNIQUE',    
    'NULL',      
    'IF',        
    'THEN',            
    'CREATE',     #
    'REPLACE',    #
    'ABS',        
    'DATEPART',   
    'ALTER',       
    'TABLE',
    'SCHEMA',
    'COLUMN',
    'DROP',       
    'BETWEEN',    
    'DATABASE',
    'EXISTS',     
    'ALL',        #
    'ANY',        #
    'IN',         
    'INTO',
    'FULL',
    'LIKE',       
    'CHECK',      
    'DEFAULT',    
    'PRIMARY_KEY', #
    'FOREIGN_KEY', #
    'CONSTRAINT', 
    'STRING',      
    'LESS_THAN',
    'GREATER_THAN',
    'LESS_OR_EQUAL',
    'GREATER_OR_EQUAL',
    'NOT',
    'SEMICOLON',
    'NEWLINE',
    #'SPACE',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'TIMES',
    'SET',
    'ADD',        
    'INT',
    'VARCHAR'
)

t_SELECT = r'select|SELECT'
t_FROM = r'from|FROM'
t_WHERE = r'where|WHERE'
t_COMMA = r','
t_EQUALS = r'='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_OR_EQUAL = r'<='
t_GREATER_OR_EQUAL = r'>='
t_DOT = r'\.'
t_AND = r'and|AND'
t_OR = r'or|OR'
t_BEGIN = r'begin|BEGIN'
t_RETURNS = r'returns|RETURNS'
t_DECLARE = r'declare|DECLARE'
t_LANGUAGE = r'language|LANGUAGE'
t_DOLARS = r'\$\$'
t_FUNCTION = r'function|FUNCTION'
t_REFERENCES = r'references|REFERENCES'
t_UPDATE = r'update|UPDATE'
t_DELETE = r'delete|DELETE'
t_GROUP = r'group|GROUP'
t_FLOAT = r'float|FLOAT'
t_HAVING = r'having|HAVING'
t_INSERT = r'insert|INSERT'
t_VALUES = r'values|VALUES'
t_ORDER = r'order|ORDER'
t_BY = r'by|BY'
t_ELSIF = r'ELSEIF|elseif'
t_ASC = r'asc|ASC'
t_DESC = r'desc|DESC'
t_JOIN = r'join|JOIN'
t_LEFT = r'left|LEFT'
t_RIGHT = r'right|RIGHT'
t_INNER = r'inner|INNER'
t_OUTER = r'outer|OUTER'
t_ON = r'on|ON'
t_LIMIT = r'limit|LIMIT'
t_DISTINCT = r'distinct|DISTINCT'
t_UNION = r'union|UNION'
t_ALL = r'all|ALL'
t_AS = r'as|AS'
t_CASE = r'case|CASE'
t_WHEN = r'when|WHEN'
t_THEN = r'then|THEN'
t_ELSE = r'else|ELSE'
t_END = r'end|END'
t_EXCEPT = r'except|EXCEPT'
t_INTERSECT = r'intersect|INTERSECT'
t_SUM = r'sum|SUM'
t_AVG = r'avg|AVG'
t_MAX = r'max|MAX'
t_MIN = r'min|MIN'
t_COUNT = r'count|COUNT'
t_COALESCE = r'coalesce|COALESCE'
t_UNIQUE = r'unique|UNIQUE'
t_NULL = r'null|NULL'
t_IF = r'if|IF'
t_CREATE = r'create|CREATE'
t_REPLACE = r'replace|REPLACE'
t_ABS = r'abs|ABS'
t_DATEPART = r'datepart|DATEPART'
t_ALTER = r'alter|ALTER'
t_TABLE = r'table|TABLE'
t_SCHEMA = r'schema|SCHEMA'
t_COLUMN = r'column|COLUMN'
t_DROP = r'drop|DROP'
t_BETWEEN = r'between|BETWEEN'
t_DATABASE = r'database|DATABASE'
t_EXISTS = r'exists|EXISTS'
t_ANY = r'any|ANY'
t_IN = r'in|IN'
t_INTO = r'into|INTO'
t_FULL = r'full|FULL'
t_LIKE = r'~'
t_CHECK = r'check|CHECK'
t_DEFAULT = r'default|DEFAULT'
t_CONSTRAINT = r'constraint|CONSTRAINT'
t_STRING = r"'([^']*)'|\"([^\"]*)\""
t_NOT = r'not|NOT'
t_SEMICOLON = r';'
#t_SPACE = r'\s'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\\'
t_SET = r'set|SET'
t_INT = r'int|INT'
t_VARCHAR = r'varchar|VARCHAR'
t_ADD = r'add|ADD'


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    return t


def t_NUMBER(t):
    r'-?\d+\.?\d*'
    t.value = int(t.value)
    return t

def t_error(t):
    if not re.match(r'\s',t.value):
        print("Nieznany symbol: '%s'" % t.value[0])
    t.lexer.skip(1)


def t_FOREIGN_KEY(t):
    r'foreign\s*key|FOREIGN\s*KEY'
    return t


def t_PRIMARY_KEY(t):
    r'primary\s*key|PRIMARY\s*KEY'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in keywords:
        t.type = t.value.upper()
    else:
        t.type = 'ID'
    return t


lexer = lex.lex()

# Przykładowe zapytanie SQL
sql_query = """
SELECT id, name
FROM users
WHERE id = 1
AND age > 18
ORDER BY name ASC
LIMIT 10 PRIMARY KEY;
"""

# Analiza leksykalna
lexer.input(sql_query)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
