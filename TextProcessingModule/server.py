"""
    Autori: Bogdan Stefan
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from text_processing import process_text
import json


def parse_url_path(path):
    """Returns a dictionary containing http arguments"""
    # check path validity
    if len(path) < 2 or path[1] != "?":
        # invalid path, return None
        return None
    else:
        # valid path, get rid of starting characters "/?"
        path = path[2:]

    items = dict()

    # check for multiple arguments
    arguments = None
    if "&" in path:
        arguments = path.split("&")

    if arguments is not None:
        # multiple arguments, parse each one
        for arg in arguments:
            if "=" in arg:
                key, value = arg.split("=")
                items[key] = value
    else:
        # single argument
        if "=" in path:
            key, value = path.split("=")
            items[key] = value

    if items == dict():
        # no valid arguments found
        return None

    return items


def get_input(arguments):
    if "input" in arguments:
        return arguments["input"]
    return None


def sanitize(text):
    return text.replace("%20", " ")


def build_error_report():
    report = dict()
    report["exception"] = "[TextProcessing] invalid input! Should be '/?input=user's input'"
    return report


class TextProcessingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # get arguments from request
        arguments = parse_url_path(self.path)

        # get input if possible
        text = None
        if arguments is not None:
            text = get_input(arguments)
            text = sanitize(text)

        if text is None:
            # invalid input
            self.send_response(404)
            message = json.dumps(build_error_report())
        else:
            # process input
            self.send_response(200)
            message = json.dumps(process_text(text))

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return


def run(ip="127.0.0.1", port=8081):
    server_ip = ip
    server_port = port

    print('[TextProcessing] starting server...')
    server_address = (server_ip, server_port)
    httpd = HTTPServer(server_address, TextProcessingHandler)
    print('[TextProcessing] running server...')
    httpd.serve_forever()


run("127.0.0.1", 8081)
