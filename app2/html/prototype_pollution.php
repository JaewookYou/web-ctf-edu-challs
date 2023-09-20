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
}
?>
<html>
<head>
<title>Prototype Pollution Simple Chall!</title>
<script>

function isObject(obj) {
  return obj !== null && typeof obj === 'object';
}

function merge(a, b) {
  for (let key in b) {
    if (isObject(a[key]) && isObject(b[key])) {
      merge(a[key], b[key]);
    } else {
      a[key] = b[key];
    }
  }
  return a;
}
 
CLOB = {
  'name':'arang'
}

window.onload = ()=>{
  params = new URLSearchParams(location.search);
  c = JSON.parse(params.get("c"));
  
  merge(CLOB, c);
  document.getElementById('name').innerText = `Hello ${CLOB.name}`;
  
  if(CLOB.isAdmin){
    params = new URLSearchParams(location.search);
    eval(CLOB.code);
  }
}
</script>
</head>
<body>
<form id="form" method="POST" action="/prototype_pollution.php">
  <input type="text" hint="input url to bot visit" name="url">
  <input type="submit" value="submit">
</form>
<div id='name'>
</div>

<div id='flag'>
<?php
$flag = file_get_contents("/pp_flag.txt");
if(str_contains($_SERVER['REMOTE_ADDR'],'172.')){
  echo $flag;
}
?>
</div>
<br><br>
</body>
</html>
<?php highlight_file(__FILE__);  ?>

