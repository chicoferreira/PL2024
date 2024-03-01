import ply.lex as lex

tokens = (
    'SELECT_OP',
    'VARIABLE',
    'COMMA',
    'FROM_OP',
    'WHERE_OP',
    'NUMBER',
    'EQUALS',
    'GREATER_THAN',
    'LESS_THAN',
    'GREATER_THAN_EQUALS',
    'LESS_THAN_EQUALS'
)

t_SELECT_OP = r'SELECT'
t_VARIABLE = r'[A-Za-z_]+[A-Za-z0-9-_\.]'
t_COMMA = r'\,'
t_FROM_OP = r'FROM'
t_WHERE_OP = r'WHERE'
t_EQUALS = r'\='
t_GREATER_THAN = r'\>'
t_LESS_THAN = r'\<'
t_GREATER_THAN_EQUALS = r'\>\='
t_LESS_THAN_EQUALS = r'\<\='


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def main():
    lexer = lex.lex()
    data = input()
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


if __name__ == '__main__':
    main()
