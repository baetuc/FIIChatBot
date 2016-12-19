"""
Modul creat de Moisii Cosmin grupa 3A5

get_sentiment returnează un dicționar cu valori pentru: pozitiv, neutaral și negative.
"""

import httplib, urllib
import nltk
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

