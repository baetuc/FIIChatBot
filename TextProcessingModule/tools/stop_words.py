"""
    Au participat: Munteanu Bogdan

        Changelog
    Version1.1
    - added special words which should never be seen as stop words

    Version1.2
    - refactoring operations
"""
from nltk.corpus import stopwords


def remove_stop_words(input_text):
    other_words = ['what', 'where', 'when', 'who', 'why', 'how', 'not', 'i', 'me', 'we', 'us',
                   'you', 'she', 'her', 'he', 'him', 'it', 'they', 'them', 'that', 'which', 'who',
                   'whom', 'whose', 'whichever', 'whoever', 'whomever', 'my', 'your', 'his', 'her',
                   'its', 'our', 'your', 'their', 'mine', 'yours', 'hers', 'ours', 'yours',
                   'theirs']
    output_text = list()

    for tpl in input_text:
        if tpl[0] in other_words:
            output_text.append(tpl)
        elif tpl[0] not in (stopwords.words('english')):
            output_text.append(tpl)

    return output_text
