import re

lookAhead = 0
operatorDetector = False
lastLA = 0
counter = 100
reserveID = 0
varID = 200
staticID = 100

symbolTable = dict()

with open('test.txt') as test:
    lines = test.readlines()

reservedWords = ['EOF', 'public', 'class', 'static', 'void', 'main', 'extends',
                 'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
                 'true', 'false']

reserveLetters = ['{', '}', ';', '(', ')', '<', '-', '*', '+', ',', '=', '.', '/']
digitPattern = re.compile('[0-9]')
letterPattern = re.compile('[A-Za-z]')
tokens = []


def delete_multi_line_comment():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID
    lookAhead += 1
    while lookAhead < len(line):
        lookAhead += 1
        if line[lookAhead] == '*' and line[lookAhead + 1] == '*':
            lookAhead += 2
            break


def is_integer():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID
    intgr = line[lookAhead]
    while True:
        lookAhead += 1
        if digitPattern.match(line[lookAhead]):
            intgr += line[lookAhead]

        elif letterPattern.match(line[lookAhead]):
            lookAhead += 1
            break
        else:
            operatorDetector = True
            symbolTable[staticID] = {'type': 'static', 'name': intgr, 'scope': 'scope'}
            token = ['integer', staticID]
            tokens.append(token)
            staticID += 4
            break


# todo beporsam

def is_identifier():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID
    identifier = ''
    identifier += line[lookAhead]
    while True:
        lookAhead += 1

        if letterPattern.match(line[lookAhead]) or digitPattern.match(line[lookAhead]):

            identifier += line[lookAhead]

        elif line[lookAhead] in reserveLetters or lookAhead == len(line) - 1 or line[lookAhead] == ' ':
            if identifier in reservedWords:
                symbolTable[reserveID] = {'type': 'reserved', 'name': identifier, 'scope': 'scope'}
                token = ['reserved', reserveID]
                tokens.append(token)
                reserveID += 4

            else:
                symbolTable[varID] = {'type': 'var', 'name': identifier, 'scope': 'scope'}
                token = ['identifier', varID]
                tokens.append(token)
                varID += 4

            operatorDetector = True
            break

        else:
            lookAhead += 1
            break


def is_equal():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID
    operatorDetector = False

    if line[lookAhead + 1] == '=':
        symbolTable[reserveID] = {'type': 'reserved', 'name': '==', 'scope': 'scope'}
        token = ['reserved', reserveID]
        tokens.append(token)
        reserveID += 4
        lookAhead += 2

    else:

        symbolTable[reserveID] = {'type': 'reserved', 'name': '=', 'scope': 'scope'}
        token = ['reserved', reserveID]
        tokens.append(token)
        reserveID += 4
        lookAhead += 1


def plus_counter():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID
    if line[lookAhead + 1] == '=':
        symbolTable[reserveID] = {'type': 'reserved', 'name': '+=', 'scope': 'scope'}
        token = ['reserved', reserveID]
        tokens.append(token)
        reserveID += 4
        lookAhead += 2

        # todo
        # elif digitPattern.match(line[lookAhead +1]) and (!(digitPattern.match(line[lookAhead-1])))


def paranteses():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID
    symbolTable[reserveID] = {'type': 'reserved', 'name': '()', 'scope': 'scope'}
    token = ['reserved', reserveID]
    tokens.append(token)
    reserveID += 4
    lookAhead += 2


def line_to_tokens(line):
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID
    while lookAhead < len(line):

        if line[lookAhead] == ' ':
            lookAhead += 1

        elif line[lookAhead] == '/' and line[lookAhead + 1] == '*':
            delete_multi_line_comment()

        elif line[lookAhead] == '/' and line[lookAhead + 1] == '/':
            break

        elif line[lookAhead] == '&' and line[lookAhead + 1] == '&':

            symbolTable[reserveID] = {'type': 'reserved', 'name': '&&', 'scope': "scope"}
            token = ['reserved', reserveID]
            tokens.append(token)
            lookAhead += 1

        elif digitPattern.match(line[lookAhead]) or (
                operatorDetector == False and (
                line[lookAhead] == '+' or line[lookAhead] == '-') and digitPattern.match(
            line[lookAhead + 1])):

            is_integer()

        elif letterPattern.match(line[lookAhead]):
            is_identifier()

        elif line[lookAhead] == '=':
            is_equal()

        elif line[lookAhead] == '+':
            plus_counter()

        elif line[lookAhead] == '(' and line[lookAhead + 1] == ')':
            paranteses()

        elif line[lookAhead] in reserveLetters:
            operatorDetector = False
            symbolTable[reserveID] = {'type': 'reserved', 'name': line[lookAhead], 'scope': 'scope'}
            token = ['reserved', reserveID]
            tokens.append(token)
            reserveID += 4
            lookAhead += 1

        else:
            lookAhead += 1


for line in lines:
    line_to_tokens(line)
