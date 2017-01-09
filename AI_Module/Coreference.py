from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
input_sentence = "I like the movies with Johhny Depp. They are nice ."

history = []
MAX_HISTORY_BUFFER_SIZE = 5


def resolution_last_message(message):
    message = str(message)
    print('###',message)
    res = nlp.annotate(message,
                       properties={
                           'annotators': 'coref',
                           'outputFormat': 'json'
                       })

    result = message
    for coreferences in res["corefs"].values():
        for item in coreferences:
            if item["isRepresentativeMention"]:
                representative = item["text"]

        for item in coreferences:
            if item["sentNum"] == len(res["sentences"]):
                # Item is in the last sentence
                tokens = res["sentences"][-1]["tokens"]
                for tokens_id in range(item["startIndex"] - 1, item["endIndex"] - 1):
                    try:
                        del tokens[tokens_id]
                    except:
                        print (tokens_id)

                if representative is not None:
                    tokens.insert(item["startIndex"] - 1, {"originalText": representative})

    last_sentence = ""

    for index, message in enumerate(res["sentences"]):
        for token in message["tokens"]:
            if index == len(res["sentences"]) - 1:
                last_sentence += (token["originalText"] + " ")

    return last_sentence


def coreference_resolution(message):
    if not (message.endswith(".") or message.endswith("?") or message.endswith("!")):
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
        for token in sentence["tokens"]:
            sentences += (token["originalText"] + " ")
        resolution = resolution_last_message(sentences)
        result += resolution
        sentences += resolution

    history.append(result)

    return result