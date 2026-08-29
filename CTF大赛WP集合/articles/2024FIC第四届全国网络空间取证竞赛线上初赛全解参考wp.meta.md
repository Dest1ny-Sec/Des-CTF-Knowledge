---
title: 2024 FIC 第四届全国网络空间取证竞赛 初赛 WP
contest: 第四届全国网络空间取证竞赛 (FIC 2024)
year: 2024
difficulty: hard
vuln_type: [forensic_disk, forensic_memory, misc_unknown]
tags: [杀猪盘, ESXi, vmdk, Docker, MySQL, 若依, RuoYi, jar-反编译, vmdk挂载, 微信取证, iStoreOS, OpenWrt, NasTools, 鲁盒]
attack_chain: ["案：卢某被'杀猪盘'诈骗 → 查李某手机(检材1) + 服务器(检材2) + 赵某PC(检材3)", "ESXi vmdk esxcfg-volume -l 挂载", "微信 wxid 提取 → 赌博群 URL http://www.honglian7001.com/down", "服务器扫 192.168.110.110:8000/login + 密码 limoon890", "docker inspect 9b 看 MYSQL_ROOT_PASSWORD", "ruoyi-admin.jar 解压改 application-druid.yml 启动 /api/shopOrder", "iStoreOS OpenWrt NasTools PassWall2 → token 订阅地址", "TrueCrypt 卷密码 qwerasdfzxcv", "火眼鲁盒 dst01.jpeg 镜像 0.85 缩放"]
key_payload: "ruoyi-admin.jar BOOT-INF/classes/application-druid.yml → MYSQL_ROOT_PASSWORD=my-secret-pw"
one_liner: 杀猪盘综合取证：手机+服务器+PC 三检材联动
lesson: 综合取证赛三大类：微信/QQ 聊天记录；ESXi/Docker 容器部署链路；加密卷密码与镜像；iStoreOS 软路由+订阅 token
quality: high
---

# 2024 FIC 第四届全国网络空间取证竞赛 初赛 WP

原文 https://www.ctfiot.com/176442.html

## 案情
"杀猪盘"诈骗 — 卢某被赌博群骗 → 抓李某（手机=检材1）+ 服务器（检材2）+ 赵某PC（检材3）。

## 检材 1: 李某手机
- 微信号：`wxid_wnigmud8aj6j12`（李某），`wxid_06f01lnpavn722`（赵某）
- 赌博 URL：`http://www.honglian7001.com/down`
- 服务器入口：`192.168.110.110:8000/login`
- 登录密码：`limoon890`

## 检材 2: 服务器
- ESXi 6.7，VMID `65efb8a8-ddd817f6-04ff-000c297bd0e6`
- `esxcfg-volume -l` 查 datastore
- 内部 IP `192.168.8.112`，网关 `192.168.8.89`
- 网卡 mac `qqqqqq...`/端口 14131
- Web 根 `/webapp`
- SSH 弱密码 `!@#qaaxcfvghhjllj788+_)(()(`
- 若依 ruoyi 部署：
  ```bash
  jar xf ruoyi-admin.jar BOOT-INF/classes/application-druid.yml
  vim BOOT-INF/classes/application-druid.yml
  jar uf ruoyi-admin.jar BOOT-INF/classes/application-druid.yml
  java -jar ruoyi-admin.jar
  ```
- SpringBoot 3.8.2，订单接口 `/api/shopOrder`，订单总额 7354468.56
- MySQL 密码 `my-secret-pw`（`docker inspect 9b | grep MYSQL_ROOT_PASSWORD`）
- 容器间通信 172.17.0.2，外部 IP 182.33.2.250 / 43.139.0.193
- Redis 端口 3000，root 邮箱 `admin@admin.com`，Redis 5.0.24，备份大小 104857600
- 镜像 sha256:
  - `9bf1cecec3957a5cd23c24c0915b7d3dd9be5238322ca5646e3d9e708371b765`
  - `66c0e7ca4921e941cbdbda9e92242f07fe37c2bcbbaac4af701b4934dfc41d8a`

## 检材 3: 赵某 PC
- SSH 改端口 / 编辑 `/etc/ssh/sshd_config`
- 软路由 `iStoreOS` (OpenWrt)，内核 5.10.201
- IP `192.168.8.5` 网桥 `br-lan`，Docker 20.10.22
- NasTools 路径 `/root/Configs/NasTools`，PassWall2 节点数 54
- 机场订阅 token：`https://pqjc.site/api/v1/client/subscribe?token=243d7bf31ca985f8d496ce078333196a`

## 加密卷与镜像
- TrueCrypt 卷密码：`qwerasdfzxcv`
- 加密卷序列号：`404052-011088-453090-291500-377751-349536-330429-257235`
- 鲁盒镜像 `dst01.jpeg` 缩放 0.85，磁盘 db.jpg 大小 146794496
- 赌博站点 `www.585975.com`
- 钓鱼页面 `http://hi.pcmoe.net/buddha.html`
- 内部 IP `192.168.8.17`
- 易有云账号 `hl@7001` / `aa123456`，端口 28300

## 镜像 hash（SHA1）
- `FFD2777C0B966D5FC07F2BAED1DA5782F8DE5AD6`
- `B25E2804B586394778C800D410ED7BCDC05A19C8`
- `E6EB3D28C53E903A71880961ABB553EF09089007`

## 教学价值
- 真实诈骗案模拟：手机+服务器+PC 三件套
- ESXi vmdk 挂载 / Docker inspect / RuoYi 反编译 / iStoreOS 软路由
- TrueCrypt 加密卷密码爆破（字典：`qwerasdfzxcv`）
- 微信 wxid 关联嫌疑人身份
- 机场订阅 token 反查赌博站关联
- 鲁盒（火眼）镜像分析
