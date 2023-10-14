<?php
include('dbconn.php');

function waf($input){
	$t = strtolower($input);
	if(preg_match("/or|union|admin|\||\&|\d|-|\\\\|\x09|\x0b|\x0c|\x0d|\x20|\//",$t)){
		die('no hack..');
	} else {
		return $input;
	}
}

if(isset($_GET["userid"]) && isset($_GET["userpw"])){
	$mysqli = new mysqli($host, $sqli2_username, $sqli2_password, $database);

	if ($mysqli->connect_error) {
	    die("connection fail:" . $mysqli->connect_error);
	}

	$uid = waf($_GET["userid"]);
	$upw = waf($_GET["userpw"]);

	$query = "SELECT userid FROM sqli2_table where userid='$uid' and userpw='$upw'";
	$result = $mysqli->query($query);
	$userid = "";
	
	if ($result->num_rows > 0) {
	    while ($row = $result->fetch_assoc()) {
		    $userid = $row['userid'];
		    break;
	    }
	}
	$mysqli->close();

	if($userid == "admin"){
		echo file_get_contents('/sqli2_flag.txt');
	} else {
		echo $userid;
	}
}
?>
<br><br>
<?php highlight_file(__FILE__); ?>
