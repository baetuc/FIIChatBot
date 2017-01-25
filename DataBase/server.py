import simplejson
import BDHandler
from bottle import run, post, request, response, get, route

@route('/',method = 'POST')
def process():
    data = request.body.read()
    data = simplejson.loads(data)
    responseBDH = BDHandler.init(data)
    return responseBDH


@route('/reset',method = 'POST')
def reset():
    status = BDHandler.resetOntologii()
    return status # True / None


@route('/inactivity',method = 'POST')
def inactivity():
    pass #TODO


run(host='localhost', port=4000, debug=True)
