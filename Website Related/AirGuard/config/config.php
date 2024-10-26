<?php
require __DIR__ . '/../vendor/autoload.php';

use Dotenv\Dotenv;

try {
    $dotenv = Dotenv::createImmutable(__DIR__ . '/../');
    $dotenv->load();  // Load the .env file explicitly
} catch (Exception $e) {
    die('Error loading .env file: ' . $e->getMessage());
}

// Global declarations
global $vtApiKey, $cpApiKey, $ipqsApiKey;

// Retrieve API keys
$vtApiKey = getenv('VT_API_KEY') ?: $_ENV['VT_API_KEY'] ?? null;
$cpApiKey = getenv('CP_API_KEY') ?: $_ENV['CP_API_KEY'] ?? null;
$ipqsApiKey = getenv('IPQS_API_KEY') ?: $_ENV['IPQS_API_KEY'] ?? null;


// Check if the keys are correctly set
if (!$vtApiKey || !$cpApiKey || !$ipqsApiKey) {
    die('API keys are not set correctly in the environment.');
}
