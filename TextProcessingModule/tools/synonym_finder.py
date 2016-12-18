"""
    Autori: Codrin Pascal, Dan Nastasa

        Changlog
    Version 2.0
    - rework of whole module

    Version 2.1
    - limited number of generated synonyms to 3
    - synonyms are now stored in a tuple instead of a list
"""

from nltk.corpus import wordnet as wn


def getFirst3SynonymsForWord(wordTuple):
    synonyms = []
    counter = 0
    for syn in wn.synsets(wordTuple[0]):
        for l in syn.lemmas():
            if l.name() not in synonyms and l.name().lower() != wordTuple[0].lower():
                synonyms.append(l.name())
                counter += 1
            if counter == 3:
                return tuple(synonyms)
    return tuple(synonyms)


def get_synonyms(wordsTupleList):
    result = []
    for wordTuple in wordsTupleList:
        word = wordTuple[0]
        part_of_speech = wordTuple[1]

        wordWithSynonyms = []
        wordWithSynonyms.append(word)
        wordWithSynonyms.append(part_of_speech)
        wordWithSynonyms.append(getFirst3SynonymsForWord(wordTuple))

        wordTuple = tuple(wordWithSynonyms)
        result.append(wordTuple)

    return result
