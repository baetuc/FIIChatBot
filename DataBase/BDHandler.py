import simplejson
import json
import searchWeb
import AIML
import Ontologii
from what_why import FavoriteHandler

# my_data = {
#     "number_of_sentences": "1",
#     "sentences": [
#       {
#         "is_negation": "false",
#         "topic": "Arts & Entertainment",
#         "words": [
#           {
#             "part_of_speech": "WP",
#             "synonyms": [
#               "World Health Organization"
#             ],
#             "word": "who"
#           },
#           {
#             "part_of_speech": "N",
#             "synonyms": [
#               "Jackson",
#               "Michael Joe Jackson"
#             ],
#             "word": "michael jackson"
#           }
#         ],
#         "subtopic": "music",
#         "sentence": "Tell me a joke with chuck norris",
#         "type": "question"
#       }
#     ],
#     "is_end": "False"
#   }
#
# my_data2 = {
#     "number_of_sentences": "1",
#     "sentences": [
#       {
#         "is_negation": "false",
#         "topic": "Arts & Entertainment",
#         "words": [
#           {
#             "part_of_speech": "WP",
#             "synonyms": [
#               "World Health Organization"
#             ],
#             "word": "who"
#           },
#           {
#             "part_of_speech": "N",
#             "synonyms": [
#               "Jackson",
#               "Michael Joe Jackson"
#             ],
#             "word": "michael jackson"
#           }
#         ],
#         "subtopic": "music",
#         "sentence": "why is red your favourite color?",
#         "type": "question"
#       }
#     ],
#     "is_end": "False"
#   }

handler = FavoriteHandler()

def init(data):
    global handler

    response= []
    numberS = int(data["number_of_sentences"])
    responsServ = " "
    responsetopic=None
    responseOntologii = None

    for index in range(numberS):
        sentences = data["sentences"][index]
        sentence = sentences["sentence"]
        type = sentences["type"]
        is_negation = sentences["is_negation"]
        words = sentences["words"]
        topic = sentences["topic"].lower()
        subtopic = sentences["subtopic"].lower()

        Ontologii.jsonConverterAndInserter(data)

        print 'AIML'

        responseAIML = None
        if handler.is_why_question(sentence):
            responseAIML = handler.answer_why(sentence)

        elif handler.is_favorite_question(sentence):
            responseAIML = handler.answer_what(sentence)

        if responseAIML is None:
            responseAIMLsentence = AIML.getResponse(sentence)
        else:
            responseAIMLsentence = 'I have no answer for that.'


        print 'AIML topic'

        if responseAIMLsentence != 'I have no answer for that.':
            responseAIML = responseAIMLsentence

        responsetopic=None

        if responseAIML is None:
            responseAIMLtopic = AIML.getResponseForTopic(topic)
            responseAIMLsubtopic = AIML.getResponseForTopic(subtopic)

            if responseAIMLtopic != 'I have no answer for that.':
                responsetopic = responseAIMLtopic
            else:
                if responseAIMLsubtopic != 'I have no answer for that.':
                    responsetopic = responseAIMLsubtopic
                else:
                    responsetopic = None

        print 'web'

        responseWeb = None
        if responseAIML is None:
            gooAnswer = searchWeb.get_google_answer(sentence)

            if gooAnswer is not None:
                responseWeb = gooAnswer
            else:
                gooAnswerSumm = searchWeb.get_google_summary(sentence)
                if gooAnswerSumm is not None:
                    responseWeb = gooAnswerSumm
                else:
                    try:
                        wikiAnswer = searchWeb.Wiki(sentence)
                    except:
                        wikiAnswer = None

                    if wikiAnswer:
                        responseWeb = wikiAnswer
                    else:
                        responseWeb  = None


        print 'ont'

        responseOntologii = None
        responseOntologiiTopic = Ontologii.getWords(topic, subtopic)
        if responseOntologiiTopic is not None:
            responseOntologii = responseOntologiiTopic

        r = {"question":sentence, "AIML":responseAIML, "WEB":responseWeb}
        response.insert(index, r);


    dictionaryToJson = json.dumps({"response":response, "ontologii": responseOntologii, "topic": responsetopic})

    return dictionaryToJson

# print(init(my_data))
# print(init(my_data2))
