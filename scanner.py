import re

reservedWords = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
                 'return', 'boolean', 'System.out.println', 'int', 'if', 'else', 'while', 'for',
                 'true', 'false', '&&', '==', '<', '>', '+=', '-', '*', '+', '//', '/*', '*/', ',', '=', '.']

tokens = []
symbolTable = []
reservedSymbolTable = []

flag = False

with open('test.txt') as test:
    lines = test.readlines()

id = 0
ID = 499

for line in lines:
    print("------")
    print(line)
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

    print(line)
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

                else:
                    array = [words, id]
                    tokens.append(array)
                    reservedSymbolTable.append(words)
                    id = id + 1

            elif words == 'SOT':
                array = ['System.out.println', id]
                tokens.append(array)
                reservedSymbolTable.append('System.out.println')
                id = id + 1

            elif words == 'EQEQ':
                array = ['==', id]
                tokens.append(array)
                reservedSymbolTable.append('==')
                id = id + 1

            elif len(words) == 1:
                letterPattern = re.compile('[A-Za-z]')
                digitPattern = re.compile('[0-9]')
                ID = ID + 1

                if letterPattern.match(words):
                    array = ['identifier', ID]
                    tokens.append(array)
                    symbolTable.append(words)
                elif digitPattern.match(words):
                    array = ['integer', ID]
                    tokens.append(array)
                    symbolTable.append(words)
                else:
                    print(words + "did not match any")

            else:
                ID = ID + 1
                identifierPattern = re.compile('[A-Za-z]([A-Za-z]|[0-9])+')
                integerPattern = re.compile('[0-9]+')

                if identifierPattern.match(words):
                    array = ['identifier', ID]
                    tokens.append(array)
                    symbolTable.append(words)

                elif integerPattern.match(words):
                    array = ['integer', ID]
                    tokens.append(array)
                    symbolTable.append(words)


def send_next_token():
    data = [tokens[0]]

    del tokens[0]

    return (data)
