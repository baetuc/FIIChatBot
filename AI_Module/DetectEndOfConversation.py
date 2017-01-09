"""
    Autor: Dan Nastasa

        Changlog
    Version 1.0
    - first implementation
"""

import string

# IMPORTANT: If you add more endings, make sure they are lowercase
basicEndings = ["bye","goodbye", "ciao", "cya", "later", "adio", "sayonara", "servus", "farewell", "adios",
                "peace out", "so long", "have a good one", "see you later", "talk to you later", "bye bye",
                "take care", "have a good day", "see you later", "see you next time", "im out"]

def isEndOfConversation(prop):
    eliminatePunctuation = str.maketrans({key: None for key in string.punctuation})

    parsedProp = prop.translate(eliminatePunctuation)
    parsedProp = parsedProp.replace(" ", "")

    for phrase in basicEndings:
        checkString = phrase.replace(" ", "")

        if checkString == parsedProp.lower():
            return True
        if parsedProp.startswith(checkString):
            return True
        if parsedProp.endswith(checkString):
            return True

    return False

# print (isEndOfConversation("Goodbye! Im gonna go now. See you later!!"))
