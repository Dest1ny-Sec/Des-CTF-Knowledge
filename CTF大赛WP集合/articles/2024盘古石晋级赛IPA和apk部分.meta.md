---
title: 2024 盘古石晋级赛 IPA 和 APK 部分（iOS + Android 取证）
contest: 2024 盘古石晋级赛
year: 2024
difficulty: medium
vuln_type: [forensic_disk, misc_unknown]
tags: [iOS IPA 毛雪柳手机取证, iCost 记账 APP default.realm Realm 数据库, Mattermost 内部 IM, base.apk 伏季雅手机, 威尼斯诈骗 APP, w2a.W2Ah5.jsgjzfx.org.cn 包名, __W2A__h5.jsgjzfx.org.cn 打包 ID, io.dcloud.PandoraEntry 启动项, 雷电 APP 智能分析, app.db Mattermost]
attack_chain:
  - 毛雪柳 iOS: iCost 记账 APP Documents/default.realm → realm 数据库
  - 2 月收入 9600+2357=11957 元
  - Mattermost IM 共享目录 /private/var/mobile/Containers/Shared/AppGroup/BBE0D501-AB0B-422E-9B4D-02E2D86130D4
  - gxyt 老板 user_id=enf863dp1ifi3ffos7bpduynny + gxyt@163.com
  - 私聊频道 "发财" 加入时间 1713931168391 → 2024-04-24-11-59-28
  - 老板最后发送时间 1714011890182 → 2024-04-25-10-24-50
  - 伏季雅 Android: 诈骗 APP 威尼斯，包名 w2a.W2Ah5.jsgjzfx.org.cn
  - 服务器 192.168.137.125 + 打包 ID __W2A__h5.jsgjzfx.org.cn + 启动 io.dcloud.PandoraEntry
  - 义言手机 Mattermost app.db 服务器 192.168.137.97
  - 数据库名 aHR0cDovLzE5Mi4xNjguMTM3Ljk3OjgwNjU=.db
key_payload: "iCost APP default.realm + realm studio 2 月 type=1 收入 11957"
one_liner: 盘古石晋级赛：iOS 毛雪柳记账 iCost+ Mattermost + Android 伏季雅威尼斯诈骗 APP + 义言 Mattermost 多检材协同；雷电 APP 智能分析一键导出 base.apk 元数据。
lesson: iOS 取证从 iTunes 备份 + 雷电 APP 分析 + realm studio 看 realm 数据库是 2024 主流流程；Mattermost 数据库名 = base64(URL).db 是反取证隐藏套路；雷电模拟器自带 APP 智能分析比 jadx 快很多。
quality: high
---

# 2024 盘古石晋级赛 IPA + APK 取证

## iOS 毛雪柳取证

### Q1 记账 APP 数据库
- APP: **iCost**  
- 数据库: `default.realm`（Realm 格式，Documents 目录）  
- 答案: `default.realm`

### Q2 2 月总收入
- 用 Realm Studio 打开 `default.realm`  
- `type=1` 收入筛选  
- 2 月内两条：9600 + 2357 = **11957**

### Q3 内部 IM 老板邮箱
- APP: **Mattermost**  
- 共享目录: `/private/var/mobile/Containers/Shared/AppGroup/BBE0D501-AB0B-422E-9B4D-02E2D86130D4`  
- user_id: `enf863dp1ifi3ffos7bpduynny`  
- 邮箱: **`gxyt@163.com`**

### Q4 老板加入私聊频道时间
- 私聊频道名: **发财**（vs 群聊 Off-Topic、Town Square）  
- 加入时间戳: 1713931168391  
- 转换: **2024-04-24-11-59-28**

### Q5 老板最后发送时间
- 时间戳: 1714011890182  
- 转换: **2024-04-25-10-24-50**

## Android 伏季雅取证

### Q1 诈骗 APP 包名
- APP: **威尼斯**  
- 包名: **`w2a.W2Ah5.jsgjzfx.org.cn`**

### Q2 服务器地址
- 用雷电 APP 智能分析 base.apk  
- 服务器: **192.168.137.125**

### Q3 打包 ID
- `__W2A__h5.jsgjzfx.org.cn`

### Q4 主启动项
- `io.dcloud.PandoraEntry`（HBuilder 标准入口）

## 义言 Mattermost

- 服务器地址: `192.168.137.97`  
- 数据库名: `aHR0cDovLzE5Mi4xNjguMTM3Ljk3OjgwNjU=.db`（base64 解码 = `http://192.168.137.97:8065`，是 Mattermost 默认端口 8065）  
- 团队内部沟通群用户数: 待补
