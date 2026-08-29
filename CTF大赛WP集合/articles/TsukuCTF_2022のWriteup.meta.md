---
title: TsukuCTF 2022 の Writeup
contest: TsukuCTF 2022
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [pdp11_1971_re, friday_lunch_logic, osint_japan_postal, osint_airport_train, osint_hotel_room, ssh_public_key_search, sherlock_username, dp_kill_circuit, ohnobori]
attack_chain: 题 1:file a.out PDP-11 old overlay → pdp11dasm 反汇编 → 0x11000 halt + br 14 循环 asl r1*16 + asl r2 + add r1,r2 算 1+1=2 / 题 2:看 3 张电路图 DefBom1/2/3 找唯一不爆炸的切割线 (442) / 题 3-7:日本 OSINT 找车站/航空港/酒店/机器人设施 (South China University of Technology) 郵便番号 → TsukuCTF22{8770013} / 题 8:Flash.bin strings grep 31 → apa-316-2428 → アパホテル&リゾート〈両国駅タワー〉_2428 / 题 9-10:開業日/猫生年月日 (2019/03/29 / 2021/09/16) / 题 11:緯度経度十進法五桁目切捨 (34.5763_136.5313) / 题 12:stalking sns 配对 (6491331) / 题 13:SSH 公钥 GitHub Ann0nymusTsukushi / 题 14:DM 威胁 gross_poem → sherlock.py → Instagram/Trakt/XXX → TsukuCTF22{M4ny_0S1N7_700ls_3x157}
key_payload: pdp11dasm version 0.0.3 / 算 1+1 = 2 (題1) / ssh -T git@github.com -i ./a (Hi Ann0nymusTsukushi!) / python sherlock.py gross_poem
one_liner: TsukuCTF 2022 14 题 OSINT 杂烩：PDP-11 1971 复古二进制 → 日本 OSINT 找车站/机场/酒店/猫生年月日/开业日 → SSH 公钥寻 GitHub 用户 → sherlock.py 找社交网络。
lesson: 日本 OSINT 邮政编号是 7 位数字（ハイフン除き）；stalking 找地点常通过社交媒体广告或 SNS 帖子线索；PDP-11 1971 复古 CPU 的指令集是 CTF 复古题型。
quality: high
---
