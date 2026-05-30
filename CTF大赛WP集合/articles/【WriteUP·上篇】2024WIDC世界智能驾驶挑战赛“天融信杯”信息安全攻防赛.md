# 【WriteUP·上篇】2024WIDC世界智能驾驶挑战赛“天融信杯”信息安全攻防赛

> 原文: https://www.ctfiot.com/185724.html
> ID: 185724

某车辆OEM制造厂商遭受勒索病毒攻击，重要数据被加密，请帮助厂商恢复重要数据

（1）从初始地址提取每笔交易的calldatahttps://sepolia.etherscan.io/address/0xa9bf5b94b191bd39407376dc3af147c367b0ad 9d

（3）直接使用python实现这段代码↓拿到flag

import sys

def decrypt_and_print_flag(encrypted_string):

decrypted_flag = “”

for c in encrypted_string[:67]:  # 只处理前67个字符

decrypted_char = (ord(c) + 3) ^ 9

decrypted_flag += chr(decrypted_char)

print(decrypted_flag)

if __name__ == “__main__”:

if len(sys.argv) != 2:

print(“Usage: python script.py <encrypted_string>”)

sys.exit(1)

encrypted_string = sys.argv[1]

decrypt_and_print_flag(encrypted_string)

（5）转化成ASCII字符串：LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUNJd0RRWUpLb1pJaHZjTkFRRUJCUUFERVFBd0RnSUhBanJKQjAzczV3SURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==

（6）Base64解码得到pem文件：

—–BEGIN PUBLIC KEY—–

MCIwDQYJKoZIhvcNAQEBBQADEQAwDgIHAjrJB03s5wIDAQAB

—–END PUBLIC KEY—–

（8）得到私钥：（n,d）= 627585038806247 119987789848673

对seed使用私钥加密发送给服务端，服务端用公钥解密即可过27服务：

5a6d4e764d47786a613368686133427564484a6f5a7a426a4e3259354e474a68597a4d35595463344e7a46714e57526f4e6a466a4e46565551323957646e704f64586447636d5a5251576b33624756545957356e636e6b3d

（9）转ASCII：

ZmNvMGxja3hha3BudHJoZzBjN2Y5NGJhYzM5YTc4NzFqNWRoNjFjNFVUQ29WdnpOdXdGcmZRQWk3bGVTYW5ncnk=

Base64解码：

fco0lckxakpntrhg0c7f94bac39a7871j5dh61c4UTCoVvzNuwFrfQAi7leSangry

                                                                                                                          

WriteUP系列将持续更新，敬请关注护车行动！

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/5-1717633893.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1717633895.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/2-1717633897.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/7-1717633897.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1717633898.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/5-1717633899.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/10-1717633900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/10-1717633900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1717633903.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/6-1717633904.png)