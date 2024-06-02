<?php
$servername = "localhost";
$username = "phpmyadmin";
$password = "xji],x4~hSTBCqd";
$database = "itp";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}  
//echo "Connected successfully";
?>
