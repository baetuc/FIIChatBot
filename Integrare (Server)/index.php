<?php
	header('Content-Type: application/json');

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
		echo json_encode($finalJson);
	}

?>