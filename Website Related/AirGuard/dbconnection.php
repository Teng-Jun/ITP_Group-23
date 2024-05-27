<?php
$servername = "4.145.97.58";
$username = "itpgroup23";
$password = "xji],x4~hSTBCqd";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";
?>
