<?php
	header('Content-Type: application/json');
	header('Access-Control-Allow-Origin: *');

	//Server definitions
	$textProcessingURL = 'http://localhost:2000';
	$aiTopic = 'http://localhost:2500/topic';
	$databaseURL = 'http://localhost:4000';
	$outputURL = 'http://localhost:7000';


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
		$result = $parsedResult[1] ? json_decode($parsedResult[1]) : $parsedResult[0];
		return $result;
	}

	//Parse message
	if ( isset($_REQUEST["input"]) ){
		//Get message from client
		$currentInput = $_REQUEST["input"];

		//Setting master json
		$finalJson = array();
		$finalJson["input"] = $currentInput;

		//Call text processing
		$inputJSON = json_encode(array("input" => $currentInput));
		$textProcessingPath = $textProcessingURL;
		$textProcessingResponse = post_to($textProcessingPath, $inputJSON);
		// $overloadedTextProcessingResponse = json_encode(array("sentences" => json_decode($textProcessingResponse), "numberSentences"=>1));
		$finalJson["text_processing"] = json_decode($textProcessingResponse);

		//Call AI for topic
		$aiResponse = post_to($aiTopic, $textProcessingResponse);
		$finalJson["ai"] = json_decode($aiResponse);

		// Call database
		$databasePath = $databaseURL;
		$databaseResponse = post_to($databasePath, $aiResponse);
		$finalJson["database"] = json_decode($databaseResponse);

		// Call output
		$outputInput = $databaseResponse;
		$outputPath = $outputURL;
		$outputResponse = post_to($outputPath, $outputInput);
		$finalJson["output"] = $outputResponse;

		// Final penis
		echo json_encode($finalJson);
	}
?>