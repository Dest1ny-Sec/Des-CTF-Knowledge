---
title: 西湖论剑-信呼oa审计复盘
contest: 西湖论剑 信呼OA
year: 2021
difficulty: medium
vuln_type: web_unknown
tags: [信呼OA, source-audit, seay-audit, phpstudy, php7.3.4, xdebug, code-audit, LFI, view-php-traversal, base64-surl, phpinfo-exposure]
attack_chain:
- 题目源码:信呼OA v2.3.1(seay源代码审计系统+phpstudypro+php7.3.4+wind10+vscode+xdebug)
- 关键代码:
  - $tplpaths = ''.$temppath.''.$d.''.$m.'/';
  - $temppath = ''.ROOT_PATH.'/'.$p.'/';
  - $p = PROJECT;
  - $xhrock = new $clsname();
  - $clsname = ''.$m.'ClassAction';
  - $m = $rock->get('m', $m);
  - $surl = $this->jm->base64decode($this->get('surl'));
  - $actfile = $rock->strformat('?0/?1Action.php',$actpath, $m);
  - $actbstr = $xhrock->$actname();
  - $actname = ''.$a.'Action';
  - $a = $rock->get('a', $a);
- 漏洞:view.php/../../phpinfo.php 目录穿越
- payload:view.php?m=index&a=getshtml&surl=Li4vLi4vcGhwaW5mbw==
- (Li4vLi4vcGhwaW5mbw== = ../../phpinfo base64编码)
- 审计思路:跟踪m/a参数+类加载+方法分发
key_payload: view.php?m=index&a=getshtml&surl=Li4vLi4vcGhwaW5mbw==
one_liner: 西湖论剑信呼OA v2.3.1审计复盘,seay+phpstudy+php7.3.4+xdebug环境搭建,view.php目录穿越(surl base64编码../../phpinfo)+ClassAction方法分发+m/a参数可控。
lesson: 信呼OA是国产化OA代表,代码审计+seay+xdebug是标准工作流;view.php的surl base64可控是LFI常见入口;ClassAction+Action.php方法是国产CMS通用模式。
quality: medium
---

## 题目列表

1道信呼OA代码审计:v2.3.1

## 关键考点

### 环境搭建
- seay源代码审计系统
- phpstudypro
- php7.3.4
- Windows 10
- VSCode
- xdebug

### 关键代码
```php
$tplpaths = ''.$temppath.''.$d.''.$m.'/';
$tplname .= '.'.$xhrock->tpldom.'';
$temppath = ''.ROOT_PATH.'/'.$p.'/';
$p = PROJECT;
$xhrock = new $clsname();
$clsname = ''.$m.'ClassAction';
$m = $rock->get('m', $m);
$surl = $this->jm->base64decode($this->get('surl'));
$actfile = $rock->strformat('?0/?1Action.php',$actpath, $m);
$actbstr = $xhrock->$actname();
$actname = ''.$a.'Action';
$a = $rock->get('a', $a);
```

### 漏洞:view.php目录穿越
- 入口:view.php
- 路径穿越:surl参数base64编码
- payload:view.php?m=index&a=getshtml&surl=Li4vLi4vcGhwaW5mbw==
- 解析:`../../phpinfo.php` (base64解码)
- 触发:file_exists或include 任意php文件

### 审计思路
1. 入口文件view.php
2. m参数控制类名($m.'ClassAction')
3. a参数控制方法名($a.'Action')
4. 类加载机制:`new $clsname()`
5. 模板路径拼接:`$temppath.''.$d.''.$m.'/'`
6. surl参数base64解码后进入文件操作
7. 触发目录穿越读任意PHP

### 国产CMS通用模式
- ClassAction + Action.php 命名约定
- m/a参数分发
- 模板路径在views/下
- base64编码的surl绕过简单字符串检查
- root_path拼接

## 实战价值
- 信呼OA是国产化OA代表,代码审计+seay+xdebug是标准工作流
- view.php的surl base64可控是LFI常见入口
- ClassAction+Action.php方法是国产CMS通用模式
- m/a参数分发是MVC简化版,审计入口
- phpstudy+php7.3.4是国产PHP环境标配
