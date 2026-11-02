#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_articles.py — 把抓取到的公众号文章按题目边界拆成单题 WP 入库。

现有 1027 篇大赛 WP 都是"一篇文章 = 一个文件"，但微信公众号的赛后合集
往往一篇文章里有 5-30 道题。直接整篇入库会让 agent 检索时拿到一堆无关题面，
因此这里按题目边界拆分，每道题生成独立 WP + 标准 frontmatter。

用法：
    python3 tools/import_articles.py --dry-run
    python3 tools/import_articles.py
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_DIR = os.path.join(ROOT, "CTF大赛WP集合", "articles")
SRC_DIR = "/tmp/wparticles"

# 每篇文章的切分规则：(源键, 输出大赛名, category, 正则, 年份)
JOBS = [
    {
        "src": "ind",
        "contest": "2026中国工业互联网安全大赛-线上预选赛",
        "category_default": "crypto",
        "year": 2026,
        "url": "https://mp.weixin.qq.com/s/cgHv-Q7oTSufiJK9QOxu4w",
        "pattern": r"^任务(\d+)｜(.+?)：(.+)$",
        "cat_of": {"misc": "misc", "crypto": "crypto", "pwn": "pwn",
                   "reverse": "reverse", "web": "web"},
    },
    {
        "src": "qwb3",
        "contest": "强网杯 2026 第十届",
        "category_default": "misc",
        "year": 2026,
        "url": "https://mp.weixin.qq.com/s/onGfTPOi9N7Ak9UWWmMNoA",
        "pattern": r"^((?:Misc|Crypto|Pwn|Reverse|Web)\d*)[-－]\s*(.+)$",
        "cat_of": {"misc": "misc", "crypto": "crypto", "pwn": "pwn",
                   "reverse": "reverse", "web": "web"},
    },
    {
        "src": "mimic",
        "contest": "强网拟态防御 第九届",
        "category_default": "misc",
        "year": 2025,
        "url": "https://mp.weixin.qq.com/s/iTgaxzumnH3cE4N5nH6VvQ",
        "pattern": r"^((?:WEB|MISC|PWN|RE|CRYPTO)[-－]\s*.+|FilmReader-镜像取证|失陷主机流量分析.*)$",
        "cat_of": {"web": "web", "misc": "misc", "pwn": "pwn",
                   "re": "reverse", "crypto": "crypto"},
    },
]


def split_sections(text, pattern):
    """按题目正则切分，返回 [(title, body, cat_prefix)]。"""
    lines = text.split("\n")
    marks = []
    rx = re.compile(pattern)
    for i, l in enumerate(lines):
        s = l.strip()
        if not s or len(s) > 60:
            continue
        m = rx.match(s)
        if m:
            marks.append((i, s, m))
    out = []
    for k, (i, s, m) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(lines)
        body = "\n".join(lines[i:end]).strip()
        if len(body) < 200:      # 太短的是目录条目，不是题解
            continue
        out.append((s, body))
    return out


def guess_cat(job, title, body):
    low = title.lower()
    # 1) 标题里的显式前缀（crypto-2 / misc-3 / pwn-1）最可信
    m = re.search(r"\b(crypto|misc|pwn|reverse|web|re)[-－]?\d*\s*[:：]", low)
    if m:
        return job["cat_of"].get(m.group(1), job["category_default"])
    # 2) 标题整体前缀（Misc1- / WEB- / CRYPTO-）
    for pref, cat in job["cat_of"].items():
        if low.startswith(pref.lower() + "-") or low.startswith(pref.lower() + "1-"):
            if pref.lower() in ("crypto", "misc", "pwn", "re", "web"):
                # Misc1 / Crypto1 形式
                if re.match(r"^" + pref.lower() + r"\d", low):
                    return cat
    if low.startswith("web-"):
        return "web"
    if low.startswith("misc-"):
        return "misc"
    if low.startswith("crypto-"):
        return "crypto"
    if low.startswith("pwn-"):
        return "pwn"
    # 3) 正文关键词兜底
    if re.search(r"逆向分析|ida|反编译|opcode|vm 解释器", body[:800], re.I):
        return "reverse"
    if re.search(r"流量|pcap|取证|modbus|iec104|opc ua|磁盘", body[:900], re.I):
        return "misc"
    if re.search(r"aes|cbc|ecb|gcm|ghash|lfsr|rsa|ecc|nonce|格|共模", body[:900], re.I):
        return "crypto"
    if re.search(r"heap|stack|libc|rop|uaf|栈溢出", body[:800], re.I):
        return "pwn"
    return job["category_default"]


def safe_name(s):
    s = re.sub(r"[\\/:*?\"<>|\n\r\t]", "_", s)
    s = re.sub(r"\s+", "_", s.strip())
    return s[:80]


def build_fm(title, contest, year, category, url, body):
    # 提取 flag
    flags = re.findall(r"flag\{[^}\n]{1,120}\}", body)
    # 提取关键步骤：带编号的小节标题
    steps = re.findall(r"^\s*(?:\d+(?:\.\d+)*|[一二三四五六七八九十]+)[\.、]?\s*(.{4,50})$", body, re.M)
    steps = [s.strip() for s in steps if s.strip()][:6]

    fm = {
        "title": title,
        "contest": contest,
        "contest_normalized": contest,
        "contest_year": year,
        "year": year,
        "category": category,
        "subcategory": category + "_other",
        "tags": [],
        "attack_chain": steps,
        "one_liner": (body.split("\n")[1] if len(body.split("\n")) > 1 else title)[:120],
        "lesson": "",
        "quality": "medium",
        "schema_version": "v3.0.0-P0",
        "source_type": "wechat_article",
        "source_url": url,
        "last_verified": "2026-11-02",
    }
    if flags:
        fm["flag_observed"] = sorted(set(flags))[:3]
    return fm


def dump_fm(d):
    out = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            if not v:
                out.append(f"{k}: []")
            else:
                out.append(f"{k}:")
                for it in v:
                    out.append(f"- '{str(it).replace(chr(39), chr(39)*2)}'")
        elif isinstance(v, int):
            out.append(f"{k}: {v}")
        else:
            s = str(v).replace("'", "''")
            out.append(f"{k}: '{s}'")
    out.append("---")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total = 0
    for job in JOBS:
        p = os.path.join(SRC_DIR, job["src"] + ".txt")
        if not os.path.exists(p):
            print(f"⚠ 缺少源文件 {p}", file=sys.stderr)
            continue
        text = open(p, encoding="utf-8").read()
        secs = split_sections(text, job["pattern"])
        print(f"\n[{job['contest']}] 切出 {len(secs)} 道题")
        for title, body in secs:
            cat = guess_cat(job, title, body)
            fm = build_fm(title, job["contest"], job["year"], cat, job["url"], body)
            fname = safe_name(f"{job['contest']}_{title}") + ".full.md"
            total += 1
            print(f"  - {cat:8} {title[:45]:45} {len(body):6}字 -> {fname[:60]}")
            if not args.dry_run:
                with open(os.path.join(WP_DIR, fname), "w", encoding="utf-8") as f:
                    f.write(dump_fm(fm) + "\n\n" + body + "\n")
    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}共 {total} 道题")
    return 0


if __name__ == "__main__":
    sys.exit(main())
