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
                key = key.rstrip().lstrip()
                value = value.lstrip().lstrip()
                items[key] = value
    else:
        # single argument
        if "=" in path:
            key, value = path.split("=")
            key = key.rstrip().lstrip()
            value = value.rstrip().lstrip()
            items[key] = value

    if items == dict():
        # no valid arguments found
        return None

    return items


def get_input(arguments):
    """
        Retrieves input from arguments if possible
    :param arguments: http GET arguments
    :return: value of input or None if it does not exist
    """
    if "input" in arguments:
        return arguments["input"]
    return None


def sanitize(text):
    """Used to decode invalid characters from http get requests. WIP"""
    sanitized_text = text.replace("%20", " ")
    sanitized_text = sanitized_text.replace("%27", "\'")
    return sanitized_text


def build_error_report():
    """
        Builds a dictionary to serve as an error message in case something bad happens.
    :return: report: a dictionary with an error message stored in key "exception"
    """
    report = dict()
    report["exception"] = '[TextProcessing] invalid input! Should be "/?input=user\'s input"'
    return report


class TextProcessingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # get arguments from request
        path = sanitize(self.path)
        arguments = parse_url_path(path)
        print(self.path, path)

        # get input if possible
        text = None
        if arguments is not None:
            text = get_input(arguments)

        if text is None:
            # invalid input
            self.send_response(404)
            message = json.dumps(build_error_report())
        else:
            # process input
            self.send_response(200)
            message = json.dumps(process_text(text))

        # send http headers
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # send output of text-processing module
        self.wfile.write(bytes(message, "utf8"))
        return


def run(ip="127.0.0.1", port=8081):
    print('[TextProcessing] starting server...')
    server_address = (ip, port)
    httpd = HTTPServer(server_address, TextProcessingHandler)
    print('[TextProcessing] running server at {}:{}'.format(ip, port))
    httpd.serve_forever()


# run("127.0.0.1", 8081)
