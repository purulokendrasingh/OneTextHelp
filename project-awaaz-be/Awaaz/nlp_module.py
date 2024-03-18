import nltk
from nltk.corpus import wordnet


def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
    person_list = []
    person_names = person_list
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

        for person in person_list:
            person_split = person.split(" ")
            for name in person_split:
                if wordnet.synsets(name):
                    if name in person:
                        person_names.remove(person)
                        break

    return person_names
