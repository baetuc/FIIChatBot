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


def process_text(user_input):
    """
        Processes the input and returns a list of dictionaries, one for each sentence, with the
        following structure:
        output = {
            "sentence": the original sentence
            "type": type of sentence (statement, question or exclamation)
            "is_negation": True if sentence is a negation, False otherwise
            "words": contains a list of tuples, each tuple representing a word/idiom, it's part
                of speech and a tuple of synonyms
        }
    :param user_input: a string representing the user's input
    :return: output: a dictionary object
    """

    # prepare sentences for processing
    user_input = user_input.lower()
    user_input = correct(user_input)
    sentences = split_sentences(user_input)

    output = list()
    for sentence in sentences:
        sentence_data = dict()
        sentence_data["sentence"] = sentence

        # detect sentence type
        sentence_type, is_negation = detect_type(sentence)
        sentence_data["type"] = sentence_type
        sentence_data["is_negation"] = is_negation

        # parse sentence
        words = process_sentence(sentence)

        # eliminarea stop words
        words = remove_stop_words(words)

        # generate synonyms for each word
        words = get_synonyms(words)

        # do some final retouching
        final_words = list()
        for item in words:
            # replace "_" with " " in synonyms
            final_synonyms = list()
            for synonym in item[2]:
                final_synonyms.append(synonym.replace("_", " "))

            # build final words list replacing "_" with " " for each idiom
            final_words.append((item[0].replace("_", " "), item[1], tuple(final_synonyms)))

        # add result into dictionary
        sentence_data["words"] = final_words
        output.append(sentence_data)

    return output
