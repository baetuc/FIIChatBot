from bottle import request, post, run, route
import json
import Topic

@route('/topic', method = 'POST')
def handle_topic():
    data = request.json
    for sentence in data["sentences"]:
        try:
            result = Topic.get_text_topics(sentence["sentence"])

            sentence["topic"] = result[0]["category"]
            sentence["subtopic"] = result[0]["subcategory"]
        except Exception:
            sentence["topic"] = "random"
            sentence["subtopic"] = "random"

    return data
# @route('/emoticon', method = 'POST')
# def handle_emoticon():

run(host="localhost", port=2500)