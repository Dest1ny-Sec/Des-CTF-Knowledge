---
title: 2022 MOVEment Aptos writeup by ChaMd5
contest: 2022 MOVEment CTF (Aptos / Move 语言)
year: 2022
difficulty: medium
vuln_type: [logic, web_unknown]
tags: [Move, Aptos, blockchain, Web3, signer, event, account, init_challenge, discrete_log, hash, add, resource]
attack_chain: ["Q1 checkin: 调 get_flag entry 函数即得 flag", "aptos move run --function-id 0x3dd3f092...::checkin::get_flag", "Q2 hello_move: 三关", "(1) init_challenge 拿 Challenge 资源", "(2) hash 提交 [103,111,111,100] = 'good'", "(3) discrete_log: 计算 3123592912467026955 的对数", "(4) add(2u8, 0u8) 让 res.balance < Initialize_balance", "(5) get_flag 拿 flag", "Move script 调 init_challenge（不是 entry 需 script 包装）"]
key_payload: "discrete_log(3123592912467026955u128) 需解"
one_liner: Aptos Move 智能合约 checkin + 三关 hello_move
lesson: Move 资源 + 入口函数 + script 调 entry-less 函数是 Web3 入门
quality: high
---

# 2022 MOVEment Aptos writeup by ChaMd5

原文 https://www.ctfiot.com/86671.html （ChaMd5 Venom 复盘）

## Q1: checkin（入门）
```move
module ctfmovement::checkin {
    use std::signer;
    use aptos_framework::account;
    use aptos_framework::event;

    struct FlagHolder has key {
        event_set: event::EventHandle<Flag>,
    }

    struct Flag has drop, store {
        user: address,
        flag: bool
    }

    public entry fun get_flag(account: signer) acquires FlagHolder {
        let account_addr = signer::address_of(&account);
        if (!exists<FlagHolder>(account_addr)) {
            move_to(&account, FlagHolder {
                event_set: account::new_event_handle<Flag>(&account),
            });
        };
        let flag_holder = borrow_global_mut<FlagHolder>(account_addr);
        event::emit_event(&mut flag_holder.event_set, Flag {
            user: account_addr,
            flag: true
        });
    }
}
```

**调用：**
```bash
aptos move run --function-id 0x3dd3f092f3329fba1818779cc7940b681e37277c43b88f1ac0ebf8b67b7879e3::checkin::get_flag
```

**flag:**
```
flag{#AKHsfaf-33SFxfGA-H134aB-2022CTFMovement-#}!48e986dd-13f0-49e8-87ef-faa49f3a5c0b
```

## Q2: hello_move（三关）

### 关卡 1: init_challenge
- 函数没有 `entry` 属性，必须在 script / module 里调用
- 写 script 包装：
  ```move
  script {
      fun call_init_challenge(account: signer) {
          ctfmovement::hello_move::init_challenge(&account);
          ...
      }
  }
  ```

### 关卡 2: hash
- 提交 `[103, 111, 111, 100]` = `"good"`

### 关卡 3: discrete_log
- 计算 `discrete_log(3123592912467026955u128)`
- 用 sage / sympy 求解离散对数

### 关卡 4: add
- `add(2u8, 0u8)` 让 `res.balance < Initialize_balance`

### EXP script
```move
script {
    fun call_init_challenge(account: signer) {
        ctfmovement::hello_move::init_challenge(&account);
        ctfmovement::hello_move::hash(&account, vector[103u8, 111u8, 111u8, 100u8]);
        ctfmovement::hello_move::discrete_log(&account, 3123592912467026955u128);
        ctfmovement::hello_move::add(&account, 2u8, 0u8);
        ctfmovement::hello_move::get_flag(&account);
    }
}
```

## 教学价值
- **Aptos / Move** 是 Meta（前 Diem）系区块链
- Move 语言特性：
  - **资源 (Resource)** = 类型 + key 能力 = 链上存储
  - **script** 包装无 entry 函数
  - **signer** 类型证明身份
  - **acquires** 声明借用的资源
- **discrete_log** 是密码学基础
- **add 函数边界条件** 触发不平衡

## 工具
- aptos CLI：`aptos move run`
- 链 ID：testnet
- 钱包：aptos 官方 / petra / martian
- 函数 ID 格式：`0xADDRESS::MODULE::FUNCTION`
