---
title: Hugging Face 仿冒 OpenAI 仓库供应链投毒分析
contest: 事件分析
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags: [供应链投毒, OpenAI, Hugging Face, MITRE ATT&CK, 凭证窃取]
attack_chain: |
  1. 仿冒 OpenAI 官方仓库在 Hugging Face 上发布（含恶意代码）
  2. 受害者 pip/clone 时执行恶意 payload → 钓鱼初始访问 T1661
  3. 防御规避: 禁用安全工具 SSL 验证 (T1562.001) + 添加 Defender 排除 (T1547.001)
  4. 凭证访问: 浏览器凭证 (T1555.003) + 凭据文件未保护存储 (T1552.001) + 私钥窃取 (T1552.004)
  5. 数据外泄: 6 大类目标 - 浏览器 (Cookie/密码/密钥) / Discord 令牌 / 加密货币钱包 / SSH-FTP-VPN 凭证 / 本地敏感文件 / 系统信息截图
  6. 通过 C2 信道 (T1041) 外泄至 bmwqia84@mail.ru SMTP 服务器
key_payload: |
  # 恶意样本目标清单 (6 类):
  # 1. 浏览器: Chromium/Gecko Cookie/密码/加密密钥/历史/会话令牌
  # 2. 即时通讯: Discord 令牌/数据库/主密钥
  # 3. 加密货币: 钱包 + 浏览器扩展
  # 4. 远程访问: SSH/FTP/VPN 凭证 (含 FileZilla)
  # 5. 敏感文件: 本地敏感文件 + 钱包种子/密钥
  # 6. 系统信息: 完整系统信息 + 屏幕截图
one_liner: Hugging Face 仿冒 OpenAI 仓库的 RedLine/Stealer 类投毒事件，按 MITRE ATT&CK 战术编号梳理的标准化分析。
lesson: |
  供应链投毒的标准写法:
  - 仿冒品牌 (OpenAI) + 合理命名 (whisper/gpt-4 热门仓库名) 降低用户警惕
  - 投递后立即做 SSL Pinning bypass + 杀软排除 (T1562.001/T1547.001) 以保证后续扫描不被发现
  - 6 大类目标覆盖浏览器/IM/币圈/远程访问/本地文件/系统信息，几乎是 RedLine/Vidar/Raccoon 标配
  - 注册时间 2026-02-16 + Cloudflare 解析 + TUCOWS.COM 注册商 → 攻击者提前 12 个月准备域名
quality: medium
---

# Hugging Face 仿冒 OpenAI 仓库供应链投毒

> 来源: ctfiot.com 307729

## 事件概况

攻击者在 Hugging Face 上传仿冒 OpenAI 官方的仓库（含 `whisper` / `gpt-4` / `transformers` 等热门名字变体），开发者 pip install 或 git clone 时触发恶意 payload。

| 属性 | 详情 |
|------|------|
| 注册时间 | 2026-02-16 |
| 到期时间 | 2027-02-16 |
| 注册商 | TUCOWS.COM, CO. |
| 名称服务器 | deborah.ns.cloudflare.com / west.ns.cloudflare.com |
| 当前解析 IP | 172.67.165.218 / 104.21.66.235 |
| 安全状态 | 未见公开恶意标记 |

## 6 大数据窃取目标

1. **浏览器数据** — Chromium/Gecko Cookie、保存的密码、加密密钥、浏览历史、会话令牌
2. **即时通讯** — Discord 令牌、本地数据库、主密钥
3. **加密货币** — 加密货币钱包 + 浏览器扩展
4. **远程访问** — SSH / FTP / VPN 凭证及配置文件（含 FileZilla）
5. **敏感文件** — 本地敏感文件 + 钱包种子/密钥
6. **系统信息** — 完整系统信息 + 屏幕截图

## MITRE ATT&CK 战术映射

| 战术阶段 | 技术编号 | 技术名称 |
|----------|----------|----------|
| 初始访问 | T1661 | 钓鱼攻击（社会工程） |
| 初始访问 | T1526 | 供应链攻陷 |
| 持久化 | T1547.001 | 引导登录完成时自启动（添加 Defender 排除列表） |
| 防御规避 | T1562.001 | 禁用安全工具（禁用 SSL 验证） |
| 防御规避 | T1562.001 | 添加安全工具排除项 |
| 防御规避 | T1497.001 | 虚拟机/沙箱检测 |
| 凭证访问 | T1555.003 | 浏览器凭证窃取 |
| 凭证访问 | T1552.001 | 凭据文件未保护存储 |
| 凭证访问 | T1552.004 | 私钥窃取 |
| 发现 | T1592.004 | 收集受害者主机信息 |
| 数据外泄 | T1041 | 通过 C2 信道外泄数据 |

## 评价

是一份"标准化"的供应链投毒事件分析报告，ATT&CK 编号齐全 + 数据目标分类清晰，6 大类几乎与 RedLine / Vidar / Raccoon 等主流 stealer 一致。

缺技术细节（具体 payload / 投递机制 / 实际 C2 通信样本），但作为 ATT&CK 映射 + IOC (恶意域名/IP/注册商) 的事件卡，够用。
