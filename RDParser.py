
INVALID, STRING, KEYWORD, EOI= -1, 0, 1, 2

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def __repr__(self):
        if (self.type in [STRING, KEYWORD]):
            return self.value
        if (self.type == EOI):
            return ""
        else:
            return "Invalid"


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
KEYTAGS = "</>"

class Lexer:

    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement
    def __init__ (self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if (self.ch == '<'):# is a keyword
                val = self.consumeChars("</")
                if (self.ch in [LETTERS, DIGITS]):
                    val += self.consumeChars(LETTERS+DIGITS)
                    if (self.ch == '>'):
                        self.nextChar()
                        val += '>'
                        return Token(KEYWORD, val)
                    else:
                        return Token(INVALID, val)
                else:
                    return Token(INVALID, val)

            if (self.ch in [LETTERS, DIGITS]): # is a string
                val = self.consumeChars(LETTERS+DIGITS)
                return Token(STRING, val)

            elif self.ch==' ': self.nextChar()
            elif self.ch=='':
                return Token(EOI,"")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1

    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

#    def checkChar(self, c):
#        if (self.ch==c):
#            self.nextChar()
#            return True
#        else: return False

import sys

# NOT YET IMPLEMENTED

class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.statement()

    def statement(self):
        print("<Statement>")
        self.assignmentStmt()
        while self.token.getTokenType() == SEMICOLON:
            print("\t<Semicolon>;</Semicolon>")
            self.token = self.lexer.nextToken()
            self.assignmentStmt()
        self.match(EOI)
        print("</Statement>")

    def assignmentStmt(self):
        print("\t<Assignment>")
        val = self.match(ID)
        print("\t\t<Identifier>" + val + "</Identifier>")
        self.match(ASSIGNMENTOP)
        print("\t\t<AssignmentOp>:=</AssignmentOp>")
        self.expression()
        print("\t</Assignment>")

    def expression(self):
        if self.token.getTokenType() == ID:
            print("\t\t<Identifier>" + self.token.getTokenValue() \
                   + "</Identifier>")
        elif self.token.getTokenType() == INT:
            print("\t\t<Int>" + self.token.getTokenValue() + "</Int>")
        elif self.token.getTokenType() == FLOAT:
            print("\t\t<Float>" + self.token.getTokenValue() + "</Float>")
        else:
            print("Syntax error: expecting an ID, an int, or a float" \
                  + "; saw:" \
                  + typeToString(self.token.getTokenType()))
            sys.exit(1)
        self.token = self.lexer.nextToken()


    def match (self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else: self.error(tp)
        return val

    def error(self, tp):
        print ("Syntax error: expecting: " + typeToString(tp) \
               + "; saw: " + typeToString(self.token.getTokenType()))
        sys.exit(1)