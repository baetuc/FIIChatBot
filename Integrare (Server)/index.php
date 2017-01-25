<?php
    error_reporting(0);
	header('Content-Type: application/json');
	header('Access-Control-Allow-Origin: *');
	set_time_limit(9999);
	session_start();


	//Server definitions
	$textProcessingURL = 'http://localhost:2000';
	$aiFirst = 'http://localhost:2500/slang_and_coreference';
	$aiSecond = 'http://localhost:2500/topic_and_end';
	$inactivityURL = 'http://localhost:2500/inactivity';
	$resetAIUrl = 'http://localhost:2500/reset';
	$databaseURL = 'http://localhost:4000';
	$resetDBUrl = 'http://localhost:4000/reset';
	$outputURL = 'http://localhost:7000';
	$emotionURL = 'http://localhost:7521/emotion';

	//Route definitions
	/*
	The following function will strip the script name from URL i.e.  http://www.something.com/search/book/fitzgerald will become /search/book/fitzgerald
	*/
	function getCurrentUri()
	{
		$basepath = implode('/', array_slice(explode('/', $_SERVER['SCRIPT_NAME']), 0, -1)) . '/';
		$uri = substr($_SERVER['REQUEST_URI'], strlen($basepath));
		if (strstr($uri, '?')) $uri = substr($uri, 0, strpos($uri, '?'));
		$uri = '/' . trim($uri, '/');
		return $uri;
	}

	$base_url = getCurrentUri();
	$routes = array();
	$routes = explode('/', $base_url);
	foreach($routes as $route)
	{
		if(trim($route) != '')
			array_push($routes, $route);
	}

	/*
	Now, $routes will contain all the routes. $routes[0] will correspond to first route. For e.g. in above example $routes[0] is search, $routes[1] is book and $routes[2] is fitzgerald
	*/


	//POST request function
	function post_to($url, $jsonData){
		$options = array(
			'http' => array(
				'header'  => "Content-type: application/json",
				'method'  => 'POST',
				'content' => $jsonData
			)
		);
		$context  = stream_context_create($options);
		$result = file_get_contents($url, false, $context);

		//Removing headers
		$parsedResult = split("\r\n\r\n", $result, 2);
        //echo $parsedResult;
		$result = $parsedResult[1] ? json_decode($parsedResult[1]) : $parsedResult[0];
		return $result;
	}

	//Parse message
	try {
		if (isset($routes[1]) && $routes[1]=='inactivity'){
			$inactivityResponse = post_to($inactivityURL, "");
			$finalJson = array();
			$finalJson["output"] = $inactivityResponse;
			$finalJson["emotion_score"] = 0;
			$finalJson["TrimmedOutput"] = $inactivityResponse;
			// Final
			echo json_encode($finalJson);
		} else if (isset($routes[1]) && $routes[1]=='reset'){
			$resetDBResponse = post_to($resetDBUrl, "");
			$resetAIResponse = post_to($resetAIUrl, "");
			echo "";
		}
		else {
			if ( isset($_REQUEST["input"]) && $_REQUEST["input"]){
				//Get message from client
				$currentInput = $_REQUEST["input"];
				//Setting master json
				$finalJson = array();
				$inputJSON = json_encode(array("input" => $currentInput));
				$finalJson["input"] = json_decode($inputJSON);

				//Call AI for slang_and_coreference
				$aiResponse1 = post_to($aiFirst, $inputJSON);
				$finalJson["ai1"] = $aiResponse1;

				//Call text processing
				$textProcessingPath = $textProcessingURL;
				$aiResponseJSON1 = json_encode(array("input" => $aiResponse1));
				$textProcessingResponse = post_to($textProcessingPath, $aiResponseJSON1);
				$finalJson["text_processing"] = json_decode($textProcessingResponse);

				//Call AI for topic_and_end
				$aiResponse2 = post_to($aiSecond, $textProcessingResponse);
				$decodedAiResponse2 = json_decode($aiResponse2);
				$finalJson["ai2"] = $decodedAiResponse2;


				// Call database
				$databasePath = $databaseURL;
				$databaseResponse = post_to($databasePath, $aiResponse2);
				$finalJson["database"] = json_decode($databaseResponse);

				// Call output
				$outputInput = $databaseResponse;
				$outputPath = $outputURL;
				$outputResponse = post_to($outputPath, $outputInput);
				$finalJson["output"] = $outputResponse;
				$finalJson['emotion_score'] = 0;

				//Call emotion
				$emotionPath = $emotionURL;
				$emotionInput = $outputResponse;
				$emotionJSON = json_encode(array("botText" => $emotionInput, "userText" => $finalJson["ai1"]));
				$emotionResponse = post_to($emotionPath, $emotionJSON);
				$decodedEmotionResponse = json_decode($emotionResponse);
				$finalJson["output"] = $decodedEmotionResponse->text;
				$finalJson["emotion_score"] = $decodedEmotionResponse->emotionScore;
				$finalJson["TrimmedOutput"] = $decodedEmotionResponse->TrimmedOutput;

				// Final
				echo json_encode($finalJson);
			}
		}
	} catch (Exception $e) {
		$errorJSON = json_encode(array("output" => "I don't know how to answer that."));
		echo $errorJSON;
	}
?>
