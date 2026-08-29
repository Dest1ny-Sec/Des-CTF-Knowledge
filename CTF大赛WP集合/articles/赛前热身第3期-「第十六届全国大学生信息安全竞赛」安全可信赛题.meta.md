---
title: 赛前热身第3期|「第十六届全国大学生信息安全竞赛」安全可信赛题
contest: 第十六届全国大学生信息安全竞赛 安全可信赛题
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [trusted-computing, TCM, TPM, PCR-quote, SM2, cube-1.3, vtcm-emulator, key_manage, policy-verification, integrity-report]
attack_chain:
- 镜像环境:cube-1.3(通用可信软件基框架)+gm_sm2_master(开源SM2库)+cube-tcm(可信密码模块模拟器+驱动)+cube_tcmplugin(模块封装)+tcmenv_exec(测试环境)
- 运行tcm_quote.sh启动可信报告机制
- 五个角色:user/term/server/crypt_user/crypt_hub
- 阶段1:user发可信报告命令→term拦截转到server→server拦截转给crypt_user→key_manage生成防重放随机数→返回term
- 阶段2:term交给key_event添加节点和用户信息(MESSAGE,INSTANCE_INFO)→拦截到crypt_user→key_manage配可信报告模板(TCM_PIK_DESC,PCRQUOTE)→pcr_multirw读pcr值→quote_report生成报告
- 报告回term→转server→crypt_hub的key_event接收→key_manage存储报告→quote_report验证→删报告内容→key_manage解析报告内容→结论返回user
- 关键:pcr_set.sh清零pcr,调用pcr_set实例向14号pcr寄存器写入数据(策略摘要值)
- policy_list中列出某几项数据的摘要值
- 修改instance/node/pcr_set/policy_write.msg中的return_value(14号寄存器+策略摘要名)
- 验证逻辑:遍历内存库所有摘要值,确定pcr由哪些策略组合,policy_choice->return_value输出
- 故意留下bug:完整性报告验证过程有bug,感兴趣的同学可研究
key_payload: TCM_PIK_DESC + PCRQUOTE + 策略组合
one_liner: 第十六届全国大学生信息安全竞赛安全可信赛题,基于cube-1.3+cube-tcm可信计算模拟器,涵盖可信报告两阶段流程+PCR寄存器设置+策略组合验证+SM2密码学。
lesson: 可信计算(TCM/TPM)是新兴CTF方向,cube-1.3是国内主流可信计算模拟器框架;可信报告机制(PCR_QUOTE)是核心安全机制;策略组合验证需要遍历内存库+解析return_value。
quality: high
---

## 题目列表

可信计算方向:基于cube-1.3的TCM可信报告机制

## 关键考点

### 环境框架
- cube-1.3:通用可信软件基框架(基础库/数据格式/头文件/模块集合/主程序)
- gm_sm2_master:开源SM2算法库(国密)
- cube-tcm:可信密码模块模拟器(vtcm_netlink_emulator)+驱动(vtcmd_dev)+访问库(libtcm.so)+管理工具(vtcm_utils)
- cube_tcmplugin:本环境精华,封装tcm访问功能为模块
- tcmenv_exec:测试环境(编译+运行)

### 环境变量配置
- 所有环境:`source set_env.sh` (cube-1.3目录下)
- tcmenv_exec:普通环境+`set_tcmenv.sh`(含密码功能)
- run_cube.sh + run_cubetcm.sh:LIBRARY_PATH配置

### 五个实例角色
- user:发送可信报告命令
- term:接收并转发
- server:拦截+转发
- crypt_user:key_manage生成防重放随机数
- crypt_hub:存储+验证报告

### 可信报告两阶段
**阶段1:防重放随机数生成**
- user发可信报告命令→term拦截→server→crypt_user
- key_manage生成防重放随机数→返回term
- term交给key_event准备正式可信报告

**阶段2:报告生成与验证**
- key_event添加节点+用户信息(MESSAGE,INSTANCE_INFO)
- 拦截到crypt_user→key_manage配可信报告模板(TCM_PIK_DESC,PCRQUOTE)
- pcr_multirw读pcr值→quote_report生成报告
- 报告回term→server→crypt_hub key_event接收
- crypt_hub key_manage存储+quote_report验证
- 删报告内容→key_manage解析→结论返回user

### PCR寄存器
- pcr_set.sh:清零pcr,调用pcr_set实例向14号pcr寄存器写入数据
- 写入内容:crypt_hub/policy_list中列出的某几项数据的摘要值
- 修改instance/node/pcr_set/policy_write.msg中的return_value(14号寄存器+策略摘要名)

### 验证逻辑
- key_manage模块收到验证结果后处理
- 遍历内存库中所有摘要值
- 准备将分析结果写入policy_choice->return_value
- 与pcr写入内容一致

### 故意bug
- 完整性报告验证过程中有bug(故意留,解决不难)

## 实战价值
- 可信计算(TCM/TPM)是新兴CTF方向,国密+PCR+quote三件套
- cube-1.3是国内主流可信计算模拟器框架
- 可信报告机制(PCR_QUOTE)是核心安全机制
- 策略组合验证需要遍历内存库+解析return_value
- SM2国密算法是中国特色密码学
