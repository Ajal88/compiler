import re

global lookAhead, reserveID, identifierID, operatorDetector, staticID, lastLA, counter
lookAhead = 0
operatorDetector = False
lastLA = 0
counter = 100
reserveID = 0
varID = 200
staticID = 100

symbolTable = []

with open('test.txt') as test:
    lines = test.readlines()

reservedWords = ['EOF', 'public', 'class', 'static', 'void', 'main', 'extends',
                 'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
                 'true', 'false']

reserveLetters = ['{', '}', ';', '(', ')', '<', '-', '*', '+', ',', '=', '.', '/']
digitPattern = re.compile('[0-9]')
letterPattern = re.compile('[A-Za-z]')
tokens = []


def deleteMultyLineComment():
    lookAhead += 1
    while (lookAhead < len(line)):
        lookAhead += 1
        if (line[lookAhead] == '*' and line[lookAhead + 1] == '*'):
            lookAhead += 2
            break


def isInteger():
    Int = ''
    Int = line[lookAhead]
    while True:
        lookAhead += 1
        if digitPattern.match(line[lookAhead]):
            Int += line[lookAhead]

        elif letterPattern.match(line[lookAhead]):
            lookAhead += 1
            break
        else:
            operatorDetector = True
            dict.append({staticID: {'type': 'static', 'name': Int, 'scope': 'scope'}})
            token = ['integer', staticID]
            tokens.append(token)
            staticID += 4
            break


# todo beporsam

def isIdentifier():
    identifier = ''
    identifier += line[lookAhead]
    while True:
        lookAhead += 1

        if letterPattern.match(line[lookAhead]) or digitPattern.match(line[lookAhead]):

            identifier += line[lookAhead]

        elif line[lookAhead] in reserveLetters or lookAhead == len(line) - 1 or line[lookAhead] == ' ':
            if identifier in reservedWords:
                dict.append({reserveID: {'type': 'reserved', 'name': identifier, 'scope': 'scope'}})
                token = ['reserved', reserveID]
                tokens.append(token)
                reserveID += 4

            else:
                dict.append({varID: {'type': 'var', 'name': identifier, 'scope': 'scope'}})
                token = ['identifier', varID]
                tokens.append(token)
                varID += 4

            operatorDetector = True
            break

        else:
            lookAhead += 1
            break


def isEqual():
    operatorDetector = False

    if line[lookAhead + 1] == '=':
        dict.append({reserveID: {'type': 'reserved', 'name': '==', 'scope': 'scope'}})
        token = ['reserved', reserveID]
        tokens.append(token)
        reserveID += 4
        lookAhead += 2

    else:

        dict.append({reserveID: {'type': 'reserved', 'name': '=', 'scope': 'scope'}})
        token = ['reserved', reserveID]
        tokens.append(token)
        reserveID += 4
        lookAhead += 1


def plusCounter():
    if line[lookAhead + 1] == '=':
        dict.append({reserveID: {'type': 'reserved', 'name': '+=', 'scope': 'scope'}})
        token = ['reserved', reserveID]
        tokens.append(token)
        reserveID += 4
        lookAhead += 2

        # todo
        # elif digitPattern.match(line[lookAhead +1]) and (!(digitPattern.match(line[lookAhead-1])))


def paranteses():
    dict.append({reserveID: {'type': 'reserved', 'name': '()', 'scope': 'scope'}})
    token = ['reserved', reserveID]
    tokens.append(token)
    reserveID += 4
    lookAhead += 2


def Tokens(line):
    while lookAhead < len(line):

        if line[lookAhead] == ' ':
            lookAhead += 1

        elif line[lookAhead] == '/' and line[lookAhead + 1] == '*':
            deleteMultyLineComment()

        elif line[lookAhead] == '/' and line[lookAhead + 1] == '/':
            break

        elif line[lookAhead] == '&' and line[lookAhead + 1] == '&':

            symbolTable.append({reserveID: {'type': 'reserved', 'name': '&&', 'scope': "scope"}})
            token = ['reserved', reserveID]
            tokens.append(token)
            lookAhead += 1

        elif digitPattern.match(line[lookAhead]) or (
                            operatorDetector == False and (
                                    line[lookAhead] == '+' or line[lookAhead] == '-') and digitPattern.match(
                    line[lookAhead + 1])):

            isInteger()

        elif letterPattern.match(line[lookAhead]):
            isIdentifier()


        elif line[lookAhead] == '=':
            isEqual()


        elif line[lookAhead] == '+':
            plusCounter()

        elif line[lookAhead] == '(' and line[lookAhead + 1] == ')':
            paranteses()


        elif line[lookAhead] in reserveLetters:
            operatorDetector = False
            dict.append({reserveID: {'type': 'reserved', 'name': line[lookAhead], 'scope': 'scope'}})
            token = ['reserved', reserveID]
            tokens.append(token)
            reserveID += 4
            lookAhead += 1

        else:
            lookAhead += 1


for line in lines:
    lookAhead = 0
    operatorDetector = False
    Tokens(line)
