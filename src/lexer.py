import re


TOKEN_SPEC = [
    ('FUNC',    r'func'),         
    ('VAR',     r'var'),           
    ('CONST',   r'const'),        
    ('IF',      r'if'),            
    ('ELSE',    r'else'),         
    ('RET',     r'return'),       
    ('TYPE',    r'int|bool|flo|str'),      
    ('BOOL_VAL',r'TRUE|FALSE'),    
    ('ASSIGN',  r'=='),         
    ('COLON',   r':'),            
    ('COMMA',   r','),             
    ('ID',      r'[a-z_]+'),       
    ('NUM',     r'\d+'),          
    ('TAB',     r'\t'),            
    ('NEWLINE', r'\n'),           
    ('SKIP',    r'[ ]+'),          
    ]
    
def lex_barracuda(code):
    lines = code.split('\n')
    tokens = []
    current_level = 0  

    for line_num, line in enumerate(lines):
        if not line.strip(): continue 
        
        
        stripped_line = line.lstrip('\t')
        tab_count = len(line) - len(stripped_line)
        
        
        if tab_count > current_level:
            tokens.append(('INDENT', tab_count))
            current_level = tab_count
        elif tab_count < current_level:
            tokens.append(('DEDENT', tab_count))
            current_level = tab_count

        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)
        for mo in re.finditer(tok_regex, stripped_line):
            kind = mo.lastgroup
            value = mo.group()
            if kind != 'SKIP':
                tokens.append((kind, value))
                
    return tokens
