<meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
<form method="post"><textarea name="q"></textarea><input type="submit" value="Submit"></form>

<?php
$q = $_POST['q'];

mb_internal_encoding("UTF-8");

function uniord($u) { 
    $k = mb_convert_encoding($u, 'UCS-2LE', 'UTF-8'); 
    $k1 = ord(substr($k, 0, 1)); 
    $k2 = ord(substr($k, 1, 1)); 
    return $k2 * 256 + $k1; 
}

function unichr($intval) {
  return mb_convert_encoding(pack('n', $intval), 'UTF-8', 'UTF-16BE');
}


$trans = array( 65 => array( 913, 1040, ), 66 => array( 914, 1042, ), 67 => array( 1057, 8557, ), 68 => array( 8558, ), 69 => array( 917, 1045, ), 70 => array( 988, ), 72 => array( 919, 1053, ), 73 => array( 921, 1030, 1216, 8544, ), 74 => array( 1032, ), 75 => array( 922, 8490, ), 76 => array( 8556, ), 77 => array( 924, 1052, 8559, ), 78 => array( 925, ), 79 => array( 927, 1054, ), 80 => array( 929, 1056, ), 83 => array( 1029, ), 84 => array( 932, 1058, ), 86 => array( 8548, ), 88 => array( 935, 1061, 8553, ), 89 => array( 933, 1198, ), 90 => array( 918, ), 211 => array( 7886, ), 97 => array( 1072, ), 99 => array( 1089, 8573, ), 100 => array( 8574, ), 101 => array( 1077, ), 104 => array( 1211, ), 105 => array( 1110, 8560, ), 106 => array( 1011, 1112, ), 108 => array( 8572, ), 109 => array( 8575, ), 111 => array( 959, 1086, ), 112 => array( 1088, ), 243 => array( 972, 8057, ), ); 
//print_r($trans);

$new = '';
$rep=0;
for($i=0; $i<mb_strlen($q); ++$i) {

  $char = mb_substr($q, $i, 1);
  $number = uniord($char);
  
  $replacements = $trans[$number];
  if ($replacements === NULL) {
    $new.=$char;
  }
  else {
    $index = mt_rand(0, count($replacements));
    if ($index === count($replacements))
      $new.=$char;
    else {
      $new.=unichr($replacements[$index]);
      ++$rep;
    }
  }

}
echo 'Number of replacements: '.$rep.'<br>';
echo '<textarea>'.$new.'</textarea>';