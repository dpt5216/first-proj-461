
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
                    if (self.ch == '>')
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
