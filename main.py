# authored by Nathan Williams; npw5145; description of purpose of the file
import sys

#Definitions
STRING, KEYWORD, WEBPAGE, TEXT, LISTITEM, INVALID, EOI = 1, 2, 3, 4, 5, 6, 7 
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
KEYWORDLIST = ["<body>", "</body>", "<b>" , "</b>" ,"<i>" , "</i>", "<ul>" , "</ul>" , "<li>" , "</li>"] 


def typeToString (tp):
    if (tp == STRING): return "String"
    elif (tp == KEYWORD): return "Keyword"
    elif (tp == WEBPAGE): return "Webpage"
    elif (tp == TEXT): return "Text"
    elif (tp == LISTITEM): return "Listitem"
    elif (tp == EOI): return "EOI"
    return "Invalid"

class Token:
    "A class for representing Tokens"
    # a Token object has two fields: the token's type and its value
    def __init__ (self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal
    def getTokenType(self):
        return self.type
    def getTokenValue(self):
        return self.val
    def __repr__(self):
        if (self.type in [STRING, KEYWORD, WEBPAGE, TEXT, LISTITEM]): 
            return self.val
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"

class Lexer:
   
    def __init__ (self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch.isdigit() or self.ch.isalpha(): #Creates String tokens
                string = self.consumeChars(LETTERS+DIGITS)
                return Token(STRING, string)
            elif self.ch == "<": #Creates KEYWORD tokens if valid o/w creates INVALID tokens
                key = self.consumeKey(LETTERS+"/")
                if key in KEYWORDLIST:
                    return Token(KEYWORD,key)
                else:
                    return Token(INVALID, key)
            elif self.ch == " ": #Skips over blank spaces
                self.nextChar()
            elif self.ch == "$": #Checks if there is no more characters left and creates EOI Token
                return Token(EOI,"")
            else: #If the character is not a valid characters it creates an INVALID Token
                return Token(INVALID, self.ch)
   
    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    def consumeKey(self,set):
        r = self.ch
        self.nextChar()
        while (self.ch != ">" and self.ch in set):
            r = r + self.ch
            self.nextChar()

        if self.ch == ">":
            r = r + self.ch
            self.nextChar()
        return r

    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1


#The Parser using Recursive Descent
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


#Test Code
print("Testing the lexer: test 1")
lex = Lexer ("<body> google <b><i><b> yahoo</b></i></b></body> $")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the lexer: test 2")
lex = Lexer ("<body> google <x><i><b> yahoo</b></i></b></body> $")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

print("Testing the lexer: test 3")
lex = Lexer ("google yahoo $")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")

'''
print("Testing the parser: test 1")
parser = Parser ("x := 1");
parser.run();
print("Testing the parser: test 2")
parser = Parser ("x := 1; y := 2.3; z := x");
parser.run();
print("Testing the parser: test 3")
parser = Parser ("x := 1; y ; 2; z := x");
parser.run();
'''