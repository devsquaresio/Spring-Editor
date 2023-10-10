import string, functools

DIGITS = string.digits
LETTERS = string.ascii_letters

FULL_RANGE = DIGITS + LETTERS

PY_KEYWORD_LIST = [
    "False", "None", "True", "and", "as", "assert", "async", "await", "break", "case",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "match", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"
]

PY_TYPE_LIST = [
    "int", "str", "list", "self", "bool"
]

C_KEYWORD_LIST = [
    "asm", "auto", "break", "case", "continue", "do", "elif", "else", "for", "goto",
    "if", "return", "switch", "void", "while"

]

C_TYPE_LIST = [
    "const", "char", "double", "enum", "extern", "float", "inline", "int",
    "long", "register", "restrict", "short", "signed", "sizeof", "static", "struct",
    "typedef", "union", "unsigned", "volatile"
]

def check_escape(line, index):
    num = 1
    count = 0
    while line[index - num] == '\\':
        count += 1
        num += 1
    if count % 2 == 0: return True
    return False

class Token:
    def __init__(self, type, start_line, start_index, end_line, end_index):
        self.type = type
        self.start_line = start_line
        self.start_index = start_index
        self.end_line = end_line
        self.end_index = end_index

class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.line = self.lines[0]
        self.rows = len(lines)
        
        self.index = 0
        self.row = 0

        self.current_char = self.line[self.index]

    def advance(self):
        self.index += 1
        try:
            if self.current_char == '\n':
                self.row += 1
                self.index = 0
                self.line = self.lines[self.row]
            self.current_char = self.line[self.index] if self.index < len(self.line) else None
        except IndexError:
            self.current_char = None

    def make_num(self):
        num_str = ''
        is_float = 0
        start_index = self.index

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if is_float > 0: break
                is_float += 1
                num_str += self.current_char
            else: num_str += self.current_char
        
            self.advance()

        return Token("NUMBER", self.row, start_index, self.row, self.index)
    
    def make_word(self, lang):
        word_str = ""
        start_index = self.index

        while self.current_char != None and self.current_char in FULL_RANGE + '_':
            word_str += self.current_char
            self.advance()

        match lang:
            case 'python':
                if word_str in PY_KEYWORD_LIST:
                    return Token("KEYWORD", self.row, start_index, self.row, self.index)
            case 'c':
                if word_str in C_KEYWORD_LIST:
                    return Token("KEYWORD", self.row, start_index, self.row, self.index)
            case _:
                return Token("ERROR: INVALID LANG", 0, 0, 0, 0)
                
        if self.current_char == '(': return Token("FUNCTION", self.row, start_index, self.row, self.index)
        
    def make_comment(self):
        start_index = self.index

        while self.current_char != '\n' and self.current_char != None:
            self.advance()

        return Token("COMMENT", self.row, start_index, self.row, self.index)
    
    def make_string(self, str_token):
        start_index = self.index
        start_row = self.row
        is_comment_block = False
        self.advance()

        while self.current_char != None:
            if self.current_char == str_token:
                try:
                    if check_escape(self.line, self.index):
                        break
                except IndexError:
                    break
            self.advance()
            if self.index == len(self.line) - 1 and self.row == self.rows - 1:
                return Token("STRING", start_row, start_index, self.row, self.index+1)

        return Token("STRING", start_row, start_index, self.row, self.index+1)

    @functools.cache
    def py_decode(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_num())
            elif self.current_char in LETTERS+'_':
                i = self.make_word('python')
                if i: tokens.append(i)
            elif self.current_char == '#':
                tokens.append(self.make_comment())
            elif self.current_char in ["'", '"']:
                str_token = self.current_char
                tokens.append(self.make_string(str_token))
                self.advance()
            else:
                self.advance()

        return tokens
    
    def c_decode(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_num())
            elif self.current_char in LETTERS+'_':
                i = self.make_word('c')
                if i: tokens.append(i)
            elif self.current_char == '#':
                tokens.append(self.make_comment())
            elif self.current_char in ["'", '"']:
                str_token = self.current_char
                tokens.append(self.make_string(str_token))
                self.advance()
            else:
                self.advance()

        return tokens
    
if __name__ == "__main__":
    with open("test.txt", "r") as f:
        lines = f.readlines()
    for i in Lexer(lines).py_decode():
        print(f"TYPE: {i.type}. The first coords are ({i.start_line}, {i.start_index}). The second coords are ({i.end_line}, {i.end_index})")
