---
title: 冠军Writeup大放送 | DataCon2022域名体系安全赛道之"NDNS"战队
contest: DataCon2022 域名体系安全
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [DataCon, 域名分类, CDN, 动态域名, Sinkhole, Domain Parking, Webhosting, FastFlux, 域名接管, CNAME, TXT归属权, DNSSEC, DMARC]
attack_chain:
  - 国防科技大学 NDNS 战队 (DNSLab) 域名体系安全冠军
  - 域名分类: 8 类 (CDN/动态/隐藏/Sinkhole/Parking/Webhosting/p2p/FastFlux)
  - CDN 特征: 大量 CNAME, SLD FQDN 多, IP 数量多分布广
  - 判定: SLD CNAME > 100, IP 地理位置数 > 0/2 (得分 100/22)
  - 隐藏域名 (GFW): IP ASO 集中 (Google/Twitter/Facebook/Dropbox), IP 解析 > 14W
  - 动态域名: 花生壳/3322/dnspod/aliyun/huaweicloud
  - Sinkhole: NS 改研究者控制 DNS, IP 集中
  - Domain Parking: 停放服务商 Sedo/Bodis/IONOS
  - Webhosting: 000Webhost/Wix.com/Squarespace
  - FastFlux: storm worm 2006, 频繁换 IP/NS
  - 域名接管 level1-5: CNAME 注销 + TXT 归属权验证
  - level1: 无验证直接接管
  - level2-5: TXT 记录/文件/API 验证差异化
key_payload: 'CDN CNAME>100 + GFW ASO+14W + 域名接管 CNAME/TXT'
one_liner: DataCon2022 域名体系安全冠军 NDNS：8 类域名分类判定指标 + 5 关域名接管 (CNAME + TXT 归属权验证)。
lesson: CDN 域名为厂商 SLD 下的 CNAME 链 (如 admin.datacon.cdn.)；GFW 隐藏域名 IP ASO 集中 (Google/Twitter/Facebook) 解析 >14W；域名接管是 CNAME 注销 + TXT 验证绕过。
quality: high
---

# 冠军Writeup大放送 | DataCon2022域名体系安全赛道之"NDNS"战队

## 概览
- **来源**: ctfiot 92019
- **赛事**: DataCon2022 域名体系安全赛道冠军
- **战队**: 国防科技大学 NDNS (DNSLab, 指导老师许成喜)
- **难度**: ⭐⭐⭐⭐

## 域名分类 8 类

| 类型 | 特征 | 判定指标 |
|------|------|----------|
| CDN | 大量 CNAME, SLD FQDN 多, IP 多 | SLD CNAME > 100, IP 地理位置 > 0/2 |
| 隐藏 (GFW) | IP ASO 集中 (Google/Twitter/Facebook/Dropbox) | IP 解析 > 14W |
| 动态域名 | 客户端软件上报 IP | 花生壳/3322/dnspod/aliyun |
| Domain Parking | Sedo/Bodis/IONOS, 单 IP 大量域名 | IP 解析 > 1000 |
| Webhosting | 000Webhost/Wix/Squarespace | 特定服务商 |
| Sinkhole | NS 改研究者控制 | IP 集中, 恶意域名 |
| P2P | 单域名多 IP | 单一域名多 IP |
| FastFlux | storm worm 2006 频繁换 | 频繁换 IP/NS |

## CDN 判定
- 29581826 条 CNAME 记录
- 遍历 SLD 统计 CNAME 数
- 100+ 阈值 → CDN 候选
- 14 万+ 解析 → GFW 隐藏

## 域名接管 5 关

### level1: 无验证
- `datacon2022.secrank.cn` CNAME `admin.datacon.cdn.` 未注销
- 直接注册 CDN 平台账号 + 添加自定义域名

### level2-5: 验证机制
- TXT 记录: `dns_verify=xxx`
- 文件验证: 服务商访问指定目录
- API 验证: 调用 DNS API
- DMARC rua 报告: 探测 CDN 管理员邮箱

## 关键 Python 代码
```python
# 统计 SLD CNAME 数
SLD_Ccount = {}
for row in f_csv:
    if row[3] == '5' and row[4]:
        sld = row[4].split('.')[-1]
        SLD_Ccount[sld] = SLD_Ccount.get(sld, 0) + 1

# 统计 SLD FQDN 数
CDN_fqdn_count = {sld: 0 for sld in CDN_list1}
for row in f_csv:
    sld = row[0]
    if sld in CDN_list1:
        CDN_fqdn_count[sld] += 1

# 统计 IP 地理位置
fqdn_region_list = {}
for row in f_csv:
    if row[3] == '1':
        sld = row[0]
        if sld in CDN_list1:
            region = row[7]
            fqdn_region_list.setdefault(row[1], []).append(region)
```

## 工具
- pybloom_live 布隆过滤器
- tqdm 进度条
- DNS 解析服务器 (公网)
- HTTP 服务器 (公网)

## 教学
- DNS 安全研究: 域名分类 + 域名接管
- CDN 厂商: 阿里云/腾讯云/Cloudflare/七牛/网宿
- 域名分类机器学习: FQDN 特征 + IP 分布 + ASO 集中度
