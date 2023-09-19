<?php
    session_start();
    # get flag to run /readflag binary
    if(!isset($_GET["p"])){
    	include 'index.php';
    } else {
        $_SESSION["p"] = $_GET["p"];
    	include $_GET["p"];
    }
?>
<br><br>
<?php highlight_file(__FILE__); ?>
