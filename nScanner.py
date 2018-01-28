import re

lookAhead = 0
operatorDetector = False
lastLA = 0
counter = 100
reserveID = 0
varID = 200
staticID = 100
scope = 0
flag = False
singleFlag = False

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
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag
    lookAhead += 2
    while lookAhead < len(line):

        if line[lookAhead] == '*' and line[lookAhead + 1] == '/':
            lookAhead += 2
            break

        lookAhead += 1


def is_integer():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag
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
            symbolTable[staticID] = {'type': 'static', 'name': intgr, 'scope': scope}
            token = ['integer', staticID]
            tokens.append(token)
            staticID += 4
            break


def is_identifier():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag

    identifier = line[lookAhead]

    lookAhead += 1

    while True:

        if letterPattern.match(line[lookAhead]) or digitPattern.match(line[lookAhead]):

            identifier += line[lookAhead]

        elif line[lookAhead] in reserveLetters or line[lookAhead] == ' ':
            if identifier in reservedWords:
                for i in symbolTable.keys():
                    if symbolTable[i]['name'] == identifier:
                        continue

                    else:
                        symbolTable[reserveID] = {'type': 'reserved', 'name': identifier, 'scope': scope}
                        token = [identifier, reserveID]
                        tokens.append(token)
                        reserveID += 1

            else:
                symbolTable[varID] = {'type': 'var', 'name': identifier, 'scope': scope}
                token = ['identifier', varID]
                tokens.append(token)
                varID += 4

            operatorDetector = True
            break

        else:
            lookAhead += 1
            break

        lookAhead += 1


def is_equal():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag
    operatorDetector = False

    if line[lookAhead + 1] == '=':

        for i in symbolTable.keys():
            if symbolTable[i]['name'] == '==':
                break

            else:

                symbolTable[reserveID] = {'type': 'reserved', 'name': '==', 'scope': scope}
                token = ['==', reserveID]
                tokens.append(token)
                reserveID += 1
                lookAhead += 2

    else:

        for i in symbolTable.keys():
            if symbolTable[i]['name'] == '=':
                break

            else:
                symbolTable[reserveID] = {'type': 'reserved', 'name': '=', 'scope': scope}
                token = ['=', reserveID]
                tokens.append(token)
                reserveID += 1
                lookAhead += 1


def plus_counter():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag
    if line[lookAhead + 1] == '=':

        for i in symbolTable.keys():
            if symbolTable[i]['name'] == '+=':
                break
            else:
                symbolTable[reserveID] = {'type': 'reserved', 'name': '+=', 'scope': scope}
                token = ['+=', reserveID]
                tokens.append(token)
                reserveID += 1
                lookAhead += 2


    elif digitPattern.match(line[lookAhead + 1]) and (
                        line[lookAhead - 1] == '<' or line[lookAhead - 1] == '=' or line[lookAhead - 1] == '*',
                        line[lookAhead - 1] == ',', line[lookAhead - 1] == '/', line[lookAhead - 1] == ';',
                        line[lookAhead - 1] == '(', line[lookAhead - 1] == '-', line[lookAhead - 1] == '+',
                        line[lookAhead - 1] == '{'):
        operatorDetector = False
        is_integer()

    else:
        for i in symbolTable.keys():
            if symbolTable[i]['name'] == '+':
                break
            else:

                symbolTable[reserveID] = {'type': 'reserved', 'name': '+', 'scope': scope}
                token = ['+', reserveID]
                tokens.append(token)
                reserveID += 1
                lookAhead += 1


def minus_counter():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag

    if digitPattern.match(line[lookAhead + 1]) and (
                        line[lookAhead - 1] == '<' or line[lookAhead - 1] == '=' or line[lookAhead - 1] == '*',
                        line[lookAhead - 1] == ',', line[lookAhead - 1] == '/', line[lookAhead - 1] == ';',
                        line[lookAhead - 1] == '(', line[lookAhead - 1] == '-', line[lookAhead - 1] == '+',
                        line[lookAhead - 1] == '{'):
        operatorDetector = False
        is_integer()


    else:

        for i in symbolTable.keys():
            if symbolTable[i]['name'] == '-':
                break
            else:
                symbolTable[reserveID] = {'type': 'reserved', 'name': '-', 'scope': scope}
                token = ['-', reserveID]
                tokens.append(token)
                reserveID += 1
                lookAhead += 1


def paranteses():
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag
    symbolTable[reserveID] = {'type': 'reserved', 'name': '()', 'scope': scope}
    token = ['()', reserveID]
    tokens.append(token)
    reserveID += 1
    lookAhead += 2


def line_to_tokens(line):
    global lookAhead, reserveID, operatorDetector, staticID, lastLA, counter, varID, scope, flag, singleFlag
    lookAhead = 0
    while lookAhead < len(line):

        if line[lookAhead] == ' ' or flag == True or singleFlag == True:
            lookAhead += 1

        elif line[lookAhead] == '/' and line[lookAhead + 1] == '*':
            flag = True
            delete_multi_line_comment()

        elif line[lookAhead] == '*' and line[lookAhead + 1] == '/':
            flag = False
            lookAhead += 2


        elif line[lookAhead] == '/' and line[lookAhead + 1] == '/':
            singleFlag = True
            lookAhead += 2

        elif line[lookAhead] == '&' and line[lookAhead + 1] == '&':

            for i in symbolTable.keys():
                if symbolTable[i]['name'] == '&&':
                    break

                else:
                    symbolTable[reserveID] = {'type': 'reserved', 'name': '&&', 'scope': scope}
                    token = ['reserved', reserveID]
                    tokens.append(token)
                    reserveID += 1
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

        elif line[lookAhead] == '-':

            minus_counter()


        elif line[lookAhead] == '(' and line[lookAhead + 1] == ')':
            paranteses()

        elif line[lookAhead] in reserveLetters:
            if line[lookAhead] == '{':
                scope += 1
            elif line[lookAhead] == '}':
                scope -= 1
            # operatorDetector = False

            for i in symbolTable.keys():
                if symbolTable[i]['name'] == line[lookAhead]:
                    break

                else:
                    symbolTable[reserveID] = {'type': 'reserved', 'name': line[lookAhead], 'scope': scope}
                    token = [line[lookAhead], reserveID]
                    tokens.append(token)
                    reserveID += 1
                    lookAhead += 1

        else:
            lookAhead += 1
    singleFlag = False


for line in lines:
    print(line)
    line_to_tokens(line)


def get_token():
    data = [tokens[0]]
    del tokens[0]
    return data




print(symbolTable)
