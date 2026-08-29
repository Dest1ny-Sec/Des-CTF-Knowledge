---
title: [强网杯 S9] Qcalc 赛题解析
contest: 强网杯 S9 (强网杯 2025)
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [flask_receive_data, base64_decode_data_exfil, request_form_get, request_args_get, simple_data_collector, debug_mode_logging, headers_form_args_print, flag_stealer, low_quality_simple]
attack_chain: Flask app.route('/receive', methods=['POST', 'GET']) → request.form.get('flag') or request.form.get('data') (POST) or request.args.get('flag') or request.args.get('data') (GET) → base64.b64decode(data).decode('utf-8') → 写 received_flags.txt + 打印 headers/form/args → 收集 flag 的反向 webhook
key_payload: data = request.form.get('flag') or request.form.get('data') / decoded = base64.b64decode(data).decode('utf-8') / f.write(f"{decoded}\n") / debug=True
one_liner: 强网杯 S9 Qcalc 赛题解析：Flask /receive POST+GET 接收 flag/data 字段 + base64 解码 + 写 received_flags.txt + 调试模式打印 headers/form/args，是一道 flag 收集器基础设施题。
lesson: 当 CTF 题目出题方需要收集 flag 时，反向 webhook (Flask /receive endpoint) 是最简实现；base64 解码 + 调试模式自动 dump 是快速出题方案。
quality: low
---
