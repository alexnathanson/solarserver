<!DOCTYPE html>
<html>

<head>
Solar Server!
</head>

<body>

<?php


// current directory
echo getcwd() . "\n";

//get the data
$file = fopen(".home/pi/EPSolar_Tracer/data/tracerData" . date("Y-m-d") . ".csv","r");
print_r(fgetcsv($file));
fclose($file);

//variables
$pvVoltsNow = 3;
$pvCurrentNow = .33;
$pvPowerNow = 1;

$dataNow = array($pvVoltsNow, $pvCurrentNow, $pvPowerNow);

echo date("Y-m-d") . "<br>";

echo "<h3>Present PV Data: </h3>" . json_encode($dataNow);

?>

</body>
</html>