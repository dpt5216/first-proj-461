####################################################################################
#   Name:       Dean Taipale
#   Date:       2/5/2022
#   Purpose:    Implements a lexer and parser per the requirements of project 1
####################################################################################

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
            return "EOI"
        else:
            return "Invalid"

#   converts an integer type encoding (pseudo-enum) to a string
def typeToString(type):
    if (type == STRING):
        return "string"
    if (type == KEYWORD):
        return "keyword"
    if (type == EOI):
        return "EOI"
    if (type == INVALID):
        return "invalid"



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
        self.isDone = False

    def nextToken(self):
        while True:
            if (self.isDone): #are we at the end of the string?
                return Token(EOI,"")
            elif (self.ch == '<'):# is a keyword
                val = self.consumeChars(KEYTAGS)
                if (self.ch.isalpha()):
                    val = val + self.consumeChars(LETTERS)
                    if(self.ch == '>'):
                        val = val + '>'
                        self.nextChar()
                        return Token(KEYWORD, val)
            elif (self.ch.isalpha() or self.ch.isdigit()): # is a string
                val = self.consumeChars(LETTERS+DIGITS)
                return Token(STRING, val)
            elif self.ch==' ': self.nextChar() # whitespace
            else: # invalids
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self): 
        if (len(self.stmt) <= self.index): # if we are at the end of the list,
            self.isDone = True # mark as done
            return # don't walk off the end
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1

    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r


import sys

class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.webpage()

#   Implements: WEBPAGE -> <body> { TEXT } </body>
    def webpage(self):
        if (self.token.value != "<body>"):
            self.errorStd("<body>",self.token.value)
        print("<body>")
        while (self.token.value != "</body>"):
            self.token = self.lexer.nextToken()
            self.text(1)
            if (self.token.type == EOI):
                self.errorTyp(KEYWORD,self.token.type)
        print("</body>")

#   Implements: TEXT -> STRING | <b> TEXT </b> | <i> TEXT </i> | LIST
#   note: LIST is not a meaningful change in the grammar, just a useful abstraction for my code.
    def text(self, indnts):
        if(self.token.value == "</body>"):
            return
        elif(self.token.type == STRING):
            print("  "*indnts + self.token.value)
        elif(self.token.type == KEYWORD):
            matchToken = ""
            if (self.token.value == "<b>"):
                matchToken = "</b>"
            elif (self.token.value == "<i>"):
                matchToken = "</i>"
            elif (self.token.value == "<ul>"):
                self.list(indnts)
                return
            print("  "*indnts + self.token.value)
            self.token = self.lexer.nextToken()
            self.text(indnts+1)
            self.token = self.lexer.nextToken()
            if(self.token.value != matchToken):
                self.errorStd(matchToken, self.token.value)
            print("  "*indnts + matchToken)

#   Implements: LIST -> <ul> { LISTITEM } </ul>
#   note: LIST is not a meaningful change in the grammar, just a useful abstraction for my code.
    def list(self, indnts):
        if (self.token.value != "<ul>"):
            self.errorStd("<ul>",self.token.value)
        print("  "*indnts + self.token.value)
        self.token = self.lexer.nextToken()
        while (self.token.value != "</ul>"):
            self.listItem(indnts+1)
            self.token = self.lexer.nextToken()
            if (self.token.type == EOI):
                self.errorTyp(KEYWORD,self.token.type)
        print("  "*indnts + self.token.value)

#   Implements: LISTITEM -> <li> TEXT </li>
    def listItem(self, indnts):
        if (self.token.value != '<li>'):
            self.errorStd('<li>', self.token.value)
        print("  "*indnts + self.token.value)
        self.token = self.lexer.nextToken()
        self.text(indnts +1 )
        self.token = self.lexer.nextToken()
        if (self.token.value != '</li>'):
            self.errorStd('</li>', self.token.value)
        print("  "*indnts + self.token.value)
        

#   Error type for passing strings
    def errorStd(self, exp, saw):
        print ("Syntax error: expecting literally: " + exp \
               + "; saw: " + saw )
        sys.exit(1)

#   Error type for passing token types
    def errorTyp(self, exp, saw):
        print ("Syntax error: expecting type: " + typeToString(exp) \
               + "; saw: " + typeToString(saw) )
        sys.exit(1)




print("Testing the lexer: test 1")
lex = Lexer ("<body> google <b><i><b> yahoo</b></i></b></body>")
tk = lex.nextToken()
while (tk.getType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the lexer: test 2")
lex = Lexer("<body> google <ul> <li> pizza </li> <li> apple </li> <li> bannana </li> </ul><i>pizza</i><b><i><b> yahoo</b></i></b></body>")
tk = lex.nextToken()
while (tk.getType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the lexer: test 3")
lex = Lexer("<body> google <ul> <li> pizza </li> <li> <b>apple </b> </li> <li> <i> <b>bannana</b> </i> </li> </ul><i> <b> pizza </b> </i><b><i><b> yahoo</b></i></b></body>")
tk = lex.nextToken()
while (tk.getType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the parser: test 1")
parser = Parser ("<body> google <b><i><b> yahoo</b></i></b></body>")
parser.run()

print("Testing the parser: test 2")
parser = Parser ("<body> google <ul> <li> pizza </li> <li> apple </li> <li> bannana </li> </ul><i>pizza</i><b><i><b> yahoo</b></i></b></body>")
parser.run()

print("Testing the parser: test 3")
parser = Parser("<body> google <ul> <li> pizza </li> <li> <b>apple </b> </li> <li> <i> <b>bannana</b> </i> </li> </ul><i> <b> pizza </b> </i><b><i><b> yahoo</b></i></b></body>")
parser.run()