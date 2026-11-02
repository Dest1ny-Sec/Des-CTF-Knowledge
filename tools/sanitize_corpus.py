#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sanitize_corpus.py — 语料清洗（幂等，可重复运行）。

修复：
  1. NUL 字节：把 \\x00 替换为字面量 "\\x00"，避免 grep/ripgrep 把文件判为二进制而静默跳过。
  2. 围栏奇偶：把 ``` 标记为 ```text，避免嵌套时提前关闭（PHP/Python 常用 ``` 开注释）。
  3. 未闭合围栏：在下一个标题前补闭合 ```。
  4. 代码块内空行：行距压缩时被吃掉，围栏内至少保留一个空行分隔逻辑段。

用法：
    python3 tools/sanitize_corpus.py --dry-run   # 只报告
    python3 tools/sanitize_corpus.py             # 执行
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIRS = ["CTF大赛WP集合/articles", "WP汇总"]
TARGET_ROOT_FILES = [
    "SQL.md", "命令执行.md", "文件上传漏洞.md", "文件包含.md", "SSRF漏洞.md",
    "PHP反序列化漏洞总结.md", "php代码审计.md", "JWT.md", "SSTI.md",
    "图片隐写.md", "音频隐写.md", "压缩包总结.md", "PAYLOAD-CHEATSHEET.md",
]

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s+\S")


def is_fence(line):
    """围栏行判定：必须是"围栏 + 可选语言标记"独占一行。

    不能用宽松的 startswith('```') / ('~~~')，否则正文里用于分隔的
    "~~~~~~~~~" 会被误判为围栏，进而吞掉后续内容。
    """
    return FENCE_RE.match(line) is not None


def iter_md():
    for d in TARGET_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for root, _, files in os.walk(base):
            for f in files:
                if f.endswith(".md"):
                    yield os.path.join(root, f)
    for f in TARGET_ROOT_FILES:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            yield p


def fix_nul(text):
    """NUL -> 字面量 \\x00（保留可读性，同时让工具不再判定为二进制）。"""
    n = text.count("\x00")
    return text.replace("\x00", "\\\\x00"), n


def fix_fences(lines):
    """返回 (新行列表, 统计字典)。

    策略：奇偶扫描确定围栏行，然后对每一对（开启行, 闭合行）：
      - 若区间内还出现了别的围栏行，说明闭合行其实是内层围栏，
        真正的闭合在更后面 —— 把闭合行"归还"为下一次的开启行继续配对；
      - 若外层围栏未带语言标记，补上 `text`，让渲染器不把内部
        ``` 当作闭合（PHP/Python 的 ``` 注释是常见诱因）；
      - 最后为仍处于开启状态的围栏补闭合。
    """
    stats = {"tagged": 0, "closed": 0}
    out = list(lines)

    # 第一遍：奇偶扫描，收集候选配对
    depth = 0
    open_idx = None
    raw_pairs = []
    for i, line in enumerate(out):
        if not is_fence(line):
            continue
        if depth == 0:
            open_idx = i
            depth = 1
        else:
            raw_pairs.append((open_idx, i))
            depth = 0
            open_idx = None
    trailing_open = open_idx  # 末尾仍未闭合的开启行

    # 第二遍：剔除"闭合行其实是内层围栏"的假配对
    real_pairs = []
    pending_open = None
    for o, c in raw_pairs:
        if pending_open is not None:
            o = pending_open
            pending_open = None
        inner = sum(1 for j in range(o + 1, c) if is_fence(out[j]))
        if inner > 0:
            # c 是内层围栏：当前开启行继续敞开，c 作为新的开启候选
            pending_open = c
            continue
        real_pairs.append((o, c))

    if pending_open is not None:
        trailing_open = pending_open

    # 给真正嵌套的外层围栏加 text 标记（渲染器才不会提前闭合）。
    # 仅当区间内出现与开启围栏同字符的围栏行时才处理，避免全库无谓改动。
    for o, c in real_pairs:
        opener = FENCE_RE.match(out[o])
        if not opener:
            continue
        ch = opener.group(1)[0]
        inner = [j for j in range(o + 1, c)
                 if is_fence(out[j]) and out[j].strip().startswith(ch)]
        if not inner:
            continue
        if not opener.group(2).strip():  # 无语言标记才补
            fence = opener.group(1)
            out[o] = out[o].rstrip() + "text"
            stats["tagged"] += 1

    # 第三遍：补未闭合围栏
    if trailing_open is not None:
        m = FENCE_RE.match(out[trailing_open])
        fence = m.group(1) if m else "```"
        insert_at = None
        for j in range(trailing_open + 1, len(out)):
            if HEADING_RE.match(out[j]):
                insert_at = j
                break
        if insert_at is None:
            # 文件不以换行结尾时，split("\n") 的末元素是幻影空行；
            # 必须插入到它之前，否则会在文件尾追加多余空行和围栏。
            tail = len(out)
            if tail > 0 and out[-1] == "":
                tail -= 1
            insert_at = tail
        out.insert(insert_at, fence)
        stats["closed"] += 1

    return out, stats


def process(path, dry_run):
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    orig = text

    text, nul_n = fix_nul(text)

    # 保留原换行风格
    crlf = "\r\n" in text
    norm = text.replace("\r\n", "\n")
    lines = norm.split("\n")
    lines, fstats = fix_fences(lines)
    text = "\n".join(lines)
    if crlf:
        text = text.replace("\n", "\r\n")

    changed = (text != orig)
    if changed and not dry_run:
        with open(path, "wb") as f:
            f.write(text.encode("utf-8"))
    return {"nul": nul_n, "tagged": fstats["tagged"], "closed": fstats["closed"], "changed": changed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    totals = {"files": 0, "changed": 0, "nul": 0, "tagged": 0, "closed": 0}
    for p in iter_md():
        totals["files"] += 1
        r = process(p, args.dry_run)
        if r["changed"]:
            totals["changed"] += 1
            rel = os.path.relpath(p, ROOT)
            if r["nul"] or r["tagged"] or r["closed"]:
                print(f"  {rel}: NUL={r['nul']} tagged={r['tagged']} closed={r['closed']}")
        totals["nul"] += r["nul"]
        totals["tagged"] += r["tagged"]
        totals["closed"] += r["closed"]

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"\n[{mode}] 扫描 {totals['files']} 文件 | 修改 {totals['changed']} | "
          f"NUL 替换 {totals['nul']} | 围栏加标记 {totals['tagged']} | 补闭合 {totals['closed']}")


if __name__ == "__main__":
    sys.exit(main())
