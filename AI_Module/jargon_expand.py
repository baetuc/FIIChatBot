dictionary = dict()
with open('jargon_dictionary.txt') as f:
    for line in f:
        list = line.split('#')
        dictionary[list[0]] = list[1]


from nltk import word_tokenize
from nltk import data


def jargon_change(sentences):
    result = ""

    for sentence in split_sentences(sentences):
        tagged = word_tokenize(sentence)
        for word in tagged:
            result += jargon_expand(word) + " "

    return result


def split_sentences(text):
    """ Returns a list of sentences found in the input parateter "text"."""
    sentence_detector = data.load("tokenizers/punkt/english.pickle")
    sentences = sentence_detector.tokenize(text.strip())
    return sentences


def jargon_expand(word):
    # print(dictionary)
    if word.upper() in dictionary.keys():
        return dictionary.get(word.upper()).replace("\n", "")
    else:
        return word
