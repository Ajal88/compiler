import re

reservedWords = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
                 'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
                 'true', 'false', '&&', '==', '<', '>', '+=', '-', '*', '+', '//', '/*', '*/', ',', '=', '.']

tokens = []

flag = False

symbolTable = dict()

with open('in.txt') as test:
    lines = test.readlines()

reserveID = 0
varID = 200
staticID = 100
scope = 0
notAssigned = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
               'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
               'true', 'false', '&&', '==', '<', '>', '+=', '-', '*', '+', '//', '/*', '*/', ',', '=', '.']

assignedIdentifiers = []

assignedStatic = []


def not_assign_update():
    global notAssigned, symbolTable
    for i in symbolTable.keys():
        if symbolTable[i]['name'] in notAssigned:
            notAssigned.remove(symbolTable[i]['name'])


def not_assigned_identifers(word, scope):

    global assignedIdentifiers
    canAdd = False
    for i in assignedIdentifiers:
        if i[0] == word and i[1] == scope:
            canAdd = False
            break
        else:
            canAdd = True

    return canAdd


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

        if flag:
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
                    scope += 1
                    if words in notAssigned:
                        symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                        token = ['{', reserveID]
                        tokens.append(token)
                        reserveID += 1
                        not_assign_update()

                elif words == '}':
                    scope -= 1
                    if words in notAssigned:
                        symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                        token = ['}', reserveID]
                        tokens.append(token)
                        reserveID += 1
                        not_assign_update()

                else:
                    if words in notAssigned:
                        symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                        token = [words, reserveID]
                        tokens.append(token)
                        reserveID += 1
                        not_assign_update()

            elif words == 'SOT':
                if 'System.out.println' in notAssigned:
                    symbolTable[reserveID] = {'type': 'reserved', 'name': 'System.out.println', 'scope': scope}
                    token = ['System.out.println', reserveID]
                    tokens.append(token)
                    reserveID += 1
                    not_assign_update()

            elif words == 'EQEQ':
                if '==' in notAssigned:
                    symbolTable[reserveID] = {'type': 'reserved', 'name': '==', 'scope': scope}
                    token = ['==', reserveID]
                    tokens.append(token)
                    reserveID += 1
                    not_assign_update()

            elif len(words) == 1:
                letterPattern = re.compile('[A-Za-z]')
                digitPattern = re.compile('[0-9]')

                if letterPattern.match(words):
                    if not_assigned_identifers(words, scope) or len(assignedIdentifiers) == 0:
                        symbolTable[varID] = {'type': 'var', 'name': words, 'scope': scope}
                        token = ['identifier', varID]
                        tokens.append(token)
                        varID += 4
                        assignedIdentifiers.append([words, scope])

                elif digitPattern.match(words):
                    if words not in assignedStatic:
                        symbolTable[staticID] = {'type': 'static', 'name': words, 'scope': scope}
                        token = ['integer', staticID]
                        tokens.append(token)
                        staticID += 4
                        assignedStatic.append(words)

                else:
                    print(words + "did not match any")

            else:

                identifierPattern = re.compile('[A-Za-z]([A-Za-z]|[0-9])+')
                integerPattern = re.compile('[+-]?[0-9]+')

                if identifierPattern.match(words):
                    if not_assigned_identifers(words, scope) or len(assignedIdentifiers) == 0:
                        symbolTable[varID] = {'type': 'var', 'name': words, 'scope': scope}
                        token = ['identifier', varID]
                        tokens.append(token)
                        varID += 4
                        assignedIdentifiers.append([words, scope])

                elif integerPattern.match(words):
                    if words not in assignedStatic:
                        symbolTable[staticID] = {'type': 'static', 'name': words, 'scope': scope}
                        token = ['integer', staticID]
                        tokens.append(token)
                        staticID += 4
                        assignedStatic.append(words)


def send_next_token():
    data = tokens[0]
    del tokens[0]
    return data
