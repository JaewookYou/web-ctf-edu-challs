<?php
# flag is at lfiflag.php
    if(!isset($_GET["p"])){
    	include 'index.php';
    } else {
    	include $_GET["p"];
    }
?>
<br><br>
<?php highlight_file(__FILE__); ?>
