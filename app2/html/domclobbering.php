<?php
if(isset($_POST["url"])){
  $url = "http://arang_client:9000/run";
  $data = "url=$_POST[url]";

  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL,$url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 60);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
  curl_setopt($ch, CURLOPT_POST, true);

  $response = curl_exec($ch);
  echo $response;
  curl_close($ch);
} else {
  function waf($input){
    $t = strtolower($input);
    if(preg_match("/script|on|frame|object|embed|data|&#|src|\/\/|'|\"|`|\*/",$t)){
      return "";
    } else {
      return $input;
    }
  }
?>
<html>
<head>
<title>Dom Clobbering Simple Chall!</title>
<script>
window.onload = ()=>{
  if(!window.CLOB){
    CLOB = {
      isAdmin: false
    }
  }
  
  if(CLOB.isAdmin){
    params = new URLSearchParams(location.search);
    eval(params.get("c"));
  }
}
</script>
</head>
<body>
<form id="form" method="POST" action="/domclobbering.php">
  <input type="text" hint="input url to bot visit" name="url">
  <input type="submit" value="submit">
</form>
<?php
if(isset($_GET["c"])){
  echo waf($_GET["c"]);
}else{
  echo "Hello!";
}
?>
<br><br>
<div id='flag'>
<?php
$flag = file_get_contents("/domclobbering_flag.txt");
if(str_contains($_SERVER['REMOTE_ADDR'],'172.')){
  echo $flag;
}
?>
</div>
</body>
</html>
<?php highlight_file(__FILE__); } ?>

