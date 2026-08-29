---
title: 【2026春节】全自动AI做题的实现及初8逆向AI Agent对话记录及wp
contest: 春节活动
year: 2026
difficulty: hard
vuln_type: reverse
tags: [AI-Agent, multi-model, point-system, OpenViking-context, calling-func, jadx, IDA, libhajimi.so, JNI, multi-arch]
attack_chain: 多模型协作 + 总结反思系统 + 点子系统 + 常见工具 calling func 减少 token/上下文压缩和会话分支参考 OpenViking 实现/打 tag 系统/JNI: 1. jadx 反编译 APK 找 native 调用 2. IDA 分析 libhajimi.so (x86_64) 找 JNI 函数 3. 提取密钥和常量 4. 写脚本恢复 flag
key_payload: Aclasses.dex (Java/Kotlin) + libhajimi.so (多架构 native)
one_liner: 2026 春节 Tokeii 的全自动 AI Agent 做题系统分享，逆向题 Android JNI 实战。
lesson: AI Agent 多模型协作可降低单模型偏差；常见工具 calling func 大幅减少 token；OpenViking 上下文压缩参考实现；Android JNI 逆向两件套 jadx (Java 层) + IDA (native 层) 是标准流程。
quality: high
---

# 【2026春节】全自动AI做题的实现及初8逆向 AI Agent 对话记录及wp

## 概览
2026 春节 Tokeii 设计的 AI Agent 多模型协作 CTF 做题系统，覆盖 Android JNI 逆向实战。

## AI Agent 系统设计

### 核心组件
- **多模型协作**：不依赖单一模型，按题目类型分给更合适的子 Agent
- **总结反思系统**：每题做完反思整个过程，下次遇到会怎么应对
- **点子系统**：每个解题步骤打 tag，方便下次调用
- **常见工具 calling func**：python 代码执行、字符串搜索、web 请求等工具直接调用减少 token
- **上下文压缩和会话分支**：参考字节开源 OpenViking 项目实现
- **打 tag 系统**：每次生成反思/总结/wp 时对内容打 tag

### 提示词设计原则
- Each step should be a TESTABLE hypothesis (e.g., "Test for SQL injection on /login param"), not vague
- Include WHAT tool to use and WHAT to look for in each step
- First step should always be information gathering (read source, analyze binary, fetch target)
- Have at least one backup approach from a different attack angle
- Skip approaches marked as 'failed' — they already proved unsuccessful
- Prioritize 'pending' ideas — they haven't been tried yet
- Build your plan around untried approaches

## Android JNI 逆向实战

### 题目
- Aclasses.dex (Java/Kotlin code)
- native library libhajimi.so (多架构)

### 攻击步骤
1. **jadx 反编译 APK**：分析 Java/Kotlin 层逻辑，找验证入口和 native 方法调用
2. **IDA 分析 libhajimi.so (x86_64)**：找 JNI 函数和核心验证逻辑
3. **分析加密/验证算法**：提取密钥和常量
4. **编写脚本逆向算法**：恢复 flag
5. **提交 flag**

## 经验提炼
- AI Agent 多模型协作可降低单模型偏差，提高解题成功率
- 常见工具 calling func（python/shell/web）大幅减少 token 消耗
- OpenViking 上下文压缩是会话管理好范式
- Android JNI 逆向两件套：jadx (Java/Kotlin) + IDA (native .so)
- 多架构 .so 通常只看 x86_64 (主调试) 或 arm64-v8a (真机)
- Agent 提示词要具体到 "用什么工具" 和 "看什么特征"，避免空泛指令
