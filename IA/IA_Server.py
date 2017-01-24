from bottle import request, post, run, route
import json
import Topic
from Generate_Question_Based_on_Topic import generate_question_based_on_topic
topic = None
subtopic = None

@route('/topic', method = 'POST')
def handle_topic():
    data = request.json
    if "generate_question" in data.keys() and data["generate_question"]=='true':
        return generate_question_based_on_topic(topic,subtopic)
    for sentence in data["sentences"]:
        try:
            result = Topic.get_text_topics(sentence["sentence"])

            sentence["topic"] = result[0]["category"]
            topic = result[0]["category"]
            sentence["subtopic"] = result[0]["subcategory"]
            subtopic = result[0]["subcategory"]
        except Exception:
            sentence["topic"] = "random"
            sentence["subtopic"] = "random"

    return data
# @route('/emoticon', method = 'POST')
# def handle_emoticon():

run(host="localhost", port=2500)