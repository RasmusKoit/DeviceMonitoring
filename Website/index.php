<?php
/**
 * Created by PhpStorm.
 * User: rasmus
 * Date: 5.05.18
 * Time: 14:10
 */




$cmd = isset($_GET["cmd"]) ? $_GET["cmd"] : "login";

if ($cmd == "home") {
    $path = "template/base.php";
    require_once("template/base.php");



} else if ($cmd == "hubList") {
    $path = "add.php";
    require_once("template/base.php");


} else if ($cmd == "addHub") {

    $path = "addHub.php";
    require_once("template/addHub.php");
    //header("Location: ?cmd=list");

} else if ($cmd == "login") {
    require_once("template/login.php");
} else if ($cmd == "saveHub") {
    //run php script that adds hub to db

    header("Location: ?cmd=hubList");
}