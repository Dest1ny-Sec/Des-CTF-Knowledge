#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_frontmatter.py — 统一 WP 的 frontmatter 字段，便于 agent 结构化过滤。

改动（只增不改，幂等）：
  1. 新增 contest_normalized：去掉年份/战队名/括注，统一大小写与别名，用于"找某场大赛"
  2. 新增 contest_year：从 contest / year 字段提取，`year: null` 时也能补全
  3. 原 contest 字段保持不变（保留原始信息，不破坏溯源）
  4. subcategory 为 *_other 时新增 subcategory_guess（基于 tags/attack_chain 的启发式归类），
     不覆盖原值

用法：
    python3 tools/normalize_frontmatter.py --dry-run
    python3 tools/normalize_frontmatter.py
"""
import argparse
import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_DIR = os.path.join(ROOT, "CTF大赛WP集合", "articles")

# 大赛别名表：key 为规范名，values 为可识别的变体（小写、去空格后匹配）
ALIASES = {
    "KCTF": ["kctf", "看雪kctf"],
    "强网杯": ["强网杯", "qiangwang", "qiangwang cup"],
    "强网拟态": ["强网拟态"],
    "西湖论剑": ["西湖论剑"],
    "网鼎杯": ["网鼎杯"],
    "长城杯": ["长城杯", "ccb"],
    "春秋杯": ["春秋杯"],
    "羊城杯": ["羊城杯"],
    "CISCN": ["ciscn", "国赛", "全国大学生信息安全竞赛"],
    "SCTF": ["sctf"],
    "RCTF": ["rctf"],
    "N1CTF": ["n1ctf"],
    "NCTF": ["nctf"],
    "WCTF": ["wctf"],
    "WMCTF": ["wmctf"],
    "ByteCTF": ["bytectf"],
    "SUCTF": ["suctf"],
    "HITCON": ["hitcon"],
    "SECCON": ["seccon"],
    "RealWorld CTF": ["realworld", "rwctf", "real world ctf"],
    "DASCTF": ["dasctf"],
    "DataCon": ["datacon"],
    "HCTF": ["hctf"],
    "ACTF": ["actf"],
    "BCTF": ["bctf"],
    "Google CTF": ["google ctf"],
    "Plaid CTF": ["plaid ctf"],
    "DEFCON": ["defcon"],
    "0CTF/TCTF": ["0ctf", "tctf", "0ctf/tctf"],
    "数字中国": ["数字中国"],
    "蓝帽杯": ["蓝帽杯"],
    "AWS CTF": ["aws ctf"],
    "HKCERT": ["hkcert"],
    "腾讯游戏安全": ["腾讯游戏安全"],
    "TCTF": ["tctf"],
    "CSAW": ["csaw"],
    "AIxCC": ["aixcc"],
}

# subcategory 启发式关键词（按优先级）
SUBCAT_RULES = [
    ("sql_injection", ["sql注入", "union select", "information_schema", "报错注入", "盲注", "sql injection"]),
    ("ssrf", ["ssrf", "gopher", "dict://", "内网探测"]),
    ("ssti", ["ssti", "模板注入", "jinja2", "twig", "smarty", "__subclasses__"]),
    ("xxe", ["xxe", "xml外部实体", "外部实体"]),
    ("lfi", ["lfi", "文件包含", "php://filter", "php://input"]),
    ("file_upload", ["文件上传", "upload", "webshell", "一句话木马"]),
    ("deserialization", ["反序列化", "pop链", "phar", "unserialize", "wakeup", "gadget"]),
    ("jwt", ["jwt", "alg none", "kid注入"]),
    ("xss", ["xss", "跨站脚本"]),
    ("prototype_pollution", ["原型链污染", "prototype pollution"]),
    ("rce", ["rce", "命令执行", "command injection", "反弹shell", "disable_functions"]),
    ("stego", ["隐写", "lsb", "stegsolve", "盲水印", "zsteg"]),
    ("archive", ["压缩包", "zip", "crc爆破", "伪加密", "明文攻击"]),
    ("traffic_analysis", ["流量分析", "pcap", "usb流量", "wireshark", "tshark"]),
    ("memory_forensics", ["内存取证", "volatility", "coredump"]),
    ("disk_forensics", ["磁盘取证", "disk image", "e01"]),
    ("reverse", ["逆向", "undo", "逆向分析", "反编译"]),
    ("rsa", ["rsa", "共模", "低加密指数", "wiener"]),
    ("lattice", ["lattice", "格攻击", "lll", "格基"]),
    ("symmetric", ["aes", "des", "分组密码", "cbc", "ecb"]),
    ("heap_exploitation", ["heap", "堆布局", "tcache", "unsorted bin", "house of"]),
    ("rop", ["rop", "ret2", "栈溢出", "gadget chain"]),
    ("kernel", ["kernel", "内核", "提权"]),
    ("vm", ["虚拟机", "opcode", "字节码"]),
    ("blockchain", ["区块链", "solidity", "智能合约", "ethereum"]),
    ("osint", ["osint", "开源情报"]),
    ("misc_misc", ["misc"]),
]

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def load_fm(path):
    b = open(path, "rb").read()
    if not b.startswith(b"---\n"):
        return None, b, None
    e = b.find(b"\n---\n", 4)
    if e < 0:
        return None, b, None
    return yaml.safe_load(b[4:e + 1].decode("utf-8", "replace")), b, e


def normalize_contest(contest, title):
    raw = str(contest or "") + " " + str(title or "")
    low = raw.lower()
    for canonical, pats in ALIASES.items():
        for p in pats:
            if p in low:
                return canonical
    # 无别名命中：去掉括注/战队名/年份后作为规范名
    base = str(contest or "").strip()
    base = re.sub(r"[（(].*?[)）]", "", base)
    base = re.sub(r"\b(19|20)\d{2}\b", "", base)
    base = re.sub(r"\s+", " ", base).strip(" -_·")
    return base or None


def guess_year(contest, year, title):
    for src in (year, contest, title):
        if src is None:
            continue
        m = YEAR_RE.search(str(src))
        if m:
            return int(m.group(0))
    return None


def guess_subcategory(tags, attack_chain, observations, title, one_liner):
    blob = " ".join(
        [str(x) for x in (tags or [])]
        + [str(x) for x in (attack_chain or [])]
        + [str(x) for x in (observations or [])]
        + [str(title or ""), str(one_liner or "")]
    ).lower()
    for name, keys in SUBCAT_RULES:
        for k in keys:
            if k in blob:
                return name
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(WP_DIR, "*.md")))
    stats = {"files": 0, "changed": 0, "new_contest": 0, "new_year": 0, "new_subcat": 0}
    frag_before, frag_after = set(), set()

    for p in files:
        fm, raw, end = load_fm(p)
        if fm is None:
            continue
        stats["files"] += 1
        frag_before.add(str(fm.get("contest")))

        norm = normalize_contest(fm.get("contest"), fm.get("title"))
        yr = guess_year(fm.get("contest"), fm.get("year"), fm.get("title"))
        if yr:
            frag_after.add(f"{norm} {yr}")

        changed = False
        additions = []
        if norm and fm.get("contest_normalized") != norm:
            additions.append(("contest_normalized", norm))
            changed = True
        if yr and fm.get("contest_year") != yr:
            additions.append(("contest_year", yr))
            changed = True

        sub = str(fm.get("subcategory") or "")
        if sub.endswith("_other"):
            g = guess_subcategory(fm.get("tags"), fm.get("attack_chain"),
                                  fm.get("key_observations"), fm.get("title"),
                                  fm.get("one_liner"))
            if g and fm.get("subcategory_guess") != g:
                additions.append(("subcategory_guess", g))
                changed = True

        if not changed:
            continue
        stats["changed"] += 1
        if any(a[0] == "contest_normalized" for a in additions):
            stats["new_contest"] += 1
        if any(a[0] == "contest_year" for a in additions):
            stats["new_year"] += 1
        if any(a[0] == "subcategory_guess" for a in additions):
            stats["new_subcat"] += 1

        # 在 frontmatter 末尾插入（保持原有字段顺序与格式）
        fm_block = raw[4:end + 1].decode("utf-8", "replace")
        if not fm_block.endswith("\n"):
            fm_block += "\n"
        for k, v in additions:
            if isinstance(v, int):
                fm_block += f"{k}: {v}\n"
            else:
                # 必须用 json.dumps 安全转义：contest 名里含双引号
                # （如 首届"山石·蒙山杯"）会破坏 YAML 块结构
                fm_block += f"{k}: {json.dumps(str(v), ensure_ascii=False)}\n"
        new_raw = b"---\n" + fm_block.encode("utf-8") + raw[end + 1:]

        # 写前自检：新 frontmatter 必须能被严格解析，否则跳过并记录
        try:
            yaml.safe_load(fm_block)
        except Exception as ex:
            stats.setdefault("_skipped", []).append((os.path.basename(p), str(ex)[:80]))
            continue

        if not args.dry_run:
            with open(p, "wb") as f:
                f.write(new_raw)

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"[{mode}] WP {stats['files']} | 修改 {stats['changed']} | "
          f"contest_normalized {stats['new_contest']} | contest_year {stats['new_year']} | "
          f"subcategory_guess {stats['new_subcat']}")
    print(f"  contest 去重: {len(frag_before)} → {len(frag_after)}")
    skipped = stats.get("_skipped", [])
    if skipped:
        print(f"  ⚠ 解析自检未通过而跳过 {len(skipped)} 个文件:", file=sys.stderr)
        for name, err in skipped[:5]:
            print(f"    - {name}: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
