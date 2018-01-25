import fileinput
import re

reservedWords = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
                 'return', 'boolean', 'int', 'if', 'else', 'while', 'for', 'System.out.println', '.',
                 'true', 'false', '&&', '==', '<', '>', '-', '*', '+', '//', '/*', '*/', ',', '=' , '+=']

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
            print(Terminal)
            print(len(Terminal))
            print(line.index(Terminal))

            if line.index(Terminal) == 0:
                line = line[:len(Terminal)] + ' ' + line[len(Terminal):]

            else:
                line = line[:line.index(Terminal)]+ ' ' + line[line.index(Terminal):]
                line = line[:line.index(Terminal)+len(Terminal)] + ' ' + line[line.index(Terminal)+len(Terminal):]


    print(line)
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

                else:
                    array = [words, id]
                    tokens.append(array)
                    reservedSymbolTable.append(words)
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
                    tokens.append(dict)
                    symbolTable.append(words)


def sendNextToken():
    data = [tokens[0]]

    del tokens[0]
    print(data)


print(symbolTable)
print(reservedSymbolTable)

sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
sendNextToken()
