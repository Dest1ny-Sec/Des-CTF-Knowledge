# php代码审计.idx — 按需分段读取

总行数: ~1641 | 使用: Read offset=行号 limit=行数 只读目标章节

## 快速导航
- L1-L100: PHP弱类型比较（==/===/hash比较/0e绕过/md5碰撞/数组绕过）
- L101-L320: Hash比较操作符（md5碰撞脚本/恒为真语句/特殊md5值）
- L321-L400: 十六进制转换/json绕过
- L401-L519: PHP内置函数松散性（MD5/SHA1/switch/strcmp/array_search/in_array绕过）
- L520-L675: preg_match绕过（数组绕过/PCRE回溯次数限制/换行符绕过）
- L676-L805: 变量覆盖（extract/parse_str/import_request_variables/$$变量覆盖/register_globals）
- L806-L969: is_numeric绕过/空白字符绕过过滤
- L970-L989: 多重加密
- L990-L1112: SQL注入 WITH ROLLUP绕过
- L1113-L1174: ereg正则%00截断
- L1175-L1251: session绕过/密码md5比较绕过
- L1252-L1322: url二次编码绕过/sql闭合绕过/x-forwarded-for绕过
- L1323-L1437: intval四舍五入/浮点数精度/常见截断（iconv/ereg/move_uploaded_file/include）
- L1438-L1641: strpos数组绕过/十六进制数字比较/数字验证正则绕过/switch字符与0比较/数组绕过逻辑

## 常用搜索关键词
```
grep -n "弱类型\|preg_match\|变量覆盖\|extract\|strcmp\|md5\|截断\|intval\|register_globals\|PCRE\|%00" CTF知识库/php代码审计.md
```
