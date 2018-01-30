import re

reservedWords = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
                 'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
                 'true', 'false', '&&', '==', '<', '+=', '-', '*', '+', '//', '/*', '*/', ',', '=', '.']

tokens = []

flag = False

symbolTable = dict()

with open('test.txt') as test:
    lines = test.readlines()

reserveID = 0
varID = 200
staticID = 100
scope = 0
notAssigned = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
               'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
               'true', 'false', '&&', '==', '<', '+=', '-', '*', '+', '//', '/*', '*/', ',', '=', '.']

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

            line = line.replace(Terminal, ' ' + Terminal + ' ', line.count(Terminal))

            if Terminal == 'System.out.println':
                line = line.replace(Terminal, '>>>')
                continue
            elif Terminal == '==':
                line = line.replace(Terminal, ' !!! ')
                continue

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
                    else:
                        for i in symbolTable:
                            if symbolTable[i]['name'] == words:
                                address = i
                                token = [words, address]
                                tokens.append(token)
                                break

                elif words == '}':
                    scope -= 1
                    if words in notAssigned:
                        symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                        token = ['}', reserveID]
                        tokens.append(token)
                        reserveID += 1
                        not_assign_update()

                    else:
                        for i in symbolTable:
                            if symbolTable[i]['name'] == words:
                                address = i
                                token = [words, address]
                                tokens.append(token)
                                break

                else:
                    if words in notAssigned:
                        symbolTable[reserveID] = {'type': 'reserved', 'name': words, 'scope': scope}
                        token = [words, reserveID]
                        tokens.append(token)
                        reserveID += 1
                        not_assign_update()
                    else:
                        for i in symbolTable:
                            if symbolTable[i]['name'] == words:
                                address = i
                                token = [words, address]
                                tokens.append(token)
                                break


            elif words == '>>>':
                if 'System.out.println' in notAssigned:
                    symbolTable[reserveID] = {'type': 'reserved', 'name': 'System.out.println', 'scope': scope}
                    token = ['System.out.println', reserveID]
                    tokens.append(token)
                    reserveID += 1
                    not_assign_update()
                else:
                    for i in symbolTable:
                        if symbolTable[i]['name'] == 'System.out.println':
                            address = i
                            token = ['System.out.println', address]
                            tokens.append(token)
                            break


            elif words == '!!!':
                if '==' in notAssigned:
                    symbolTable[reserveID] = {'type': 'reserved', 'name': '==', 'scope': scope}
                    token = ['==', reserveID]
                    tokens.append(token)
                    reserveID += 1
                    not_assign_update()
                else:

                    for i in symbolTable:
                        if symbolTable[i]['name'] == '==':
                            address = i
                            token = ['==', address]
                            tokens.append(token)
                            break


            elif len(words) == 1:
                letterPattern = re.compile('[A-Za-z]$')
                digitPattern = re.compile('[0-9]$')

                if letterPattern.match(words):
                    if not_assigned_identifers(words, scope) or len(assignedIdentifiers) == 0:
                        symbolTable[varID] = {'type': 'var', 'name': words, 'scope': scope}
                        token = ['identifier', varID]
                        tokens.append(token)
                        varID += 4
                        assignedIdentifiers.append([words, scope])
                    else:

                        for i in symbolTable:
                            if symbolTable[i]['name'] == words and symbolTable[i]['scope'] == scope:
                                token = ['identifier', i]
                                tokens.append(token)

                elif digitPattern.match(words):
                    if words not in assignedStatic:
                        symbolTable[staticID] = {'type': 'static', 'name': words, 'scope': scope}
                        token = ['integer', staticID]
                        tokens.append(token)
                        staticID += 4
                        assignedStatic.append(words)

                    else:

                        for i in symbolTable:
                            if symbolTable[i]['name'] == words:
                                token = ['integer', i]
                                tokens.append(token)

                else:
                    print(words + "did not match any of characters/digits")

            else:

                identifierPattern = re.compile('[A-Za-z][A-Za-z0-9]+$')
                integerPattern = re.compile('[+-]?[0-9]+$')

                if identifierPattern.match(words):
                    if not_assigned_identifers(words, scope) or len(assignedIdentifiers) == 0:
                        symbolTable[varID] = {'type': 'var', 'name': words, 'scope': scope}
                        token = ['identifier', varID]
                        tokens.append(token)
                        varID += 4
                        assignedIdentifiers.append([words, scope])

                    else:
                        for i in symbolTable:
                            if symbolTable[i]['name'] == words and symbolTable[i]['scope'] == scope:
                                token = ['identifier', i]
                                tokens.append(token)

                elif integerPattern.match(words):
                    if words not in assignedStatic:
                        symbolTable[staticID] = {'type': 'static', 'name': words, 'scope': scope}
                        token = ['integer', staticID]
                        tokens.append(token)
                        staticID += 4
                        assignedStatic.append(words)

                    else:
                        for i in symbolTable:
                            if symbolTable[i]['name'] == words:
                                token = ['integer', i]
                                tokens.append(token)

                else:
                    print(words + 'did not match any identifier/integer')


def send_next_token():
    data = tokens[0]
    del tokens[0]
    return data



