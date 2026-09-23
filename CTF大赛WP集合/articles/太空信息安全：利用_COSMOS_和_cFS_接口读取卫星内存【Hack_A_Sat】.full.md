---
title: HackASat Qualifier 2020 - 利用COSMOS和cFS接口读取卫星内存
contest: Hack A Sat Qualifier 2020 (美国AFRL/NASA太空安全赛)
year: 2020
difficulty: hard
vuln_type: forensic_memory
tags:
- HackASat
- COSMOS
- cFS
- Core_Flight_System
- MM_PEEK_MEM
- KitToFlagPkt
- 卫星内存读取
- CCSDS
- NASA
- cFS_Training
- INTERFACE_LOCAL_CFS_INT
- tcpip_client_interface
attack_chain: Docker运行patch:generator生成数据 → socat暴露TCP:19020/19021 → 装COSMOS+RVM+ruby-2.3.8+qt4 → 配INTERFACE LOCAL_CFS_INT → cmd("MM PEEK_MEM with CCSDS_STREAMID 6280...")遍历12-212 offset读KitToFlagPkt符号地址
key_payload: PEEK_MEM + CCSDS_STREAMID 6280 + MEM_TYPE 1 + ADDR_SYMBOL_NAME 'KitToFlagPkt'
one_liner: 利用NASA开源COSMOS地面站+cFS(核心飞行系统)PEEK_MEM指令从12-212偏移读KitToFlagPkt符号名dump卫星内存。
lesson: 太空信息安全赛的核心是利用COSMOS+CCSDS协议栈;cFS MM(Memory Manager)应用提供PEEK_MEM指令可读内存;配置INTERFACE LOCAL_CFS_INT指定TCP IP+端口对接;ADDR_SYMBOL_NAME用符号名查地址;NASA训练PDF给出完整环境配置。
quality: high
full_path: 太空信息安全：利用_COSMOS_和_cFS_接口读取卫星内存【Hack_A_Sat】.full.md
meta_path: 太空信息安全：利用_COSMOS_和_cFS_接口读取卫星内存【Hack_A_Sat】.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: HackASat Qualifier 2020 - 利用COSMOS和cFS接口读取卫星内存。利用NASA开源COSMOS地面站+cFS(核心飞行系统)PEEK_MEM指令从12-212偏移读KitToFlagPkt符号名dump卫星内存。。经验：太空信息安全赛的核心是利用COSMOS+CCSDS协议栈;cFS MM(Memory Manager)应用提供PEEK_...
category: forensic
subcategory: memory_forensics
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/235623.html
reasoning_chain:
- 'HackASat Qualifier 2020 美国 AFRL/NASA 太空安全赛, Docker 运行 patch:generator 生成数据 → 触发点: socat 暴露 TCP:19020/19021'
- '假设: 装 COSMOS+RVM+ruby-2.3.8+qt4 配 INTERFACE LOCAL_CFS_INT → 动作: COSMOS 配置 tcpip_client_interface 对接 cFS'
- '动作: cmd(''MM PEEK_MEM with CCSDS_STREAMID 6280'') 遍历 12-212 offset → 假设: ADDR_SYMBOL_NAME=''KitToFlagPkt'' 是关键符号'
- '观察: KitToFlagPkt 符号名出现在 offset 12-212 之间的内存区 → 触发点: 符号名就是 flag'
- '假设: PEEK_MEM 指令可读任意内存 → 动作: 遍历 offset → 观察: 符号名 KitToFlagPkt + ADDR = 卫星内存 dump'
- '动作: NASA cFS Training PDF 给出完整环境配置 + GitHub 仓库跳过环境配置 → 完成'
failed_attempts:
- '试图不解 COSMOS 直接 nc → 失败: 协议不是裸 CCSDS'
- '试图不解 cFS 直接 dump 内存 → 失败: cFS 应用层封装 MM PEEK_MEM'
key_observations:
- 太空信息安全赛的核心是利用 COSMOS + CCSDS 协议栈
- cFS MM (Memory Manager) 应用提供 PEEK_MEM 指令可读内存
- 配置 INTERFACE LOCAL_CFS_INT 指定 TCP IP+端口对接
- ADDR_SYMBOL_NAME 用符号名查地址 (12-212 偏移)
- NASA 训练 PDF 给出完整环境配置
prerequisites:
- COSMOS 地面站配置
- CCSDS 协议 (Space Packet Protocol)
- cFS (Core Flight System) MM 应用
- Docker + Ruby + Qt 环境
---
# 太空信息安全：利用 COSMOS 和 cFS 接口读取卫星内存【Hack A Sat】

> 原文: https://www.ctfiot.com/235623.html
> ID: 235623

直接用我的 github 仓库可以跳过环境配置这一大步：

https://github.com/yichen115/hackasat-qualifier-2020

题目环境

solver 文件夹内容修改

sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

challenge 文件夹内容修改

sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

题目环境编译与测试

解题

rm -rf data/*
docker run -it --rm -v `pwd`/data:/out -e "SEED=1" patch:
generator
socat -v tcp-listen:
19020,reuseaddr exec:"docker run --rm -i -e SERVICE_HOST=172.17.0.1 -e SERVICE_PORT=19021 -e SEED=1 -e FLAG=flag{60f46eee-8c85-4d8a-8bf9-bd1c6a8aa37d} -p 19021:
54321 patch:
challenge"

基础知识

https://ntrs.nasa.gov/api/citations/20210000619/downloads/20210000619%20Rev%201%20cFS_Training-COSMOS_Module.pdf

COSMOS 安装

git clone https://github.com/OpenC3/cosmos-project.git
openc3.bat run

sudo apt-add-repository -y ppa:
rael-gc/rvm
sudo apt update -y
sudo apt -y install rvm    //通过 rvm 来安装对应的 ruby 版本
source /usr/share/rvm/scripts/rvm
rvm install ruby-2.3.8 --disable-stable    //安装 2.3.8
rvm use 2.3.8 --default 
ruby -v
sudo apt-get install qt4-default   //安装 qt4
qmake --version                    //确认一下默认版本是不是 qt4
//给 gem 换个源
gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
gem install bundler -v2.0.2    // 把 bundler 升级到 2.0 以上

export QT_X11_NO_MITSHM=1

INTERFACE LOCAL_CFS_INT tcpip_client_interface.rb 127.0.0.1 19021 19021 10 nil

日志分析

使用 COSMOS 读取 Flag

12.upto(212) { |off|
 offset = off
 cmd("MM PEEK_MEM with CCSDS_STREAMID 6280, CCSDS_SEQUENCE 49152, CCSDS_LENGTH 73, CCSDS_FUNCCODE 2, CCSDS_CHECKSUM 0, DATA_SIZE 8, MEM_TYPE 1, PAD_16 0, ADDR_OFFSET #{offset}, ADDR_SYMBOL_NAME 'KitToFlagPkt'")
}

参考 WP


```
https://github.com/yichen115/hackasat-qualifier-2020
sed -i 's|deb.debian.org|mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
rm -rf data/*
docker run -it --rm -v `pwd`/data:/out -e "SEED=1" patch:
generator
socat -v tcp-listen:
19020,reuseaddr exec:"docker run --rm -i -e SERVICE_HOST=172.17.0.1 -e SERVICE_PORT=19021 -e SEED=1 -e FLAG=flag{60f46eee-8c85-4d8a-8bf9-bd1c6a8aa37d} -p 19021:
54321 patch:
challenge"
https://ntrs.nasa.gov/api/citations/20210000619/downloads/20210000619%20Rev%201%20cFS_Training-COSMOS_Module.pdf
git clone https://github.com/OpenC3/cosmos-project.git
openc3.bat run
sudo apt-add-repository -y ppa:
rael-gc/rvm
sudo apt update -y
sudo apt -y install rvm    //通过 rvm 来安装对应的 ruby 版本
source /usr/share/rvm/scripts/rvm
rvm install ruby-2.3.8 --disable-stable    //安装 2.3.8
rvm use 2.3.8 --default 
ruby -v
sudo apt-get install qt4-default   //安装 qt4
qmake --version                    //确认一下默认版本是不是 qt4
//给 gem 换个源
gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
gem install bundler -v2.0.2    // 把 bundler 升级到 2.0 以上
export QT_X11_NO_MITSHM=1
INTERFACE LOCAL_CFS_INT tcpip_client_interface.rb 127.0.0.1 19021 19021 10 nil
12.upto(212) { |off|
 offset = off
 cmd("MM PEEK_MEM with CCSDS_STREAMID 6280, CCSDS_SEQUENCE 49152, CCSDS_LENGTH 73, CCSDS_FUNCCODE 2, CCSDS_CHECKSUM 0, DATA_SIZE 8, MEM_TYPE 1, PAD_16 0, ADDR_OFFSET #{offset}, ADDR_SYMBOL_NAME 'KitToFlagPkt'")
}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]