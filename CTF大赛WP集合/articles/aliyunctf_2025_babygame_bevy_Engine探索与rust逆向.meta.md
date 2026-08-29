---
title: aliyunctf 2025 babygame bevy Engine 探索与 rust 逆向
contest: aliyunctf
year: 2025
difficulty: medium
vuln_type: reverse
tags: [rust, bevy, ecs, unity-like, scene, query, transform]
attack_chain:
  - 解压 bevy_packed 资源
  - 加载 .scn 场景文件
  - 解析世界/资源/实体表
  - 重放 ECS System
  - 还原 state machine
  - 拼装 transform
key_payload: flag 通过 ECS Query<&mut Transform> 状态推进触发
one_liner: 阿里云 CTF 2025 Rust bevy 引擎逆向题，从 .scn 场景文件还原 ECS 实体组件系统状态机。
lesson: 现代 Rust 游戏引擎(bevy)逆向关键是理解 ECS 模型 + App schedule + 系统依赖图，不必纠结 Rust 闭包语法。
quality: high
---

阿里云 CTF 2025 一道 Rust 写的 bevy 引擎小游戏逆向。bevy 是 Rust 生态类 Unity 框架，
核心范式是 ECS(Entity Component System) + Schedule(系统调度器)。题面给一个编译好的
bevy 程序，需要从 `.scn` 场景文件逆出 ECS 实体与组件布局，再通过静态分析还原
State Machine 状态推进逻辑。

作者博客风格详尽：从环境搭建、bevy 0.x vs 0.13 差异、scene 文件结构
(world/res/entity 三段 + 实体表 + 组件表)、ECS Query<&mut Transform> 范式、
到 add_systems vs add_plugins 的依赖关系都讲清楚。

关键点：state machine 通过 `States` trait + `OnEnter/OnUpdate/OnExit` 三个
system 切分；玩家操作映射到 component 上的 marker 字段；flag 在 READ→PICK→
COMBINE 三状态推进中按 Query 顺序依次拼接。逆向时先把 scene 文件解析出
entity/transform 列表，再定位 add_systems(Update, (...)) 链式调用。

适合作为 Rust + bevy 入门材料，作者同时对比了 ECS 与 OOP 思维差异，并给出
从 .scn 直接读取 transform 绕过 Rust ABI 痛苦的"作弊"思路。
