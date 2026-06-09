import re

TOKEN_SPEC = [
    ('FUNC',     r'func'),
    ('PRINTLN',  r'println'),
    ('VAR',      r'var'),
    ('WHILE',    r'while'),
    ('CONST',    r'const'),
    ('IF',       r'if'),
    ('ELSE',     r'else'),
    ('RET',      r'return'),
    ('TYPE',     r'int|bool|flo|str'),
    ('BOOL_VAL', r'TRUE|FALSE'),
    ('EQ',       r'=='),     # equality: == must come before = (assignment)
    ('NE',       r'!='),
    ('GTE',      r'>='),
    ('STE',      r'<='),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('ST',       r'<'),
    ('GT',       r'>'),
    ('COLON',    r':'),
    ('COMMA',    r','),
    ('ASSIGN',   r'='),      # assignment: single =
    ('ID',       r'[a-z_]+'),
    ('NUM',      r'\d+'),
    ('SKIP',     r'[ ]+'),
]

_tok_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC))

def lexBarracuda(code):
    lines = code.split('\n')
    tokens = []
    indent_stack = [0]

    for line in lines:
        stripped_line = line.lstrip(' \t')
        indent_count = len(line) - len(stripped_line)

        if not stripped_line:
            tokens.append(('NEWLINE', '\n'))
            continue

        if indent_count > indent_stack[-1]:
            tokens.append(('INDENT', indent_count))
            indent_stack.append(indent_count)
        elif indent_count < indent_stack[-1]:
            # emit one DEDENT per indentation level closed
            while indent_stack and indent_stack[-1] > indent_count:
                indent_stack.pop()
                tokens.append(('DEDENT', indent_count))

        for mo in _tok_regex.finditer(stripped_line):
            kind = mo.lastgroup
            value = mo.group()
            if kind != 'SKIP':
                tokens.append((kind, value))

        tokens.append(('NEWLINE', '\n'))

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('DEDENT', 0))

    return tokens
