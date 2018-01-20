import fileinput
import re

# create an array for reserved words

reservedWords = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '()', '}', 'extends', ';', '(', ')',
                 'return', 'boolean', 'int', 'if', 'else', 'while', 'for', 'System.out.println', '.',
                 'true', 'false', '&&', '==', '<', '-', '*', '+', '//', '/*', '*/']

tokens = []

with open('test.txt') as test:
    lines = test.readlines()

for line in lines:

    wordsInLine = line.split()
    for words in wordsInLine:
        if words in reservedWords:
            # dict = {words: reservedWords.index(words)}
            dict = {words : 'reservedWord'}
            tokens.append(dict)

        elif len(words) == 1:
            letterPattern = re.compile('[A-Za-z]')
            digitPattern = re.compile('[0-9]')

            if letterPattern.match(words):
                dict = {words : 'letter'}
                tokens.append(dict)
            elif digitPattern.match(words):
                dict = {words : 'digit'}
                tokens.append(dict)
            else:
                print(words + "did not match any")


        else:
            identifierPattern = re.compile('[A-Za-z]([A-Za-z]|[0-9])+')
            integerPattern = re.compile('[0-9]+')

            if identifierPattern.match(words):
                dict = {words : 'identifier'}
                tokens.append(dict)

            elif integerPattern.match(words):
                dict = {words : 'integer'}
                tokens.append(dict)




for token in tokens:
    print(token)
