<!DOCTYPE html>
<html>
<body>
<?php
    // Include the MongoDB PHP driver
    require 'vendor/autoload.php';
    $client = new MongoDB\Client("mongodb://localhost:27017/");
    $db = $client->{"nyse-db"}; // Access the 'nyse-db' database
    $collection = $db->{"active-stocks"}; // Access the 'active-stocks' collection
    $active_stocks = $collection->find([]);

    // Function to generate an HTML table from stock data
    function generateHTMLTable($stocks){
        // Generate HTML Table
        echo '<table border="1">';
        echo '<tr><th><a href="?sort=_id">Index</a></th><th><a href="?sort=Symbol">Symbol</a></th><th><a href="?sort=Name">Name</a></th><th><a href="?sort=Price (Intraday)">Price (Intraday)</a></th><th><a href="?sort=Change">Change</a></th><th><a href="?sort=Volume">Volume</a></th></tr>';
        // Iterate through each stock and create table rows
        foreach ($stocks as $active_stock) {
            echo '<tr>';
            echo '<td>' . $active_stock['_id'] . '</td>';
            echo '<td>' . $active_stock['Symbol'] . '</td>';
            echo '<td>' . $active_stock['Name'] . '</td>';
            echo '<td>' . $active_stock['Price (Intraday)'] . '</td>';
            echo '<td>' . (($active_stock['Change']) > 0 ? '+' . $active_stock['Change'] : $active_stock['Change']) . '</td>';
            echo '<td>' . $active_stock['Volume'] . 'M</td>';
            echo '</tr>';
        }
        echo '</table>';
    }
    // Check if sorting parameter is present in the URL
    if (isset($_GET['sort'])) {
        $sortField = $_GET['sort'];
        // Sort the collection based on the specified field
        $sorted = $collection->find([], ['sort' => [$sortField => 1]]);
        // Generate HTML table with sorted data
        generateHTMLTable($sorted);
    } else {
        // Generate HTML table with unsorted data
        generateHTMLTable($active_stocks);
    }
?>
</body>
</html> 