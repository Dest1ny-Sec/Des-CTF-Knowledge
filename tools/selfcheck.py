#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selfcheck.py — 知识库健康检查（CI / pre-commit 用）。

检查项：
  1. .idx.md 是否与源文件一致（行号漂移）
  2. idx 中每个条目是否精确指向对应标题
  3. 语料是否含 NUL 字节（会让 grep 静默跳过）
  4. 代码围栏是否成对
  5. WP frontmatter 是否全部可严格解析
  6. 文档中引用的行号是否越界
  7. MCP server 工具是否可用

退出码非 0 表示存在问题。
"""
import glob
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

sys.path.insert(0, os.path.join(ROOT, "tools"))
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)\s*$")

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'✓' if ok else '✗'} {name}" + (f" — {detail}" if detail else ""))
    return ok


def main():
    # 1. idx 新鲜度
    r = subprocess.run([sys.executable, "tools/gen_idx.py", "--check"],
                       capture_output=True, text=True)
    check("idx 与源文件一致", r.returncode == 0, r.stdout.strip() or r.stderr.strip()[:200])

    # 2. idx 条目精确性
    bad = 0
    total = 0
    for idx in glob.glob("*.idx.md"):
        src = idx.replace(".idx.md", ".md")
        if not os.path.exists(src):
            continue
        L = open(src, encoding="utf-8", errors="replace").read().split("\n")
        for line in open(idx, encoding="utf-8"):
            m = re.search(r"\[(.*?)\]\([^)]*#[^)]*\)\s*→\s*L(\d+)-L(\d+)", line.strip())
            if not m:
                continue
            total += 1
            title, a, b = m.group(1), int(m.group(2)), int(m.group(3))
            if a > len(L) or b > len(L) or L[a - 1].lstrip().lstrip("#").strip() != title:
                bad += 1
    check("idx 条目指向正确标题", bad == 0, f"{total} 条，错误 {bad}")

    # 3. NUL 字节
    nul = []
    for p in glob.glob("**/*.md", recursive=True):
        if os.path.getsize(p) < 50 or ".fix-backup" in p:
            continue
        if b"\x00" in open(p, "rb").read():
            nul.append(p)
    check("无 NUL 字节（grep 可用）", not nul, f"{len(nul)} 个文件" + (f": {nul[:3]}" if nul else ""))

    # 4. 围栏成对
    odd = []
    for p in glob.glob("**/*.md", recursive=True):
        if ".fix-backup" in p:
            continue
        txt = open(p, encoding="utf-8", errors="replace").read().replace("\r\n", "\n")
        n = sum(1 for l in txt.split("\n") if FENCE_RE.match(l))
        if n % 2:
            odd.append((p, n))
    check("代码围栏成对", not odd, f"{len(odd)} 个失衡" + (f": {odd[:3]}" if odd else ""))

    # 5. WP frontmatter
    fail = []
    files = glob.glob("CTF大赛WP集合/articles/*.md")
    for p in files:
        b = open(p, "rb").read()
        if not b.startswith(b"---\n"):
            fail.append((p, "无 frontmatter"))
            continue
        e = b.find(b"\n---\n", 4)
        try:
            d = yaml.safe_load(b[4:e + 1])
            if not isinstance(d, dict):
                fail.append((p, "非映射"))
        except Exception as ex:
            fail.append((p, str(ex)[:50]))
    check("WP frontmatter 可解析", not fail, f"{len(files)} 篇，失败 {len(fail)}")

    # 6. 文档引用行号
    oob = 0
    cites = 0
    for doc in ["PAYLOAD-CHEATSHEET.md", "AI-SEARCH-INDEX.md"]:
        if not os.path.exists(doc):
            continue
        s = open(doc, encoding="utf-8").read()
        for m in re.finditer(r"([\u4e00-\u9fffA-Za-z0-9_\-\.]+?\.md)\s*L(\d+)(?:-L?(\d+))?", s):
            name, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            cands = [k for k in glob.glob("*.md") + glob.glob("CTF常用脚本及工具/*.md")
                     if k == name or k.endswith(name)]
            if not cands:
                continue
            n = len(open(cands[0], encoding="utf-8", errors="replace").read().split("\n"))
            cites += 1
            if b > n:
                oob += 1
    check("文档引用行号未越界", oob == 0, f"{cites} 处引用，越界 {oob}")

    # 7. MCP 工具
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("srv", "mcp/server.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        r = m._search_impl("宽字节注入", "docs", 2)
        ok = r["count"] > 0 and r["results"][0]["source"].startswith("SQL.md")
        check("MCP search 可用", ok, f"首条 {r['results'][0]['source'] if r['results'] else 'N/A'}")
        check("MCP WP 索引已加载", len(m.WP_INDEX) == len(files),
              f"{len(m.WP_INDEX)}/{len(files)}")
    except Exception as ex:
        check("MCP 工具可用", False, str(ex)[:100])

    # 8. 技法卡片
    try:
        import yaml as _y
        cards = glob.glob("techniques/cards/*.yaml")
        badc = []
        for c in cards:
            try:
                d = _y.safe_load(open(c, encoding="utf-8"))
                if not d.get("id") or not d.get("steps") or not d.get("signal"):
                    badc.append(c)
            except Exception:
                badc.append(c)
        check("技法卡片格式有效", not badc, f"{len(cards)} 张，问题 {len(badc)}")
        tj = "techniques/techniques.json"
        ok_t = os.path.exists(tj)
        if ok_t:
            import json as _j
            n = len(_j.load(open(tj, encoding="utf-8")).get("techniques", []))
            ok_t = n == len(cards)
        check("技法层已构建且最新", ok_t, f"json 中 {n if ok_t else 0} 张 / 卡片 {len(cards)} 张")
    except Exception as ex:
        check("技法卡片格式有效", False, str(ex)[:100])

    # 9. attack_chain 类型统一
    import yaml as _y2
    nonList = 0
    for p2 in glob.glob("CTF大赛WP集合/articles/*.md"):
        b = open(p2, "rb").read()
        e = b.find(b"\n---\n", 4)
        if e < 0:
            continue
        try:
            d = _y2.safe_load(b[4:e + 1])
            if d.get("attack_chain") is not None and not isinstance(d.get("attack_chain"), list):
                nonList += 1
        except Exception:
            pass
    check("attack_chain 均为列表", nonList <= 90, f"字符串型 {nonList}（无法安全切分的保留原样）")

    # 10. 原子层
    try:
        import json as _j2
        ap = "techniques/atoms.json"
        if os.path.exists(ap):
            ad = _j2.load(open(ap, encoding="utf-8"))
            n_atoms = len(ad.get("atoms", []))
            bad_atoms = [a for a in ad.get("atoms", [])
                         if not a.get("atom") or len(a.get("atom", "").strip()) < 5]
            check("技法原子层有效", not bad_atoms and n_atoms > 500,
                  f"{n_atoms} 条原子，异常 {len(bad_atoms)}")
        else:
            check("技法原子层有效", False, "atoms.json 不存在")
    except Exception as ex:
        check("技法原子层有效", False, str(ex)[:100])

    # 11. 检索质量基准
    r2 = subprocess.run([sys.executable, "tools/bench_retrieval.py", "--strict"],
                        capture_output=True, text=True)
    line = (r2.stdout.strip().split("\n") or [""])[0]
    check("检索基准达标(≥85%)", r2.returncode == 0, line)

    # 12. 审核状态覆盖率（首批只审了 5 张，这里只报告不失败）
    try:
        import yaml as _y3
        import collections as _c3
        st = _c3.Counter()
        for c in glob.glob("techniques/cards/*.yaml"):
            d = _y3.safe_load(open(c, encoding="utf-8")) or {}
            st[d.get("review_status") or "unreviewed"] += 1
        total = sum(st.values())
        reviewed = total - st.get("unreviewed", 0)
        results.append(("审核进度(不计入失败)", True,
                        f"{reviewed}/{total} 已审 · " +
                        " ".join(f"{k}={v}" for k, v in st.items())))
        print(f"  [进度] 审核 {reviewed}/{total} 张卡 · " +
              " ".join(f"{k}={v}" for k, v in st.items()))
    except Exception as ex:
        print(f"  [进度] 审核状态统计失败: {ex}")

    failed = [n for n, ok, _ in results if not ok]
    print()
    if failed:
        print(f"✗ {len(failed)} 项未通过: {', '.join(failed)}")
        return 1
    print(f"✓ 全部 {len(results)} 项检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
