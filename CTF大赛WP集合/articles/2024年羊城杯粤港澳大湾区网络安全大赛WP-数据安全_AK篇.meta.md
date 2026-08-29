---
title: 2024 羊城杯数据安全 AK 篇（CSV 数据清洗 + 身份证校验）
contest: 2024 羊城杯粤港澳大湾区网络安全大赛
year: 2024
difficulty: easy
vuln_type: [misc_unknown, sqli]
tags: [CSV 字段整理, 身份证校验码, 性别位奇偶, 手机号段黑名单, 中文姓名正则, error.log 解析, tshark json.value.string, garbled data 过滤]
attack_chain:
  - tshark -Y http.request.method==POST -T fields -e json.value.string 抽 POST body
  - 8 字段正则分类（手机/身份证/出生日期/性别/密码/姓名/编号/用户名）
  - validate_id_number: 加权 [7,9,10,5,8,4,2] % 11 + check_codes 10X98765432
  - validate_sex_idcard: 身份证倒数第 2 位奇偶 vs 男/女
  - validate_phone: 53 段手机号前缀白名单
  - error.log: re.search 'username=.*' 取账户行 + '\x81\xe4\xb8\xba'/'为' 关键字行拼 password
  - parser2list: 用户名/姓名首末保留+中间 * 化 + 身份证 6+4+8 * 化 + 手机号 3+4+4
  - hashlib.md5(password.encode()).hexdigest() 加密字段
key_payload: "if int(idcard[-2]) % 2 == 0: idcard_sex = \"女\" else: idcard_sex = \"男\""
one_liner: 数据安全 AK 流水线：tshark 抽 POST→正则按字段分类→身份证 GB 11643 校验+性别位+手机号段白名单→写 garbage_data.csv。
lesson: 身份证 18 位校验码是 GB 11643 强约束（加权 [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2] 再 % 11 对 '10X98765432'），手机号段归属地可作反欺诈证据；error.log 解析要按业务中文关键字定位上下文（"为" = 输入密码提示）。
quality: medium
---

# 2024 羊城杯数据安全 AK 篇

**data-analy1** 流水线，三段脚本串成一个数据清洗任务：

## Step 1：tshark 抽 HTTP POST
```bash
tshark -r data.pcapng -Y http.request.method==POST -T fields -e json.value.string > 1.csv
```

## Step 2：CSV 字段重整
8 字段正则字典：
```python
field_patterns = {
    '手机号码': r'^d{11}$',
    '身份证号': r'^d{17}[dX]$',
    '出生日期': r'^d{8}$',
    '性别': r'^(男|女)$',
    '密码': r'^[a-fA-Fd]{32}$',
    '姓名': r'^[u4e00-u9fff]+$',
}
```
遍历 row 按 match_field 填到 8 字段 result_row；编号 1-10000 数字单独成列，其余归用户名。

## Step 3：垃圾数据过滤（garbage_data.csv）
四类校验：
- **validate_username**：`^[a-zA-Z0-9]+$`  
- **validate_name**：`^[u4e00-u9fa5]+$`（CJK 基本区）  
- **validate_sex_idcard**：身份证倒数第 2 位奇偶对男女  
- **validate_birth**：birth == idcard[6:14]  
- **validate_id_number**（GB 11643 完整校验）：  
  ```python
  weights = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
  total = sum(int(id_number[i])*weights[i] for i in range(17))
  remainder = total % 11
  check_codes = '10X98765432'
  if check_codes[remainder] != id_number[-1]: return False
  ```
- **validate_phone**：53 段前缀白名单（`734/735/736/.../799`）

任意一项 False → 写入 garbage_data.csv。

## Step 4：error.log 解析 + 脱敏
```python
match = re.search(r'username=.*', line)
if '\x81\xe4\xb8\xba' in line: password = line.strip().split(': ')[-1][:-2]
elif '\xe5\x9c\xa8\xef\xbc\x81' in line: password = ''  # 失败无密码
```
然后 `parser2list` 脱敏：
- 用户名：`u[0]+'*'*(len-2)+u[-1]`（2 字符只首+`*`）  
- 密码：`md5(password).hexdigest()`  
- 姓名：同用户名  
- 身份证：`'*'*6 + idcard[6:10] + '*'*8`（省市区+生年）  
- 手机：`phone[:3] + '*'*4 + phone[7:]`

最后按校验通过的写 `final.txt`，其余 `no_final.txt`。
