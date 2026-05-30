# corCTF 2024-the-conspiracy writeup

> 原文: https://www.ctfiot.com/195925.html
> ID: 195925


```
1. 从一个csv里读取源地址，目的地址，需要发送的消息。第一列源ip，第二列为目的ip，第三列为明文消息。
2. 通过encrypt函数加密消息，加密函数逻辑也很简单，读取消息中每个字符将其转换为ascii码，然后随机生成一个1-100的整数key，每个字符的密文=明文字符ascii码*随机key。
3. 每给对方发送一个消息后，需继续在把对应的key发送给对方
try:
   x = list(payload)
   if num % 2 != 0:
       message_num_list.append(eval(payload.decode('utf-8')))
   else:
       key_list.append(eval(payload.decode('utf-8')))
   num+=1
except:
   pass
message_num_list = [[1234,578,325],[5958,4828,1234,2222],[2222]]
key_list = [[10,20,30],[11,24,32,13],[42]]
message_num_list[0][0] = 3104
key_list[0][0] = 32
3104 / 32 = 97
97对应的字符是a
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/6-1722067948.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/2-1722067949.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1722067950.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1722067951.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1722067952.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/6-1722067953.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1722067954.png)