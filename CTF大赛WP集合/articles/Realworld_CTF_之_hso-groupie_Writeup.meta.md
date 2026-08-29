---
title: Realworld CTF 之 hso-groupie Writeup (xpdf 4.03 JBIG2 RCE)
contest: Realworld CTF
year: 2022
difficulty: high
vuln_type: misc_unknown
tags: [xpdf, pdftohtml, jbig2-decode, integer-overflow, heap-overflow, turing-complete, jbig2-encoder, project-zero, arith-coder, bitmap]
attack_chain:
  - Project Zero 启示: NSO 0-click iMessage 漏洞 = JBIG2Stream 整数溢出 + 图灵完备运算
  - 题目: xpdf 4.03 pdftohtml Clone-and-Pwn + flag in /run/secrets/flag
  - jbig2enc fcd14492 标准 + jbjbarith.cpython 算术编码库 + sploit.py 利用脚本
  - 漏洞点: JBIG2Stream::readTextRegionSeg numSyms += getSize() 整数溢出
  - gmallocn(numSyms, sizeof(JBIG2Bitmap *)) 分配过小 → syms[] 堆溢出
  - 关键构造: refSegs 中一些 seg->getSize() 很大 (4GB) 但实际可控制 segment 类型
  - 堆风水: 溢出块覆盖 GList 后备存储指针
  - 大 size segment 指针被替换为 jbig2SegBitmap 跳过检索
  - 利用 chain: 整数溢出 → 堆溢出 → 写 pageBitmap.Width/Height
  - pageBitmap.expand 越界读写 + combine (与/或/异或/替换) 5 种运算
  - 利用 pageBitmap 与其它 bitmaps 的与或非运算构建图灵完备小型计算机
  - 全加器 → ROP 构造 → 栈上 shellcode
  - PDF 构造: MyStream1 (FlateDecode) + MyStream2 (JBIG2Decode) + JBIG2Globals 引用
  - JBIG2Segment: EOFSeg / SymbolDictSeg / PageInfoSeg / GenericRegionSeg
  - combine 函数: dest |= src1 & m2 / dest &= src1 | m1 等 5 种
  - 完整 exp: jbig2enc + python3 sploit.py + python2 pdf.py sploit > sploit.pdf
  - gdbserver --cap-add=SYS_PTRACE --security-opt seccomp=unconfined docker 调试
key_payload: gmallocn(numSyms, sizeof(JBIG2Bitmap*)) 整数溢出后 syms[k++] = symbolDict->getBitmap(k) 堆溢出
one_liner: Realworld CTF 之 hso-groupie：xpdf 4.03 JBIG2Stream 整数溢出 + 堆风水覆盖 GList 后备存储 + 图灵完备 (全加器 + 5 种 bit 操作) + ROP/Shellcode 完整 exp PDF。
lesson: JBIG2 算术编码 + pageBitmap 与/或/异或/替换 5 种运算可以构建图灵完备计算机；整数溢出 + 堆风水是 Project Zero 0-click 攻击核心思路；Clone-and-Pwn 模式需看最近 CVE 修复记录。
quality: high
---
