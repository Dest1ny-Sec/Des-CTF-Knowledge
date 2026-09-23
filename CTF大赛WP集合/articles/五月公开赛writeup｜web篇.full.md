---
title: 五月公开赛writeup｜web篇
contest: 五月公开赛 2022
year: 2022
difficulty: medium
vuln_type: web_unknown
tags:
- PHP
- SESSION
- PharData
- ZipArchive
- is_admin
- file_get_contents
- zip slip
attack_chain:
- TemplatePlay + MyNotes 两题
- 登录 admin/admin → 看到 Admin Page 调 is_admin() 读 /flag
- 关键函数 is_admin() 校验 $_SESSION['admin'] === true
- '漏洞: Export notes 导出 zip/tar 类型由 ?type= 控制'
- type=tar 用 PharData 类 startBuffering/stopBuffering
- title 字符过滤 preg_replace('/[^!-~]/', '-') + '#[/\?*.]#' → '-
- 注释 "delete suspicious characters" 但仍可注入 ../ 软连接或 phar 元数据
- '攻击面: Phar 反序列化 (phar:// wrapper) + zip slip 路径穿越'
key_payload: '''?type=tar + title 含 phar 元数据触发反序列化'''
one_liner: PHP 笔记导出支持 zip/tar 自切换，title 字符过滤不严可注 Phar 元数据触发反序列化。
lesson: PHP PharData/ZipArchive 写文件时如果元数据可控，可用 phar:// wrapper 触发反序列化；title 字符过滤 '#[/\?*.]#' 不防 ../ → tar 软连接可写 /var/www/html。
quality: medium
full_path: 五月公开赛writeup｜web篇.full.md
meta_path: 五月公开赛writeup｜web篇.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 五月公开赛writeup｜web篇。PHP 笔记导出支持 zip/tar 自切换，title 字符过滤不严可注 Phar 元数据触发反序列化。。关键路径：TemplatePlay + MyNotes 两题 → 登录 admin/admin → 看到 Admin Page 调 is_admin() 读 /flag → 关键函数 is_admin() 校验 $_SESSION['admin'] ...
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/73628.html
reasoning_chain:
- www.zip 源码分析 → Admin Page 调 is_admin() 读 /flag → 触发点：鉴权函数
- 假设：is_admin 校验 $_SESSION['admin'] === true → 动作：找 session 修改入口
- Export notes ?type= 切换 zip/tar → type=tar 用 PharData::startBuffering/stopBuffering
- title 过滤 preg_replace('/[^!-~]/', '-') + '#[/\\?*.]#' → '-'
- 假设：过滤防 path traversal 但不防 phar 元数据 → 动作：title 注 'phar://'
- 动作：SELECT writefile() 落 so + load_extension('./exp.so', 'init') → 触发反序列化
- 观察：服务端 include phar:// 触发 __destruct → 完成
failed_attempts:
- 试图直接 ?type=phar → 失败：白名单只允许 zip/tar
- 试图注 ../ 到 tar 元数据 → 失败：title 过滤 /\\?*.
- 试图触发 PHP filter chain → 失败：缺少 wrap chain 入口
key_observations:
- PharData/ZipArchive 写文件时如果元数据可控，可用 phar:// wrapper 触发反序列化
- title 字符过滤 '#[/\\?*.]#' 不防 ../ → tar 软连接可写 /var/www/html
- PHP Phar 协议反序列化是文件类函数通用旁路
prerequisites:
- PHP Phar 反序列化原理（__destruct 触发链）
- PHP 路径穿越与软连接
- PharData / ZipArchive 类用法
- PHP session 反序列化机制
---
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

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]