from bottle import request, post, run, route
import json
import Topic

@route('/topic', method = 'POST')
def handle_topic():
    data = request.json
    for sentence in data["sentences"]:
        result = Topic.get_text_topics(sentence["sentence"])

        sentence["topic"] = result[0]["category"]
        sentence["subtopic"] = result[0]["subcategory"]

    return data
# @route('/emoticon', method = 'POST')
# def handle_emoticon():

run(host="localhost", port=2500)