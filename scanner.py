import fileinput
import re

reservedWords = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
                 'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
                 'true', 'false', '&&', '==', '<', '>', '+=', '-', '*', '+', '//', '/*', '*/', ',', '=', '.']

tokens = []

flag = False

symbolTable = dict()

with open('test.txt') as test:
    lines = test.readlines()

reserveID = 0
varID = 200
staticID = 100
scope = 0

for line in lines:

    for Terminal in reservedWords:
        if Terminal in line:

            if Terminal == 'System.out.println':
                line = line.replace(Terminal, 'SOT')
                continue
            elif Terminal == '==':
                line = line.replace(Terminal, ' EQEQ ')
                continue

            if line.index(Terminal) == 0:
                line = line[:len(Terminal)] + ' ' + line[len(Terminal):]

            else:
                line = line[:line.index(Terminal)] + ' ' + line[line.index(Terminal):]
                line = line[:line.index(Terminal) + len(Terminal)] + ' ' + line[line.index(Terminal) + len(Terminal):]

    wordsInLine = line.split()
    for words in wordsInLine:

        if flag == True:
            if words == '*/':
                flag = False
                continue
            else:
                continue

        else:
            if words in reservedWords:
                if words == '//':
                    break

                elif words == '/*':
                    flag = True
                    continue

                elif words == '{':

                    symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                    token = ['reserved', reserveID]
                    tokens.append(token)
                    reserveID += 4
                    scope += 1

                elif words == '}':
                    symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                    token = ['reserved', reserveID]
                    tokens.append(token)
                    reserveID += 4
                    scope -= 1

                else:
                    symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                    token = ['reserved', reserveID]
                    tokens.append(token)
                    reserveID += 4

            elif words == 'SOT':
                symbolTable[reserveID] = {'type': 'reserved', 'name': 'System.out.println', 'scope': scope}
                token = ['reserved', reserveID]
                tokens.append(token)
                reserveID += 4

            elif words == 'EQEQ':
                symbolTable[reserveID] = {'type': 'reserved', 'name': '==', 'scope': scope}
                token = ['reserved', reserveID]
                tokens.append(token)
                reserveID += 4


            elif len(words) == 1:
                letterPattern = re.compile('[A-Za-z]')
                digitPattern = re.compile('[0-9]')


                if letterPattern.match(words):
                    symbolTable[varID] = {'type': 'var', 'name': words, 'scope': scope}
                    token = ['identifier', varID]
                    tokens.append(token)
                    varID += 4

                elif digitPattern.match(words):
                    symbolTable[staticID] = {'type': 'static', 'name': words, 'scope': scope}
                    token = ['integer', staticID]
                    tokens.append(token)
                    staticID+= 4

                else:
                    print(words + "did not match any")

            else:

                identifierPattern = re.compile('[A-Za-z]([A-Za-z]|[0-9])+')
                integerPattern = re.compile('[0-9]+')

                if identifierPattern.match(words):
                    symbolTable[varID] = {'type': 'var', 'name': words, 'scope': scope}
                    token = ['identifier', varID]
                    tokens.append(token)
                    reserveID += 4


                elif integerPattern.match(words):
                    symbolTable[staticID] = {'type': 'static', 'name': words, 'scope': scope}
                    token = ['integer', staticID]
                    tokens.append(token)
                    reserveID += 4


def sendNextToken():
    data = [tokens[0]]

    del tokens[0]

    return data

