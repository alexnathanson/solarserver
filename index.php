<!DOCTYPE html>
<html>

<head>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<title>Solar Server</title>

<h1>Solar Server!</h1>
</head>

<body>

<?php

//get the query string
$date = htmlspecialchars($_GET["date"]);

$fileDate = date("Y-m-d");
if ($date == 'yesterday'){
	$fileDate = date("Y-m-") . (date(d)-1);
}elseif( $date == 'before'){
	$fileDate = date("Y-m-") . (date(d)-2);
}

//variables
$fileName = "/home/pi/EPSolar_Tracer/data/tracerData" . $fileDate . ".csv";
$rawDataArray = [];

echo "<h3>Today's Date:</h3>" . $fileDate . "<br>";

echo "<p>View: <a href='/?date=today' id='today'>Today</a> | <a href='/?date=yesterday' id='yesterday'>Yesterday</a> | <a href='/?date=before' id='daybefore'>The Day Before</a></p>";

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

	//remove the time column from the end
	for (var p =0; p <phpData.length; p++){
		phpData[p].pop();
	}
      
	Array.prototype.clone = function() {
		return JSON.parse(JSON.stringify(this)); //deep copy

		//return this.slice(0); //shallow copy
	};
//PV DATA
	//var pvData = ;
/*
	for (var sp = 0; sp < pvData.length;sp++){
		pvData[sp].splice(10,3);//remove columns 10-13
		pvData[sp].splice(4,5);//remove colums 4-8
	}
	
*/
	var pvData = cleanData(phpData.clone(), "date");

	//remember this happens AFTER the columns are shuffled around!
	for (var sp = 0; sp < pvData.length;sp++){
		pvData[sp].splice(1,3);//remove columns
		pvData[sp].splice(5);//remove colums
	}
	
	//console.log(pvData);

//BAT DATA
	//var batData = phpData.slice(4,6);

	var batData = cleanData(phpData.clone(), "date");

	//console.log(batData);
	//remember this happens AFTER the columns are shuffled around!
	for (var sp = 0; sp < batData.length;sp++){
		batData[sp].splice(1,7);//remove columns
		//batData[sp].splice(8);//remove colums
	}
	
	//scale bat percentage to 0-100
	for (var bper = 1; bper < batData.length; bper++){
		batData[bper][1] *= 100.0;
	}

//LOAD DATA
	//var loadData = phpData.slice(9);//if only 1 element it goes to the end
	var loadData = cleanData(phpData.clone(), "date");

	//remember this happens AFTER the columns are shuffled around!
	for (var sp = 0; sp < loadData.length;sp++){
		loadData[sp].splice(4);//remove columns
		//batData[sp].splice(8);//remove colums
	}
	//select columns
      //this only works for taking a contiguous subset
      //var mapData = phpData.map(function(val){
	  //  return val.slice(10,(val.length));
		//});

      function cleanData(tempData, stringForX){

      	console.log(tempData[0]) //print headers

      	//Set X axis
      	var useAsX = 0;
      	//find string in first row
      	for (var getX = 0; getX < tempData[0].length; getX++){
      		if (tempData[0][getX] == stringForX){
      			useAsX = getX;
      			console.log(stringForX + " " + useAsX);
      			break;
      		}
      	}
		//go through each row
      	for (var i = 0; i < tempData.length; i++) {
      	//send the first column to the back until the selected column is first
	      	for (var c=0; c < useAsX;c++){
			 	tempData[i][tempData[i].length-1] = tempData[i].shift();
	      		}
		}

      //make floats, exclude header and X-axis
      for (var i = 1; i < tempData.length; i++) {
      	for (var c=1; c < tempData[i].length;c++){
		 	tempData[i][c] = parseFloat(tempData[i][c]);
      		}
		}

      //console.log(tempData);

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
          width: 1500,
        	height: 500
        };

        var BAToptions = {
          title: 'Battery',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 1500,
        	height: 500
        };

        var LOADoptions = {
          title: 'Load',
          curveType: 'function',
          legend: { position: 'bottom' },
          width: 1500,
        	height: 500
        };

        var PVchart = new google.visualization.LineChart(document.getElementById('PV_chart'));

        PVchart.draw(PVdataMap, PVoptions);

        var BATchart = new google.visualization.LineChart(document.getElementById('BAT_chart'));

        BATchart.draw(BATdataMap, BAToptions);

        var LOADchart = new google.visualization.LineChart(document.getElementById('LOAD_chart'));

        LOADchart.draw(LOADdataMap, LOADoptions);
    }

    
</script>

<div id="PV_chart" style="width: 1500px; height: 500px"></div>
<div id="BAT_chart" style="width: 1500px; height: 500px"></div>
<div id="LOAD_chart" style="width: 1500px; height: 500px"></div>

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