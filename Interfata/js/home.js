var localURL = 'http://localhost:1000';



$( document ).ready(function() {
	$("#input-left-position").on('keypress', function(e){
		console.log("fired key");
		if(e.which == 13) {
			console.log("fired");
			SendUserMessage();
		}
	});
});

function GetBotAnswer(userText){
	$.ajax(
		{
			url: localURL+'getMessage',
			data: userText,
			success: function(result){
				SendBotMessage(result);
			}
		}
	);
}

function SendBotMessage(message){

	responsiveVoice.setDefaultVoice("US English Male");
	responsiveVoice.speak(message);

	var chat = $('.chat');
				chat.append('\
					<li class=\"left clearfix\"><span class=\"chat-img pull-left\">\
							<img src=\"http://placehold.it/50/55C1E7/fff&text=Bot\" alt=\"User Avatar\" class=\"img-circle\" />\
						</span>\
							<div class=\"chat-body clearfix\">\
								<div class=\"header\">\
									<strong class=\"primary-font\">Chat Bot</strong> <small class=\"pull-right text-muted\">\
										<span class=\"glyphicon glyphicon-time\"></span></small>\
								</div>\
								<p>'
									+
										message
									+
								'</p>\
							</div>\
						</li>\
				');
}

function SendUserMessage(){
	var inputBox = $('#input-left-position')[0];
	var message = inputBox.value;
	if(message=='')
		return;

	//Adding to frontend
	 $('.chat').append('<li class=\"right clearfix\"><span class=\"chat-img pull-right\">\
							<img src=\"http://placehold.it/50/55C1E7/fff&text=ME\" alt=\"User Avatar\" class=\"img-circle\" />\
							</span>\
						 <div class=\"chat-body clearfix\">\
							<div class=\"header\">\
								<strong class=\"pull-right primary-font\">User</strong> <small class=\"pull-left text-muted\">\
						\
							</div>\
							 <p>'+
								 message
								 +'\
							 </p>\
						 </div>\
						</li>');
	inputBox.value = "";


	var randomNr = Math.floor(Math.random()*(50-(-50)+1)+(-50));
	ApplyEmotion(randomNr);

	//Send input to server
	$.ajax(
		{
			url: localURL,
			type: 'get',
			data: {
				'input': message
			},
			success: function(result){
				console.log(result);
				SendBotMessage(result.output);
				ApplyEmotion(result.emotion_score);
			},
			error: function(result){
				console.log(result);
			}
		}
	);
}

function ApplyEmotion(scoreAsString){
	var score = parseInt(scoreAsString);
	var newBackgroundColor = "white";
	if(score > 25){
		newBackgroundColor = "#e4e4e4";
	}else{
		newBackgroundColor = "#c5e3ed";
	}

	$('#collapseOne').css('background', newBackgroundColor);
}
