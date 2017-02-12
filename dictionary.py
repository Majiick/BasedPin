from random import choice

nouns = [line.rstrip('\n') for line in open('C:\\Users\\Ecoste\\PycharmProjects\\BasedPin\\dictionary\\nouns.txt')]
adjectives = [line.rstrip('\n') for line in open('C:\\Users\\Ecoste\\PycharmProjects\\BasedPin\\dictionary\\adjectives.txt')]


def get_string():
    return ''.join([choice(adjectives).capitalize(), choice(adjectives).capitalize(), choice(nouns).capitalize()])
