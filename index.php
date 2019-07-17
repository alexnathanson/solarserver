<!DOCTYPE html>
<html>

<head>
<h1>Solar Server!</h1>
</head>

<body>

<?php

//variables
$pvVoltsNow = 3;
$pvCurrentNow = .33;
$pvPowerNow = 1;
$fileName = "/home/pi/EPSolar_Tracer/data/tracerData" . date("Y-m-d") . ".csv";

echo "<h3>Today's date:</h3>" . date("Y-m-d") . "<br>";

echo "<h3>File name:</h3>". $fileName . "<br>";

// current directory
//echo getcwd() . "\n";

//get the data
$file = fopen($fileName,"r");
print_r(fgetcsv($file));
fclose($file);



$dataNow = array($pvVoltsNow, $pvCurrentNow, $pvPowerNow);



echo "<h3>Present PV Data:</h3>" . json_encode($dataNow);

?>

</body>
</html>