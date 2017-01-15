var express = require('express');
var bodyParser = require('body-parser');
var request = require('request');


var app = express();

// var alchemyApiKey = "20d8312f540cc6d9cbd4ecf51a32077d24b9a242";

var alchemyApi = require('./alchemyapi_node/alchemyapi');
var alchemy = new alchemyApi();

app.use(bodyParser.json());

app.post('/emoticon', function (request, response) {
	var text = request.body.text;
	console.log(text);
	if (text) {
		alchemy.sentiment("text", text, {}, function (alchemyResponse) {
			var score;
			if (alchemyResponse["docSentiment"]){
				score = alchemyResponse["docSentiment"]["score"];
			}
			else {
				score = 0;
			}
			var emoticon = "";
			if (score) {
				if (score < -0.7)
					emoticon = " :'(";
				else
					if (score < 0)
						emoticon = " :(";
					else
						if (score < 0.7)
							emoticon = " :)";
						else
							emoticon = " :D";
			}
			response.send(text + emoticon);
		});
	}
	else {
		response.send(text);
	}
});


// start the server
var port = process.env.PORT || 7521;
app.listen(port);
console.log('sentiment analysis at http://localhost:' + port);
