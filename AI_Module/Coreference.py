from pycorenlp import StanfordCoreNLP
import re

nlp = StanfordCoreNLP('http://localhost:9000')
input_sentence = "I like the movies with Johhny Depp. Do you like him?"

history = []
MAX_HISTORY_BUFFER_SIZE = 5


def resolution_last_message(message):
    message = str(message)
    res = nlp.annotate(message,
                       properties={
                           'annotators': 'coref',
                           'outputFormat': 'json'
                       })

    result = message
    for coreferences in res["corefs"].values():
        for item in coreferences:
            if item["isRepresentativeMention"]:
                representative = res["sentences"][item["sentNum"] - 1]["tokens"][
                                 item["startIndex"] - 1:item["endIndex"] - 1]

        for item in coreferences:
            if item["sentNum"] == len(res["sentences"]):
                if item["text"].lower() in ["you", "i", "me", "my", "myself", "mine", "yourself", "yours", "your"]:
                    continue
                # Item is in the last sentence
                tokens = res["sentences"][-1]["tokens"]
                del tokens[item["startIndex"] - 1:item["endIndex"] - 1]

                if representative is not None:
                    index = item["startIndex"] - 1
                    for element in representative:
                        tokens.insert(index, element)
                        index += 1

    last_sentence = ""

    for index, message in enumerate(res["sentences"]):
        for token in message["tokens"]:
            if index == len(res["sentences"]) - 1:
                last_sentence += (token["originalText"] + " ")

    return last_sentence


def coreference_resolution(message):
    try:
        # if not (message.endswith(".") or message.endswith("?") or message.endswith("!")):
        #     message += ""

        if re.match(".*[\w]$", message):
            message += "."

        if len(history) == MAX_HISTORY_BUFFER_SIZE:
            del history[0]

        res = nlp.annotate(message,
                           properties={
                               'annotators': 'coref',
                               'outputFormat': 'json'
                           })

        sentences = "".join(history)
        result = ""

        for sentence in res["sentences"]:
            copy_sentences = sentences
            for token in sentence["tokens"]:
                copy_sentences += (token["originalText"] + " ")
            resolution = resolution_last_message(copy_sentences)
            result += resolution
            sentences += resolution

        history.append(result)
        return result

    except Exception:
        history.append(message)
        return message

# print(coreference_resolution("Do you like Michael Jackson? I like him."))
# print(coreference_resolution("He always gives me ice cream."))
# print(coreference_resolution("Also he likes girls"))
# print(coreference_resolution("They are hot"))
# print(coreference_resolution("I remember World War II."))
# print(coreference_resolution("It was cruel."))

# print(coreference_resolution("Who is the president of Romania?"))
# print(coreference_resolution("He is Klaus Johannis"))
# print(coreference_resolution("And how old is he?"))