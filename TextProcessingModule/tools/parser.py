"""
    Autori: Cip Baetu, Sebastian Ciobanu
"""

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import MWETokenizer

contractions = {}
with open("assets/english_contractions.txt", "r") as f:
    for line in f:
        contraction, long_form = line.strip().split(" --- ")
        contractions[contraction] = long_form

mwe_list = []
mwe_to_pos = {}

with open("assets/mwe_words.txt", "r") as f:
    for mwe_pos in f:
        mwe, pos = mwe_pos.strip().split(" ")
        mwe_to_pos[mwe] = pos
        mwe_list.append(tuple(mwe.split("_")))

punctuation_marks = [".", "?", "!", ":", ";", "-", "(", ")", "[", "]", "...", "\"", ","]

lemmatizer = WordNetLemmatizer()


############# Start processing single sentence ####################

def replace_contractions(sentence):
    for contraction, long_form in contractions.items():
        sentence = sentence.replace(contraction, long_form)
    return sentence


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def recognise_expressions(tagged):
    for index, tag in enumerate(tagged):
        if get_wordnet_pos(tag[1]) == wordnet.VERB:
            del tagged[index]
            tagged.insert(index, (lemmatizer.lemmatize(tag[0], wordnet.VERB), wordnet.VERB))

    words = [word for (word, pos) in tagged]

    tokenizer = MWETokenizer(mwe_list)
    words = tokenizer.tokenize(words)
    return pos_tag(words)


def retag_pos(tagged):
    for index, tag in enumerate(tagged):
        del tagged[index]
        if "_" in tag[0]:
            tagged.insert(index, (tag[0], mwe_to_pos[tag[0]]))
            continue

        pos = get_wordnet_pos(tag[1])
        if pos != '':
            tagged.insert(index, (lemmatizer.lemmatize(tag[0], pos), tag[1]))
        else:
            tagged.insert(index, (tag[0], tag[1]))


def postprocess(result):
    for index, (word, pos) in enumerate(result):
        if word == "n't":
            del result[index]
            result.insert(index, ("not", pos))


def delete_punctuations(result):
    for index, (word, pos) in enumerate(result):
        if word in punctuation_marks:
            del result[index]


def process_sentence(sentence):
    sentence = replace_contractions(sentence)
    tagged = pos_tag(word_tokenize(sentence))
    new_tagged = recognise_expressions(tagged)
    retag_pos(new_tagged)
    delete_punctuations(new_tagged)

    postprocess(new_tagged)
    return new_tagged
