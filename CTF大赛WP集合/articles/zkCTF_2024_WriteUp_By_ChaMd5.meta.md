---
title: zkCTF 2024 WriteUp By ChaMd5
contest: zkCTF
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [zk-SNARK, circom, groth16, halo2_proofs, fibonacci-circuit, div-circuit, range-check]
attack_chain: CheckIn 题：circom 写 .circom→r1cs/wasm/sym 编译→input.json witness.wtns→snarkjs groth16 prove 生成 proof.json+public.json/中高级题 halo2_proofs Rust 实现 FibonacciCircuit 配置 add gate + U8 range-check table + DivCircuit a/b/c/r/k 列 + mul+add 双 gate + assign_range + assign_witness + expose_public 三件套 / generate_keys 调 ParamsKZG::setup + keygen_vk/pk / generate_proof 调 create_proof 用 KZGCommitmentScheme+ProverGWC+Challenge255 transcript + 写出 proof/param/vk 三文件
key_payload: circom checkin.circom --r1cs --wasm --sym -c  snarkjs groth16 prove ../CheckIn_groth16.zkey witness.wtns proof.json public.json
one_liner: zkCTF 2024 zkSNARK 系列，覆盖 circom groth16 入门到 halo2_proofs Rust 自定义 gate 高级用法。
lesson: circom 是 zkSNARK DSL 入门工具，halo2_proofs 是 Rust 实现 zk 电路的工业级库；range check 通过 (1..range).fold(expr * (value - a)) 实现；BN256 Pasta 域 + KZG commitment 是现代 zk 标准组合。
quality: high
---

# zkCTF 2024 WriteUp By ChaMd5

## 概览
zkCTF 2024 ChaMd5 战队的 zkSNARK 专题，涵盖 circom 和 halo2_proofs 两种主流 zk 框架。

## 题目1: CheckIn (circom + groth16)
- 工作流：
  ```bash
  circom checkin.circom --r1cs --wasm --sym -c
  node generate_witness.js checkin.wasm input.json witness.wtns
  snarkjs groth16 prove ../CheckIn_groth16.zkey witness.wtns proof.json public.json
  snarkjs generatecall
  ```
- 关键产物：R1CS 约束系统、witness 见证、proof.json + public.json
- 公开信号示例：`["0x2478448102d76d164d4cd8c001ace8a50b2b6232a5ec1801cb7d1f1bf8bae8c1", ...]`

## 题目2: FibonacciCircuit (halo2_proofs)
- **列结构**：col_a/Advice + col_b/Advice + col_c/Advice + col_pa/col_pb/col_pc/Fixed + selector + instance
- **add gate**：`s * (a + b - c)` 强制 c = a + b
- **assign_first_row**：从 instance 取 f(0) 和 f(1)，assign 三个 cell
- **assign_row**：循环产生 f(2) = f(0)+f(1), f(3) = f(1)+f(2), ...，每行用 pa=125, pb=127 作 fixed 标记
- **synthesize**：`for _i in 3..5` 跑 2 次循环
- **expose_public**：把最后一个 prev_c 暴露为 instance row 2
- **test 案例**：F[0]=2, F[1]=3, out=13 (3 次迭代后 = 2+3+3+5 = 13)

## 题目3: DivCircuit (halo2_proofs 高级)
- **6 列结构**：a(被除数) + b(除数) + c(商) + r(余数) + k(辅助) + range(LookupTable)
- **3 个 gate**：
  - `mul`: s * (b * c - k)  →  k = b * c
  - `add`: s * (a - r - k)  →  a = r + k = r + b*c
  - `range check`: 4 个 fold 表达式 (1..255).fold(expr * (value - a)) 约束 a/b/c/r < 255
- **RANGE_BITS = 8**：U8 范围
- **assign_range**：(1 << RANGE_BITS) - 1 = 255 个值填充 range table
- **assign_witness**：分配 a/b/c 三 witness + r = a - k + 余数修正
- **generate_keys**：ParamsKZG::setup(k=10, OsRng) + keygen_vk/pk
- **generate_proof**：KZGCommitmentScheme + ProverGWC + Challenge255 + Blake2bWrite transcript，写出 proof/param/vk 三文件

## 经验提炼
- circom 是 zkSNARK DSL 入门，halo2_proofs 是工业级 Rust 库
- halo2 的 Lookup Table 配合 fold 表达式实现 range check
- Pasta 域（Fp, Fq）+ BN256 + KZG 是现代 zk 标准组合
- MockProver::run(k, &circuit, vec![public_input]) 是 zk 电路单元测试标准方式
- SerdeFormat::RawBytes 用于 dump 原始字节（避免 JSON 序列化开销）
