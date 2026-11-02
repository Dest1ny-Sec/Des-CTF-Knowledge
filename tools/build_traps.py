#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_traps.py — 把 WP 里的 failed_attempts 聚合成 agent 可用的"陷阱表"。

为什么需要：
    真人做错会意识到"我走错了"，agent 不会——它会在错误路径上继续堆砌。
    把 1027 篇 WP 里的失败尝试按"失败信号"聚类，agent 观察到自己处于某个信号时，
    就能主动触发"我可能走错路了"的怀疑。

输出：
    traps/TRAPS-INDEX.md   — 人类可读 + 机器可解析的陷阱总表
    traps/traps.json       — 结构化版本，供 MCP server / RAG 消费

解析规则：
    形如 "尝试X → 失败：原因" 的条目，切分为 (attempt, reason)。
    reason 再按关键词聚类成"信号组"，每组给出：何时怀疑、怎么办、出处 WP。

用法：
    python3 tools/build_traps.py
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_DIR = os.path.join(ROOT, "CTF大赛WP集合", "articles")
OUT_DIR = os.path.join(ROOT, "traps")

# "尝试A → 失败：B" / "试图A → 失败：B" / "A 失败：B"
SPLIT_RE = re.compile(r"\s*(?:→|->|=>)\s*失败\s*[：:]\s*")

# 信号聚类：命中关键词归入该组
SIGNALS = [
    ("标准方法不适用（需变种）", ["不是标准", "非标准", "变种", "自定义", "魔改", "改过", "改了", "被修改"],
     "结果对不上时，先怀疑题目改过算法参数（delta/sum/轮数/常量），而不是你的实现错了"),

    ("被过滤/拦截", ["被过滤", "过滤", "拦截", "黑名单", "waf", "blocked", "关键字", "被禁用", "无法执行", "script-src", "csp", "nonce"],
     "payload 无效时先定位过滤点（输入/参数名/输出），再决定编码还是换路子"),

    ("性能/规模受限", ["太大", "太慢", "超时", "爆不完", "跑不完", "查询次数上限", "太多", "指数"],
     "搜索空间太大时改用约束/剪枝/数学化简，别硬加机器"),

    ("前提条件不成立", ["不适用", "前提", "需要先", "必须先", "条件", "不成立", "不满足", "仅在"],
     "攻击方法都有前提（如 Wiener 需 d 小、CRLF 需 gbk），前提不满足立刻换方法"),

    ("环境/权限受限", ["权限", "permission", "root", "沙箱", "容器", "没有网络", "已移除", "被删"],
     "拿不到结果前先确认环境：当前用户、可用工具、是否断网，别假设自己能做"),

    ("输入/格式错误", ["格式错误", "无效", "invalid", "不是有效", "缺少", "字节数", "长度不对", "对齐"],
     "格式类报错先查长度/对齐/填充/文件头，再怀疑算法"),

    ("校验/签名失败", ["校验", "签名", "verify", "mac", "hash 不匹配", "指纹"],
     "校验失败说明校验方认得的数据少了某段——去找被截断或未发送的部分"),

    ("加密/编码未还原", ["加密", "编码", "混淆", "密文", "需要解密", "需先解"],
     "拿到密文别硬猜，先找加密实现或常量（从二进制/源码里 dump）"),

    ("路径/入口不唯一", ["路径", "入口", "路由", "不在", "找不到", "不存在", "404"],
     "找不到入口时先重新侦察，而不是在猜测的路径上反复尝试"),

    ("精度/浮点", ["精度", "浮点", "float", "误差"],
     "数学题「差不多但不相等」时，检查整数运算 vs 浮点"),
]

GENERIC_SIGNAL = "其他"


def load_fm(path):
    b = open(path, "rb").read()
    if not b.startswith(b"---\n"):
        return None
    e = b.find(b"\n---\n", 4)
    if e < 0:
        return None
    return yaml.safe_load(b[4:e + 1].decode("utf-8", "replace"))


# 失败发生在解题的哪个阶段——比"原因"更稳定，便于 agent 定位该回退到哪一步
STAGES = [
    ("侦察/定位", ["找不到", "不在", "入口", "路径", "路由", "搜不到", "未发现", "不存在", "inline"]),
    ("取数/解密", ["密钥", "解密", "密文", "缺", "字节", "还原", "解密失败"]),
    ("构造/建模", ["方程", "不够", "太大", "解不出", "非线性", "退化", "攻击不如", "高效"]),
    ("执行/落地", ["被过滤", "拦截", "权限", "崩溃", "超时", "太慢", "不允许", "上限"]),
]


def classify_stage(text):
    low = text.lower()
    for name, keys in STAGES:
        for k in keys:
            if k in low:
                return name
    return "未分类"


def classify(reason):
    low = reason.lower()
    for name, keys, _ in SIGNALS:
        for k in keys:
            if k in low:
                return name
    return GENERIC_SIGNAL


def parse_failed(fa):
    """把 failed_attempts 列表切成 (attempt, reason) 对。"""
    out = []
    if not isinstance(fa, list):
        return out
    for item in fa:
        if not isinstance(item, str):
            continue
        parts = SPLIT_RE.split(item, maxsplit=1)
        if len(parts) == 2:
            a, r = parts[0].strip(), parts[1].strip()
        elif "失败" in item:
            a, _, r = item.partition("失败")
            a = a.strip(" ：:")
            r = r.strip(" ：:")
        else:
            a, r = item.strip(), ""
        if a or r:
            out.append((a, r))
    return out


def main():
    files = sorted(glob.glob(os.path.join(WP_DIR, "*.md")))
    groups = defaultdict(list)
    by_cat = defaultdict(lambda: defaultdict(int))
    total_pairs = 0

    for p in files:
        fm = load_fm(p)
        if not fm:
            continue
        pairs = parse_failed(fm.get("failed_attempts"))
        if not pairs:
            continue
        cat = str(fm.get("category") or "unknown")
        sub = str(fm.get("subcategory_guess") or fm.get("subcategory") or "")
        for attempt, reason in pairs:
            total_pairs += 1
            sig = classify(reason + " " + attempt)
            stage = classify_stage(reason + " " + attempt)
            groups[sig].append({
                "stage": stage,
                "attempt": attempt,
                "reason": reason,
                "category": cat,
                "subcategory": sub,
                "source": os.path.basename(p),
                "one_liner": fm.get("one_liner"),
            })
            by_cat[sig][cat] += 1

    os.makedirs(OUT_DIR, exist_ok=True)

    # 结构化 JSON
    signal_meta = {name: advice for name, _, advice in SIGNALS}
    payload = {
        "generated_from": "CTF大赛WP集合/articles/*.md :: failed_attempts",
        "total_attempts": total_pairs,
        "signals": [
            {
                "signal": sig,
                "when_to_doubt": signal_meta.get(sig, ""),
                "count": len(items),
                "by_category": dict(by_cat[sig]),
                "cases": items[:40],
            }
            for sig, items in sorted(groups.items(), key=lambda kv: -len(kv[1]))
        ],
    }
    # 按阶段汇总（跨信号轴）—— 必须在写 JSON 之前算好
    stage_counts = defaultdict(int)
    for items in groups.values():
        for it in items:
            stage_counts[it.get("stage", "未分类")] += 1
    payload["by_stage"] = dict(stage_counts)

    with open(os.path.join(OUT_DIR, "traps.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # Markdown
    lines = []
    lines.append("<!-- AUTO-GENERATED by tools/build_traps.py — 修改解读请改 tools/build_traps.py 的 SIGNALS -->")
    lines.append("# TRAPS-INDEX — agent 自我纠错陷阱表")
    lines.append("")
    lines.append(f"从 **{len(files)}** 篇 WP 的 `failed_attempts` 字段提取 **{total_pairs}** 条失败尝试记录（摘要抽取，未经逐条复现），按失败信号聚类。")
    lines.append("")
    lines.append("> **给 agent 的用法**：当你的观察与左列「信号」匹配时，**立刻停下来怀疑当前方向**，")
    lines.append("> 按「该怎么办」行动，不要继续在错误路径上堆砌。真人做错会自知，agent 不会——这张表就是弥补这一点。")
    lines.append("")
    lines.append("## 失败发生在哪一步（按阶段）")
    lines.append("")
    lines.append("| 阶段 | 次数 | 该回退到哪 |")
    lines.append("|---|---|---|")
    stage_advice = {
        "侦察/定位": "回退到信息收集：重扫端点/符号/文件类型，别在猜测上继续",
        "取数/解密": "回退到取数：确认密钥/参数从哪来，从二进制或源码里 dump 出来",
        "构造/建模": "回退到建模：检查方程/约束是否够、是否该换数学方法",
        "执行/落地": "回退到执行：确认过滤点/权限/时限，换编码或换路径",
        "未分类": "参考同类案例",
    }
    for k, v in sorted(stage_counts.items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} | {stage_advice.get(k,'')} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    # "其他"放到最后作为案例附录，避免淹没有信号价值的组
    ordered = sorted(groups.items(), key=lambda kv: (kv[0] == GENERIC_SIGNAL, -len(kv[1])))
    for sig, items in ordered:
        advice = signal_meta.get(sig, "")
        title = f"## {sig}（{len(items)} 例）"
        if sig == GENERIC_SIGNAL:
            title = f"## 附录：题目特有失败案例（{len(items)} 例，非泛化信号，按方向查阅）"
        lines.append(title)
        lines.append("")
        if advice:
            lines.append(f"> **信号**：{advice}")
            lines.append("")
        cats = dict(by_cat[sig])
        if cats:
            lines.append("分布: " + " · ".join(f"{k}={v}" for k, v in sorted(cats.items(), key=lambda kv: -kv[1])))
            lines.append("")
        lines.append("| 踩过的坑 | 失败原因 | 方向 | 出处 |")
        lines.append("|---|---|---|---|")
        limit = 200 if sig == GENERIC_SIGNAL else 25
        for it in items[:limit]:
            a = (it["attempt"] or "").replace("|", "\\|")[:70]
            r = (it["reason"] or "").replace("|", "\\|")[:70]
            lines.append(f"| {a} | {r} | {it['category']}/{it['subcategory']} | `{it['source']}` |")
        lines.append("")

    with open(os.path.join(OUT_DIR, "TRAPS-INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ 提取 {total_pairs} 条失败尝试，聚为 {len(groups)} 个信号组")
    # "其他"放到最后作为案例附录，避免淹没有信号价值的组
    ordered = sorted(groups.items(), key=lambda kv: (kv[0] == GENERIC_SIGNAL, -len(kv[1])))
    for sig, items in ordered:
        print(f"   {len(items):4d}  {sig}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
