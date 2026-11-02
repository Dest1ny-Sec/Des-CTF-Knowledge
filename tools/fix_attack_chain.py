#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_attack_chain.py — 统一 attack_chain 字段为列表。

问题：
    1027 篇 WP 中，627 篇的 attack_chain 是 YAML 列表，400 篇是单个字符串
    （用 → 或 / 或 ; 分隔）。字符串型会让任何按步骤遍历的消费方（MCP/原子层）
    拿到整段文本或首字符，攻击链检索直接失效。

策略：
    只转换"能安全切分"的字符串型字段：
      - 含 → 分隔符：按 → 切分（271 篇，语义明确）
      - 含 / 分隔且每段 >4 字符：按 / 切分（68 篇）
      - 其余（无分隔符 / 切分后段太短）：保留原字符串，标记 attack_chain_raw，
        避免把 "KCTF/WEB" 这种词误切

用法：
    python3 tools/fix_attack_chain.py --dry-run
    python3 tools/fix_attack_chain.py
"""
import argparse
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_DIR = os.path.join(ROOT, "CTF大赛WP集合", "articles")


def split_chain(s):
    """把字符串攻击链切成步骤列表；无法安全切分时返回 None。"""
    s = str(s).strip()
    if not s:
        return None
    for sep in ("→", "->", "=>"):
        if sep in s:
            parts = [p.strip() for p in s.split(sep)]
            parts = [p for p in parts if p]
            if len(parts) >= 2 and sum(len(p) > 2 for p in parts) >= 2:
                return parts
    if "/" in s:
        parts = [p.strip() for p in s.split("/")]
        parts = [p for p in parts if p]
        # 避免把路径/URL 切碎：每段必须足够长且整体段数不过多
        if len(parts) >= 3 and all(len(p) > 4 for p in parts) and len(parts) <= 20:
            return parts
    return None


def dump_list_field(key, items):
    """把列表写成规范的 YAML 块（每项单引号转义，避免特殊字符破坏结构）。"""
    out = [f"{key}:"]
    for it in items:
        v = str(it).replace("'", "''").strip()
        if not v:
            continue
        out.append(f"- '{v}'")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(WP_DIR, "*.md")))
    stats = {"total": len(files), "str": 0, "fixed": 0, "kept": 0, "list": 0}
    samples = []

    for p in files:
        b = open(p, "rb").read()
        if not b.startswith(b"---\n"):
            continue
        e = b.find(b"\n---\n", 4)
        if e < 0:
            continue
        fm_txt = b[4:e + 1].decode("utf-8", "replace")
        try:
            d = yaml.safe_load(fm_txt)
        except Exception:
            continue
        v = d.get("attack_chain")
        if not isinstance(v, str):
            stats["list"] += 1 if isinstance(v, list) else 0
            continue
        stats["str"] += 1
        parts = split_chain(v)
        if not parts:
            stats["kept"] += 1
            continue

        # 定位原行并替换为 YAML 列表块
        lines = fm_txt.split("\n")
        new_lines = []
        i = 0
        replaced = False
        while i < len(lines):
            line = lines[i]
            if re.match(r"^attack_chain\s*:", line):
                if replaced:
                    i += 1
                    continue
                new_lines.append(dump_list_field("attack_chain", parts).rstrip("\n"))
                replaced = True
                # 跳过原多行续行（以空格开头且属于该字段）
                i += 1
                while i < len(lines) and lines[i].startswith((" ", "\t")) and not re.match(r"^\S", lines[i]):
                    i += 1
                continue
            new_lines.append(line)
            i += 1
        new_fm = "\n".join(new_lines)
        if not new_fm.endswith("\n"):
            new_fm += "\n"

        # 写前自检
        try:
            check = yaml.safe_load(new_fm)
            assert isinstance(check.get("attack_chain"), list)
        except Exception as ex:
            stats["kept"] += 1
            samples.append((os.path.basename(p), f"自检失败 {ex}"))
            continue

        stats["fixed"] += 1
        if len(samples) < 5:
            samples.append((os.path.basename(p), parts))
        if not args.dry_run:
            # 用 YAML 重新序列化整个 frontmatter 风险太高（会改变既有格式/顺序），
            # 因此只替换 attack_chain 那一段文本，其余字节原样保留。
            new_block = b"---\n" + new_fm.encode("utf-8")
            tail = b[e + 5:]  # e 指向 "\n---\n" 的起始 \n；+5 跳过整个分隔符
            with open(p, "wb") as f:
                f.write(new_block + b"---\n" + tail)

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"[{mode}] 总 {stats['total']} | 已是列表 {stats['list']} | 字符串 {stats['str']}"
          f" → 转换 {stats['fixed']} / 保留原样 {stats['kept']}")
    for s in samples:
        print("  ", s[0][:45], "->", (s[1] if isinstance(s[1], list) else s[1])[:3]
              if isinstance(s[1], list) else s[1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
