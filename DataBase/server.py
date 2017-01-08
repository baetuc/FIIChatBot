
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import httplib,socket, urllib
import simplejson
import BDHandler


class myHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
       
        self.wfile.write("Hello World !")
        return

    def do_POST(self):
        self._set_headers()
        print "POST"
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = simplejson.loads(self.data_string)

        responseBDH = BDHandler.init(data)        

        pass

        try:
            self.wfile.write(simplejson.dumps(responseBDH))
        except socket.error:
            print "Failed to send data."
        return


PORT_NUMBER = 8080
try:
    server = HTTPServer(('127.0.0.1', PORT_NUMBER), myHandler)
    print 'Started server on port ', PORT_NUMBER

    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
