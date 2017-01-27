cheerups = ["Why aren't you more optimistic? Life is wonderfull.",
	"It will be just fine. Just believe in your own strength.",
	"Here's a joke. My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.",
	"Here's a funny story about my brother. He dreamt he was forced to eat a giant marshmallow. When he woke up, his pillow was gone.",
	"I know what can cheer you up. Two Elephants meet a totally naked guy. After a while one elephant says to the other: \"I really don't get how he can feed himself with that thing!\"",
	"Don't worry, be happy!",
	"I'd like to buy a new boomerang please. Also, can you tell me how to throw the old one away?",
	"Life is better when you smile.",
	"Never give up! You can be a hero.",
	"Even in this situation you should smile, bacause good things happen when you do it.",
	"Grab a beer and cheer up!",
	"You can get over this. Bad feeling are like rocks, you can throw them away.",
	"Aww, c'mon. You will talk to my hand if continue this way.",
	"If you think you are the only one with problems, think about mexicans when they heard about the new President of America.",
	"Let's take a break. Do you want to watch American Pie? It's about a smiling pie made in America."]

var express = require('express');
var bodyParser = require('body-parser');
var request = require('request');


var app = express();

// var alchemyApiKey = "20d8312f540cc6d9cbd4ecf51a32077d24b9a242";

var alchemyApi = require('./alchemyapi_node/alchemyapi');
var alchemy = new alchemyApi();

app.use(bodyParser.json());

app.post('/emotion', function (request, response) {
	var botText = request.body.botText;
	var userText = request.body.userText;
	console.log(botText + "  " + userText);
	try {
		var emoticon = "";
		var cheerUp = "";
		var botScore = 0;
		var userScore = 0;
		if (botText && userText) {
			alchemy.sentiment("text", botText, {}, function (alchemyResponse) {
				if(Math.random() > 0.3) {
					if (alchemyResponse["docSentiment"]) {
						botScore = alchemyResponse["docSentiment"]["score"];
					}
					if (botScore) {
						if (botScore < -0.7)
							emoticon = "&#x1F622;";
						else
							if (botScore < 0)
								emoticon = "&#x1F641;";
							else
								if (botScore < 0.7)
									emoticon = "&#x1F60A;";
								else
									emoticon = "&#x1F601;";
					}
					else{
						botScore = 0;
					}
				}
				alchemy.sentiment("text", userText, {}, function (alchemyResponse2) {
					userScore = 0;
					if (alchemyResponse2["docSentiment"]) {
                        console.log("Got in IF.");
						userScore = alchemyResponse2["docSentiment"]["score"];
					}
					if (userScore && userScore < -0.5 && Math.random() > 0.3) {
						cheerUp = cheerups[Math.floor((Math.random() * cheerups.length))];
					}
					else {
						cheerUp = "";
					}
					response.json({ "text": botText + emoticon + " " + cheerUp, "emotionScore": userScore * 50, "TrimmedOutput": botText + " " + cheerUp });
				});
			});
		}
		else {
			response.json({ "text": botText, "emotionScore": 0, "TrimmedOutput": botText });
		}
	}
	catch(err) {
		response.json({ "text": botText, "emotionScore": 0, "TrimmedOutput": botText });
	}
	// response.json({ "text": botText, "emotionScore": 0, "TrimmedOutput": botText });
});

// start the server
var port = process.env.PORT || 7521;
app.listen(port);
console.log('sentiment analysis at http://localhost:' + port);
