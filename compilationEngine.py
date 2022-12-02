from jackTokenizer import *
from symbolTable import *
from VMWriter import *


class CompilationEngine:
    def __init__(self, filename, tokenizer):
        self.tokenizer = tokenizer
        self.indents = 1
        self.symbolTable = SymbolTable()
        self.VMWriter = VMWriter(filename[:-5] + 'C.vm')
        self.functionNamePrefix = ''

        try:
            self.compile_class()
        except:
            print('ERRORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR token ' + self.tokenizer.current_token + ' ' + self.tokenizer.token_type().name)

    # advances
    def advance(self):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

    # advances a token if the argument 'advance' is true and checks if it is
    # in the list of tokens, literally 'tokens'.
    def check_token(self, advance, tokens):
        if advance:
            self.advance()

        wrote = False
        for token in tokens:
            if self.tokenizer.current_token == token:
                wrote = True
                break

        if not wrote:
            raise ValueError('The current token is incorrect.')

    def compile_identifier(self, advance):
        if advance:
            self.advance()

        if self.tokenizer.token_type() != TokenType.IDENTIFIER:
            raise ValueError('The current token is incorrect.')

    # grammar: 'class' identifier '{' classVarDec* subroutineDec* '}'
    # code effect: sets the function name prefix to the class name
    def compile_class(self):
        # 'class'
        self.check_token(True, ['class'])

        # identifier
        self.compile_identifier(True)

        self.functionNamePrefix = self.tokenizer.current_token

        # '{'
        self.check_token(True, ['{'])

        self.advance()
        # classVarDec*
        while self.tokenizer.current_token in ['static', 'field']:
            self.compile_class_var_dec()
            self.advance()

        # subroutineVarDec*
        while self.tokenizer.current_token in ['constructor', 'function',
                                               'method']:
            self.compile_subroutine_dec()
            self.advance()

        # '}'
        self.check_token(False, ['}'])

    # grammar: 'static'/'field' type varName *(',' varName) ';'
    # code effect: generates a variable with a type of 'type', a kind of
    # 'static' or 'field', and a name of 'name'.
    def compile_class_var_dec(self):
        # 'static'/'field'
        self.check_token(False, ['static', 'field'])
        varKind = VarType.NONE
        match self.tokenizer.current_token:
            case 'static':
                varKind = VarType.STATIC
            case 'field':
                varKind = VarType.FIELD

        # type, which does not end advanced
        self.compile_type(True)
        varType = self.tokenizer.current_token

        # varName
        self.compile_identifier(True)
        varName = self.tokenizer.current_token

        self.symbolTable.define(varName, varType, varKind)

        self.advance()
        # *( and checks if the token is a comma
        while self.tokenizer.current_token == ',':
            self.check_token(False, ',')

            # varName
            self.compile_identifier(True)
            varName = self.tokenizer.current_token

            # advance so that we're ready to check if the current token is a comma again
            self.advance()

            self.symbolTable.define(varName, varType, varKind)

        # ';'
        self.check_token(False, ';')

    # grammar: 'int', 'boolean', 'char', or an identifier. sometimes you'll
    # want to advance, other times you won't. for example, if you just called
    # check_token() or compile_identifier(), you'll want to advance. if you
    # just did an advance() or you just finished an asterisk loop or question
    # if-else statement.
    def compile_type(self, advance=True):
        # advance if we want to advance
        if advance:
            self.advance()

        # 'int', 'boolean', or 'char' with the if-else statement
        if self.tokenizer.current_token in ['int', 'boolean', 'char']:
            self.check_token(False, ['int', 'boolean', 'char'])
        else:  # and otherwise it's className, an identifier.
            self.compile_identifier(False)

    # grammar: constructor/function/method void/type subroutineName
    # '(' parameterList ')' subroutineBody
    # code effect:
    def compile_subroutine_dec(self):
        # constructor/function/method. note that because we just checked that it
        # was a constructor, functon, or method, we don't need to advance.
        self.check_token(False, ['constructor', 'function', 'method'])
        isMethod = self.tokenizer.current_token == 'method'

        # 'void' or a type.
        self.tokenizer.advance()
        isVoid = False
        if self.tokenizer.current_token == 'void':
            self.check_token(False, ['void'])
            isVoid = True
        else:
            # this is an 'or' case where we need to check if it's 'void' or a type.
            # because of this, we've already advanced, so we shouldn't advance.
            # if we did advance, it would still pass the tests if the code worked
            # because it would have an identifier right after.
            self.compile_type(False)

        # subroutineName, which is the equivalent of an identifier. we advance
        self.compile_identifier(True)

        funcName = self.functionNamePrefix + '.' + self.tokenizer.current_token

        # '(', the symbol
        self.check_token(True, ['('])

        # parameterList, a function. based on the formula, it ends advanced to
        # the next token
        self.symbolTable.startSubroutine()
        self.compile_parameter_list(isMethod)

        # read the last comment to show description of why we don't advance for our right paren
        self.check_token(False, [')'])

        # subroutineBody, the function
        self.compile_subroutine_body(funcName, isVoid)


    # grammar: ?(type varname *(',' type varName))
    # effect on code: generate however many args are in the parameter list with
    # type 'type', kind 'arg', and name 'name'. if the function is a method,
    # add 'this' as the first argument with a type of whatever the class name
    # is.
    def compile_parameter_list(self, isMethod):
        if isMethod:
            self.symbolTable.define('this', self.functionNamePrefix,
                                    VarType.ARG)

        # ?(type
        self.advance()
        if self.tokenizer.token_type() in [TokenType.KEYWORD,
                                           TokenType.IDENTIFIER]:
            self.compile_type(False)
            varType = self.tokenizer.current_token

            # varName
            self.compile_identifier(True)
            varName = self.tokenizer.current_token

            self.symbolTable.define(varName, varType, VarType.ARG)

            # *(','
            self.tokenizer.advance()
            while self.tokenizer.current_token == ',':
                self.check_token(False, [','])

                # type
                self.compile_type(True)
                varType = self.tokenizer.current_token

                # varName
                self.compile_identifier(True)
                varName = self.tokenizer.current_token

                self.symbolTable.define(varName, varType, VarType.ARG)

                # prepare for the next iteration of this
                self.tokenizer.advance()

    # grammar: '{' varDec* statements '}'
    # code effect: writes all statements down, has the var decs, and makes a
    # call to VMWriter's writeFunction command. if isVoid is true, it is sent
    # to compile_statements() to inform it that its return statement will be
    # void.
    def compile_subroutine_body(self, funcName, isVoid):
        # '{'
        self.check_token(True, ['{'])

        # varDec*
        self.tokenizer.advance()
        while self.tokenizer.current_token == 'var':
            self.compile_var_dec()
            self.tokenizer.advance()

        self.VMWriter.writeFunction(funcName, self.symbolTable.varCount(VarType.VAR))

        # statements
        self.compile_statements()

        # '}'
        self.check_token(False, ['}'])

    # grammar: 'var' type varName *(',' varName) ';'. the only time this is called
    # we have already started advance()
    # effect on code: add a variable with a name varName, type 'type', and
    # kind 'local' to the symbol table. repeat for however many variables are
    # in the var dec
    def compile_var_dec(self):
        # 'var'
        self.check_token(False, ['var'])

        # type
        self.compile_type(True)  # do advance

        varType = self.tokenizer.current_token

        # varName
        self.compile_identifier(True)

        varName = self.tokenizer.current_token

        self.symbolTable.define(varName, varType, VarType.VAR)

        # grammar: repeat ',' varName
        self.advance()
        while self.tokenizer.current_token == ',':
            self.check_token(False, [','])
            self.compile_identifier(True)
            varName = self.tokenizer.current_token
            self.symbolTable.define(varName, varType, VarType.VAR)
            self.advance()

        # repeat ';'
        self.check_token(False, [';'])

    # grammar: statement*
    def compile_statements(self):
        # not only does compile_statement() write down everything needed for a statement,
        # but it returns true if there is a statement and false if there isn't. it also takes care of advancing
        # by itself because of the formula of the if statement, ending right after the optional else statement
        # meaning that all other statements have advanced after.
        while self.compile_statement():
            pass

    # grammar: letStatement | doStatement | whileStatement | ifStatement | returnStatement
    def compile_statement(self):
        match self.tokenizer.current_token:
            case 'let':  # letStatement
                self.compile_let()
                self.advance()
                return True
            case 'do':  # doStatement
                self.compile_do()
                self.advance()
                return True
            case 'return':  # returnStatement
                self.compile_return()
                self.advance()
                return True
            case 'while':  # whileStatement
                self.compile_while()
                self.advance()
                return True
            case 'if':  # ifStatement
                self.compile_if()
                return True
        return False

    # grammar: 'let' varName ?('[' expression ']') '=' expression ';'
    def compile_let(self):
        # 'let', which defines the name of this function
        self.check_token(False, ['let'])

        # varName = identifier
        self.compile_identifier(True)

        # ?('['
        self.advance()
        if self.tokenizer.current_token == '[':
            self.check_token(False, ['['])

            # expression
            self.compile_expression(True)

            # ']'
            self.check_token(False, [']'])

            self.advance()

        # '=' note that after the question mark, both ways we've advanced.
        # the first is that you didn't find the bracket, meaning that the
        # token must be an equals sign. the second is that you got out of the brackets
        # for list accessing, and I advanced right after so that neither way you would advance.
        self.check_token(False, ['='])

        # expression
        self.compile_expression(True)

        # ';'
        self.check_token(False, [';'])

    # grammar: 'do' identifier ?('.' identifier) '(' expressionList ')'.
    def compile_do(self):
        # 'do'
        self.check_token(False, ['do'])

        # identifier
        self.compile_identifier(True)

        # ?('.'
        self.advance()
        if self.tokenizer.current_token == '.':
            self.check_token(False, ['.'])

            # identifier
            self.compile_identifier(True)

            self.tokenizer.advance()

        # left paren. we don't advance because of the same reason we don't advance for the equal sign in compileLet().
        self.check_token(False, ['('])

        # expressionList. Since this comes out already advanced to the next token, we don't advance on the next.
        self.compile_expression_list()

        # read the last comment to see why we don't advance on right paren
        self.check_token(False, [')'])

        # ';'
        self.check_token(True, [';'])

    # grammar: ?(expression *(',' expression))
    def compile_expression_list(self):
        # ?(expression
        self.advance()
        if ((self.tokenizer.token_type() in [TokenType.IDENTIFIER,
                                             TokenType.STRING_CONST,
                                             TokenType.INT_CONST])
                or (self.tokenizer.current_token in ['true', 'false', 'null',
                                                     'this', '(', '-', '~'])):
            self.compile_expression(False)

            # *(','
            while self.tokenizer.current_token == ',':
                self.check_token(False, [','])

                # expression
                self.compile_expression(True)

    # grammar: term *(op term)
    def compile_expression(self, advance):
        # term
        self.compile_term(advance)

        # *(op
        if self.tokenizer.current_token in ['+', '-', '*', '/', '&', '|',
                                            '<', '>', '=']:
            self.check_token(False,
                             ['+', '-', '*', '/', '&', '|', '<', '>', '='])

            # term
            self.compile_term(True)

    # grammar: integerConstant | stringConstant | 'true' | 'false' | 'null' | 'this' | identifier | identifier ('[' expression ']' | ?('.' identifier) '(' expressionList ')') | '(' expression ')' | '-' term | '~' term
    def compile_term(self, advance):
        if advance:
            self.advance()
        match self.tokenizer.token_type():
            case TokenType.IDENTIFIER:
                # identifier
                self.compile_identifier(False)
                self.advance()

                # and then we search for some extensions to the identifier
                match self.tokenizer.current_token:
                    # '[' expression ']'
                    case '[':
                        self.check_token(False, ['['])
                        self.compile_expression(True)
                        self.check_token(False, [']'])
                        self.advance()
                    # '.' identifier '(' expressionList ')'
                    case '.':
                        self.check_token(False, ['.'])
                        self.compile_identifier(True)
                        self.check_token(True, ['('])
                        self.compile_expression_list()
                        self.check_token(False, [')'])
                        self.advance()
                    # '(' expressionList ')'
                    case '(':
                        self.check_token(False, ['('])
                        self.compile_expression_list()
                        self.check_token(False, [')'])
                        self.advance()

            case TokenType.KEYWORD:
                # 'this' | 'null' | 'true' | 'false'
                self.check_token(False, ['this', 'null', 'true', 'false'])
                self.advance()

            case TokenType.SYMBOL:
                match self.tokenizer.current_token:
                    # '(' expression ')'
                    case '(':
                        self.check_token(False, ['('])
                        self.compile_expression(True)
                        self.check_token(False, [')'])
                        self.advance()
                    # '-' term
                    case '-':
                        self.check_token(False, ['-'])
                        self.compile_term(True)
                    # '~' term
                    case '~':
                        self.check_token(False, ['~'])
                        self.compile_term(True)

            # others: intConst | stringConst
            case TokenType.INT_CONST:
                self.advance()
            case TokenType.STRING_CONST:
                self.advance()

    # grammar: 'return' expression? ';'
    def compile_return(self):
        # 'return'
        self.check_token(False, ['return'])

        # expression?
        self.advance()
        if ((self.tokenizer.token_type() in [TokenType.IDENTIFIER,
                                             TokenType.STRING_CONST])
                or (self.tokenizer.current_token in ['true', 'false', 'null',
                                                     'this', '-', '~'])):
            self.compile_expression(False)

        # ';'
        self.check_token(False, [';'])

    # 'if' '(' expression ')' '{' statements '}' ?('else' '{' statements '}')
    def compile_if(self):
        # 'if'
        self.check_token(False, ['if'])

        # '('
        self.check_token(True, ['('])

        # expression
        self.compile_expression(True)

        # ')'
        self.check_token(False, [')'])

        # '{'
        self.check_token(True, ['{'])

        # statements
        self.advance()
        self.compile_statements()

        # '}'
        self.check_token(False, ['}'])

        # ?('else'
        self.advance()
        if self.tokenizer.current_token == 'else':
            self.check_token(False, ['else'])

            # '{'
            self.check_token(True, ['{'])

            # statements
            self.advance()
            self.compile_statements()

            # '}'
            self.check_token(False, ['}'])

            self.advance()

    # grammar: 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        # 'while'
        self.check_token(False, ['while'])

        # '('
        self.check_token(True, ['('])

        # expression
        self.compile_expression(True)

        # ')'
        self.check_token(False, [')'])

        # '{'
        self.check_token(True, ['{'])

        # statements
        self.advance()
        self.compile_statements()

        # '}'
        self.check_token(False, ['}'])
