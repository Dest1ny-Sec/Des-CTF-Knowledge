# [强网杯S9]Qcalc赛题解析

> 原文: https://www.ctfiot.com/289098.html
> ID: 289098

fromflaskimportFlask, requestimportbase64app = Flask(__name__)@app.route('/receive', methods=['POST','GET'])defreceive_data():
ifrequest.method =='POST': data = request.form.get('flag')orrequest.form.get('data')else: data = request.args.get('flag')orrequest.args.get('data')ifdata:
try:# 尝试base64解码 decoded = base64.b64decode(data).decode('utf-8')print(f"解码后的数据:{decoded}")withopen('received_flags.txt','a')asf: f.write(f"{decoded}n")
except:
print(f"原始数据:{data}")withopen('received_flags.txt','a')asf: f.write(f"{data}n")print(f"收到请求:{request.method}")print(f"Headers:{dict(request.headers)}")print(f"Form data:{request.form}")print(f"Args:{request.args}")return"OK",200if__name__ =='__main__': app.run(host='0.0.0.0', port=8000, debug=True)

看雪ID：Shangwendada

https://bbs.kanxue.com/user-home-979679.htm

*本文为看雪论坛优秀文章，由Shangwendada原创，转载请注明来自看雪社区

# 往期推荐

V8 Bytecode反汇编/反编译不完全指南

静态程序分析之数据流分析(Foundations + LiveVar Analysis Code)续

tt x-gorgon分析

基于Minifilter实现目录保护软件，自定义保护目录，用户可选择是否允许文件行为

一道简单的RE迷宫题

球分享

球点赞

球在看

点击阅读原文查看更多


```
fromflaskimportFlask, requestimportbase64app = Flask(__name__)@app.route('/receive', methods=['POST','GET'])defreceive_data():
ifrequest.method =='POST': data = request.form.get('flag')orrequest.form.get('data')else: data = request.args.get('flag')orrequest.args.get('data')ifdata:
try:# 尝试base64解码 decoded = base64.b64decode(data).decode('utf-8')print(f"解码后的数据:{decoded}")withopen('received_flags.txt','a')asf: f.write(f"{decoded}n")
except:
print(f"原始数据:{data}")withopen('received_flags.txt','a')asf: f.write(f"{data}n")print(f"收到请求:{request.method}")print(f"Headers:{dict(request.headers)}")print(f"Form data:{request.form}")print(f"Args:{request.args}")return"OK",200if__name__ =='__main__': app.run(host='0.0.0.0', port=8000, debug=True)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829912-wxsync-2025-12-96f81765f21430234c0f6ce1cdd5d288.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829914-wxsync-2025-12-772d75ea4bc2c3eacf1f810679995756.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829916-wxsync-2025-12-080953bc2fca2c9f5653f738c5de865f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829917-wxsync-2025-12-848f04c3845e83552b00ecdd4eb08e4b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829919-wxsync-2025-12-b72aba58555a49517b0f0094a17a78c2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829921-wxsync-2025-12-1db10b4c648020729221bf4620335ccf.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829923-wxsync-2025-12-45861eb94f0c19c283b857ffb1f0e470.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829925-wxsync-2025-12-8af6ff0df046ce2aab534d7c2c5f8a0e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829927-wxsync-2025-12-38b7bcc80b9e9674068b2228be8a76ee.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766829929-wxsync-2025-12-b9b23cfa48e5e940d75c4c5fb1e8c5de.png)