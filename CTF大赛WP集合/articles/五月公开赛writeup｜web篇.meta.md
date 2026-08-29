---
title: 五月公开赛writeup｜web篇
contest: 五月公开赛 2022
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [PHP, SESSION, PharData, ZipArchive, is_admin, file_get_contents, zip slip]
attack_chain:
  - TemplatePlay + MyNotes 两题
  - 登录 admin/admin → 看到 Admin Page 调 is_admin() 读 /flag
  - 关键函数 is_admin() 校验 $_SESSION['admin'] === true
  - 漏洞: Export notes 导出 zip/tar 类型由 ?type= 控制
  - type=tar 用 PharData 类 startBuffering/stopBuffering
  - title 字符过滤 preg_replace('/[^!-~]/', '-') + '#[/\?*.]#' → '-'
  - 注释 "delete suspicious characters" 但仍可注入 ../ 软连接或 phar 元数据
  - 攻击面: Phar 反序列化 (phar:// wrapper) + zip slip 路径穿越
key_payload: '?type=tar + title 含 phar 元数据触发反序列化'
one_liner: PHP 笔记导出支持 zip/tar 自切换，title 字符过滤不严可注 Phar 元数据触发反序列化。
lesson: PHP PharData/ZipArchive 写文件时如果元数据可控，可用 phar:// wrapper 触发反序列化；title 字符过滤 '#[/\?*.]#' 不防 ../ → tar 软连接可写 /var/www/html。
quality: medium
---

# 五月公开赛writeup｜web篇

## 概览
- **来源**: ctfiot 73628
- **赛事**: 五月公开赛 2022
- **题目**: TemplatePlay + MyNotes

## MyNotes 源码核心

### config.php
```php
define('TEMP_DIR', '/var/www/tmp');
```

### init.php
```php
session_save_path(TEMP_DIR);  // /var/www/tmp
session_start();
```

### lib.php 关键函数
```php
function is_admin() {
    if (!isset($_SESSION['admin'])) return false;
    return $_SESSION['admin'] === true;
}

function validate_user($user) {
    return preg_match('/A[0-9A-Z_-]{4,64}z/i', $user);
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
```

### export.php 导出
```php
$type = $_GET['type'] ?? 'zip';
$filename = get_user() . '-' . bin2hex(random_bytes(8)) . '.' . $type;
$filename = str_replace('..', '', $filename);
$path = TEMP_DIR . '/' . $filename;

if ($type === 'tar') {
    $archive = new PharData($path);
    $archive->startBuffering();
} else {
    $archive = new ZipArchive();
    $archive->open($path, ZIPARCHIVE::CREATE | ZipArchive::OVERWRITE);
}

for (...) {
    $title = $note['title'];
    $title = preg_replace('/[^!-~]/', '-', $title);
    $title = preg_replace('#[/\?*.]#', '-', $title);  // delete suspicious
    $archive->addFromString("{$index}_{$title}.json", json_encode($note));
}
```

## 攻击面
- **PharData 元数据**: tar 归档保存 Phar 元数据 → `phar://xxx.tar` wrapper 触发反序列化
- **title 过滤不全**: `'#[/\?*.]#'` 只过滤 4 个字符 → 可注 `\` (Windows) 或 `..\`
- **session_save_path 在 /var/www/tmp**: 配合 session 上传进度 + LFI 经典

## flag 路径
- Admin Page → `file_get_contents('/flag')` 输出
