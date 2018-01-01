from ply import *
import lexer

tokens = lexer.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('right', 'UMINUS')
)

# Program -> dictionary of tuples (indexed by line number)


def p_program(p):
    '''program : program statement
               | statement'''

    if len(p) == 2 and p[1]:
        p[0] = {}
        line, stat = p[1]
        p[0][line] = stat
    elif len(p) == 3:
        p[0] = p[1]
        if not p[0]:
            p[0] = {}
        if p[2]:
            line, stat = p[2]
            p[0][line] = stat

def p_program_error(p):
    '''program : error'''
    p[0] = None
    p.parser.error = 1


def p_statement(p):
    '''statement : INTEGER command NEWLINE'''
    if isinstance(p[2], str):
        print("%s %s %s" % (p[2], "AT LINE", p[1]))
        p[0] = None
        p.parser.error = 1
    else:
        lineno = int(p[1])
        p[0] = (lineno, p[2])

def p_statement_interactive(p):
    '''statement : RUN NEWLINE
                 | LIST NEWLINE
                 | NEW NEWLINE'''
    p[0] = (0, (p[1], 0))

def p_statement_blank(p):
    '''statement : INTEGER NEWLINE'''
    p[0] = (0, ('BLANK', int(p[1])))

def p_statement_bad(p):
    '''statement : INTEGER error NEWLINE'''
    print("MALFORMED STATEMENT AT LINE %s" % p[1])
    p[0] = None
    p.parser.error = 1

def p_statement_newline(p):
    '''statement : NEWLINE'''
    p[0] = None

def p_command_let(p):
    '''command : LET variable EQUALS expr'''
    p[0] = ('LET', p[2], p[4])

def p_command_let_bad(p):
    '''command : LET variable EQUALS error'''
    p[0] = "BAD EXPRESSION IN LET"

def p_command_read(p):
    '''command : READ varlist'''
    p[0] = ('READ', p[2])

def p_command_read_bad(p):
    '''command : READ error'''
    p[0] = "MALFORMED VARIABLE LIST IN READ"