<?php
include('dbconn.php');

if(isset($_GET["userid"]) && isset($_GET["userpw"])){
	$mysqli = new mysqli($host, $sqli1_username, $sqli1_password, $database);

	if ($mysqli->connect_error) {
	    die("connection fail:" . $mysqli->connect_error);
	}

	$query = "SELECT userid FROM sqli1_table where userid='$_GET[userid]' and userpw='$_GET[userpw]'";
	$result = $mysqli->query($query);
	$userid = "";
	
	if ($result->num_rows > 0) {
	    while ($row = $result->fetch_assoc()) {
	        $userid = $row['userid'];
	    }
	}
	$mysqli->close();

	if($userid == "admin"){
		echo file_get_contents('/sqli1_flag.txt');
	} else {
		echo $userid;
	}
}
?>
<br><br>
<?php highlight_file(__FILE__); ?>
