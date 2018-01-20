import fileinput
import re

reservedWords = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
                 'return', 'boolean', 'int', 'if', 'else', 'while', 'for', 'System.out.println', '.',
                 'true', 'false', '&&', '==', '<', '>', '-', '*', '+', '//', '/*', '*/', ',', '=']

tokens = []

symbolTable = []

flag = False

with open('test.txt') as test:
    lines = test.readlines()

id = -1

for line in lines:
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
                    dict = {words}
                    tokens.append(dict)

            elif len(words) == 1:
                letterPattern = re.compile('[A-Za-z]')
                digitPattern = re.compile('[0-9]')
                id = id + 1

                if letterPattern.match(words):
                    dict = {'letter': id}
                    tokens.append(dict)
                    symbolTable.append(words)
                elif digitPattern.match(words):
                    dict = {'digit': id}
                    tokens.append(dict)
                    symbolTable.append(words)
                else:
                    print(words + "did not match any")


            else:
                id = id + 1
                identifierPattern = re.compile('[A-Za-z]([A-Za-z]|[0-9])+')
                integerPattern = re.compile('[0-9]+')

                if identifierPattern.match(words):
                    dict = {'identifier': id}
                    tokens.append(dict)
                    symbolTable.append(words)

                elif integerPattern.match(words):
                    dict = {'integer': id}
                    tokens.append(dict)
                    symbolTable.append(words)


def sendNextToken():
    data = [symbolTable, tokens[0]]

    del tokens[0]

    return data
