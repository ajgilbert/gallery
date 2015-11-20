<?php
$dirname = basename(getcwd());
// make sure to send all headers first
// Content-Type is the most important one (probably)
header('Content-Type: application/octet-stream');
header('Content-disposition: attachment; filename="archive.zip"');

// use popen to execute a unix command pipeline
// and grab the stdout as a php stream
// (you can use proc_open instead if you need to
// control the input of the pipeline too)

$fp = popen("cd ..; zip -r - ./$dirname/ -x \"*.php\" \"*.html\"", 'r');

// // pick a bufsize that makes you happy (8192 has been suggested).
$bufsize = 8192;
$buff = '';
while( !feof($fp) ) {
   $buff = fread($fp, $bufsize);
   echo $buff;
}
pclose($fp);
?>