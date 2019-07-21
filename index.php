<!DOCTYPE html>
<html>

<head>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

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


?>

<script type="text/javascript">
      google.charts.load('current', {'packages':['corechart', 'line']});
      google.charts.setOnLoadCallback(drawChart);

      var phpData = <?php echo json_encode($rawDataArray) ?>;

      
//PV DATA
	var pvData = cleanData(phpData, 1, 10, -1);
//BAT DATA
	var batData = cleanData(phpData, 1, 10, -1);

//LOAD DATA
	var loadData = cleanData(phpData, 1, 10, -1);

	//select columns
      //this only works for taking a contiguous subset
      //var mapData = phpData.map(function(val){
	  //  return val.slice(10,(val.length));
		//});

      function cleanData(thisArray, _useAsX, subsetStart, subsetFinish){

      	var tempData = thisArray.map(function(val){
	    	return val.slice(subsetStart,subsetFinish);
			});

		//go through each row
      	for (var i = 0; i < tempData.length; i++) {
      	//send the first column to the back until the selected column is first
      	for (var c=0; c < useAsX;c++){
		 	tempData[i][rowLength] = tempData[i].shift();
      		}
		}

      //set x axis
      var useAsX = tempData[0].length-1; //the column number you want to use
     
      var rowLength = tempData[0].length-1;
      //go through each row
      for (var i = 0; i < tempData.length; i++) {
      	//send the first column to the back until the selected column is first
      	for (var c=0; c < useAsX;c++){
		 	tempData[i][rowLength] = tempData[i].shift();
      		}
		}

      //make floats, exclude header and X-axis
      for (var i = 1; i < tempData.length; i++) {
      	for (var c=1; c < tempData[i].length;c++){
		 	tempData[i][c] = parseFloat(tempData[i][c]);
      		}
		}

      console.log(tempData);

      return tempData;
      }
      

      function drawChart() {
        var PVdataMap = google.visualization.arrayToDataTable(pvData);
        var BATdataMap = google.visualization.arrayToDataTable(batData);
        var LOADdataMap = google.visualization.arrayToDataTable(loadData);

        //console.log(data);

        var PVoptions = {
          title: 'PV',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 500,
        	height: 700
        };

        var BAToptions = {
          title: 'Battery',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 500,
        	height: 700
        };

        var LOADoptions = {
          title: 'Load',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 500,
        	height: 700
        };

        var PVchart = new google.visualization.LineChart(document.getElementById('PV_chart'));

        PVchart.draw(PVdataMap, PVoptions);

        var BATchart = new google.visualization.LineChart(document.getElementById('BAT_chart'));

        BATchart.draw(BATdataMap, BAToptions);

        var LOADchart = new google.visualization.LineChart(document.getElementById('LOAD_chart'));

        LOADchart.draw(LOADdataMap, LOADoptions);
    }
</script>

<div id="PV_chart" style="width: 1500px; height: 700px"></div>
<div id="BAT_chart" style="width: 1500px; height: 700px"></div>
<div id="LOAD_chart" style="width: 1500px; height: 700px"></div>

<?php
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