# JWT.idx — 按需分段读取

总行数: ~424 | 使用: Read offset=行号 limit=行数 只读目标章节

## 快速导航
- L1-L24: JWT概述/传统Cookie认证
- L25-L69: JWT组成（header/payload/signature结构）
- L70-L133: JWT安全-加密算法（空加密算法None/RSA改HMAC）
- L134-L201: 密钥爆破/KID参数利用（任意文件读取/SQL注入/命令执行）
- L196-L207: JKU/X5U参数/信息泄漏
- L208-L257: JWT Tools（在线工具/c/jwt-cracker/脚本）
- L258-L414: JWT攻击案例（信息泄漏/None算法/弱密码/修改签名算法）
- L415-L424: Referer

## 常用搜索关键词
```
grep -n "None\|alg\|KID\|JKU\|HS256\|RS256\|密钥\|爆破\|cracker\|jwt.io\|header\|payload" CTF知识库/JWT.md
```
