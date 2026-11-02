#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean_cards.py — 清理技法卡片的关键词重叠。

为什么需要
    68 张卡共 405 个关键词，其中 26 个跨卡重复。重复本身不可怕，
    可怕的是**泛卡抢走专卡的关键词**：
        查询 "fastbin"  →  t012-heap-tcache（泛卡）  而不是 t087-fastbin-attack（专卡）
        查询 "tcache"   →  t012-heap-tcache（泛卡）  而不是 t086-tcache-poisoning（专卡）
    结果是用户拿到的是"大而全"的卡，看不到真正针对问题的卡。

清洗规则（按优先级）
    1. **专卡优先**：若某个关键词是某张卡 name 的核心词（专卡），
       则从其他卡里删掉这个词。
    2. **泛卡让位**：证据数最多 / 名字最泛的卡（如 heap-tcache 这种族卡），
       让出具体技术词。
    3. **保留跨卡合法性**：`oracle` 在 cryptography 语境和 blackbox 语境都合理，
       但如果两张卡领域不同则允许保留（它们不会互相抢）。
    4. **自冗余清理**：关键词已在 signal 里完整出现时，不算重复，保留。

产出
    techniques/CARDS-CLEANUP.md   清理报告（改了什么、为什么）
    直接修改 techniques/cards/*.yaml

用法
    python3 tools/clean_cards.py --dry-run
    python3 tools/clean_cards.py
"""
import argparse
import glob
import os
import re
import sys
from collections import defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_DIR = os.path.join(ROOT, "techniques", "cards")
OUT_MD = os.path.join(ROOT, "techniques", "CARDS-CLEANUP.md")


def load_cards():
    cards = []
    for p in sorted(glob.glob(os.path.join(CARD_DIR, "*.yaml"))):
        try:
            d = yaml.safe_load(open(p, encoding="utf-8"))
        except Exception as e:
            print(f"⚠ 跳过 {os.path.basename(p)}: {e}", file=sys.stderr)
            continue
        if not isinstance(d, dict) or "id" not in d:
            continue
        cards.append({"path": p, "data": d})
    return cards


def card_specificity(card):
    """专卡分：name 里出现该关键词 = 高专；证据多的族卡 = 低。"""
    d = card["data"]
    return len(str(d.get("name") or "")), int(d.get("evidence_count") or 0)


def is_family_card(d):
    """族卡判定：name 里带"总/矩阵/识别/工作流/工具链/家族"这类概括词。"""
    name = str(d.get("name") or "")
    return any(k in name for k in ["矩阵", "分派", "家族", "工具链", "工作流",
                                   "识别", "细则", "四步法", "选择"])


def plan_cleanup(cards):
    """返回 {card_id: [要删除的关键词]}，以及说明列表。"""
    owner = defaultdict(list)          # keyword -> [card]
    for c in cards:
        d = c["data"]
        for k in (d.get("keywords") or []):
            owner[str(k).lower().strip()].append(c)

    actions = []
    removals = defaultdict(list)

    for kw, cs in owner.items():
        if len(cs) < 2:
            continue
        # 领域不同的卡：允许共存（不会相互争抢）
        domains = {str(c["data"].get("domain")) for c in cs}
        if len(domains) > 1:
            actions.append((kw, "保留", f"跨领域（{sorted(domains)}），不构成争抢", [c["data"]["id"] for c in cs]))
            continue

        # 专卡：name 含该关键词
        # 专卡判定：name 的英文部分含该词，或关键词词干出现在 name 里
        def _spec(c):
            name = str(c["data"].get("name") or "").lower()
            # 归一化：去掉空格/连字符，"fastbin attack" 也能匹配 "fastbin"
            flat = re.sub(r"[\s_\-]", "", name)
            kflat = re.sub(r"[\s_\-]", "", kw)
            return kflat and (kflat in flat)

        specialist = [c for c in cs if _spec(c)]
        if specialist:
            # 多张专卡都 name 含该词时，全部保留（各自都有资格用这个词），
            # 只从"非专卡"里删掉
            winners = {c["data"]["id"] for c in specialist}
            for c in cs:
                cid = c["data"]["id"]
                if cid in winners:
                    continue
                removals[cid].append(kw)
            if len(winners) == len(cs):
                actions.append((kw, "保留",
                                f"全部是专卡（{sorted(winners)}），各自 name 都含此词",
                                sorted(winners)))
            else:
                actions.append((kw, "删除",
                                f"专卡 {sorted(winners)} 保留，其余移除",
                                [c["data"]["id"] for c in cs]))
            continue

        # 无专卡：让族卡让位，保留非族卡
        families = [c for c in cs if is_family_card(c["data"])]
        others = [c for c in cs if not is_family_card(c["data"])]
        if families and others:
            for c in families:
                removals[c["data"]["id"]].append(kw)
            actions.append((kw, "删除",
                            f"族卡 {[c['data']['id'] for c in families]} 让位给 {[c['data']['id'] for c in others]}",
                            [c["data"]["id"] for c in cs]))
            continue

        # 都非族卡也都非专卡：保留所有（多语义是合法的）
        actions.append((kw, "保留",
                        "多处合理使用且无专卡/族卡区分", [c["data"]["id"] for c in cs]))

    return removals, actions


def write_back(card, remove_kws, dry_run):
    d = dict(card["data"])
    kws = [str(k) for k in (d.get("keywords") or [])]
    keep = [k for k in kws if k.lower().strip() not in remove_kws]
    if keep == kws:
        return False
    d["keywords"] = keep
    if not dry_run:
        with open(card["path"], "w", encoding="utf-8") as f:
            yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False,
                           width=1000, default_flow_style=False)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cards = load_cards()
    removals, actions = plan_cleanup(cards)

    changed = 0
    for c in cards:
        cid = c["data"]["id"]
        if cid in removals:
            if write_back(c, set(removals[cid]), args.dry_run):
                changed += 1

    # 报告
    L = []
    L.append("<!-- AUTO-GENERATED by tools/clean_cards.py -->")
    L.append("# 卡片关键词清洗报告")
    L.append("")
    L.append(f"卡片 **{len(cards)}** 张，处理跨卡重复关键词。")
    L.append("")
    L.append("## 处理明细")
    L.append("")
    L.append("| 关键词 | 决定 | 理由 | 相关卡片 |")
    L.append("|---|---|---|---|")
    for kw, act, why, ids in actions:
        L.append(f"| `{kw}` | {act} | {why} | {', '.join(ids)} |")
    L.append("")
    L.append("## 被修改的卡片")
    L.append("")
    for cid, kws in sorted(removals.items()):
        L.append(f"- **{cid}**：移除 {', '.join(f'`{k}`' for k in kws)}")
    L.append("")
    if not args.dry_run:
        with open(OUT_MD, "w", encoding="utf-8") as f:
            f.write("\n".join(L))

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"[{mode}] 检查 {len(actions)} 组重复关键词 | 修改 {changed} 张卡")
    keeps = sum(1 for _, a, _, _ in actions if a == "保留")
    deletes = len(actions) - keeps
    print(f"  删除 {deletes} 组 / 保留 {keeps} 组")
    for cid, kws in sorted(removals.items()):
        print(f"    {cid}: -{', '.join(kws)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
