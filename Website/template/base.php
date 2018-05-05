<!DOCTYPE html>
<html lang="en">
<head>
    <title>Aio-Hub</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
<nav class="navbar navbar">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="?cmd=home">Aio-Hub</a>
        </div>
        <ul class="nav navbar-nav">
            <li class="active"><a href="?cmd=home">Home</a></li>
            <li><a href="?cmd=hubList">Hub List</a></li>
            <li><a href="?cmd=addHub">Add a Hub</a></li>
            <li><a href="?cmd=acl">User ACL</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
            <li><a href="?cmd=profile"><span class="glyphicon glyphicon-user"></span> Profile</a></li>
            <li><a href="?cmd=logout"><span class="glyphicon glyphicon-log-out"></span> Log-out</a></li>
        </ul>
    </div>
</nav>
<div class="container-fluid">

<?php
    include_once $path;
?>

</div>
</body>
</html>