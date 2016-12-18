"""
    Autori: Bogdan Stefan
"""

from nltk import data


def split_sentences(text):
    """ Returns a list of sentences found in the input parateter "text"."""
    sentence_detector = data.load("tokenizers/punkt/english.pickle")
    sentences = sentence_detector.tokenize(text.strip())
    return sentences
