"""
    Modulul procesare-text v1.0

    Ghid de instalare:
    instaleaza python3.x
    pip install -U nltk
    python -c "import nltk; nltk.download('all')"
    pip install -U textblob
"""

from tools.spell_checker import correct
from tools.sentence_splitter import split_sentences
from tools.type_detector import detect_type
from tools.parser import process_sentence
from tools.synonym_finder import get_synonyms
from tools.stop_words import remove_stop_words


def correct_text(user_input):
    user_input = user_input.lower()
    user_input = correct(user_input)

    return user_input


def process_text(user_input):
    """
        Processes the input and returns a list of dictionaries, one for each sentence, with the
        following structure:
        output = {
            "sentence": the original sentence
            "type": type of sentence (statement, question or exclamation)
            "is_negation": "true" if sentence is a negation, "false" otherwise
            "words": contains a list of tuples, each tuple representing a word/idiom, it's part
                of speech and a tuple of synonyms
        }
    :param user_input: a string representing the user's input
    :return: output: a dictionary object
    """

    # prepare sentences for processing
    sentences = split_sentences(user_input)

    # start building output
    output = dict()

    # add number of sentences
    output["number_of_sentences"] = str(len(sentences))

    # start adding data for each sentence
    sentences_output = list()
    for sentence in sentences:
        sentence_data = dict()

        # add original sentence
        sentence_data["sentence"] = sentence

        # add sentence type
        sentence_type, is_negation = detect_type(sentence)
        sentence_data["type"] = sentence_type
        if is_negation is True:
            sentence_data["is_negation"] = "true"
        else:
            sentence_data["is_negation"] = "false"

        # parse sentence, removing stop words and generating synonyms
        words = process_sentence(sentence)
        words = remove_stop_words(words)
        words = get_synonyms(words)

        # prepare words for output
        aux = list()
        for item in words:
            # replace "_" with " " in idioms and synonyms
            sanitized_synonyms = list()
            for synonym in item[2]:
                sanitized_synonyms.append(synonym.replace("_", " "))
            sanitized_word = item[0].replace("_", " ")

            # build information dictionary for current word
            word_info = dict()
            word_info["word"] = sanitized_word
            word_info["part_of_speech"] = item[1]
            word_info["synonyms"] = sanitized_synonyms

            # add built dictionary to words list
            aux.append(word_info)

        # add result into dictionary
        sentence_data["words"] = aux

        # add sentence information to output
        sentences_output.append(sentence_data)

    output["sentences"] = sentences_output
    return output
