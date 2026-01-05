import re


TOKEN_SPEC = [
    ('FUNC',    r'func'),         
    ('VAR',     r'var'),           
    ('CONST',   r'const'),        
    ('IF',      r'if'),            
    ('ELSE',    r'else'),         
    ('RET',     r'return'),       
    ('TYPE',    r'int|bool'),      
    ('BOOL_VAL',r'TRUE|FALSE'),    
    ('ASSIGN',  r'==|='),         
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
    current_level = 0  # How many tabs are we currently at?

    for line_num, line in enumerate(lines):
        if not line.strip(): continue # Skip empty lines
        
        # 2. Count leading tabs
        stripped_line = line.lstrip('\t')
        tab_count = len(line) - len(stripped_line)
        
        # 3. Handle Indent/Dedent
        if tab_count > current_level:
            tokens.append(('INDENT', tab_count))
            current_level = tab_count
        elif tab_count < current_level:
            tokens.append(('DEDENT', tab_count))
            current_level = tab_count

        # 4. Use Regex to find the "bricks" in the rest of the line
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)
        for mo in re.finditer(tok_regex, stripped_line):
            kind = mo.lastgroup
            value = mo.group()
            if kind != 'SKIP':
                tokens.append((kind, value))
                
    return tokens

# --- TEST IT WITH YOUR EXAMPLE ---
example = """func: equation: a,b,c
\tif: z = TRUE
\t\tvar int outcome == a - b"""

print(lex_barracuda(example))
