import re

from enum import Enum


class Type(Enum):
    BLOCK_COMMENT = "(/\\*.*?\\*/).*"
    LINE_COMMENT = "(//(.*?)[\r$]?\n).*"
    SPACE = "( ).*"
    OPEN_PAREN = "(\\().*"
    CLOSE_PAREN = "(\\)).*"
    SEMICOLON = "(;).*"
    COMMA = "(,).*"
    OPEN_CURLY_BRACE = "(\\{).*"
    CLOSE_CURLY_BRACE = "(\\}).*"
    OPEN_BRACE = "(\\[).*"
    CLOSE_BRACE = "(\\]).*"
    DOUBLE_CONSTANT = "\\b(\\d{1,9}\\.\\d{1,32})\\b.*"
    INT_CONSTANT = "\\b(\\d{1,9})\\b.*"
    VOID = "\\b(void)\\b.*"
    INT = "\\b(int)\\b.*"
    DOUBLE = "\\b(int|double)\\b.*"
    TAB = "(\\t).*"
    NEW_LINE = "(\\n).*"
    PUBLIC = "\\b(public)\\b.*"
    PRIVATE = "\\b(private)\\b.*"
    FALSE = "\\b(false)\\b.*"
    TRUE = "\\b(true)\\b.*"
    NULL = "\\b(null)\\b.*"
    RETURN = "\\b(return)\\b.*"
    NEW = "\\b(new)\\b.*"
    CLASS = "\\b(class)\\b.*"
    IF = "\\b(if)\\b.*"
    ELSE = "\\b(else)\\b.*"
    WHILE = "\\b(while)\\b.*"
    STATIC = "\\b(static)\\b.*"
    STRING = "\\b(String)\\b.*"
    CHAR = "\\b(char)\\b.*"
    FINAL = "\\b(final)\\b.*"
    ABSTRACT = "\\b(abstract)\\b.*"
    CONTINUE = "\\b(continue)\\b.*"
    FOR = "\\b(for)\\b.*"
    SWITCH = "\\b(switch)\\b.*"
    ASSERT = "\\b(assert)\\b.*"
    DEFAULT = "\\b(default)\\b.*"
    GOTO = "\\b(goto)\\b.*"
    PACKAGE = "\\b(package)\\b.*"
    SYNCHRONIZED = "\\b(synchronized)\\b.*"
    BOOLEAN = "\\b(boolean)\\b.*"
    DO = "\\b(do)\\b.*"
    THIS = "\\b(this)\\b.*"
    BYTE = "\\b(byte)\\b.*"
    IMPORT = "\\b(import)\\b.*"
    THROWS = "\\b(throws)\\b.*"
    BREAK = "\\b(break)\\b.*"
    IMPLEMENTS = "\\b(implements)\\b.*"
    PROTECTED = "\\b(protected)\\b.*"
    THROW = "\\b(throw)\\b.*"
    CASE = "\\b(case)\\b.*"
    ENUM = "\\b(enum)\\b.*"
    INSTANCEOF = "\\b(instanceof)\\b.*"
    TRANSIENT = "\\b(transient)\\b.*"
    CATCH = "\\b(catch)\\b.*"
    EXTENDS = "\\b(extends)\\b.*"
    SHORT = "\\b(short)\\b.*"
    TRY = "\\b(try)\\b.*"
    INTERFACE = "\\b(INTERFACE)\\b.*"
    FINALLY = "\\b(FINALLY)\\b.*"
    LONG = "\\b(LONG)\\b.*"
    STRICTFP = "\\b(strictfp)\\b.*"
    VOLATILE = "\\b(volatile)\\b.*"
    CONST = "\\b(const)\\b.*"
    FLOAT = "\\b(float)\\b.*"
    NATIVE = "\\b(native)\\b.*"
    super = "\\b(super)\\b.*"
    POINT = "(\\.).*"
    PLUS = "(\\+{1}).*"
    MINUS = "(\\-{1}).*"
    MULTIPLY = "(\\*).*"
    DIVIDE = "(/).*"
    EQUAL = "(==).*"
    ASSIGNMENT = "(=).*"
    NOT_EQUAL = "(\\!=).*"
    CLOSE_CARET = "(>).*"
    OPEN_CARET = "(<).*"
    IDENTIFIER = "\\b([a-zA-Z]{1}[0-9a-zA-Z_]{0,31})\\b.*"
    STRING_LITERAL = '"(\\.|[^\\"])*"'
    CHARACTER_LITERAL = r"\'(\\.|[^\\'])*\'"


brackets = {
    Type.OPEN_PAREN: Type.CLOSE_PAREN,  # ()
    Type.OPEN_BRACE: Type.CLOSE_BRACE,  # []
    Type.OPEN_CURLY_BRACE: Type.CLOSE_CURLY_BRACE,  # {}
}

str_brackets = {
    Type.OPEN_PAREN: "(",
    Type.CLOSE_PAREN: ")",
    Type.OPEN_BRACE: "[",
    Type.CLOSE_BRACE: "]",
    Type.OPEN_CURLY_BRACE: "{",
    Type.CLOSE_CURLY_BRACE: "}",
}


class Token:
    def __init__(self, begin, end, value, type):
        self.begin = begin
        self.end = end
        self.value = value
        self.type = type

    def __str__(self):
        return self.type.name + "\t\t" + self.value

    __repr__ = __str__


class CodeStack:
    data = ""
    stack = []
    tokens = []

    def __init__(self, data):
        self.data = data

    def add(self, token):
        self.tokens.append(token)

        if token.type in brackets:
            self.stack.append(token)
        if token.type in brackets.values():
            if len(self.stack) == 0:
                line_num, line_text = self.get_trouble_line(token.end)
                raise Exception(f"Missing open brackets! line {line_num}:\n{line_text}")
            elif token.type == brackets[self.stack[-1].type]:
                if not self.is_valid_end():
                    line_num, line_text = self.get_trouble_line(self.stack[-1].end)
                    raise Exception(f"Missing semicolon! line {line_num}:\n{line_text}")
                self.stack.pop()
            elif token.type != brackets[self.stack[-1].type]:
                need_type = str_brackets[brackets[self.stack[-1].type]]
                line_num, line_text = self.get_trouble_line(token.end)
                raise Exception(
                    f'Incorrect close bracket! Must be "{need_type}"! line {line_num}:\n{line_text}'
                )
            else:
                self.stack.append(token)

    def get_tokens(self):
        if len(self.stack) == 0:
            return self.tokens
        else:
            print(self.stack)
            line_num, line_text = self.get_trouble_line(self.stack[-1].begin)
            raise Exception(f"Missing close brackets! line {line_num}:\n{line_text}")

    def is_valid_end(self):
        for t in self.tokens[::-1]:
            if t.type == Type.SPACE:
                continue
            elif t.type == Type.SEMICOLON or t.type in str_brackets:
                return True
            else:
                return False
        return False

    def get_trouble_line(self, index):
        line_number = self.data.count("\n", 0, index)
        lines = self.data.split("\n")

        return line_number + 1, lines[line_number]


def get_token(string, begin):
    if begin < 0 or begin >= len(string):
        raise IndexError(string, "Index out of bounds: " + begin)
    for type in Type:
        pattern = r".{" + str(begin) + "}" + type.value
        match = re.match(pattern, string, re.DOTALL)
        if match:
            end = match.end(1)
            if type == Type.STRING_LITERAL or type == Type.CHARACTER_LITERAL:
                end += 1
            return Token(begin, end, string[begin:end], type)
    return None


def lex_java_file(file_name):
    with open(file_name, "r") as file:
        data = file.read()
        tokens = CodeStack(data)

        index = 0
        while index < len(data):
            token = get_token(data, index)
            if token is None:
                break
            index = token.end

            tokens.add(token)
        if index != len(data):
            raise Exception(f"Lexical error at position {index}")

    return tokens.get_tokens()
