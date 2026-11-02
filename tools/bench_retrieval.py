#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bench_retrieval.py — 检索质量基准测试。

为什么需要：知识库的检索质量会随卡片/关键词增删而漂移，
必须有可回归的基准，否则"感觉变好了"是不可验证的。

用例分两类：
  signal_queries   用"我观察到什么"这种自然语句（模拟 agent 的真实输入）
  evidence_queries 用真实逆向证据（导入函数/文件类型/节区大小），验证领域判别

用法
    python3 tools/bench_retrieval.py            # 跑基准
    python3 tools/bench_retrieval.py --strict   # 低于阈值(85%)则退出码非 0
"""
import argparse
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (query, 期望命中的卡片 id 片段, 说明)
CASES = [
    # —— 自然语言信号 ——
    ("栈溢出但程序里没有后门函数", "ret2libc", "无 win 函数"),
    ("给了 AES 加密的密文能观察填充错误", "aes-cbc", "padding oracle"),
    ("图片能打开但 zsteg 没结果", "png-crc", "否定语境：排除 LSB"),
    ("JWT 的 alg 头可以改", "jwt", "算法混淆"),
    ("二进制被 strip 了找不到 main", "elf-strip", "stripped 定位"),
    ("任意文件读取但读不到 flag", "lfi", "LFI 召回"),
    ("压缩包有密码但知道里面有一个小文件", "zip", "明文攻击"),
    ("服务器会发起请求", "ssrf", "SSRF"),
    ("程序有 seccomp 禁了 execve", "orw", "seccomp/ORW"),
    ("只有一个 API 查询预算有限", "adversarial", "黑盒预算"),
    ("命令执行被过滤了", "rce", "RCE 绕过"),
    ("SSRF 打了但 gopher 没反应", "ssrf", "主题词保护：仍给 SSRF"),
    ("反序列化 phar 打不通", "phar", "主题词保护：仍给 phar"),
    ("格式化字符串能改 GOT", "fmt-string", "fmt"),
    # 版本查询应先命中「版本分派总卡」而非某个具体 house —— 2026-11 新增 t080 后修正期望
    ("堆题 glibc 版本是 2.35", "glibc-version", "堆版本分派"),
    ("Android 关键逻辑在 so 里", "android", "JNI"),

    # —— 真实逆向证据（领域判别）——
    ("刚拿到堆题，还没定攻击方向，libc 版本未知",
     "glibc-version", "Pwn3 imgz：堆题先判版本"),
    ("堆题有 UAF，想 malloc 到任意地址", "tcache", "具体技术仍需命中具体卡"),
    ("700KB 静态链接 stripped ELF，控制流被拍平，疑似自定义虚拟机",
     "custom-vm", "Re3 chain_lock_vm"),
    ("printf(buf) 无格式化参数，PIE，只有 read/printf，6KB",
     "fmt-string", "Pwn1 blindfmt"),
    # —— 2026-11 第二轮补卡后新增 ——
    ("Java 反序列化，classpath 里有 CommonsBeanutils", "java-deser", "Java gadget"),
    ("JSON 深拷贝接口能控制 key，怀疑原型链", "node-proto", "Node 原型链"),
    ("Linux 内核模块有任意写，想提权", "kernel-pwn", "内核提权"),
    ("给了 vmem 内存镜像，要做取证", "forensics", "内存取证"),
    ("pyinstaller 打包的 exe", "rev-toolchain", "打包逆向"),
    ("AES 结构，256 字节表 + MixColumns + 14 轮", "aes-internals", "AES 内部"),
    ("只有一张 256 字节替换表，不知道是什么密码", "sbox", "纯 S-Box 场景仍走通用卡"),
    ("国密 SM4 加解密", "sm-cipher", "国密"),
    ("crackme 需要输对密码", "crackme", "crackme"),
    # —— 关键词清洗后：重复词必须落到专卡（2026-11 清洗回归）——
    ("fastbin", "fastbin-attack", "专卡优先"),
    ("tcache", "tcache-poisoning", "专卡优先"),
    ("uaf", "tcache-poisoning", "专卡优先"),
    ("double free", "fastbin-attack", "专卡优先"),
    ("phar", "phar-deser", "专卡优先"),
    ("coppersmith", "crypto-number-theory", "专卡优先"),
    ("jinja2", "ssti-jinja2-rce", "专卡优先"),
    # —— 停用词/分词回归（2026-11：泛词"二进制""只有"曾误命中 AES 卡）——
    ("二进制约 6KB PIE，只有 printf 和 read，判断有 seccomp", "orw-seccomp", "泛词不误导"),
    # 256 字节表 + 结构特征 → AES 内部卡更具体；纯表无结构时才是通用 S-Box
    ("二进制里出现 256 字节表", "aes-internals", "256字节表优先判 AES"),
    ("只有一张 256 字节替换表，不知道是什么密码", "sbox", "无结构时走通用 S-Box"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--threshold", type=float, default=0.85)
    args = ap.parse_args()

    sys.path.insert(0, os.path.join(ROOT, "mcp"))
    spec = importlib.util.spec_from_file_location("srv", os.path.join(ROOT, "mcp", "server.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    ok = 0
    fails = []
    for q, exp, note in CASES:
        r = m._find_technique_impl(signal=q, limit=1)["results"]
        got = r[0]["id"] if r else "(无)"
        hit = exp in got
        ok += hit
        if not hit:
            fails.append((q, exp, got, note))

    rate = ok / len(CASES)
    print(f"Top-1 命中: {ok}/{len(CASES)} = {rate:.1%}")
    if fails:
        print("\n未通过：")
        for q, exp, got, note in fails:
            print(f"  ✗ [{note}] {q[:40]!r}")
            print(f"      期望含 {exp}，实际 {got}")
    else:
        print("✓ 全部通过")

    if args.strict and rate < args.threshold:
        print(f"\n低于阈值 {args.threshold:.0%}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
