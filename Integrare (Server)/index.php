<?php
	header('Content-Type: application/json');

	//POST request function
	function post_to($url, $data){
		$options = array(
			'http' => array(
				'header'  => "Content-type: application/json",
				'method'  => 'POST',
				'content' => $data
			)
		);
		$context  = stream_context_create($options);
		$result = file_get_contents($url, false, $context);

		return json_decode($result);
	}

	//Parse message
	if ( isset($_REQUEST["input"]) ){
		//Get message from client
		$currentInput = $_REQUEST["input"];

		//Setting master json
		$finalJson = array();
		$finalJson["input"] = $currentInput;

		//Call text processing
		$textProcessingPath = 'http://localhost:2000?input='.urlencode($currentInput);
		$textProcessingResponse = file_get_contents($textProcessingPath);
		$finalJson["text_processing"] = json_decode($textProcessingResponse);

		//Call output
		$outputArray = array("action" => "answer_what", "question" => "what is your favorite food?");
		$outputInput = json_encode($outputArray);
		$outputPath = 'http://localhost:7000';
		$finalJson["output"] = post_to($outputPath, $outputInput);

		//Final
		echo json_encode($finalJson);
	}

?>