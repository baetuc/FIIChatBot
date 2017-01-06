<?php
	header('Content-Type: application/json');

	//Server definitions
	$textProcessingURL = 'http://localhost:2000';
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
		return json_decode($parsedResult[1]);
	}

	//Parse message
	if ( isset($_REQUEST["input"]) ){
		//Get message from client
		$currentInput = $_REQUEST["input"];

		//Setting master json
		$finalJson = array();
		$finalJson["input"] = $currentInput;

		//Call text processing
		$textProcessingPath = $textProcessingURL.'?input='.urlencode($currentInput);
		$textProcessingResponse = file_get_contents($textProcessingPath);
		$overloadedTextProcessingResponse = json_encode(array("sentences" => json_decode($textProcessingResponse), "numberSentences"=>1));
		$finalJson["text_processing"] = json_decode($textProcessingResponse);

		//Call database
		$databasePath = $databaseURL;
		$databaseResponse = post_to($databasePath, $overloadedTextProcessingResponse);
		$finalJson["database"] = $databaseResponse;

		//Call output
		$outputInput = $databaseResponse;
		$outputPath = $outputURL;
		$outputResponse = post_to($outputPath, $outputInput);
		$finalJson["output"] = $outputResponse;

		// Final
		echo json_encode($finalJson);
	}
?>