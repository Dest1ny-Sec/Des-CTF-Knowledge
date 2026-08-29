---
title: SunshineCTF 2022 Challenges
contest: SunshineCTF
year: 2022
difficulty: easy
vuln_type: misc_unknown
tags: [challenge-release, pwnmake, ctf-organization, mit-license]
attack_chain:
- 公开 SunshineCTF 2022 所有挑战
- MIT 许可证
- 使用 pwnmake (基于 PwnableHarness) 编译/构建 Docker
- pwnmake / pwnmake docker-build / pwnmake docker-start
- pwnmake publish 输出到 publish 文件夹
- GitHub Projects 跟踪挑战
- server-based 挑战迁移到 https://ctf.hackucf.org
key_payload: pwnmake
one_liner: SunshineCTF 2022 公开题库 release (RE/Pwn/Web 全部源码 + Docker)，pwnmake 标准化构建。
lesson: 高质量 CTF 结束后公开题库 + 构建工具是社区贡献的重要形式。
quality: low
---
# SunshineCTF 2022 Challenges

## 简介
公开 SunshineCTF 2022 全部挑战源码 (RE/Pwn/Web)，MIT 许可证。

## 构建工具
- [PwnableHarness](https://github.com/C0deH4cker/PwnableHarness) 提供 `pwnmake` 工具
- 编译所有二进制: `pwnmake`
- 构建 Docker 镜像: `pwnmake docker-build`
- 运行 Docker 容器: `pwnmake docker-start`
- 打包分发: `pwnmake publish`

## 组织方式
- GitHub Projects 看板管理
- 跟踪：难度等级 / 开发状态 / 测试状态 / 端口号
- server-based 挑战最终迁移到 https://ctf.hackucf.org
