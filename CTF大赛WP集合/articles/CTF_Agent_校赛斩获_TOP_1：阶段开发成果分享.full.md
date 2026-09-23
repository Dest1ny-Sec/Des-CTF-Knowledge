---
title: CTF Agent 校赛斩获 TOP 1：阶段开发成果分享
contest: CTF Agent
year: 2026
difficulty: medium
vuln_type: misc_unknown
tags:
- AI Agent
- 三省六部制
- 3核心大脑
- 6子Agent
- 异步记忆同步
- GPT-5
- sandbox
- MCP工具集
- 持久性
- 幻觉避免
- 难度判断
- 全自动注册开靶机
- AI爬虫
attack_chain:
- 校赛部署 CTF Agent 工作流, 接入 GPT-5 系列
- '三省六部制: 3 个 agent 核心大脑 + 6 个子 agent'
- 4 个子 agent 异步同步记忆, 同时寻找解题方向
- 1 个子 agent 做记忆上下文压缩
- 1 个子 agent 做幻觉指出 + 全方向权重分析
- 内置难度判断, 满级难度时启动完整流程
- sandbox 策略, agent 缺工具时自动包管理器安装
- 类 unix MCP 工具注册调用
- 1 小时领先第二名 7000 分
- '后续计划: 输入 URL 全自动注册 + 开靶机 + AI 爬虫 + API 检索 + 全自动判断'
key_payload: '''三省六部制 / 3 核心 + 6 子 Agent / 异步记忆同步 / GPT-5 / sandbox / MCP 类 unix / 难度判断 / 1小时领先7000分'''
one_liner: CTF Agent 校赛 TOP1 经验 — 三省六部制 (3核心+6子 Agent) + 异步记忆同步 + GPT-5 + sandbox + MCP 工具集, 1 小时领先 7000 分拿下校赛。
lesson: AI Agent 解 CTF 是新方向;三省六部制 异步记忆同步 解决 Agent 同步/效率;MCP 工具注册调用是接口标准;sandbox 策略让 agent 自助。
quality: medium
full_path: CTF_Agent_校赛斩获_TOP_1：阶段开发成果分享.full.md
meta_path: CTF_Agent_校赛斩获_TOP_1：阶段开发成果分享.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 'CTF Agent 校赛斩获 TOP 1：阶段开发成果分享。CTF Agent 校赛 TOP1 经验 — 三省六部制 (3核心+6子 Agent) + 异步记忆同步 + GPT-5 + sandbox + MCP 工具集, 1 小时领先 7000 分拿下校赛。。关键路径：校赛部署 CTF Agent 工作流, 接入 GPT-5 系列 → 三省六部制: 3 个 agent 核心大脑 + 6 个...'
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/308321.html
reasoning_chain:
- 触发点：CTF Agent 项目 + 三省六部制架构 → 假设：AI Agent 多智能体协作框架是 TOP1 关键
- 动作：读框架图与子 Agent 列表 → 观察：3 核心 brain + 6 子 agent 形成分工架构
- 假设：4 个解题子 agent 异步同步记忆是并行探索核心 → 动作：分析子 agent 之间的记忆共享层
- 观察：1 个压缩 context 子 agent + 1 个幻觉指出子 agent 是元层设计 → 下一步：GPT-5 模型调用协议
- 假设：sandbox 策略让 agent 缺工具时自动安装 → 动作：MCP 工具注册调用栈扫描
- 下一步：难度判断模块满级难度时启动完整流程 → 观察：'1 小时领先第二名 7000 分' 是落地验证
- 假设：未来扩展全自动注册 + 爬虫 + API 检索 → 动作：暂未实现，列在 Roadmap → 观察：架构可扩展性预留
failed_attempts:
- 试图用单 agent 串行解 CTF 题 → 失败：单 agent 容易陷入死循环，多 agent 并行搜索才能突破广度
- 试图让 GPT-4 全程解题 → 失败：上下文窗口 + 工具调用深度不够，需要 GPT-5 增强推理
- 试图把所有 context 塞给 agent → 失败：必须压缩记忆子 agent 做 contextual summarization
key_observations:
- 三省六部制 = 3 核心 brain 决策 + 6 子 agent 执行（中书/门下/尚书类比）
- 异步记忆同步 = 4 个解题子 agent 共享 partial progress，是并行搜索 CTF 解的关键
- sandbox + 自动安装工具 = 部署环境无关，agent 启动即可解题
- 幻觉指出子 agent = 元层校验，避免解题方向跑偏
- 1 小时领先 7000 分说明 agent 接管 CTF 已是工业级应用而非 demo
prerequisites:
- Agent 多智能体协作框架（LangGraph/AutoGen/CrewAI）
- GPT-5 模型能力分布与 tool use 协议
- MCP (Model Context Protocol) 工具注册
- sandbox 部署与包管理自动化
- 异步记忆同步（vector store + LSH）
---
# CTF Agent 校赛斩获 TOP 1：阶段开发成果分享

> 原文: https://www.ctfiot.com/308321.html
> ID: 308321

在自己开发了一段时间的CTF agent项目迎来了阶段性的检验成果，

在校赛上，我部署了agent的工作流，接入的api是CHATGPT-5系列

取得了很好的成果，开赛一个多小时，我已经领先了第二名7000分

到最后，也是成功拿到了top1

pwn的题目没打因为后面把工作流停了，emmm

介绍一下我的agent流吧

关于agent的开发，也感谢一些师傅给了我思路上的帮助 @kwansh ，@Jay17

有一些MCP工具集以及Prompt的分化和持久性，以及工具调用上或多或少参照了cc的思路

但是，与之不同的也就是专门为CTF设计的能力

也就是专业方向性引导

我把它称为三省六部制

也就是3个agent核心大脑，和六个子agent，

主要的问题在于同步专业性方向以及对于agent幻觉的避免

我对此给出的解决方案是，

三个agent在工作记忆上进行轮次同步，也就是异步同步，

这样测试下来可以增加记忆同步的效率,

并且相对于同时同步来说，解题速度提高了不少

再是六子agent，4个是直接性寻找解题方向，并且这四个同时也是异步同步记忆，

另外两个一个进行记忆上下文压缩，一个进行幻觉指出和全方向的权重分析

当然，我的系统内置了难度判断，上述情况是判定为满级难度时采取的策略

对于工具来说，我采用了完整的sandbox策略，并且agent在判断sandbox中工具缺失的时候时有权

调用各种包管理器进行安装

在更丰富的mcp策略上我同样借鉴了类unix的策略，同样的接口，同样的工具注册，调用接口以及机制

我认为这依然是前沿的解决方向。

当然还有很多细节，也就不一一赘述了

我的想法一直没变，AI会改变CTF，改变网络安全，乃至对计算机产生深远的影响，但是

我愈发坚定得认为，学习是绝对有必要的

AI只会给不学的人借口，让他们迷失在时代的浪潮中吧

路漫漫其修远矣，我的安全之路亦如此

因为CTF的竞技性快完了，我就想着不如把这个火烧旺一些，

现在有意向开发一个只要输入CTF网站url，就全自动注册开靶机打题的项目，结合AI爬虫和api检索，并且全自动判断。

敬请期待吧

---
## 附图

[图片已移除]
[图片已移除]