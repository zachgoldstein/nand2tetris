"""
Syntax Analyser
Given some high-level Jack language files:
  - tokenize the input
  - parse the list of tokens using the given Jack grammar
  - export to xml for a tree representation
As part of writing a compiler, going from high-level langauge -> VM code -> assembly -> machine code
  
Next chapter will use this tree representation to generate VM code
"""

from io import TextIOWrapper
import argparse
from typing import List, Union, Literal, Callable
from functools import partial
from inspect import signature

from dataclasses import dataclass
from enum import Enum
import pathlib
import xml.etree.ElementTree as ET
from xml.dom import minidom


class TokenType(Enum):
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "intConstant"
    STRING_CONST = "stringConstant"

class RuleType(Enum):
    pass

# Terminals
@dataclass
class Token:
    type: TokenType
    value: str

# Nonterminals
@dataclass
class Rule:
    type: RuleType
    value: str

class Tokenizer():
    lines: List[str]
    curr_line: int
    curr_char: int

    keyword_list: List[str] = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbol_list: List[str] = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, lines):
        self.lines = lines
        self.curr_line = 0
        self.curr_char = 0
        if DEBUG:
            print(f"Starting tokenizer with {len(lines)} lines")
            print(f"First line:{self.lines[self.curr_line]}")
    
    @property
    def current_line_len(self) -> int:
        return len(self.lines[self.curr_line])

    @property
    def current_char(self) -> str:
        return self.lines[self.curr_line][self.curr_char]

    @property
    def remaining_str(self) -> str:
        return self.lines[self.curr_line][self.curr_char:self.current_line_len]

    def hasMoreTokens(self) -> bool:
        if self.curr_line >= len(self.lines):
            return False
        return True

    def advance(self, num_chars = 1):
        self.curr_char += num_chars
        # if DEBUG:
        #     print(f"Advancing {num_chars} to {self.curr_char}")
        if self.curr_char >= len(self.lines[self.curr_line]):
            self.curr_line += 1
            self.curr_char = 0
            # if DEBUG:
            #     print(f"Advanced line to line {self.curr_line}")

    # returns: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
    def token_type(self) -> Union[TokenType, None]:
        # is keyword?
        for keyword in self.keyword_list:
            keyword_to_check = self.lines[self.curr_line][self.curr_char:self.curr_char+len(keyword)]
            if keyword_to_check == keyword:
                return TokenType.KEYWORD

        # is symbol
        for symbol in self.symbol_list:
            if self.current_char == symbol:
                return TokenType.SYMBOL

        # is string?
        if self.current_char == '"':
            return TokenType.STRING_CONST

        # integer
        # separated by whitespace or box bracket
        whitespace_split = self.remaining_str.split(" ")[0]
        box_split = whitespace_split.split("[")[0]
        box_split = box_split.split("(")[0]
        box_split = box_split.rstrip(";")
        box_split = box_split.rstrip("]")
        box_split = box_split.rstrip(")")
        # print(f"self.remaining_str '{self.remaining_str}', box_split: '{box_split}'")
        if box_split.isnumeric() or whitespace_split.isnumeric():
            return TokenType.INT_CONST

        if self.current_char == " ":
            return None
        
        # identifier
        if not self.current_char.isnumeric():
            return TokenType.IDENTIFIER

        return None

    # returns: CLASS, METHOD, FUNCTION, CONSTRUCTOR,
    # INT, BOOLEAN, CHAR, VOID, VAR, STATIC, FIELD, 
    # LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS
    def key_word(self) -> Union[str, None]:
        for keyword in self.keyword_list:
            # if the keyword is longer than the rest of the line, keyword is not present
            chars_left = self.current_line_len - self.curr_char
            if len(keyword) > chars_left:
                continue
            keyword_to_check = self.lines[self.curr_line][self.curr_char:self.curr_char+len(keyword)]
            if keyword_to_check == keyword:
                return keyword
        return None
    
    def symbol(self) -> Union[str, None]:
        for symbol in self.symbol_list:
            if self.current_char == symbol:
                return symbol
    
    # identifier: not including double quote or newline '"' a sequence of letters, digits, and
    # underscore ( '_' ) not starting with a digit    
    def identifier(self) -> str:
        untrimmed_str = self.remaining_str.split(" ")[0]
        # remove any trailing symbols
        trimmed_str = untrimmed_str
        for i in range(1, len(untrimmed_str)):
            if untrimmed_str[-i] in self.symbol_list:
                # if DEBUG:
                #     print(f"trimming {untrimmed_str[-i]} from {untrimmed_str}")
                trimmed_str = trimmed_str.rstrip(untrimmed_str[-i])
            else:
                break
        # if there are any dots in the indentifier, like game.dispose, split and only use first occurence
        trimmed_str = trimmed_str.split(".")[0]
        # if there are any square brackets, only use the first piece as well
        trimmed_str = trimmed_str.split("[")[0]
        return trimmed_str

    # integerConstant:  a decimal number in the range 0 ... 32767 
    def int_val(self) -> int:
        trimmed_str = self.remaining_str.split(" ")[0]
        trimmed_str = trimmed_str.rstrip(";")
        trimmed_str = trimmed_str.rstrip("]")
        trimmed_str = trimmed_str.rstrip(")")
        return trimmed_str

    # StringConstant:'"' a sequence of Unicode characters,
    def string_val(self) -> str:
        return self.remaining_str.split('"')[1]

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.hasMoreTokens():
            tokenType = self.token_type()
            value = ""
            if tokenType == TokenType.KEYWORD:
                value = self.key_word()
            elif tokenType == TokenType.SYMBOL:
                value = self.symbol()
            elif tokenType == TokenType.INT_CONST:
                value = self.int_val()
            elif tokenType == TokenType.STRING_CONST:
                value = self.string_val()
            elif tokenType == TokenType.IDENTIFIER:
                value = self.identifier()
            if tokenType == None:
                self.advance(1)
                continue
            if DEBUG:
                print(f"token: {tokenType} with val {value}")
            tokens.append(Token(tokenType, value))
            if value == None or len(value) == 0:
                self.advance(1)
            elif tokenType == TokenType.STRING_CONST:
                self.advance(len(value) + 2) # Advance and remove the string's quotes
            else:
                self.advance(len(value))
        return tokens
    

# Parser and Compilation Engine

class CompilationEngine():
    # Handled directly with no method:
    # type, className, subroutineName, variableName, statement, subroutineCall

    # Our parseTree of statements
    compiledStatements: List[str]
    tokens: List[Token]
    current_token_index: int
    parseTree: ET
    
    class ParseException(Exception):
        pass

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token_index = 0
        self.parseTree = None

    @property
    def current_token(self) -> Token:
        return self.tokens[self.current_token_index]

    @property
    def next_token(self) -> Token:
        return self.tokens[self.current_token_index + 1]

    @property
    def current_token_value(self) -> str:
        return self.current_token.value

    def advance(self):
        self.current_token_index += 1

    def check_token(self, expected: Token):
        if self.current_token.type != expected.type:
            raise self.ParseException(f"Incorrect token type. Expected {expected.type}, got {self.current_token.type}")
        if expected.value != None and self.current_token.value != expected.value:
            raise self.ParseException(f"Incorrect token value. Expected {expected.value}, got {self.current_token.value}")
        return

    def check_tokens(self, expected_tokens:List[Token]):
        e = None
        for token in expected_tokens:
            try:
                self.check_token(token)
            except self.ParseException as e:
                e = e
            else:
                # no error, this works
                return
        tokens_pretty = [f"{token.type.value}({token.value}) " for token in expected_tokens]
        raise self.ParseException(f"Incorrect token. Expected one of {tokens_pretty}, got {self.current_token.type.value}({self.current_token.value})")

    # Start the recursive compilation of the parse tree
    def compile(self):
        if DEBUG:
            print(f"Compiling parse tree with {len(self.tokens)} tokens")
        # Make the assumption a class is at the root
        try:
            self.compileClass(None)
        except self.ParseException as e:
            print(e)
    
    # Utility functions for main token types
    def compileIdentifier(self, element):
        self.check_token(Token(TokenType.IDENTIFIER, None))
        elem = ET.SubElement(element, TokenType.IDENTIFIER.value)
        elem.text = self.current_token_value
        self.advance()

    def compileSymbol(self, element, symbol):
        self.check_token(Token(TokenType.SYMBOL, symbol))
        elem = ET.SubElement(element, TokenType.SYMBOL.value)
        elem.text = self.current_token_value
        self.advance()

    def compileKeyword(self, element, keyword):
        self.check_token(Token(TokenType.KEYWORD, keyword))
        elem = ET.SubElement(element, TokenType.KEYWORD.value)
        elem.text = self.current_token_value
        self.advance()

    def compileIntegerConstant(self, element, keyword):
        self.check_token(Token(TokenType.INT_CONST, keyword))
        elem = ET.SubElement(element, TokenType.INT_CONST.value)
        elem.text = self.current_token_value
        self.advance()

    def compileStringConstant(self, element, keyword):
        self.check_token(Token(TokenType.STRING_CONST, keyword))
        elem = ET.SubElement(element, TokenType.STRING_CONST.value)
        elem.text = self.current_token_value
        self.advance()


    # Utility functions for composeability
    def compileMultiple(self, func: Callable, element: ET.Element):
        # keep attempting a rule until it fails and we get an exception
        i = 0
        isDone = False
        while (isDone == False):
            i += 1
            try:
                print(f"compileMultiple running {func.__name__}")
                getattr(self, func.__name__)(element)
            except self.ParseException:
                print(f"Stopping running rule after {i} times")
                isDone = True
        return
    
    def compileOr(self, funcs: List[Callable], element: ET.Element, keyword: str = None):
        found = False
        for func in funcs:
            if found == True:
                break
            try:
                # Figure out if this function has two params, use if needed
                sig = signature(getattr(self, func.__name__))
                if len(sig.parameters) == 1:
                    getattr(self, func.__name__)(element)
                else:
                    print("Calling with two params")
                    getattr(self, func.__name__)(element, keyword)
            except self.ParseException:
                print(f"compileOr did not find rule {func.__name__}")
            else:
                print(f"compileOr found rule {func.__name__}")
                found = True
        if found == False:
            print(f"compileOr did not find any rules for token {self.current_token}")
            raise self.ParseException("Could not find func in compileOr")

    def compileOptional(self, func: Callable, element: ET.Element):
        try:
            getattr(self, func.__name__)(element)
        except self.ParseException:
            print(f"Optional compile and did not find rule")



    # program structure
    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compileClass(self, element: ET.Element):
        # 'class'
        self.check_token(Token(TokenType.KEYWORD, "class"))
        # Class is usually the root node, add a check to see if we need to add the root node here
        if self.parseTree == None:
            rootElement = ET.Element("class")
            self.parseTree = ET.ElementTree(rootElement)
        if element == None:
            element = self.parseTree.getroot()
        elem = ET.SubElement(element, TokenType.KEYWORD.value)
        elem.text = self.current_token_value
        self.advance()

        # className
        self.compileIdentifier(element)

        # '{'
        self.compileSymbol(element, '{')

        # one or many, classVarDec*
        self.compileMultiple(self.compileClassVarDec, element)
        
        # one or many, subroutineDec*
        self.compileMultiple(self.compileSubroutineDec, element)

        self.check_token(Token(TokenType.SYMBOL, "}"))
        elem = ET.SubElement(element, TokenType.SYMBOL.value)
        elem.text = self.current_token_value
        self.advance()

    # ('static' |'field' ) type varName (', 'varName)* ';'
    # Compiles a static variable declaration, or a field declaration
    def compileClassVarDec(self, element: ET.Element):
        print("compileClassVarDec")
        # ('static' |'field' )
        self.check_tokens([
            Token(TokenType.KEYWORD, "static"),
            Token(TokenType.KEYWORD, "field"),
        ])
        element = ET.SubElement(element, 'classVarDec')
        elem = ET.SubElement(element, TokenType.KEYWORD.value)
        elem.text = self.current_token_value
        self.advance()

        # type
        self.compileType(element)

        # varName
        self.check_token(Token(TokenType.IDENTIFIER, None))
        elem = ET.SubElement(element, TokenType.IDENTIFIER.value)
        elem.text = self.current_token_value
        self.advance()

        # (', 'varName)*
        self.compileMultiple(self.compileEndVar, element)

        self.check_token(Token(TokenType.SYMBOL, ";"))
        elem = ET.SubElement(element, TokenType.SYMBOL.value)
        elem.text = self.current_token_value
        self.advance()

    # (',' varName)
    def compileEndVar(self, element):
        self.check_token(Token(TokenType.SYMBOL, ","))
        elem = ET.SubElement(element, TokenType.SYMBOL.value)
        elem.text = self.current_token_value
        self.advance()

        self.compileIdentifier(element)

    def compileType(self, element: ET.Element):
        type_tokens: List[Token] = [
            Token(TokenType.KEYWORD, "int"),
            Token(TokenType.KEYWORD, "char"),
            Token(TokenType.KEYWORD, "boolean"),
            Token(TokenType.IDENTIFIER, None),
        ]
        self.check_tokens(type_tokens)
        elem = ET.SubElement(element, self.current_token.type.value)
        elem.text = self.current_token_value
        self.advance()


    # ('constructor'|'function' |'method') ('void' | type) subroutineName '(' parameter List ') ' subroutineBody
    # Compiles a complete method, function, or constructor
    def compileSubroutineDec(self, element: ET.Element):
        self.check_tokens([
            Token(TokenType.KEYWORD, "constructor"),
            Token(TokenType.KEYWORD, "function"),
            Token(TokenType.KEYWORD, "method"),
        ])
        element = ET.SubElement(element, 'subroutineDec')
        elem = ET.SubElement(element, TokenType.KEYWORD.value)
        elem.text = self.current_token_value
        self.advance()

        # ('void' | type)
        # TODO: make type more composeable
        self.check_tokens([
            Token(TokenType.KEYWORD, "void"),
            Token(TokenType.KEYWORD, "int"),
            Token(TokenType.KEYWORD, "char"),
            Token(TokenType.KEYWORD, "boolean"),
            Token(TokenType.IDENTIFIER, None),
        ])
        elem = ET.SubElement(element, self.current_token.type.value)
        elem.text = self.current_token_value
        self.advance()

        # subroutineName
        self.compileIdentifier(element)
        
        # '('
        self.compileSymbol(element, '(')

        # parameter List
        self.compileParameterList(element)

        # ')'
        self.compileSymbol(element, ')')

        # subroutineBody
        elem = ET.SubElement(element, "subroutineBody")
        self.compileSubroutineBody(elem)


    # ( (type varName) (',' type varName)* )?
    # Compiles a (possibly empty) parameter list. Does not handle the enclosing "()".
    def compileParameterList(self, element: ET.Element):
        element = ET.SubElement(element, "parameterList")
        self.compileOptional(self.compileParameterListBase, element)
    
    # ( (type varName) (',' type varName)* )
    def compileParameterListBase(self, element: ET.Element):
        # type
        self.compileType(element)

        # varName
        self.compileIdentifier(element)

        # (' ,' type varName)*
        self.compileMultiple(self.compileParameter, element)
    
    # (',' type varName)
    def compileParameter(self, element: ET.Element):
        self.compileSymbol(element, ',')
        self.compileType(element)
        self.compileIdentifier(element)

    # '{' varDec* statements '}'
    def compileSubroutineBody(self, element: ET.Element):
        self.compileSymbol(element, '{')
        self.compileMultiple(self.compileVarDec, element)
        self.compileStatements(element)
        self.compileSymbol(element, '}')
    
    # 'var' type varName (',' varName)* ';'
    def compileVarDec(self, element: ET.Element):
        self.check_token(Token(TokenType.KEYWORD, 'var'))
        element = ET.SubElement(element, "varDec")
        self.compileKeyword(element, 'var')
        self.compileType(element)
        self.compileIdentifier(element)
        self.compileMultiple(self.compileEndVar, element)
        self.compileSymbol(element, ';')

    def compileClassName(self, element: ET.Element):
        self.compileIdentifier(element)

    def compileSubroutineName(self, element: ET.Element):
        self.compileIdentifier(element)

    def compileVarName(self, element: ET.Element):
        self.compileIdentifier(element)

    # varName '[' expression ']'
    def compileVarNameWithBoxedExpression(self, element: ET.Element):
        print("compileVarNameWithBoxedExpression")
        self.compileIdentifier(element)
        self.compileSymbol(element, '[')
        self.compileExpression(element)
        self.compileSymbol(element, ']')

    # statements

    # statement*
    def compileStatements(self, element: ET.Element):
        element = ET.SubElement(element, "statements")
        self.compileMultiple(self.compileStatement, element)

    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compileStatement(self, element: ET.Element):
        statements = [self.compileLet, self.compileIf, self.compileWhile, self.compileDo, self.compileReturn]
        self.compileOr(statements, element)

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compileLet(self, element: ET.Element):
        print(f"start of let")
        self.check_token(Token(TokenType.KEYWORD, 'let'))
        element = ET.SubElement(element, "letStatement")
        self.compileKeyword(element, 'let')
        self.compileVarName(element)
        print("optional boxed expression...")
        self.compileOptional(self.compileBoxedExpression, element)
        self.compileSymbol(element, '=')
        print(f"compileLet after = expression current token {self.current_token}")
        self.compileExpression(element)
        self.compileSymbol(element, ';')
        print("got to end of let")

    def compileBoxedExpression(self, element: ET.Element):
        print(f"compileBoxedExpression start token {self.current_token}")
        self.compileSymbol(element, '[')
        print(f"compileBoxedExpression after [ {self.current_token}")
        self.compileExpression(element)
        print(f"compileBoxedExpression after expression {self.current_token}")
        self.compileSymbol(element, ']')
        print(f"compileBoxedExpression after ] {self.current_token}")

    # '(' expression ')'
    def compileBracketedExpression(self, element: ET.Element):
        self.compileSymbol(element, '(')
        self.compileExpression(element)
        self.compileSymbol(element, ')')

    # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def compileIf(self, element: ET.Element):
        self.check_token(Token(TokenType.KEYWORD, 'if'))
        element = ET.SubElement(element, "ifStatement")
        self.compileKeyword(element, 'if')
        self.compileBracketedExpression(element)
        self.compileSymbol(element, '{')
        self.compileStatements(element)
        self.compileSymbol(element, '}')
        self.compileOptional(self.compileElse, element)

    def compileElse(self, element: ET.Element):
        self.compileKeyword(element, 'else')
        self.compileSymbol(element, '{')
        self.compileStatements(element)
        self.compileSymbol(element, '}')

    # 'while' '(' expression ')' '{' statements '}'
    def compileWhile(self, element: ET.Element):
        self.check_token(Token(TokenType.KEYWORD, 'while'))
        element = ET.SubElement(element, "whileStatement")
        self.compileKeyword(element, 'while')
        self.compileBracketedExpression(element)
        self.compileSymbol(element, '{')
        self.compileStatements(element)
        self.compileSymbol(element, '}')
    
    # 'do' subroutineCall ';'
    def compileDo(self, element: ET.Element):
        self.check_token(Token(TokenType.KEYWORD, 'do'))
        element = ET.SubElement(element, "doStatement")
        self.compileKeyword(element, 'do')
        self.compileSubroutineCall(element)
        self.compileSymbol(element, ';')
    
    # 'return' expression? ';'
    def compileReturn(self, element: ET.Element):
        self.check_token(Token(TokenType.KEYWORD, 'return'))
        element = ET.SubElement(element, "returnStatement")
        self.compileKeyword(element, 'return')
        self.compileOptional(self.compileExpression, element)
        self.compileSymbol(element, ';')
    
    # expressions

    # term (op term)?
    def compileExpression(self, element: ET.Element):
        print("compileExpression")
        print(f"token {self.current_token}")
        element = ET.SubElement(element, "expression")
        self.compileTerm(element)
        self.compileOptional(self.compileOpTerm, element)

    # integerConstant| stringConstant| keywordConstant | varName | 
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term    
    def compileTerm(self, element: ET.Element):
        element = ET.SubElement(element, "term")
        print(f"compileTerm at token {self.current_token}, next_token {self.next_token}")
        
        # Need to look ahead a bit here to check for boxed expressions
        if self.next_token.value == "[":
            print(f"compileTerm next token is {self.next_token}, calling compileVarNameWithBoxedExpression")
            self.compileVarNameWithBoxedExpression(element)
            return
        
        statements = [
            self.compileSubroutineCall, self.compileIntegerConstant, self.compileStringConstant, 
            self.compileKeywordConstant, self.compileVarName,
            self.compileBracketedExpression, self.unaryOpTerm
        ]
        self.compileOr(statements, element)

    def unaryOpTerm(self, element: ET.Element):
        self.compileUnaryOp(element)
        self.compileTerm(element)
    
    # (op term)
    def compileOpTerm(self, element: ET.Element):
        print(f"compileOpTerm at token {self.current_token}")
        self.compileOp(element)
        self.compileTerm(element)
    
    # subroutineName '(' expressionList ')' | ( class Name | var Name) '.' subroutineName '('expressionList ')'
    def compileSubroutineCall(self, element: ET.Element):
        print("compileSubroutineCall")
        statements = [self.compileExpressionListSubroutineCall, self.compileExpressionListCall]
        self.compileOr(statements, element)

    # ( class Name | var Name) '.' subroutineName '('expressionList")'
    def compileExpressionListSubroutineCall(self, element: ET.Element):
        # we need to look ahead here to see if we're calling a method of an object
        print(f"looking ahead at next token {self.next_token}")
        if self.next_token.type != TokenType.SYMBOL or self.next_token.value != ".":
            print(f"object.subroutine() was not detected, next token {self.next_token}")
            raise self.ParseException(f"object.subroutine() was not detected, next token {self.next_token}")
        print("object.subroutine() was detected")
        statements = [self.compileClassName, self.compileVarName]
        self.compileOr(statements, element)
        self.compileSymbol(element, '.')
        self.compileSubroutineName(element)
        self.compileSymbol(element, '(')
        self.compileExpressionList(element)
        self.compileSymbol(element, ')')

    # '(' expressionList ')'
    def compileExpressionListCall(self, element: ET.Element):
        self.check_token(Token(TokenType.SYMBOL, "("))
        self.compileSubroutineName(element)
        self.compileSymbol(element, '(')
        self.compileExpressionList(element)
        self.compileSymbol(element, ')')

    # (expression (',' expression)* )?
    def compileExpressionList(self, element: ET.Element):
        self.compileOptional(self.compileExpressionListBase, element)
    
    # (expression (',' expression)* )
    def compileExpressionListBase(self, element: ET.Element):
        self.compileExpression(element)
        self.compileMultiple(self.compileExpressionMultiple, element)

    # (',' expression)
    def compileExpressionMultiple(self, element: ET.Element):
        self.compileSymbol(element, ',')
        self.compileExpression(element)

    # '+', '-', '*', '/', '&', '|', '<', '>', '='
    def compileOp(self, element: ET.Element):
        self.check_tokens([
            Token(TokenType.SYMBOL, "+"),
            Token(TokenType.SYMBOL, "-"),
            Token(TokenType.SYMBOL, "*"),
            Token(TokenType.SYMBOL, "/"),
            Token(TokenType.SYMBOL, "&"),
            Token(TokenType.SYMBOL, "|"),
            Token(TokenType.SYMBOL, "<"),
            Token(TokenType.SYMBOL, ">"),
            Token(TokenType.SYMBOL, "=")
        ])
        elem = ET.SubElement(element, TokenType.SYMBOL.value)
        elem.text = self.current_token_value
        self.advance()
    
    # '-' | '~'
    def compileUnaryOp(self, element: ET.Element):
        self.check_tokens([
            Token(TokenType.SYMBOL, "-"),
            Token(TokenType.SYMBOL, "~"),
        ])
        elem = ET.SubElement(element, TokenType.SYMBOL.value)
        elem.text = self.current_token_value
        self.advance()
    
    # 'true'|'false'| 'null'|'this'
    def compileKeywordConstant(self, element: ET.Element):
        self.check_tokens([
            Token(TokenType.KEYWORD, 'true'),
            Token(TokenType.KEYWORD, 'false'),
            Token(TokenType.KEYWORD, 'null'),
            Token(TokenType.KEYWORD, 'this')
        ])
        self.check_token(Token(TokenType.KEYWORD, None))
        elem = ET.SubElement(element, TokenType.KEYWORD.value)
        elem.text = self.current_token_value
        self.advance()    

"""
• The top-most / main module
• Input: a single fileName.jack, or a folder containing 0 or more such files
• For each file:
    1. Creates a JackTokenizer from fileName.jack 
    2. Creates an output file named fileName.xml
    3. Creates a CompilationEngine, and calls the compileClass method.
"""
class JackAnalyser():
    # tokens: List[Token] = []
    # parsed_output = []

    @dataclass
    class JackFile:
        name: str
        path: str
        # each line is a single long string
        data: List[str]

    # File or directory
    input_path: str
    output_path: str
    files: List[JackFile]
    
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.files = []

        # find all files, read data from them, clean data
        # for file_path in dir:
        #     jackFile = self.read_file(file_path)
        #     self.files.append(jackFile)
        jackFile = self.read_file(input_path)
        self.files.append(jackFile)


    def read_file(self, file_path) -> List[JackFile]:
        path = pathlib.PurePath(file_path)
        if DEBUG:
            print(f"Reading raw file {path.name} at {file_path}")

        fileReader = open(file_path, "r")
        lines = fileReader.readlines()
        fileReader.close()

        lines = self.clean_lines(lines)
        return self.JackFile(path.name, file_path, lines)

    def clean_lines(self, lines: List[str]) -> List[str]:
        # just read the whole file, trim out whitespace, empty lines
        clean_lines = []
        for line in lines:
            clean_line = self.trim_line(line)
            if clean_line == "\n":
                continue
            if clean_line == "":
                continue
            if clean_line[0:2] == "/*" and clean_line[-2:len(clean_line)] == "*/":
                continue
            clean_lines.append(clean_line)
        return clean_lines

    def trim_line(self, line: str):
        # if DEBUG:
        #     print(f"trimming line:'{line}' ")
        # remove comments and whitespace
        lstripped = line.lstrip()
        # remove lines that start with comment
        if lstripped[0:2] == "//":
            # if DEBUG:
            #     print("trimmed to '\n'")
            return "\n"
        # remove comments at end of line
        if "//" in lstripped:
            lstripped = lstripped.split('//')[0]

        # strip newlines
        line_trimmed = lstripped.rstrip()
        # if DEBUG:
        #     print(f"trimmed to:'{line_trimmed}'")
        return line_trimmed

    def analyse(self):
        for file in self.files:
            if DEBUG:
                print(f"Analysing file {file.name} at {file.path}")
            tokenizer = Tokenizer(file.data)
            tokens = tokenizer.tokenize()
            # print tokens to compare with xxxT.xml file
            # self.write_token_XML(tokens)

            # if DEBUG:
            #     [ print(f"{token.type}, value:{token.value}") for token in tokens ]
            compilationEngine = CompilationEngine(tokens)
            compilationEngine.compile()
            self.write_XML(compilationEngine.parseTree, self.output_path)

    # Walk the parse tree and write to XML
    def write_XML(self, parseTree:ET, file_location: str):
        if DEBUG:
            print(f"writing to location {file_location}")
        # ET.dump(parseTree)
        xmlstr = minidom.parseString(ET.tostring(parseTree.getroot())).toprettyxml(indent="   ")
        print(xmlstr)
        return

    def write_token_XML(self, tokens: List[Token]):
        rootElement = ET.Element("tokens")
        parseTree = ET.ElementTree(rootElement)
        element = parseTree.getroot()
        for token in tokens:
            elem = ET.SubElement(element, token.type.value)
            elem.text = token.value

        xmlstr = minidom.parseString(ET.tostring(element)).toprettyxml(indent="")
        print(xmlstr)


def main():
    global DEBUG
    argparser = argparse.ArgumentParser(description='SyntaxAnalyser')
    argparser.add_argument('--fileread')
    argparser.add_argument('--filewrite')
    argparser.add_argument('--debug', action=argparse.BooleanOptionalAction)

    args = argparser.parse_args()
    if args.debug is not None:
        DEBUG = args.debug
    if DEBUG:
        print("Running SyntaxAnalyser")
        print(f"reading from {args.fileread}")
        print(f"writing to {args.filewrite}")

    analyser = JackAnalyser(args.fileread, args.filewrite)
    analyser.analyse()

DEBUG = True

if __name__ == "__main__":
    main()