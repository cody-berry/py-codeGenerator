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

        self.varTypeToSegmentMapping = {
            VarType.VAR: Segments.LOCAL,
            VarType.ARG: Segments.ARG,
            VarType.FIELD: Segments.THIS,
            VarType.STATIC: Segments.STATIC
        }

        try:
            self.compile_class()
        except ValueError:
            print(
                'ERROR R R R R R R R  token ' + self.tokenizer.current_token + ' ' + self.tokenizer.token_type().name)
            print('...[Recalibrating] [System failure]')

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
        if self.tokenizer.current_token == 'void':
            self.check_token(False, ['void'])
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
        self.compile_subroutine_body(funcName)

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
    def compile_subroutine_body(self, funcName):
        # '{'
        self.check_token(True, ['{'])

        # varDec*
        self.tokenizer.advance()
        while self.tokenizer.current_token == 'var':
            self.compile_var_dec()
            self.tokenizer.advance()

        self.VMWriter.writeFunction(funcName,
                                    self.symbolTable.varCount(VarType.VAR))

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
    # code effect: accesses the kind and index of the first identifier and push
    # it onto the stack. if an array has been accessed, we compile the
    # expression and push it. Then we add. also, we keep track of whether we are
    # popping unto an array or not. Then we evaluate the second expression. If
    # we didn't look at the array, we simply pop to varName. If we did have to
    # look at an array, we write this sequence of commands: pop temp 0, pop
    # pointer 1, push temp 0, pop that 0.
    def compile_let(self):
        # 'let', which defines the name of this function
        self.check_token(False, ['let'])

        # varName = identifier
        self.compile_identifier(True)

        varName = self.tokenizer.current_token

        # ?('['
        self.advance()
        accessedArray = False
        if self.tokenizer.current_token == '[':
            self.check_token(False, ['['])
            accessedArray = True

            # if we really want to access a field, doesn't this imply that we're
            # in a method and the first argument is this?
            if self.symbolTable.kindOf(varName) == VarType.FIELD:
                self.VMWriter.writePush(Segments.ARG, 0)
                self.VMWriter.writePop(Segments.POINTER, 0)
            self.VMWriter.writePush(self.varTypeToSegmentMapping[
                                        self.symbolTable.kindOf(varName)],
                                    self.symbolTable
                                    .indexOf(varName))

            # expression
            self.compile_expression(True)

            # ']'
            self.check_token(False, [']'])

            self.advance()

            self.VMWriter.writeArithmetic(Command.ADD)

        # '=' note that after the question mark, both ways we've advanced.
        # the first is that you didn't find the bracket, meaning that the
        # token must be an equals sign. the second is that you got out of the brackets
        # for list accessing, and I advanced right after so that neither way you would advance.
        self.check_token(False, ['='])

        # expression
        self.compile_expression(True)

        # ';'
        self.check_token(False, [';'])

        if accessedArray:
            self.VMWriter.writePop(Segments.TEMP, 0)
            self.VMWriter.writePop(Segments.POINTER, 1)
            self.VMWriter.writePush(Segments.TEMP, 0)
            self.VMWriter.writePop(Segments.THAT, 0)
        else:
            # if we really want to access a field, doesn't this imply that we're
            # in a method and the first argument is this?
            if self.symbolTable.kindOf(varName) == VarType.FIELD:
                self.VMWriter.writePush(Segments.ARG, 0)
                self.VMWriter.writePop(Segments.POINTER, 0)
            self.VMWriter.writePop(self.varTypeToSegmentMapping[
                                       self.symbolTable.kindOf(varName)],
                                   self.symbolTable
                                   .indexOf(varName))

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
        numExpressions = 0
        # ?(expression
        self.advance()
        if ((self.tokenizer.token_type() in [TokenType.IDENTIFIER,
                                             TokenType.STRING_CONST,
                                             TokenType.INT_CONST])
                or (self.tokenizer.current_token in ['true', 'false', 'null',
                                                     'this', '(', '-', '~'])):
            self.compile_expression(False)
            numExpressions += 1

            # *(','
            while self.tokenizer.current_token == ',':
                self.check_token(False, [','])

                # expression
                self.compile_expression(True)

        return numExpressions

    # grammar: term *(op term)
    # code effect: compiles the first term. then compiles the second term,
    # the first op, the third term, the second op, and so on.
    def compile_expression(self, advance):
        # term
        self.compile_term(advance)

        # *(op
        if self.tokenizer.current_token in ['+', '-', '*', '/', '&', '|',
                                            '<', '>', '=']:
            self.check_token(False,
                             ['+', '-', '*', '/', '&', '|', '<', '>', '='])
            currentOp = self.tokenizer.current_token

            # term
            self.compile_term(True)

            # case +: this is the Command.ADD arithmetic command.
            # case -: this is the Command.SUB arithmetic command, or subtract.
            # case *: this is the equivalent of calling Math.multiply on 2
            # arguments.
            # case /: this is the equivalent of calling Math.divide on 2
            # arguments.
            # case &: this is the Command.AND arithmetic command.
            # case |: this is the Command.OR arithmetic command.
            # case <: this is the Command.LT arithmetic command, or less than.
            # case >: this is the Command.GT arithmetic command, or greater than.
            # case =: this is the Command.EQ arithmetic command, or equal to.
            match currentOp:
                case '+':
                    self.VMWriter.writeArithmetic(Command.ADD)
                case '-':
                    self.VMWriter.writeArithmetic(Command.SUB)
                case '*':
                    self.VMWriter.writeCall('Math.multiply', 2)
                case '/':
                    self.VMWriter.writeCall('Math.divide', 2)
                case '&':
                    self.VMWriter.writeArithmetic(Command.AND)
                case '|':
                    self.VMWriter.writeArithmetic(Command.OR)
                case '<':
                    self.VMWriter.writeArithmetic(Command.LT)
                case '>':
                    self.VMWriter.writeArithmetic(Command.GT)
                case '=':
                    self.VMWriter.writeArithmetic(Command.EQ)

    # grammar: integerConstant | stringConstant | 'true' | 'false' | 'null' | 'this' | identifier | identifier ('[' expression ']' | ?('.' identifier) '(' expressionList ')') | '(' expression ')' | '-' term | '~' term
    # code effect: look at the token type and proceed from there.
    # case identifier: make a variable named identifier for the current token
    # case identifier→'[': push the kind and index of the identifier variable.
    # compile the expression, call add, pop to pointer 1, and push that 1. make
    # sure to complete the ']'!
    # case identifier→'.': add the next identifier plus a dot to 'identifier'
    # and then compile the expression list and call. compiling the expression
    # list will return the number of args.
    # case identifier→'(': Same as last time. Make sure you complete the ')',
    # and no longer add the identifier because there is none.
    # case keyword: it must be a keyword constant.
    # case symbol: no information until you read the token.
    # case symbol→'(': parenthesis with an expression in it. make sure to
    # complete the ')'!
    # case symbol→'-': after compiling the term, do 'neg'.
    # case symbol→'~': after compiling the term, do 'not'.
    # case int constant: push the int const.
    # case string constant: push the id of the first character of the string and
    # call String.new(). then call String.appendChar() for the appended string
    # and the new string from String.new().
    def compile_term(self, advance):
        if advance:
            self.advance()
        match self.tokenizer.token_type():
            case TokenType.IDENTIFIER:
                # identifier
                self.compile_identifier(False)
                identifier = self.tokenizer.current_token
                self.advance()

                # and then we search for some extensions to the identifier
                match self.tokenizer.current_token:
                    # '[' expression ']'
                    case '[':
                        if self.symbolTable.kindOf(identifier) == VarType.FIELD:
                            self.VMWriter.writePush(Segments.ARG, 0)
                            self.VMWriter.writePop(Segments.POINTER, 0)
                        self.VMWriter.writePush(self.varTypeToSegmentMapping[
                                                    self.symbolTable.kindOf(
                                                        identifier)],
                                                self.symbolTable
                                                .indexOf(identifier))
                        self.check_token(False, ['['])
                        self.compile_expression(True)
                        self.VMWriter.writeArithmetic(Command.ADD)
                        self.VMWriter.writePop(Segments.POINTER, 1)
                        self.VMWriter.writePush(Segments.THAT, 0)
                        self.check_token(False, [']'])
                        self.advance()
                    # '.' identifier '(' expressionList ')'
                    case '.':
                        self.check_token(False, ['.'])
                        self.compile_identifier(True)
                        identifier += '.' + self.tokenizer.current_token
                        self.check_token(True, ['('])
                        nArgs = self.compile_expression_list()
                        self.check_token(False, [')'])
                        self.VMWriter.writeCall(identifier, nArgs)
                        self.advance()
                    # '(' expressionList ')'
                    case '(':
                        self.check_token(False, ['('])
                        nArgs = self.compile_expression_list()
                        self.check_token(False, [')'])
                        self.VMWriter.writeCall(identifier, nArgs)
                        self.advance()
                    case _:
                        if self.symbolTable.kindOf(identifier) == VarType.FIELD:
                            self.VMWriter.writePush(Segments.ARG, 0)
                            self.VMWriter.writePop(Segments.POINTER, 0)
                        self.VMWriter.writePush(self.varTypeToSegmentMapping[
                                                    self.symbolTable.kindOf(
                                                        identifier)],
                                                self.symbolTable
                                                .indexOf(identifier))

            case TokenType.KEYWORD:
                # 'this' | 'null' | 'true' | 'false'
                self.check_token(False, ['this', 'null', 'true', 'false'])
                match self.tokenizer.current_token:
                    case 'this':
                        self.VMWriter.writePush(Segments.POINTER, 0)
                    case 'null':
                        self.VMWriter.writePush(Segments.CONST, 0)
                    case 'false':
                        self.VMWriter.writePush(Segments.CONST, 0)
                    case 'true':
                        self.VMWriter.writePush(Segments.CONST, 1)
                        self.VMWriter.writeArithmetic(Command.NEG)
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
                        self.VMWriter.writeArithmetic(Command.NEG)
                    # '~' term
                    case '~':
                        self.check_token(False, ['~'])
                        self.compile_term(True)
                        self.VMWriter.writeArithmetic(Command.NOT)

            # others: intConst | stringConst
            case TokenType.INT_CONST:
                self.VMWriter.writePush(Segments.CONST, self.tokenizer.current_token)
                self.advance()
            case TokenType.STRING_CONST:
                self.advance()

    # grammar: 'return' expression? ';'
    # code effect: after pushing const 0 or compiling an expression, return.
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
        else:
            self.VMWriter.writePush(Segments.CONST, 0)

        # ';'
        self.check_token(False, [';'])

        self.VMWriter.writeReturn()

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
