---
title: HackASat Qualifier 2020 - 利用COSMOS和cFS接口读取卫星内存
contest: Hack A Sat Qualifier 2020 (美国AFRL/NASA太空安全赛)
year: 2020
difficulty: hard
vuln_type: forensic_memory
tags: [HackASat, COSMOS, cFS, Core_Flight_System, MM_PEEK_MEM, KitToFlagPkt, 卫星内存读取, CCSDS, NASA, cFS_Training, INTERFACE_LOCAL_CFS_INT, tcpip_client_interface]
attack_chain: Docker运行patch:generator生成数据 → socat暴露TCP:19020/19021 → 装COSMOS+RVM+ruby-2.3.8+qt4 → 配INTERFACE LOCAL_CFS_INT → cmd("MM PEEK_MEM with CCSDS_STREAMID 6280...")遍历12-212 offset读KitToFlagPkt符号地址
key_payload: PEEK_MEM + CCSDS_STREAMID 6280 + MEM_TYPE 1 + ADDR_SYMBOL_NAME 'KitToFlagPkt'
one_liner: 利用NASA开源COSMOS地面站+cFS(核心飞行系统)PEEK_MEM指令从12-212偏移读KitToFlagPkt符号名dump卫星内存。
lesson: 太空信息安全赛的核心是利用COSMOS+CCSDS协议栈;cFS MM(Memory Manager)应用提供PEEK_MEM指令可读内存;配置INTERFACE LOCAL_CFS_INT指定TCP IP+端口对接;ADDR_SYMBOL_NAME用符号名查地址;NASA训练PDF给出完整环境配置。
quality: high
---
