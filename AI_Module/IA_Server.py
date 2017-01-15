from bottle import request, post, run, route
import json
import Topic
import Coreference
import jargon_expand
import DetectEndOfConversation


@route('/slang_and_coreference', method='POST')
def handle_slang_and_coreference():
    after_jargon = jargon_expand.jargon_change(request.json["input"])
    smth = Coreference.coreference_resolution(after_jargon)
    print('####',smth)
    return smth
    # return after_jargon

@route('/topic_and_end', method='POST')
def handle_topic_and_end():
    data = request.json
    is_end = False

    for sentence in data["sentences"]:
        add_topic(sentence)
        if DetectEndOfConversation.isEndOfConversation(sentence["sentence"]):
            is_end = True

    data["is_end"] = str(is_end)
    return data


def add_topic(sentence):
    result = Topic.get_text_topics(sentence["sentence"])
    sentence["topic"] = result[0]["category"]
    sentence["subtopic"] = result[0]["subcategory"]


run(host="localhost", port=2500)
