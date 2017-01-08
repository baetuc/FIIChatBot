from bottle import request, post, run, route
import json
import text_processing


@route('/processor', method='POST')
def handle_processing():
    return text_processing.process_text(request.json["input"])


run(host="localhost", port=9020)
