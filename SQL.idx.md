# SQL.idx — 按需分段读取

总行数: ~2611 | 使用: Read offset=行号 limit=行数 只读目标章节

## 快速导航
- L1-L24: 联合注入Payload（查字段/库/表/列/数据）
- L26-L53: 报错注入（extractvalue/updatexml/BigInt/floor）
- L59-L100: 堆叠注入
- L100-L180: 盲注（bool/时间）
- L180-L450: WAF绕过合集
- L450-L700: 宽字节注入（GBK）
- L700-L1100: 二次注入/DNS注入
- L1100-L1500: SQL注入读写文件
- L1500-L2000: 各种数据库特殊技巧（MSSQL/Oracle/PostgreSQL）
- L2000-L2611: 靶场WP/案例

## 常用搜索关键词
```
grep -n "宽字节\|GBK\|bigint\|updatexml\|堆叠\|盲注\|WAF\|绕过" CTF知识库/SQL.md
```
