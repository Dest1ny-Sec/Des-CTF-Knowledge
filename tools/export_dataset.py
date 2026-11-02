#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_dataset.py — 把知识库导出成三种下游可直接用的格式。

为什么需要这个脚本
    本库的定位是「素材」而不是「产品」：使用者要自己决定做 RAG、做 CPT 语料、
    还是做 SFT。每种用途需要的数据形态完全不同，手工整理既慢又容易出错。

三种导出（互不干扰，可以只导出一种）
    rag    jsonl，一行一篇：{id, content, metadata}   给 AnythingLLM/Dify/RAGFlow 等
    cpt    txt，纯正文拼接（带分隔符）                 给继续预训练 (continue pretraining)
    sft    jsonl，{instruction, input, output}         给监督微调（只导出答案可验证的样本）

关键约定
    1. SFT 只导出「flag 真实且可验证」的样本，宁可少不可脏。
       假 flag（占位符、脱敏、<snip>）一律剔除，详见 is_verifiable_flag()。
    2. 本库 100% 图片被移除、约 57% 代码块换行被压平，
       导出时把这一事实写进每条 metadata，避免下游误以为代码可直接运行。
    3. 不修改源文件，只读。

用法
    python3 tools/export_dataset.py --format rag --out exports/
    python3 tools/export_dataset.py --format all --out exports/
    python3 tools/export_dataset.py --format sft --out exports/ --strict-flag
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
TECH_DIR = os.path.join(ROOT, "techniques")
TRAP_JSON = os.path.join(ROOT, "traps", "traps.json")

FLAG_RE = re.compile(r"flag\{[^}\n]{3,80}\}")

# 明显不是真实 flag 的形态
FAKE_PATTERNS = [
    re.compile(r"^flag\{[xX*·.\-_\s]+\}$"),                      # flag{xxxx}
    re.compile(r"^flag\{.{0,12}xxxx", re.I),                      # flag{18xxx23xxx}
    re.compile(r"<snip>|\.\.\.|<\.\.\.>|⋯", re.I),                # 被截断
    re.compile(r"(?i)^flag\{(thisisnotarealflag|notreal|fake|"
               r"example|placeholder|test|dummy|your_flag)", ),
]


def is_verifiable_flag(fl: str) -> bool:
    """判断一个 flag 字符串是否可能是真实、可验证的答案。"""
    if not FLAG_RE.fullmatch(fl):
        return False
    for pat in FAKE_PATTERNS:
        if pat.search(fl):
            return False
    body = fl[5:-1]
    if len(body) < 8:
        return False
    # 一半以上是 x/X 视为占位
    if (body.count("x") + body.count("X")) >= len(body) * 0.4:
        return False
    return True


def load_wps():
    out = []
    for path in sorted(glob.glob(os.path.join(WP_DIR, "*.md"))):
        b = open(path, "rb").read()
        if not b.startswith(b"---\n"):
            continue
        e = b.find(b"\n---\n", 4)
        if e < 0:
            continue
        try:
            fm = yaml.safe_load(b[4:e + 1].decode("utf-8", "replace")) or {}
        except Exception:
            continue
        body = b[e + 5:].decode("utf-8", "replace")
        out.append({"fm": fm, "body": body,
                    "file": os.path.basename(path),
                    "rel": os.path.relpath(path, ROOT)})
    return out


def content_quality(body):
    """给正文打质量标记，供下游过滤。"""
    issues = []
    if body.count("```") % 2:
        issues.append("fence_unbalanced")
    # 孤立短行 = 换行被压平的痕迹
    in_code = False
    orphans = 0
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code and 0 < len(line.strip()) <= 6 and not re.match(r"^\s*[}\]\)#/*]", line):
            orphans += 1
    if orphans >= 2:
        issues.append("code_newlines_flattened")
    if len(body) < 800:
        issues.append("very_short")
    return issues


def extract_flags(body):
    return sorted(set(FLAG_RE.findall(body)))


def build_record(wp, include_body=True):
    fm = wp["fm"]
    body = wp["body"]
    flags = [f for f in extract_flags(body) if is_verifiable_flag(f)]
    meta = {
        "source_file": wp["rel"],
        "title": fm.get("title"),
        "contest": fm.get("contest_normalized") or fm.get("contest"),
        "contest_year": fm.get("contest_year") or fm.get("year"),
        "category": fm.get("category"),
        "subcategory": fm.get("subcategory_guess") or fm.get("subcategory"),
        "tags": fm.get("tags") or [],
        "source_url": fm.get("source_url") or fm.get("wp_url"),
        "quality_issues": content_quality(body),
        "has_verifiable_flag": bool(flags),
        "images_removed": True,          # 全库事实
        "warnings": ["图片全部被移除，无法从正文恢复截图信息"],
    }
    rec = {"id": wp["rel"].replace("/", "__"), "metadata": meta}
    if include_body:
        rec["content"] = f"# {fm.get('title')}\n\n{body}"
    return rec, flags


# ---------------------------------------------------------------- 导出器
def export_rag(wps, out_dir):
    path = os.path.join(out_dir, "rag_corpus.jsonl")
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for wp in wps:
            rec, _ = build_record(wp)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return path, n


def export_cpt(wps, out_dir, min_len=800):
    path = os.path.join(out_dir, "cpt_corpus.txt")
    n, chars = 0, 0
    with open(path, "w", encoding="utf-8") as f:
        for wp in wps:
            fm = wp["fm"]
            body = wp["body"].strip()
            if len(body) < min_len:
                continue
            header = (f"\n\n===== {fm.get('contest_normalized') or fm.get('contest')}"
                      f" | {fm.get('category')} | {fm.get('title')} =====\n\n")
            f.write(header)
            f.write(body)
            n += 1
            chars += len(body)
    return path, n, chars


def export_sft(wps, out_dir):
    """
    生成 {instruction, input, output}。

    关键取舍（实测决定了这个设计）：
      本库 92% 的 WP 抽不到「题面」——开头是团队广告/赛事介绍，不是题干。
      因此不能用「题面→flag」这种 SFT 范式（会退化成背答案）。

      改用 WP 真正具备的结构：**相邻攻击链步骤构成「现象→应对」对**。
      实测 958 篇攻击链≥2步，其中 90% 的首步是可作现象的观察句。

    每篇 WP 可产出多个样本：
      (step[i] -> step[i+1])  现象→应对
      (最后一步 -> flag)      → 答案

    同时剔除跨题的污染：步骤里带「题1/题2」「第N题」的，在跳题处断开。
    """
    path = os.path.join(out_dir, "sft_dataset.jsonl")
    n = 0
    skipped = {"no_flag": 0, "too_thin": 0}
    broken = re.compile(r"^(题\s*\d|第[一二三四五六七八九十\d]+题|Q\d|Part\s*\d)")

    with open(path, "w", encoding="utf-8") as f:
        for wp in wps:
            fm = wp["fm"]
            body = wp["body"]
            flags = [x for x in extract_flags(body) if is_verifiable_flag(x)]
            if not flags:
                skipped["no_flag"] += 1
                continue
            chain = fm.get("attack_chain") or []
            if isinstance(chain, str):
                chain = [x.strip() for x in re.split(r"[→;；]", chain) if x.strip()]
            chain = [str(x).strip() for x in chain if str(x).strip()]
            if len(chain) < 2:
                skipped["too_thin"] += 1
                continue

            cat = str(fm.get("category") or "misc")
            sub = fm.get("subcategory_guess") or fm.get("subcategory") or cat
            base_instr = f"这是一道 CTF {cat}/{sub} 题。基于给出的观察，给出下一步该怎么做。"

            # 切分成"题内连续段"：遇到「题N」开头就断开，避免跨题配对
            segments, cur = [], []
            for step in chain:
                if broken.match(step) and cur:
                    segments.append(cur)
                    cur = []
                cur.append(step)
            if cur:
                segments.append(cur)

            meta_base = {"source_file": wp["rel"],
                         "contest": fm.get("contest_normalized"),
                         "category": cat, "flag": flags[0]}

            for seg in segments:
                if len(seg) < 2:
                    continue
                # 段内相邻配对
                for a, b in zip(seg, seg[1:]):
                    a = FLAG_RE.sub("[REDACTED]", a)
                    b = FLAG_RE.sub("[REDACTED]", b)
                    rec = {
                        "instruction": base_instr,
                        "input": a[:300],
                        "output": b[:400],
                        "meta": dict(meta_base, kind="step_pair"),
                    }
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n += 1
                # 段末 → flag
                # 若末步已含 flag，说明答案在输入里——截掉 flag，否则模型直接抄答案
                last = FLAG_RE.sub("[REDACTED]", seg[-1])
                if fm.get("lesson"):
                    out = f"{fm['lesson']}\n[flag] {flags[0]}"
                else:
                    out = f"[flag] {flags[0]}"
                rec = {
                    "instruction": base_instr,
                    "input": last[:300],
                    "output": out[:500],
                    "meta": dict(meta_base, kind="step_to_flag"),
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
    return path, n, skipped


def export_techniques(out_dir):
    """技法层单独导出——这是本库相对同类资源最有差异化的部分。"""
    made = []
    tj = os.path.join(TECH_DIR, "techniques.json")
    if os.path.exists(tj):
        d = json.load(open(tj, encoding="utf-8"))
        p = os.path.join(out_dir, "techniques.json")
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        made.append((p, len(d.get("techniques", []))))
    aj = os.path.join(TECH_DIR, "atoms.json")
    if os.path.exists(aj):
        d = json.load(open(aj, encoding="utf-8"))
        p = os.path.join(out_dir, "atoms.json")
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        made.append((p, len(d.get("atoms", []))))
    if os.path.exists(TRAP_JSON):
        d = json.load(open(TRAP_JSON, encoding="utf-8"))
        p = os.path.join(out_dir, "traps.json")
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        made.append((p, d.get("total_attempts", 0)))
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", default="all",
                    choices=["rag", "cpt", "sft", "tech", "all"])
    ap.add_argument("--out", default="exports")
    ap.add_argument("--strict-flag", action="store_true",
                    help="SFT 只保留 flag 形态非常规整的样本")
    args = ap.parse_args()

    out_dir = os.path.join(ROOT, args.out)
    os.makedirs(out_dir, exist_ok=True)
    wps = load_wps()
    print(f"扫描 {len(wps)} 篇 WP\n")

    if args.format in ("rag", "all"):
        p, n = export_rag(wps, out_dir)
        print(f"[RAG]  {os.path.relpath(p, ROOT)}  共 {n} 条")

    if args.format in ("cpt", "all"):
        p, n, chars = export_cpt(wps, out_dir)
        print(f"[CPT]  {os.path.relpath(p, ROOT)}  {n} 篇 / {chars/1e6:.1f}M 字符")

    if args.format in ("sft", "all"):
        p, n, sk = export_sft(wps, out_dir)
        print(f"[SFT]  {os.path.relpath(p, ROOT)}  {n} 条  "
              f"(跳过 WP: 无可用flag {sk['no_flag']}, 攻击链太短 {sk['too_thin']})")

    if args.format in ("tech", "all"):
        made = export_techniques(out_dir)
        for p, n in made:
            print(f"[TECH] {os.path.relpath(p, ROOT)}  {n} 条")

    print(f"\n✓ 输出目录: {args.out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
