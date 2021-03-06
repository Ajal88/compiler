from scanner import *
from intermediate_code_generator import *


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ter = ['EOF', 'public', 'class', '{', 'static', 'void', 'main', '(', ')', '}', 'extends', ';',
       'return', ',', 'boolean', 'int', 'if', 'else', 'while', 'for', '=', '+', 'System.out.println', '*',
       'true', 'false', '&&', 'identifier', 'integer', '-', '.', '==', '<', '$']
non_ter = []
action_symbol = []
file = open('grammar.txt', 'r')
file_action = open('grammar_action.txt', 'r')
rules = file.readlines()
actions = file_action.readlines()
a_r = dict()
i = 0
for rule in rules:
    rule = rule.rstrip()
    actions[i] = actions[i].rstrip()
    a_r[rule] = actions[i]
    sp = rule.split(' ')
    ac = actions[i].split(' ')
    for a in ac:
        if a.startswith('#'):
            action_symbol.append(a)
    for s in sp:
        if s == '->':
            break
        if s not in non_ter:
            non_ter.append(s)
    i += 1
i = 0
# first and follow sets
ff = {
    'Goal': {'first': ['public', 'class'], 'follow': ['$']},
    'Source': {'first': ['public', 'class'], 'follow': ['EOF']},
    'MainClass': {'first': ['public'], 'follow': ['EOF']},
    'ClassDeclarations': {'first': ['ℇ', 'class'], 'follow': ['public']},
    'ClassDeclaration': {'first': ['class'], 'follow': ['public', 'class']},
    'Extension': {'first': ['extends', 'ℇ'], 'follow': ['{']},
    'FieldDeclarations': {'first': ['ℇ', 'static'], 'follow': ['public', 'class', '}']},
    'FieldDeclaration': {'first': ['static'], 'follow': ['public', 'class', '}', 'static']},
    'VarDeclarations': {'first': ['ℇ', 'boolean', 'int'],
                        'follow': ['EOF', '{', 'if', 'while', 'for', 'System.out.println', 'identifier', '}',
                                   'public', 'return']},
    'VarDeclaration': {'first': ['boolean', 'int'],
                       'follow': ['EOF', '{', 'if', 'while', 'for', 'System.out.println', 'identifier', '}',
                                  'boolean', 'int', 'public', 'return']},
    'MethodDeclarations': {'first': ['ℇ', 'public'], 'follow': ['}']},
    'MethodDeclaration': {'first': ['public'], 'follow': ['}', 'public']},
    'Parameters': {'first': ['ℇ', 'boolean', 'int'], 'follow': [')']},
    'Parameter': {'first': [',', 'ℇ'], 'follow': [')']},
    'Type': {'first': ['boolean', 'int'], 'follow': ['identifier']},
    'Statements': {'first': ['ℇ', '{', 'if', 'while', 'for', 'System.out.println', 'identifier'],
                   'follow': ['}', 'return']},
    'A': {'first': ['ℇ', '{', 'if', 'while', 'for', 'System.out.println', 'identifier'], 'follow': ['}', 'return']},
    'Statement': {'first': ['{', 'if', 'while', 'for', 'System.out.println', 'identifier'],
                  'follow': ['}', 'return', '{', 'if', 'while', 'for', 'System.out.println', 'identifier', 'else']},
    'GenExpression': {'first': ['(', 'true', 'false', 'identifier', 'integer'], 'follow': [';', ')', ',']},
    'E': {'first': ['ℇ', '==', '<'], 'follow': [';', ')', ',']},
    'Expression': {'first': ['(', 'true', 'false', 'identifier', 'integer'], 'follow': [')', '&&', ';', ',']},
    'B': {'first': ['ℇ', '+', '-'], 'follow': [';', ')', '==', '<', ',', '&&']},
    'Term': {'first': ['(', 'true', 'false', 'identifier', 'integer'],
             'follow': ['+', '-', ';', ')', '==', '<', '&&', ',']},
    'C': {'first': ['*', 'ℇ'], 'follow': [';', ')', '+', '-', '==', '<', '&&', ',']},
    'Factor': {'first': ['(', 'true', 'false', 'identifier', 'integer'],
               'follow': ['*', ';', ')', '+', '-', '==', '<', ',', '&&']},
    'D': {'first': ['&&', 'ℇ'], 'follow': [';', ')', ',']},
    'RelTerm': {'first': ['(', 'true', 'false', 'identifier', 'integer'], 'follow': [';', '&&', ')', ',']},
    'Arguments': {'first': ['false', 'true', '(', 'ℇ', 'integer', 'identifier'], 'follow': [')']},
    'Argument': {'first': [',', 'ℇ'], 'follow': [')']},
    'Identifier': {'first': ['identifier'],
                   'follow': ['{', 'extends', 'public', 'class', ';', '(', ',', ')', '=', '+', '.', '*', '-', '==',
                              '<', '&&']},
    'Integer': {'first': ['integer'], 'follow': [';', ')', '*', '+', '-', '==', '<', '&&', ',']},
    'Expression1': {'first': ['+', '-'], 'follow': [';', ')', '==', '<', '+', '-', ',', '&&']},
    'Factor1': {'first': ['(', 'ℇ'], 'follow': ['*', ';', ')', '+', '-', '==', '<', '&&', ',']},
    'Factor2': {'first': ['.', 'ℇ'], 'follow': ['*', ';', ')', '+', '-', '==', '<', '&&', ',']},
    'RelTerm1': {'first': ['==', '<'], 'follow': ['&&', ';', ')', ',']},
    'Arguments1': {'first': [',', 'ℇ', '==', '<'], 'follow': [')']},
    'Arguments2': {'first': [',', 'ℇ', '==', '<'], 'follow': [')']},
    'Arguments3': {'first': [',', 'ℇ', '==', '<'], 'follow': [')']},
    'Arguments4': {'first': [',', 'ℇ', '==', '<'], 'follow': [')']},
    'Arguments5': {'first': [',', 'ℇ', '==', '<'], 'follow': [')']}}

# parse table
ll1 = {
    'Goal': {'EOF': '-1', 'public': 'Goal -> Source EOF', 'class': 'Goal -> Source EOF', '{': '-1',
             'static': '-1', 'void': '-1', 'main': '-1', '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1',
             'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
             'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1',
             '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1',
             '$': 'Goal -> Source EOF'},
    'Source': {'EOF': 'Source -> ClassDeclarations MainClass', 'public': 'Source -> ClassDeclarations MainClass',
               'class': 'Source -> ClassDeclarations MainClass', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
               '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1',
               'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1',
               'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1', 'identifier': '-1',
               'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'MainClass': {'EOF': '-1',
                  'public': 'MainClass -> public class Identifier { public static void main ( ) { VarDeclarations Statements } }',
                  'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1', ')': '-1', '}': '-1',
                  'extends': '-1', ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1',
                  'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1',
                  'true': '-1', 'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1',
                  '==': '-1', '<': '-1', '$': '-1'},
    'ClassDeclarations': {'EOF': '-1', 'public': 'ClassDeclarations -> \'\'',
                          'class': 'ClassDeclarations -> ClassDeclaration ClassDeclarations', '{': '-1', 'static': '-1',
                          'void': '-1', 'main': '-1', '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1',
                          'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1',
                          'while': '-1', 'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1',
                          'true': '-1', 'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1',
                          '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'ClassDeclaration': {'EOF': '-1', 'public': '-1',
                         'class': 'ClassDeclaration -> class Identifier Extension { FieldDeclarations MethodDeclarations }',
                         '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1', ')': '-1', '}': '-1',
                         'extends': '-1', ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1',
                         'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1',
                         'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
                         'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'Extension': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': 'Extension -> \'\'', 'static': '-1', 'void': '-1',
                  'main': '-1', '(': '-1', ')': '-1', '}': '-1', 'extends': 'Extension -> extends Identifier',
                  ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1',
                  'while': '-1', 'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                  'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1',
                  '<': '-1', '$': '-1'},
    'FieldDeclarations': {'EOF': '-1', 'public': 'FieldDeclarations -> \'\'', 'class': 'FieldDeclarations -> \'\'',
                          '{': '-1', 'static': 'FieldDeclarations -> FieldDeclaration FieldDeclarations', 'void': '-1',
                          'main': '-1', '(': '-1', ')': '-1', '}': 'FieldDeclarations -> \'\'', 'extends': '-1',
                          ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1',
                          'while': '-1', 'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1',
                          'true': '-1', 'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1',
                          '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'FieldDeclaration': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1',
                         'static': 'FieldDeclaration -> static Type Identifier ;', 'void': '-1', 'main': '-1',
                         '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
                         'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1',
                         '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
                         'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'VarDeclarations': {'EOF': 'VarDeclarations -> \'\'', 'public': 'VarDeclarations -> \'\'', 'class': '-1',
                        '{': 'VarDeclarations -> \'\'', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1', ')': '-1',
                        '}': 'VarDeclarations -> \'\'', 'extends': '-1', ';': '-1', 'return': 'VarDeclarations -> \'\'',
                        ',': '-1', 'boolean': 'VarDeclarations -> VarDeclaration VarDeclarations',
                        'int': 'VarDeclarations -> VarDeclaration VarDeclarations', 'if': 'VarDeclarations -> \'\'',
                        'else': '-1', 'while': 'VarDeclarations -> \'\'', 'for': 'VarDeclarations -> \'\'', '=': '-1',
                        '+': '-1', 'System.out.println': 'VarDeclarations -> \'\'', '*': '-1', 'true': '-1',
                        'false': '-1', '&&': '-1', 'identifier': 'VarDeclarations -> \'\'', 'integer': '-1', '-': '-1',
                        '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'VarDeclaration': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1',
                       'main': '-1', '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                       ',': '-1', 'boolean': 'VarDeclaration -> Type Identifier ;',
                       'int': 'VarDeclaration -> Type Identifier ;', 'if': '-1', 'else': '-1', 'while': '-1',
                       'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                       'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1',
                       '<': '-1', '$': '-1'},
    'MethodDeclarations': {'EOF': '-1', 'public': 'MethodDeclarations -> MethodDeclaration MethodDeclarations',
                           'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1', ')': '-1',
                           '}': 'MethodDeclarations -> \'\'', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
                           'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1',
                           '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1',
                           '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1',
                           '$': '-1'},
    'MethodDeclaration': {'EOF': '-1',
                          'public': 'MethodDeclaration -> public static Type Identifier ( Parameters ) { VarDeclarations Statements return GenExpression ; }',
                          'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1', ')': '-1',
                          '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1',
                          'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1',
                          'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
                          'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1',
                          '$': '-1'},
    'Parameters': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': '-1', ')': 'Parameters -> \'\'', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
                   'boolean': 'Parameters -> Type Identifier Parameter',
                   'int': 'Parameters -> Type Identifier Parameter', 'if': '-1', 'else': '-1', 'while': '-1',
                   'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                   'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1',
                   '<': '-1', '$': '-1'},
    'Parameter': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                  '(': '-1', ')': 'Parameter -> \'\'', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                  ',': 'Parameter -> , Type Identifier Parameter', 'boolean': '-1', 'int': '-1', 'if': '-1',
                  'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1',
                  'true': '-1', 'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1',
                  '==': '-1', '<': '-1', '$': '-1'},
    'Type': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
             '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
             'boolean': 'Type -> boolean', 'int': 'Type -> int', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1',
             '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
             'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'Statements': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': 'Statements -> A', 'static': '-1', 'void': '-1',
                   'main': '-1', '(': '-1', ')': '-1', '}': 'Statements -> A', 'extends': '-1', ';': '-1',
                   'return': 'Statements -> A', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': 'Statements -> A',
                   'else': '-1', 'while': 'Statements -> A', 'for': 'Statements -> A', '=': '-1', '+': '-1',
                   'System.out.println': 'Statements -> A', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
                   'identifier': 'Statements -> A', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1',
                   '$': '-1'},
    'A': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': 'A -> Statement A', 'static': '-1', 'void': '-1',
          'main': '-1', '(': '-1', ')': '-1', '}': 'A -> \'\'', 'extends': '-1', ';': '-1', 'return': 'A -> \'\'',
          ',': '-1', 'boolean': '-1', 'int': '-1', 'if': 'A -> Statement A', 'else': '-1', 'while': 'A -> Statement A',
          'for': 'A -> Statement A', '=': '-1', '+': '-1', 'System.out.println': 'A -> Statement A', '*': '-1',
          'true': '-1', 'false': '-1', '&&': '-1', 'identifier': 'A -> Statement A', 'integer': '-1', '-': '-1',
          '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'Statement': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': 'Statement -> { Statements }', 'static': '-1',
                  'void': '-1', 'main': '-1', '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1',
                  'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1',
                  'if': 'Statement -> if ( GenExpression ) Statement else Statement', 'else': '-1',
                  'while': 'Statement -> while ( GenExpression ) Statement',
                  'for': 'Statement -> for ( Identifier = Integer ; RelTerm ; Identifier + = Integer ) Statement',
                  '=': '-1', '+': '-1', 'System.out.println': 'Statement -> System.out.println ( GenExpression ) ;',
                  '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
                  'identifier': 'Statement -> Identifier = GenExpression ;', 'integer': '-1', '-': '-1', '.': '-1',
                  '==': '-1', '<': '-1', '$': '-1'},
    'GenExpression': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                      '(': 'GenExpression -> Factor C B E', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1',
                      'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                      'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1',
                      'true': 'GenExpression -> Factor C B E', 'false': 'GenExpression -> Factor C B E', '&&': '-1',
                      'identifier': 'GenExpression -> Factor C B E', 'integer': 'GenExpression -> Factor C B E',
                      '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'E': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1',
          ')': 'E -> \'\'', '}': '-1', 'extends': '-1', ';': 'E -> \'\'', 'return': '-1', ',': 'E -> \'\'', 'boolean': '-1',
          'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1',
          'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1', 'identifier': '-1',
          'integer': '-1', '-': '-1', '.': '-1', '==': 'E -> RelTerm1 D', '<': 'E -> RelTerm1 D', '$': '-1'},
    'Expression': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': 'Expression -> Term B', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                   ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1',
                   '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': 'Expression -> Term B',
                   'false': 'Expression -> Term B', '&&': '-1', 'identifier': 'Expression -> Term B',
                   'integer': 'Expression -> Term B', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'B': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1',
          ')': 'B -> \'\'', '}': '-1', 'extends': '-1', ';': 'B -> \'\'', 'return': '-1', ',': 'B -> \'\'', 'boolean': '-1',
          'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': 'B -> Expression1 B',
          'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': 'B -> \'\'', 'identifier': '-1',
          'integer': '-1', '-': 'B -> Expression1 B', '.': '-1', '==': 'B -> \'\'', '<': 'B -> \'\'', '$': '-1'},
    'Term': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
             '(': 'Term -> Factor C', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
             'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1',
             'System.out.println': '-1', '*': '-1', 'true': 'Term -> Factor C', 'false': 'Term -> Factor C', '&&': '-1',
             'identifier': 'Term -> Factor C', 'integer': 'Term -> Factor C', '-': '-1', '.': '-1', '==': '-1',
             '<': '-1', '$': '-1'},
    'C': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1',
          ')': 'C -> \'\'', '}': '-1', 'extends': '-1', ';': 'C -> \'\'', 'return': '-1', ',': 'C -> \'\'', 'boolean': '-1',
          'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': 'C -> \'\'',
          'System.out.println': '-1', '*': 'C -> * Factor C', 'true': '-1', 'false': '-1', '&&': 'C -> \'\'',
          'identifier': '-1', 'integer': '-1', '-': 'C -> \'\'', '.': '-1', '==': 'C -> \'\'', '<': 'C -> \'\'', '$': '-1'},
    'Factor': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
               '(': 'Factor -> ( Expression )', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
               ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1',
               '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': 'Factor -> true', 'false': 'Factor -> false',
               '&&': '-1', 'identifier': 'Factor -> Identifier Factor2', 'integer': 'Factor -> Integer', '-': '-1',
               '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'D': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1', '(': '-1',
          ')': 'D -> \'\'', '}': '-1', 'extends': '-1', ';': 'D -> \'\'', 'return': '-1', ',': 'D -> \'\'', 'boolean': '-1',
          'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1',
          'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': 'D -> && RelTerm D',
          'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'RelTerm': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                '(': 'RelTerm -> ( Expression ) C B RelTerm1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1',
                'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1',
                'true': 'RelTerm -> true C B RelTerm1', 'false': 'RelTerm -> false C B RelTerm1', '&&': '-1',
                'identifier': 'RelTerm -> Identifier Factor2 C B RelTerm1',
                'integer': 'RelTerm -> Integer C B RelTerm1', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'Arguments': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                  '(': 'Arguments -> ( Expression ) C B Arguments1', ')': 'Arguments -> \'\'', '}': '-1', 'extends': '-1',
                  ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1',
                  'while': '-1', 'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1',
                  'true': 'Arguments -> true C B Arguments3', 'false': 'Arguments -> false C B Arguments4', '&&': '-1',
                  'identifier': 'Arguments -> Identifier Factor2 C B Arguments2',
                  'integer': 'Arguments -> Integer C B Arguments5', '-': '-1', '.': '-1', '==': '-1', '<': '-1',
                  '$': '-1'},
    'Argument': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                 '(': '-1', ')': 'Argument -> \'\'', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                 ',': 'Argument -> , GenExpression Argument', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1',
                 'while': '-1', 'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                 'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1',
                 '<': '-1', '$': '-1'},
    'Identifier': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
                   'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1',
                   '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
                   'identifier': 'Identifier -> identifier', 'integer': '-1', '-': '-1', '.': '-1', '==': '-1',
                   '<': '-1', '$': '-1'},
    'Integer': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1', 'boolean': '-1',
                'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1', '+': '-1',
                'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1', 'identifier': '-1',
                'integer': 'Integer -> integer', '-': '-1', '.': '-1', '==': '-1', '<': '-1', '$': '-1'},
    'Expression1': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                    '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
                    'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1',
                    '+': 'Expression1 -> + Term', 'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1',
                    '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': 'Expression1 -> - Term', '.': '-1',
                    '==': '-1', '<': '-1', '$': '-1'},
    'Factor1': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                '(': 'Factor1 -> ( Arguments )', ')': 'Factor1 -> \'\'', '}': '-1', 'extends': '-1', ';': 'Factor1 -> \'\'',
                'return': '-1', ',': 'Factor1 -> \'\'', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1',
                'while': '-1', 'for': '-1', '=': '-1', '+': 'Factor1 -> \'\'', 'System.out.println': '-1',
                '*': 'Factor1 -> \'\'', 'true': '-1', 'false': '-1', '&&': 'Factor1 -> \'\'', 'identifier': '-1',
                'integer': '-1', '-': 'Factor1 -> \'\'', '.': '-1', '==': 'Factor1 -> \'\'', '<': 'Factor1 -> \'\'',
                '$': '-1'},
    'Factor2': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                '(': '-1', ')': 'Factor2 -> \'\'', '}': '-1', 'extends': '-1', ';': 'Factor2 -> \'\'', 'return': '-1',
                ',': 'Factor2 -> \'\'', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                'for': '-1', '=': '-1', '+': 'Factor2 -> \'\'', 'System.out.println': '-1', '*': 'Factor2 -> \'\'',
                'true': '-1', 'false': '-1', '&&': 'Factor2 -> \'\'', 'identifier': '-1', 'integer': '-1',
                '-': 'Factor2 -> \'\'', '.': 'Factor2 -> . Identifier Factor1', '==': 'Factor2 -> \'\'',
                '<': 'Factor2 -> \'\'', '$': '-1'},
    'RelTerm1': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                 '(': '-1', ')': '-1', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1', ',': '-1',
                 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1', 'for': '-1', '=': '-1',
                 '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1', 'false': '-1', '&&': '-1',
                 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1', '==': 'RelTerm1 -> == Expression',
                 '<': 'RelTerm1 -> < Expression', '$': '-1'},
    'Arguments1': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': '-1', ')': 'Arguments1 -> Argument', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                   ',': 'Arguments1 -> Argument', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                   'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                   'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1',
                   '==': 'Arguments1 -> RelTerm1 D Argument', '<': 'Arguments1 -> RelTerm1 D Argument', '$': '-1'},
    'Arguments2': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': '-1', ')': 'Arguments2 -> Argument', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                   ',': 'Arguments2 -> Argument', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                   'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                   'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1',
                   '==': 'Arguments2 -> RelTerm1 D Argument', '<': 'Arguments2 -> RelTerm1 D Argument', '$': '-1'},
    'Arguments3': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': '-1', ')': 'Arguments3 -> Argument', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                   ',': 'Arguments3 -> Argument', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                   'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                   'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1',
                   '==': 'Arguments3 -> RelTerm1 D Argument', '<': 'Arguments3 -> RelTerm1 D Argument', '$': '-1'},
    'Arguments4': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': '-1', ')': 'Arguments4 -> Argument', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                   ',': 'Arguments4 -> Argument', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                   'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                   'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1',
                   '==': 'Arguments4 -> RelTerm1 D Argument', '<': 'Arguments4 -> RelTerm1 D Argument', '$': '-1'},
    'Arguments5': {'EOF': '-1', 'public': '-1', 'class': '-1', '{': '-1', 'static': '-1', 'void': '-1', 'main': '-1',
                   '(': '-1', ')': 'Arguments5 -> Argument', '}': '-1', 'extends': '-1', ';': '-1', 'return': '-1',
                   ',': 'Arguments5 -> Argument', 'boolean': '-1', 'int': '-1', 'if': '-1', 'else': '-1', 'while': '-1',
                   'for': '-1', '=': '-1', '+': '-1', 'System.out.println': '-1', '*': '-1', 'true': '-1',
                   'false': '-1', '&&': '-1', 'identifier': '-1', 'integer': '-1', '-': '-1', '.': '-1',
                   '==': 'Arguments5 -> RelTerm1 D Argument', '<': 'Arguments5 -> RelTerm1 D Argument', '$': '-1'}}
# panic mod ll1 changes
for fof in ff.keys():
    for f in ff[fof]['follow']:
        if ll1[fof][f] == '-1':
            ll1[fof][f] = 'synch'

# replace ll1 table with action rules
for key in a_r.keys():
    for nt in non_ter:
        for item in ll1[nt].keys():
            if ll1[nt][item] == key:
                ll1[nt][item] = a_r[key]

# parsing chapter
stack = ['$', 'Goal']
next_token = True
top_stack = stack.pop()
while top_stack != '$':
    if next_token:
        last_token = send_next_token()
        print(last_token)
        token = last_token[0]
        # print(token)
        next_token = False
    if top_stack in ter:
        if top_stack == token:
            top_stack = stack.pop()
            next_token = True
            # print(stack)
        else:
            if stack.__len__() > 2:
                next_token = True
            print(Color.WARNING + 'Warning: ' + top_stack + ' is missed! I add it!' + Color.ENDC)
            top_stack = stack.pop()
    elif top_stack in non_ter:
        if ll1[top_stack][token] != '-1':
            rl = ll1[top_stack][token].split(' -> ')
            for r in reversed(rl[1].split(' ')):
                if r != '\'\'':
                    stack.append(r)
            # print(stack)
        elif ll1[top_stack][token] == 'synch':
            print(Color.WARNING + 'Warning: ' + top_stack + ' popped from stack!' + Color.ENDC)
        else:
            print(Color.WARNING + 'Warning: ' + token + ' skipped from input!' + Color.ENDC)
            next_token = True
        top_stack = stack.pop()
    elif top_stack in action_symbol:
        top_stack = top_stack.replace('#', '')
        print(top_stack)
        code_gen(top_stack, symbolTable, last_token)
        # print(stack)
        top_stack = stack.pop()

# create output file
o = ''
for p in sorted(PB.keys()):
    o += str(PB[p]) + '\n'

out = open('out.txt', 'w')
out.write(o)
