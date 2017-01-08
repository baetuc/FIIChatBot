"""
    Autori: Ilinca Roman, Catalina Jijiie, Tudor Timofte


            Changelog:
    Version 1.1
    - lots of refactoring
    - removed unnecessary line in function "detect_question"
    TODO: fix function "detect_negation"
"""

import re


# detect question
def detect_question(input_string):
    if re.search("((!)*(\?)+)+", input_string):
        return "question"
    elif re.search("^(when|where|why|how|who|whom)", input_string.lower()):
        return "question"
    else:
        return -1


# detect exclamation
def detect_exclamation(input_string):
    stringLength = len(input_string)
    if "!" is input_string[stringLength - 1] and detect_question(input_string) == -1:
        return "exclamation"
    else:
        return -1


# detect statement
def detect_statement(input_string):
    if detect_question(input_string) == -1 and detect_exclamation(input_string) == -1:
        return "statement"
    else:
        return -1


# detect negation
def detect_negation(input_string):
    if re.search('(?:\s+|$)no(?i)(?:\s+|$)', input_string) \
            or re.search('^no(?i)(?:\s+|$)', input_string) \
            or re.search('(?:\s+|$)not(?i)(?:\s+|$)', input_string) \
            or re.search('^not(?i)(?:\s+|$)', input_string):
        return True
    else:
        return False


# detect input
def detect_type(input_string):
    is_negation = detect_negation(input_string)

    if detect_statement(input_string) != -1:
        sentence_type = detect_statement(input_string)
    elif detect_question(input_string) != -1:
        sentence_type = detect_question(input_string)
    else:
        sentence_type = detect_exclamation(input_string)

    return sentence_type, is_negation
