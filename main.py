from utils import Type, lex_java_file

tokens = lex_java_file("DiceGame.java")

for token in tokens:
    if token.type not in [Type.SPACE, Type.NEW_LINE]:
        print(token)

print(len(tokens))
