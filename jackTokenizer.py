from enum import Enum


class TokenType(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


class KeywordType(Enum):
    CLASS = 0
    METHOD = 1
    FUNCTION = 2
    CONSTRUCTOR = 3
    INT = 4
    BOOLEAN = 5
    CHAR = 6
    VOID = 7
    VAR = 8
    STATIC = 9
    FIELD = 10
    LET = 11
    DO = 12
    IF = 13
    ELSE = 14
    WHILE = 15
    RETURN = 16
    TRUE = 17
    FALSE = 18
    NULL = 19
    THIS = 20


class JackTokenizer:
    def __init__(self, filename):
        self.file = []
        file = open(filename, 'r')
        self.current_token = ''
        self.line_number = 0
        self.current_index = 0  # the current index of the line our token is on

        for line in file:
            try:
                line = line[:(line.index('//'))]
            except:
                pass

            line = line.strip(' ').strip('\n').strip(' ').strip('\t').strip(' ')

            if (len(line) > 0) and (line[0] != '/') and (line[0] != "*"):
                self.file.append(line)

        self.file.append('\n')

        print(self.file)

    def hasMoreTokens(self):
        return not ((self.line_number >= len(self.file) - 1) and (
                self.current_index + len(self.current_token) >= (
            len(self.file[self.line_number]))))

    def advance(self):

        # print(f'Token starting index: |{self.current_index}|')

        rest_of_line = self.file[self.line_number][self.current_index:]
        # print(f'Rest of line: |{rest_of_line}|')

        possible_token_ending_indices = [len(rest_of_line)]

        try:
            possible_token_ending_indices.append(rest_of_line.index(' ') + 1)
        except:
            pass

        for token_breaker in ['+', '-', '~', '*', '/', '&', '|', '<', '>', '=',
                              '}', '{', ')', '(', '[', ']', '.', ',', ';']:
            try:
                index = rest_of_line.index(token_breaker)
                if index > 0:
                    possible_token_ending_indices.append(index)
                else:
                    try:
                        if rest_of_line[1] == ' ':
                            possible_token_ending_indices.append(2)
                        else:
                            possible_token_ending_indices.append(1)
                    except:
                        possible_token_ending_indices.append(1)
            except:
                pass

        if len(possible_token_ending_indices) > 1:
            for i in range(0, len(possible_token_ending_indices) - 1):
                possible_token_ending_indices[0] = min(
                    possible_token_ending_indices[0],
                    possible_token_ending_indices[i + 1])

        token_end = possible_token_ending_indices[0]

        self.current_token = rest_of_line[:token_end]

        # if self.current_token[0] == "\"":
        #     self.current_token = rest_of_line[:rest_of_line.index("\"") + 1]

        # for now, just advance for every word
        # but first, we have to find the starting line index of our token which will be our self.currentIndex.
        token_start = self.current_index + len(self.current_token)
        if token_start >= len(self.file[self.line_number]):
            self.line_number += 1
            self.current_index = 0
        else:
            self.current_index = token_start

        if self.current_token[0] == ' ':
            self.advance()

        print(f'|{self.current_token}| {rest_of_line}')

        if self.current_token:
            while self.current_token[-1] == ' ':
                self.current_token = self.current_token[:-1]

        match self.current_token:
            case '<':
                self.current_token = '&lt;'
            case '>':
                self.current_token = '&gt;'
            case '&':
                self.current_token = '&amp;'

    def token_type(self):
        if self.current_token in ['class', 'constructor', 'function', 'method',
                                  'field', 'static', 'var', 'int', 'char',
                                  'boolean', 'void', 'true', 'false', 'null',
                                  'this', 'let', 'do', 'if', 'else', 'while',
                                  'return']:
            return TokenType.KEYWORD
        if self.current_token in ['{', '}', '(', ')', '[', ']', '.', ',', ';',
                                  '+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=',
                                  '~']:
            return TokenType.SYMBOL
        if self.current_token[0] in ['0', '1', '2', '3', '4', '5', '6', '7',
                                     '8', '9']:
            return TokenType.INT_CONST
        if self.current_token[0] == '"':
            return TokenType.STRING_CONST
        else:
            return TokenType.IDENTIFIER

    def string_val(self):
        # self.advance()  # like this we're skipping the first token (") so that the next token is our actual string constant
        # return_val = self.current_token
        # self.advance()  # like this we're skipping the last token (") so that the next token is the token right after the string
        if self.current_token[-1] != '"':
            return_val = self.current_token[1:]
            self.advance()
            while self.current_token[-1] != '"':
                return_val += ' ' + self.current_token
                self.advance()
            return_val += ' ' + self.current_token[:-1]
            return return_val
        else:
            return self.current_token[1:-1]

    def int_val(self):
        return int(self.current_token)

    def identifier(self):
        return str(self.current_token)

    def symbol(self):
        return str(self.current_token)

    def keyWord(self):
        match self.current_token:
            case 'class':
                return KeywordType.CLASS
            case 'method':
                return KeywordType.METHOD
            case 'function':
                return KeywordType.FUNCTION
            case 'constructor':
                return KeywordType.CONSTRUCTOR
            case 'int':
                return KeywordType.INT
            case 'boolean':
                return KeywordType.BOOLEAN
            case 'char':
                return KeywordType.CHAR
            case 'void':
                return KeywordType.VOID
            case 'var':
                return KeywordType.VAR
            case 'static':
                return KeywordType.STATIC
            case 'field':
                return KeywordType.FIELD
            case 'let':
                return KeywordType.LET
            case 'do':
                return KeywordType.DO
            case 'if':
                return KeywordType.IF
            case 'else':
                return KeywordType.ELSE
            case 'while':
                return KeywordType.WHILE
            case 'return':
                return KeywordType.RETURN
            case 'true':
                return KeywordType.TRUE
            case 'false':
                return KeywordType.FALSE
            case 'null':
                return KeywordType.NULL
            case 'this':
                return KeywordType.THIS
