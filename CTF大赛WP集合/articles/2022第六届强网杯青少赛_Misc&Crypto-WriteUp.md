# 2022第六届强网杯青少赛 Misc&Crypto-WriteUp

> 原文: https://www.ctfiot.com/71039.html
> ID: 71039

import base64f = open('chuyinweilai.png','r')content = base64.b64decode(f.read())with open('new.png','wb') as f:f.write(content)

import base64import binasciif = open('chuyinweilai.png','r')content = base64.b64decode(f.read())r = ""for i in range(0,len(content),2): #分奇偶写入文件 r += str(hex(content[i+1]))[2:].zfill(2) #这里zfill(2)很重要 一定要填充0 否则结果大相径庭 r += str(hex(content[i]))[2:].zfill(2)content = binascii.unhexlify(r)with open('new.png','wb') as f:f.write(content)

cryher = "FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]"res = ""for i in cryher: res += chr(ord(i)^32)
content = "VXPSdQceLWWOcLSOcOLWPUVLQfVVfRPOPbSS"res = "flag{"for i in content: if i.isupper(): #大写 -31 res += chr(ord(i)-31) else: #小写 -32 res += chr(ord(i)-32)res += "}"print(res.lower())

免责声明

由于传播、利用本公众号NGC660安全实验室所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，公众号NGC600安全实验室及作者不为此承担任何责任，一旦造成后果请自行承担！如有侵权烦请告知，我们会立即删除并致歉。谢谢！


```
import base64f = open('chuyinweilai.png','r')content = base64.b64decode(f.read())with open('new.png','wb') as f:f.write(content)
```



```
import base64import binasciif = open('chuyinweilai.png','r')content = base64.b64decode(f.read())r = ""for i in range(0,len(content),2): #分奇偶写入文件 r += str(hex(content[i+1]))[2:].zfill(2) #这里zfill(2)很重要 一定要填充0 否则结果大相径庭 r += str(hex(content[i]))[2:].zfill(2)content = binascii.unhexlify(r)with open('new.png','wb') as f:f.write(content)
```



```
cryher = "FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]"res = ""for i in cryher: res += chr(ord(i)^32)
content = "VXPSdQceLWWOcLSOcOLWPUVLQfVVfRPOPbSS"res = "flag{"for i in content: if i.isupper(): #大写 -31 res += chr(ord(i)-31) else: #小写 -32 res += chr(ord(i)-32)res += "}"print(res.lower())
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667724741.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1667724776.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1667724781.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1667724782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667724783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1667724785.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1667724786.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1667724790.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1667724792.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667724793.png)