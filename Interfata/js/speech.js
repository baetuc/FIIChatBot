var langs =
	[['English',         ['en-AU', 'Australia'],
						 ['en-CA', 'Canada'],
						 ['en-IN', 'India'],
						 ['en-NZ', 'New Zealand'],
						 ['en-ZA', 'South Africa'],
						 ['en-GB', 'United Kingdom'],
						 ['en-US', 'United States']],
	 ['Română',          ['ro-RO']],
	];

	var create_email = false;
	var final_transcript = '';
	var recognizing = false;
	var ignore_onend;
	var start_timestamp;
	var recognition = new webkitSpeechRecognition();
	var inputField;
	
$(document).ready(function(){
	inputField = document.getElementById('input-left-position');
	var start_button = document.getElementById('start_button');
	if (!('webkitSpeechRecognition' in window)) {
	  upgrade();
	} else {
	  start_button.style.display = 'inline-block';
	  
	  recognition.continuous = true;
	  recognition.interimResults = true;

	  recognition.onstart = function() {
		responsiveVoice.cancel();
		annyang.abort();		
		recognizing = true;
				
		// showInfo('info_speak_now');
		start_img.src = 'images/mic-animate.gif';
	  };

	  recognition.onerror = function(event) {
		if (event.error == 'no-speech') {
		  start_img.src = 'images/mic.gif';
		  // showInfo('info_no_speech');
		  ignore_onend = true;
		}
		if (event.error == 'audio-capture') {
		  start_img.src = 'images/mic.gif';
		  // showInfo('info_no_microphone');
		  ignore_onend = true;
		}
		if (event.error == 'not-allowed') {
		  if (event.timeStamp - start_timestamp < 100) {
			// showInfo('info_blocked');
		  } else {
			// showInfo('info_denied');
		  }
		  ignore_onend = true;
		}
	  };

	  recognition.onend = function() {		  
		recognizing = false;
		annyang.start();

		if (ignore_onend) {
		  return;
		}
		start_img.src = 'images/mic.gif';
		if (!final_transcript) {
		  // showInfo('info_start');
		  return;
		}
		// showInfo('');
		if (window.getSelection) {
		  window.getSelection().removeAllRanges();
		  var range = document.createRange();
		  range.selectNode(document.getElementById('input-left-position'));
		  window.getSelection().addRange(range);
		}
		if (create_email) {
		  create_email = false;
		  createEmail();
		}
	  };

	  recognition.onresult = function(event) {
		var interim_transcript = '';
		for (var i = event.resultIndex; i < event.results.length; ++i) {
		  if (event.results[i].isFinal) {
			final_transcript += event.results[i][0].transcript;
		  } else {
			interim_transcript += event.results[i][0].transcript;
		  }
		}
		final_transcript = capitalize(final_transcript);
		inputField.value = inputField.value + linebreak(final_transcript);
		
		// interim_span.innerHTML = linebreak(interim_transcript);
		// if (final_transcript || interim_transcript) {
		  // showButtons('inline-block');
		// }
	  };
	}
});

function upgrade() {
  start_button.style.display = 'none';
  // showInfo('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}

// function createEmail() {
  // var n = final_transcript.indexOf('\n');
  // if (n < 0 || n >= 80) {
    // n = 40 + final_transcript.substring(40).indexOf(' ');
  // }
  // var subject = encodeURI(final_transcript.substring(0, n));
  // var body = encodeURI(final_transcript.substring(n + 1));
  // window.location.href = 'mailto:?subject=' + subject + '&body=' + body;
// }

function copyButton() {
  if (recognizing) {
    recognizing = false;
    recognition.stop();
  }
  copy_button.style.display = 'none';
  copy_info.style.display = 'inline-block';
  // showInfo('');
}

// function emailButton() {
  // if (recognizing) {
    // create_email = true;
    // recognizing = false;
    // recognition.stop();
  // } else {
    // createEmail();
  // }
  // email_button.style.display = 'none';
  // email_info.style.display = 'inline-block';
  // // showInfo('');
// }

function startButton(event) {
  if (recognizing) {
    recognition.stop();
	annyang.start();
    return;
  }
  final_transcript = '';
  recognition.lang = '';
  
  annyang.abort();
  recognition.start();
  
  ignore_onend = false;
  //inputField.value = '';
  // interim_span.innerHTML = '';
  start_img.src = 'images/mic-slash.gif';
  // showInfo('info_allow');
  // showButtons('none');
  start_timestamp = event.timeStamp;
}

function showInfo(s) {
  var info = document.getElementById('#info');
  debuger;
  if (s) {
    for (var child = info.firstChild; child; child = child.nextSibling) {
      if (child.style) {
        child.style.display = child.id == s ? 'inline' : 'none';
      }
    }
    info.style.display = '';
  } else {
    info.style.display = 'none';
  }
}

// var current_style;
// function showButtons(style) {
  // if (style == current_style) {
    // return;
  // }
  // current_style = style;
  // // copy_button.style.display = style;
  // email_button.style.display = style;
  // copy_info.style.display = 'none';
  // email_info.style.display = 'none';
// }
