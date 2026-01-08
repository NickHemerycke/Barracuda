import re

TOKEN_SPEC = [
    ('FUNC',    r'func'),
    ('PRINTLN', r'println'),         
    ('VAR',     r'var'),
    ('WHILE',   r'while'),           
    ('CONST',   r'const'),        
    ('IF',      r'if'),            
    ('ELSE',    r'else'),         
    ('RET',     r'return'),       
    ('TYPE',    r'int|bool|flo|str'),      
    ('BOOL_VAL',r'TRUE|FALSE'), 
    ('COMPARISON', r'==='),
    ('ASSIGN',  r'=='),
    ('NE',     r'!='),
    ('PLUS',    r'\+'), 
    ('MINUS',   r'-'),
    ('GTE',     r'>='), 
    ('STE',     r'<='),   
    ('ST',      r'<'),
    ('GT',      r'>'),         
    ('COLON',   r':'),            
    ('COMMA',   r','),             
    ('ID',      r'[a-z_]+'),       
    ('NUM',     r'\d+'),          
    ('SKIP',    r'[ ]+'),          
]

def lexBarracuda(code):
    lines = code.split('\n')
    tokens = []
    current_level = 0 
    
    for line in lines:
        
        stripped_line = line.lstrip(' \t')
        indent_count = len(line) - len(stripped_line)

        
        if not stripped_line:
            tokens.append(('NEWLINE', '\n'))
            continue

       
        if indent_count > current_level:
            tokens.append(('INDENT', indent_count))
            current_level = indent_count
        elif indent_count < current_level:
            tokens.append(('DEDENT', indent_count))
            current_level = indent_count

     
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)
        for mo in re.finditer(tok_regex, stripped_line):
            kind = mo.lastgroup
            value = mo.group()
            if kind != 'SKIP':
                tokens.append((kind, value))

       
        tokens.append(('NEWLINE', '\n'))

    
    if current_level > 0:
        tokens.append(('DEDENT', 0))

    return tokens
