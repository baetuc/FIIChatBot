"""
Modul creat de Moisii Cosmin grupa 3A5

Server
"""


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import httplib,socket, urllib
import simplejson
def get_sentiment(text):
    """params = urllib.urlencode({'text': text})
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    conn = httplib.HTTPConnection("http://text-processing.com:80")
    conn.request("POST", "/api/sentiment/", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
     data = response.read()
    conn.close()"""
    params = urllib.urlencode({'text': text})
    f = urllib.urlopen("http://text-processing.com/api/sentiment/", params)
    data = f.read()
    return data

#data = get_sentiment("this was a great night")
"""data = dict(data)
print(data)"""



class myHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    # Handler for the GET requests

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World !")
        return

    def do_POST(self):
        self._set_headers()
        print "in post method"
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = simplejson.loads(self.data_string)
        text=data["text"]
        keywords=data["keywords"]
        message=dict()
        message['message']=generate_output(text,keywords)
        # proceseaza datele
        pass

        try:
            s2.send(message)
        except socket.error:
            print "Failed to send data."
        return
# decomenteaza pt server


PORT_NUMBER = 8080

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(("127.0.0.1", 2222))

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
