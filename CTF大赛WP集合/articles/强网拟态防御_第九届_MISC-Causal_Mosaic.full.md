---
title: 'MISC-Causal Mosaic'
contest: '强网拟态防御 第九届'
contest_normalized: '强网拟态防御 第九届'
contest_year: 2025
year: 2025
category: 'misc'
subcategory: 'misc_other'
tags: []
attack_chain:
- '者分别指向 event-2243b0，等两条边都消耗后它才出队。'
one_liner: '题目描述：'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/iTgaxzumnH3cE4N5nH6VvQ'
last_verified: '2026-11-02'
contest_normalized: "强网拟态"
subcategory_guess: "misc_misc"
---

MISC-Causal Mosaic
题目描述：
Given 9 events and 10 precedence constraints encoded
in
three
local
logs, merge all constraints into one directed acyclic graph and submit a valid topological order containing every event exactly once. The same order must be provided to validators A, B, and C.
题目附件：
mimic-math-lab-20261015-v5-player.zip
核心思路：三份日志是同一张有向无环图的三种编码，译成统一的先后边后做拓扑排序，把同一条事件序列同时交给 A、B、C。
POST /api/new，正文 {}。本次实际取到的实例为：
{
"session_id"
:
"wIgDQKTvlWacAx_7Kkvvlq2ID1QIfHgI"
,
"question_id"
:
"1fa2aa324f26db8eb6cdaac2"
,
"challenge"
: {
"kind"
:
"causal"
,
"events"
: [
{
"id"
:
"event-ed5faf"
,
"weight"
: 3},
{
"id"
:
"event-7ab62d"
,
"weight"
: 32},
{
"id"
:
"event-a47f00"
,
"weight"
: 33},
{
"id"
:
"event-6173da"
,
"weight"
: 6},
{
"id"
:
"event-60c0e5"
,
"weight"
: 49},
{
"id"
:
"event-5b6d68"
,
"weight"
: 33},
{
"id"
:
"event-2243b0"
,
"weight"
: 6},
{
"id"
:
"event-a99ede"
,
"weight"
: 27},
{
"id"
:
"event-9a268c"
,
"weight"
: 36}
],
"traces"
: {
"A"
: [
{
"before"
:
"event-9a268c"
,
"after"
:
"event-6173da"
,
"local_tick"
: 8814},
{
"before"
:
"event-5b6d68"
,
"after"
:
"event-2243b0"
,
"local_tick"
: 8327},
{
"before"
:
"event-60c0e5"
,
"after"
:
"event-a99ede"
,
"local_tick"
: 5612},
{
"before"
:
"event-ed5faf"
,
"after"
:
"event-a47f00"
,
"local_tick"
: 4479}
],
"B"
: [
{
"relation"
:
"event-5b6d68 <- event-9a268c"
,
"local_tick"
: 4567},
{
"relation"
:
"event-9a268c <- event-7ab62d"
,
"local_tick"
: 5956},
{
"relation"
:
"event-ed5faf <- event-60c0e5"
,
"local_tick"
: 8644}
],
"C"
: [
{
"pair"
: [2, 8],
"local_tick"
: 6835},
{
"pair"
: [3, 6],
"local_tick"
: 1786},
{
"pair"
: [7, 1],
"local_tick"
: 7764}
]
}
},
"expires_in"
: 899,
"remaining_rounds"
: 1
}
分析源码附件|三份日志的含义： A：before 必须出现在 after 之前。 B：relation 形如 左边 <- 右边，箭头右侧事件在左侧事件之前。
C：pair 为 [前下标, 后下标]，第一个下标对应的事件在第二个之前。
A 的 before 直接指向 after： event-9a268c -> event-6173da event-5b6d68 -> event-2243b0 event-60c0e5 -> event-a99ede event-ed5faf -> event-a47f00
B 取箭头右侧为起点。例如 event-5b6d68 <- event-9a268c 表示 event-9a268c 在前： event-9a268c -> event-5b6d68 event-7ab62d -> event-9a268c event-60c0e5 -> event-ed5faf
C 用原数组下标，不重新排序。[2, 8] 是下标 2 的 event-a47f00 在下标 8 的 event-9a268c 之前： event-a47f00 -> event-9a268c event-6173da -> event-2243b0 event-a99ede -> event-7ab62d
3.2 合并成两条汇合链 10 条边接成下面的依赖，终点都是 event-2243b0： event-60c0e5 -> event-a99ede -> event-7ab62d -> event-9a268c -> event-6173da -> event-2243b0 event-9a268c -> event-5b6d68 -> event-2243b0 event-60c0e5 -> event-ed5faf -> event-a47f00 -> event-9a268c
Kahn 算法维护入度。入度变为 0 的事件进入队列；初始队列按 events 的原顺序收集，出队后按边的生成顺序把后继入队。边的生成顺序是先 A、再 B、再 C，与上一节列出的顺序相同。
只有 event-60c0e5 入度为 0。它的后继按边序是 event-a99ede、event-ed5faf。继续消元：
event-a99ede 释放 event-7ab62d。
event-ed5faf 释放 event-a47f00。
event-7ab62d 使 event-9a268c 的入度从 2 降到 1，此时还不能出队。
event-a47f00 把 event-9a268c 的入度降到 0。
event-9a268c 的后继按边序是 event-6173da、event-5b6d68。
二者分别指向 event-2243b0，等两条边都消耗后它才出队。
event-60c0e5
event-a99ede
event-ed5faf
event-7ab62d
event-a47f00
event-9a268c
event-6173da
event-5b6d68
event-2243b0\
