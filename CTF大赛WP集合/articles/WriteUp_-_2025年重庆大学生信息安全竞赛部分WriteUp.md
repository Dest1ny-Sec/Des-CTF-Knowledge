# WriteUp | 2025年重庆大学生信息安全竞赛部分WriteUp

> 原文: https://www.ctfiot.com/287136.html
> ID: 287136

<?php

error_reporting(0);

if($_GET['file']) {

$file=$_GET['file'];

$file=base64_decode($file);

if(strstr($file,'./')){

die('');

}

include'upload/'.$file.'.png';

}

?>

flag{th1s1sf14g}

#include<stdio.h>

intmain()

{

char b[]="cjfor~c=~?|v &ti";

char a[16];

inti;

for(i=0;i<15;i++)

{

a[i]=b[i]^(i+5);

}

puts(a);

return0;

}

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862604-wxsync-2025-12-33fd2d254a156e7e25a62a0a2ca40414.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862606-wxsync-2025-12-c216268e92057ace946d1d3f33b02cde.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862608-wxsync-2025-12-d8b83f85b4a3e57f215dc20973cfb12f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862609-wxsync-2025-12-470e9d58151a20b9273ab05b924e2349.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862611-wxsync-2025-12-42b892a6548d459fb5d501eb8bf692a4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862613-wxsync-2025-12-e4a28733621628f6ee85c81ef28284fb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862614-wxsync-2025-12-f36e22a08b818a8aeb1d2aec18e25a4a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862616-wxsync-2025-12-b371e6f9b3ff3a0429812d13e0ef4ea6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862619-wxsync-2025-12-42a87bd85b7cccb4e3e10e7770141a0e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765862621-wxsync-2025-12-4f9f0392c5df415664192ef6d309adea.png)