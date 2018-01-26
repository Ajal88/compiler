import re

global lookAhead, ID, operatorDetector
lookAhead = 0
operatorDetector = False
lastLA = 0
counter = 100

id = 0
ID = 499

symbolTable = []
reservedSymbolTable = []

input = "class  Cls{ /n" \
        "static boolean d;/n " \
        "public static int test(int a,boolean b){/n" \
        "int c;/n" \
        "c=1;/n" \
        "b=true; return a+c; return a&&b; a==b/n" \
        "System.out.println (salam)/n" \
        "}}/n" \
        "public class Cls2{/n" \
        "public static void main(){/n" \
        "int b;/n" \
        "b+=3;/n" \
        "b=Cls.test(b,false);/n" \
        "}}/n" \
        "EOF"

reservedWords = ['EOF', 'public', 'class', 'static', 'void', 'main', '()', 'extends',
                 'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
                 'true', 'false', '&&', '==', '<', '+=', '//', '/*', '*/']

reserveLetters = ['{', '}', ';', '(', ')', '<', '-', '*', '+', ',', '=', '.']

digitPattern = re.compile('[0-9]')
letterPattern = re.compile('[A-Za-z]')

tokens = []


def deleteMultyLineComment():
    lookAhead += 1
    while (lookAhead < len(input)):
        lookAhead += 1
        if (input[lookAhead] == '*' and input[lookAhead + 1] == '*'):
            lookAhead += 2
            break


def deleteSingleLineComment():
    return "slam"


def isInteger():
    Int = input[lookAhead]
    while (True):
        lookAhead += 1
        if digitPattern.match(input[lookAhead]):
            Int += input[lookAhead]

        elif letterPattern.match(input[lookAhead]):
            lookAhead += 1
            break
        else:
            operatorDetector = True
            ID += 1
            dict = ['integer', ID]
            tokens.append(dict)
            symbolTable.append(Int)


def isIdentifier():
    identifier = ''
    identifier += input[lookAhead]
    while True:
        lookAhead += 1

        if letterPattern.match(input[lookAhead]) or digitPattern.match(input[lookAhead]):

            identifier += input[lookAhead]

        elif input[lookAhead] in reserveLetters or lookAhead == len(input) - 1 or input[lookAhead] == ' ':
            if identifier in reservedWords:
                dict = [identifier, id]
                tokens.append(dict)
                reservedSymbolTable.append(identifier)
                id += 1

            else:
                dict = ['identifier', ID]
                tokens.append(dict)
                symbolTable.append(identifier)
                ID += ID

            operatorDetector = True
            break

        else:
            lookAhead += 1
            break


def isEqual():
    operatorDetector = False

    if input[lookAhead + 1] == '=':
        dict = ['==', id]
        tokens.append(dict)
        reservedSymbolTable.append('==')
        id += 1
        lookAhead += 2

    else:
        dict = ['=', id]
        tokens.append(dict)
        reservedSymbolTable.append('=')
        id += 1
        lookAhead += 1


def plusCounter():
    dict = ['+=', id]
    tokens.append(dict)
    reservedSymbolTable.append('+=')
    id += 1
    lookAhead += 2


def paranteses():
    dict = ['()', id]
    tokens.append(dict)
    reservedSymbolTable.append('()')
    id += 1
    lookAhead += 2


while lookAhead < len(input):


    if input[lookAhead] == ' ':
        lookAhead += 1

    elif input[lookAhead] == '/' and input[lookAhead + 1] == '*':

        deleteMultyLineComment()

    elif input[lookAhead] == '/' and input[lookAhead + 1] == '/':
        # todo
        deleteSingleLineComment()

    elif input[lookAhead] == '&' and input[lookAhead + 1] == '&':

        id += 1
        dict = ['&&', id]
        tokens.append(dict)
        reservedSymbolTable.append('&&')
        lookAhead += 1



    elif digitPattern.match(input[lookAhead]) or (
                        operatorDetector == False and (
                                input[lookAhead] == '+' or input[lookAhead] == '-') and digitPattern.match(
                input[lookAhead + 1])):

        isInteger()

    elif letterPattern.match(input[lookAhead]):
        isIdentifier()


    elif input[lookAhead] == '=':

        isEqual()


    elif input[lookAhead] == '+' and input[lookAhead + 1] == '=':

        plusCounter()

    elif input[lookAhead] == '(' and input[lookAhead] == ')':

        paranteses()


    elif input[lookAhead] in reserveLetters:

        operatorDetector = False
        dict = [input[lookAhead], id]
        tokens.append(dict)
        reservedSymbolTable.append(input[lookAhead])
        id += 1
        lookAhead += 1

    else:
        lookAhead += 1




print(tokens)