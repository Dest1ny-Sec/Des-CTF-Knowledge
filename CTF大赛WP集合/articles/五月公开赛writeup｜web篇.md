# 五月公开赛writeup｜web篇

> 原文: https://www.ctfiot.com/73628.html
> ID: 73628

1. TemplatePlay

2. 题目详细解题步骤

2.MyNotes

2. 题目详细解题步骤

Export notes应该是可以打包下载文件，但是咱是下不了。

题目给出了源码www.zip，我们来分析一下，主要是以下几个源码：

END


```
<section>
        <h2>Admin Page</h2>
        
          <?php
          if (is_admin()) {
            echo "Welcome, Admin, this is your secret: <code>" . file_get_contents('/flag') . "</code>";
         } else {
            echo "You are not an admin :(";
         }
          ?>
        
      </section>
<?php
define('TEMP_DIR', '/var/www/tmp');
<?php
error_reporting(0);

require_once('config.php');
require_once('lib.php');

session_save_path(TEMP_DIR);  // /var/www/tmp
session_start();
<?php
function redirect($path) {
  header('Location: ' . $path);
  exit();
}

// utility functions
function e($str) {
  return htmlspecialchars($str, ENT_QUOTES);
}

// user-related functions
function validate_user($user) {
  if (!is_string($user)) {
    return false;
 }

  return preg_match('/A[0-9A-Z_-]{4,64}z/i', $user);
}

function is_logged_in() {
  return isset($_SESSION['user']) && !empty($_SESSION['user']);
}

function set_user($user) {  // 在session中设置user
  $_SESSION['user'] = $user;
}

function get_user() {   // 获取session中的user
  return $_SESSION['user'];
}

function is_admin() {
  if (!isset($_SESSION['admin'])) {
    return false;
 }
  return $_SESSION['admin'] === true;   // 判断是否是admin
}

// note-related functions
function get_notes() {
  if (!isset($_SESSION['notes'])) {
    $_SESSION['notes'] = [];
 }
  return $_SESSION['notes'];
}

function add_note($title, $body) {
  $notes = get_notes();
  array_push($notes, [
    'title' => $title,
    'body' => $body,
    'id' => hash('sha256', microtime())
 ]);
  $_SESSION['notes'] = $notes;
}

function find_note($notes, $id) {
  for ($index = 0; $index < count($notes); $index++) {
    if ($notes[$index]['id'] === $id) {
      return $index;
   }
 }
  return FALSE;
}

function delete_note($id) {
  $notes = get_notes();
  $index = find_note($notes, $id);
  if ($index !== FALSE) {
    array_splice($notes, $index, 1);
 }
  $_SESSION['notes'] = $notes;
}
<?php
require_once('init.php');

if (!is_logged_in()) {
  redirect('/?page=home');
}

$notes = get_notes();

if (!isset($_GET['type']) || empty($_GET['type'])) {
  $type = 'zip';
} else {
  $type = $_GET['type'];
}

$filename = get_user() . '-' . bin2hex(random_bytes(8)) . '.' . $type;   // whoami-9a989aea898.zip
$filename = str_replace('..', '', $filename); // avoid path traversal
$path = TEMP_DIR . '/' . $filename;    // /var/www/tmp/whoami-9a989aea898.zip

if ($type === 'tar') {
  $archive = new PharData($path);
  $archive->startBuffering();
} else {
  // use zip as default
  $archive = new ZipArchive();
  $archive->open($path, ZIPARCHIVE::
CREATE | ZipArchive::
OVERWRITE);
}

for ($index = 0; $index < count($notes); $index++) {
  $note = $notes[$index];
  $title = $note['title'];
  $title = preg_replace('/[^!-~]/', '-', $title);
  $title = preg_replace('#[/\?*.]#', '-', $title); // delete suspicious characters
  $archive->addFromString("{$index}_{$title}.json", json_encode($note));
}

if ($type === 'tar') {
  $archive->stopBuffering();
} else {
  $archive->close();
}

header('Content-Disposition: attachment; filename="' . $filename . '";');
header('Content-Length: ' . filesize($path));
header('Content-Type: application/zip');
readfile($path);
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1668344616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668344616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668344616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1668344618.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668344619.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1668344620.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668344621.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668344621.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1668344623.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1668344624.png)