var localURL = 'http://localhost:1000';
var dictationEnabled = true;

var idleTime = 0;
function timerIncrement() {
    idleTime = idleTime + 1;
    if (idleTime > 20) { // 20 seconds
        userIsInactive();
		idleTime = 0;
    }
}

$( document ).ready(function() {
	$("#input-left-position").on('keypress', function(e){
		if(e.which == 13) {
			console.log("fired");
			SendUserMessage();
		}
	});
	
	$('#dictationToggle').on('change', function(){
		dictationEnabled = $('#dictationToggle')[0].checked;
	});
	$('#dictationToggle').attr("checked",true);
	
	//Increment the idle time counter every second.
    var idleInterval = setInterval(timerIncrement, 1000); // 1 sec

    //Zero the idle timer on mouse movement.
    $(this).mousemove(function (e) {
        idleTime = 0;
    });
    $(this).keypress(function (e) {
        idleTime = 0;
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
	if(dictationEnabled){
		responsiveVoice.setDefaultVoice("US English Male");
		responsiveVoice.speak(message);
	}
	var chat = $('.chat');
				chat.append('\
					<li class=\"left clearfix\"><span class=\"chat-img pull-left\">\
							<img src=\"http://placehold.it/50/55C1E7/fff&text=Bot\" alt=\"User Avatar\" class=\"img-circle\" />\
						</span>\
							<div class=\"chat-body clearfix\">\
								<div class=\"header\">\
									<strong class=\"primary-font\">FII Bot</strong> <small class=\"pull-right text-muted\">\
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


	// var randomNr = Math.floor(Math.random()*(50-(-50)+1)+(-50));
	// ApplyEmotion(randomNr);
	//
	//Send input to server
	$.ajax(
		{
			url: localURL,
			type: 'get',
			data: {
				'input': message
			},
			success: function(result){
				responsiveVoice.cancel();
				SendBotMessage(result.output);

				responsiveVoice.setDefaultVoice("US English Male");
				responsiveVoice.speak(result.TrimmedOutput);

				ApplyEmotion(result.emotion_score);
			},
			error: function(result){
				console.log(result);
			}
		}
	);
}

function resetEverything(){
	$.ajax(
		{
			url: localURL + '/reset',
			type: 'get',
			success: function(result){
				alert('Reset process succeded!');
				window.location.reload();
			},
			error: function(result){
				console.log(result);
			}
		}
	);
}

function userIsInactive(){
	$.ajax(
		{
			url: localURL + '/inactivity',
			type: 'get',
			success: function(result){
				responsiveVoice.cancel();
				SendBotMessage(result.output);

				responsiveVoice.setDefaultVoice("US English Male");
				responsiveVoice.speak(result.TrimmedOutput);

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
		newBackgroundColor = "#c5e3ed";
		console.log("emotion: happy");
	}else{
		if(score<-25){
			newBackgroundColor = "#e4e4e4";
			console.log("emotion: sad");
		}
	}

	if(newBackgroundColor == "white")
		console.log("emotion: neutral");

	$('#collapseOne').css('background', newBackgroundColor);
}
