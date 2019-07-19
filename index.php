<!DOCTYPE html>
<html>

<head>
<h1>Solar Server!</h1>
</head>

<body>

<?php

//variables
$fileName = "/home/pi/EPSolar_Tracer/data/tracerData" . date("Y-m-d") . ".csv";
$rawDataArray = [];

echo "<h3>Today's Date:</h3>" . date("Y-m-d") . "<br>";

echo "<h3>File Name:</h3>". $fileName . "<br>";

// current directory
//echo getcwd() . "\n";

echo "<h3>PV Data:</h3>";

// Open the file for reading (from https://phpenthusiast.com/blog/parse-csv-with-php)
if (($h = fopen("{$fileName}", "r")) !== FALSE) 
{
  // Each line in the file is converted into an individual array that we call $data
  // The items of the array are comma separated
  while (($data = fgetcsv($h, 1000, ",")) !== FALSE) 
  {
    // Each individual array is being pushed into the nested array
    $rawDataArray[] = $data;		
  }

  // Close the file
  fclose($h);
}

/*
// Display the code in a readable format
echo "<pre>";
var_dump($rawDataArray);
echo "</pre>";
*/

echo "<h4>Most Recent Data:</h4>";
$buildNow = '<table border=1px>';
//foreach($rawDataArray as $row)

//header
{
$buildNow .= '<tr>';
foreach($rawDataArray[0] as $item)
{
$buildNow .= "<td>{$item}</td>";
}
$buildNow .= '</tr>';
}

//most recent data
$dataCount = count($rawDataArray);
$nowRow = $rawDataArray[$dataCount-1];

{
$buildNow .= '<tr>';
foreach($nowRow as $item)
{
$buildNow .= "<td>{$item}</td>";
}
$buildNow .= '</tr>';
}
$buildNow .= '</table>';
echo $buildNow;


echo "<h4>Today:</h4>";
//also from https://phpenthusiast.com/blog/parse-csv-with-php
$build = '<table border=1px>';
foreach($rawDataArray as $row)
{
$build .= '<tr>';
foreach($row as $item)
{
$build .= "<td>{$item}</td>";
}
$build .= '</tr>';
}
$build .= '</table>';
echo $build;
?>

</body>
</html>