---
title: 【卫星安全系列一】HAS-beckley 赛题复现
contest: HackASat
year: 2020
difficulty: medium
vuln_type: misc_unknown
tags: [HackASat-qualifier-2020, beckley, KML, Google-Earth, Skyfield-python-lib, satellite-imaging, LookAt-longitude-latitude]
attack_chain: 1. HackASat 2020 资格赛 beckley 题目 /2. 修改 Dockerfile 编译运行 challenge 服务端 /3. nc 172.17.0.1 19020 启动客户端 /4. 读 remote.kml 找 NetworkLink/LookAt/Link 元素 /5. 用 Skyfield 库算卫星拍摄角度 /6. Google Earth 验证经纬度 + heading
key_payload: remote.kml  Skyfield 库  LookAt 元素  longitude/latitude/altitude
one_liner: HackASat 2020 资格赛 beckley 题复现，KML + Skyfield 库 + Google Earth 三件套算卫星拍摄角度。
lesson: HackASat 是美国国防部太空 CTF；KML 是 Google Earth 数据格式；Skyfield 是 Python 卫星轨道库；LookAt 元素指定观察点/视点距离/heading 角度。
quality: high
---

# 【卫星安全系列一】HAS-beckley 赛题复现

## 概览
HackASat 2020 资格赛 beckley 题复现，KML + Skyfield + Google Earth 三件套。

## 题目介绍
- 题目名：beckley
- 利用 Google Earth + KML 文件找 flag
- 源码：https://github.com/cromulencellc/hackasat-qualifier-2020

## 编译运行
```bash
# 修改 Dockerfile 后
docker build -t beckley .
docker run -d -p 19020:19020 beckley
nc 172.17.0.1 19020
```

## 关键 KML 元素

### NetworkLink
- 用于引用本地/远程 KML 文件
- `<Link>` 标签 `<href>` 元素

### LookAt
指定地球上正被查看的点、景点与视点间的距离、视图角度：

| 问题 | LookAt 规范 |
|------|-----------|
| 当前在查看什么目标？ | `<longitude>`、`<latitude>`、`<altitude>`、`<altitudeMode>` |
| 视点距景点有多远？ | `<range>` |
| 视图方向是否北面朝上？ | `<heading>` 0-360° |

## Skyfield 库
- Python 卫星轨道计算库
- 算卫星拍摄角度 + 地面观察点
- Earth Satellite + Topos + Observer

## 经验提炼
- HackASat 是美国国防部太空 CTF
- KML 是 Google Earth 数据格式
- Skyfield 是 Python 卫星轨道库
- LookAt 元素指定观察点/视点距离/heading 角度
- altitudeMode: clampToGround / relativeToGround / absolute
- range 单位默认米
- heading 北为 0，东 90，南 180，西 270
- satellite imaging 模拟需考虑 TLE（卫星轨道根数）
- Docker compose 启动多容器
- 172.17.0.1 是 Docker 默认网桥 IP
- 网络问题需修改 Dockerfile（如换源）
