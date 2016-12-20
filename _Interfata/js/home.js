var localURL = 'localhost:1000';

function SendMessage(){
	$.ajax(
		{
			url: localURL+'getMessage', 
			success: function(result){
				var chat = $('.chat');
				// chat.append('<li class=\"left clearfix\"><span class=\"chat-img pull-left\">
							// <img src=\"http://placehold.it/50/55C1E7/fff&text=CB\" alt=\"User Avatar\" class=\"img-circle\" />
						// </span>
							// <div class=\"chat-body clearfix\">
								// <div class=\"header\">
									// <strong class=\"primary-font\">Chat Bot</strong> <small class=\"pull-right text-muted\">
										// <!-- <span class=\"glyphicon glyphicon-time\"></span>12 mins ago</small> -->
								// </div>
								// <p>
									// Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare
									// dolor, quis ullamcorper ligula sodales.
								// </p>
							// </div>
						// </li>');
			}
		}
	);
}

function dummySend(){
	// $(".chat").append("<li class=\"left clearfix\"><span class=\"chat-img pull-left\">
							// <img src=\"http://placehold.it/50/55C1E7/fff&text=CB\" alt=\"User Avatar\" class=\"img-circle\" />
						// </span>
							// <div class=\"chat-body clearfix\">
								// <div class=\"header\">
									// <strong class=\"primary-font\">Chat Bot</strong> <small class=\"pull-right text-muted\">
										
								// </div>
								// <p>
									// Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare
									// dolor, quis ullamcorper ligula sodales.
								// </p>
							// </div>
						// </li>");
}