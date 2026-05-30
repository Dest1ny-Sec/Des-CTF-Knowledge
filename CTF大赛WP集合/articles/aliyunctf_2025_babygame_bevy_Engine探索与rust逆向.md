# aliyunctf 2025 babygame bevy Engine探索与rust逆向

> 原文: https://www.ctfiot.com/236198.html
> ID: 236198

1

搜索源码

2

bevy 初探

fn main() {
 App::
new()
 // 省略
 .add_plugins((
 world::
WorldPlugin,
 audio::
GameAudioPlugin,
 player::
PlayerPlugin,
 utils::
UtilsPlugin,
 aspect::
AspectPlugin,
 ui::
UiPlugin,
 npc::
NpcPlugin,
 ))
 .run();
}

use bevy::
prelude::*;

fn move_player(mut query: Query<&mut Transform, With>) {
 for mut transform in query.iter_mut() {
 transform.translation.x += 1.0; // 每帧移动玩家
 }
}

fn main() {
 App::
new()
 .add_plugins(DefaultPlugins)
 .add_system(move_player) // 添加系统
 .run();
}

use bevy::
prelude::*;

#[derive(Debug)] // 自定义事件
struct PlayerHitEvent {
 damage: f32,
}

fn detect_collision(
 mut ev_hit: EventWriter,
 query: Query<&Transform, With>,
) {
 for transform in query.iter() {
 if transform.translation.x > 100.0 {
 ev_hit.send(PlayerHitEvent { damage: 10.0 }); // 发送事件
 }
 }
}

fn handle_hit(mut ev_hit: EventReader) {
 for event in ev_hit.iter() {
 println!("玩家受到 {} 伤害", event.damage); // 处理事件
 }
}

fn main() {
 App::
new()
 .add_plugins(DefaultPlugins)
 .add_event::() // 注册事件
 .add_system(detect_collision) // 发送事件的系统
 .add_system(handle_hit) // 监听事件的系统
 .run();
}

3

梳理逻辑

impl Plugin for AspectCombinerPlugin {
 fn build(&self, app: &mut App) {
 app.add_systems(
 Update,
 (
 select_aspects,
 show_combiner_icon,
 select_combined_aspect,
 check_all_aspects_full,
 )
 .run_if(in_state(GameState::
Gaming)),
 )
 .init_resource::<Combiner>()
 .add_event::<CombinedAspect>();
 }
}

4

rust 逆向与混淆

.text:
000000000004A33C mov eax, [rdi+78h]

.text:
000000000004A358 mov r11d, 0C57EE56Bh
.text:
000000000004A35E mov eax, 0EA433459h

case 11111：
enc_part_1
case 22222:
enc_part_3
case 22222:
enc_part_2

text:
000000000004A358 mov r11d, 0C57EE56Bh
.text:
000000000004A35E mov eax, 0EA433459h
.text:
000000000004A363 xor r14d, r14d
.text:
000000000004A366 xor esi, esi
.text:
000000000004A368 nop
.text:
000000000004A369 nop
.text:
000000000004A36A nop
.text:
000000000004A36B nop
.text:
000000000004A36C nop
.text:
000000000004A36D nop
.text:
000000000004A36E nop
.text:
000000000004A36F nop
.text:
000000000004A370 nop
.text:
000000000004A371 nop
.text:
000000000004A372 nop
.text:
000000000004A373 nop
.text:
000000000004A374 nop
.text:
000000000004A375 nop
.text:
000000000004A376 nop
.text:
000000000004A377 nop
.text:
000000000004A378 nop
.text:
000000000004A379 nop
.text:
000000000004A37A nop
.text:
000000000004A37B nop
.text:
000000000004A37C nop
.text:
000000000004A37D nop
.text:
000000000004A37E nop
.text:
000000000004A37F nop
.text:
000000000004A380 nop
.text:
000000000004A381 nop
.text:
000000000004A382 nop
.text:
000000000004A383 nop
.text:
000000000004A384 nop
.text:
000000000004A385 nop
.text:
000000000004A386 nop
.text:
000000000004A387 nop
.text:
000000000004A388 nop
.text:
000000000004A389 nop
.text:
000000000004A38A nop
.text:
000000000004A38B nop
.text:
000000000004A38C nop
.text:
000000000004A38D nop
.text:
000000000004A38E nop
.text:
000000000004A38F nop
.text:
000000000004A390 nop
.text:
000000000004A391 nop
.text:
000000000004A392 nop
.text:
000000000004A393 nop
.text:
000000000004A394 nop
.text:
000000000004A395 jmp short s_1
.text:
000000000004A397 ; ---------------------------------------------------------------------------
.text:
000000000004A397
.text:
000000000004A397 s_4: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8D5↓j
.text:
000000000004A397 mov rax, rsi
.text:
000000000004A39A shld rax, r14, 30h
.text:
000000000004A39F mov rdx, rsi
.text:
000000000004A3A2 shr rdx, 10h
.text:
000000000004A3A6 xor rsi, rdx
.text:
000000000004A3A9 xor r14, rax
.text:
000000000004A3AC mov eax, 4AD5EDBFh
.text:
000000000004A3B1 jmp short loc_4A403
.text:
000000000004A3B3 ; ---------------------------------------------------------------------------
.text:
000000000004A3B3
.text:
000000000004A3B3 s_3: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8F9↓j
.text:
000000000004A3B3 mov rax, r14
.text:
000000000004A3B6 mul r10
.text:
000000000004A3B9 imul rsi, 19660Dh
.text:
000000000004A3C0 mov r14, rax
.text:
000000000004A3C3 add r14, 3C6EF35Fh
.text:
000000000004A3CA adc rsi, rdx
.text:
000000000004A3CD mov eax, 6DFC18B3h
.text:
000000000004A3D2 jmp short s_4
.text:
000000000004A3D4 ; ---------------------------------------------------------------------------
.text:
000000000004A3D4
.text:
000000000004A3D4 s_1: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+898↑j
.text:
000000000004A3D4 mov eax, 3F551311h
.text:
000000000004A3D9 mov r14, rcx
.text:
000000000004A3DC mov rsi, r8
.text:
000000000004A3DF jmp short $+2
.text:
000000000004A3E1 ; ---------------------------------------------------------------------------
.text:
000000000004A3E1
.text:
000000000004A3E1 s_2: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8E2↑j
.text:
000000000004A3E1 mov rax, rsi
.text:
000000000004A3E4 shld rax, r14, 30h
.text:
000000000004A3E9 mov rdx, rsi
.text:
000000000004A3EC shr rdx, 10h
.text:
000000000004A3F0 xor rsi, rdx
.text:
000000000004A3F3 xor r14, rax
.text:
000000000004A3F6 jmp short s_3
.text:
000000000004A3F8 ; ---------------------------------------------------------------------------
.text:
000000000004A3F8 nop
.text:
000000000004A3F9 nop
.text:
000000000004A3FA nop
.text:
000000000004A3FB
.text:
000000000004A3FB loc_4A3FB:
.text:
000000000004A3FB nop
.text:
000000000004A3FC nop
.text:
000000000004A3FD nop
.text:
000000000004A3FE nop
.text:
000000000004A3FF nop
.text:
000000000004A400 nop
.text:
000000000004A401 nop
.text:
000000000004A402 nop
.text:
000000000004A403
.text:
000000000004A403 loc_4A403: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8B4↑j
.text:
000000000004A403 cmp r9d, 0Ah

v44 = (0x19660D * (unsigned __int128)*(unsigned int *)(v6 + 0x78)) >> 64;
 v45 = *(_DWORD *)(v6 + 0x4C); // input
 v46 = 0x19660DLL * *(unsigned int *)(v6 + 0x78) + 0x3C6EF35F;
 *((_QWORD *)&v49 + 1) = v44;
 *(_QWORD *)&v49 = v46;
 v48 = 0x19660D * (unsigned __int128)((unsigned __int64)(v49 >> 16) ^ v46)// add ADD_CONST
 + __PAIR128__(0x19660D * ((v44 >> 16) ^ v44), 0x3C6EF35FLL);
 v47 = ((__int64)v48 >> 16) ^ v48;
 if ( *(_DWORD *)(v6 + 0x48) < 0xAu )
 v45 = *(_DWORD *)(v6 + 0x48);
 v50 = HIDWORD(v72);
 v51 = (_DWORD *)v72;
 *(_DWORD *)v72 = HIDWORD(v72);
 *(_DWORD *)(v6 + 0x78) = v47;
 if ( !*(_QWORD *)(v6 + 16) )
 {
 v52 = std::
time::
SystemTime::
now(v46, *((_QWORD *)&v48 + 1) >> 16, v44);
 std::
time::
SystemTime::
duration_since(&v73, v52, v53);
 if ( (_BYTE)v73 )
 v54 = 0LL;
 else
 v54 = v74;
 *(_QWORD *)(v6 + 0x70) = v54;
 }
 *v51 = v50;
 alloc::
vec::
Vec::
push_u8_alloc::
alloc::
Global_(
 v6,
 HIBYTE(v47) + (HIWORD(v47) ^ ((v47 >> 8) + (v47 ^ v45))),
 &off_1070390,
 HIBYTE(v47));

v48 = 0x19660D * (unsigned __int128)((unsigned __int64)(v49 >> 16) ^ v46)// add ADD_CONST
 + __PAIR128__(0x19660D * ((v44 >> 16) ^ v44), 0x3C6EF35FLL);

v48 = 0x19660D * (unsigned __int128)((unsigned __int64)(v49 >> 16) ^ v46 + 0x3C6EF35FLL)// add ADD_CONST
 + __PAIR128__(0x19660D * ((v44 >> 16) ^ v44), 0x3C6EF35FLL);

v6_120 = 0 # *(unsigned int *)(v6 + 120) last_random
v6_76 = 0x2c # *(unsigned int *)(v6 + 76) input

# 常量
MULTIPLIER = 0x19660D
ADD_CONST = 0x3C6EF35F

# 步骤 1: 计算 v44
v44 = (MULTIPLIER * v6_120) >> 64

# 步骤 2: 读取 v45
v45 = v6_76

# 步骤 3: 计算 v46
v46 = MULTIPLIER * v6_120 + ADD_CONST

# 步骤 4: 将 v44 和 v46 组合成 v49
v49 = (v44 << 64) | v46

# 步骤 5: 计算 v48
v48 = ( MULTIPLIER * ((v49 >> 16) ^ v46) + ADD_CONST +
 ((MULTIPLIER * ((v44 >> 16) ^ v44)) << 64 +
 ADD_CONST
))

# 步骤 6: 计算 v47
v47 = (v48 >> 16) ^ v48

# 输出结果
print(f"v44 = {hex(v44)}")
print(f"v45 = {hex(v45)}")
print(f"v46 = {hex(v46)}")
print(f"v49 = {hex(v49)}")
print(f"(v49 >> 16) ^ v46 = {hex((v49 >> 16) ^ v46)}")
print(f"v48 = {hex(v48 & 2**64 -1)}")
print(f"v47 = {hex(v47 & 2 ** 32 -1)}")

v47 = v47 & 2 ** 32 -1
a = (v47 ^ v45)
b = a + (v47 >> 8)
c = b ^ (v47 >> 16)
d = c + (v47 >> 24)
print(f"a = {hex(a)}")
print(f"b = {hex(b)}")
print(f"c = {hex(c)}")
print(f"d = {hex(d)}")

res = (((v47 ^ v45) + (v47 >> 8) ) ^ (v47 >> 16)) + (v47 >> 24)
print(f"res = {hex(res)}")

if ( result >= 0x40 && !*(_QWORD *)(v8 + 40) )
 {
 v39 = v10;
 v48 = v9;
 v49 = v4;
 v40 = v3;
 v47 = v8 + 24;
 *(_QWORD *)&v44 = 0LL;
 *((_QWORD *)&v44 + 1) = 4LL;
 v12 = 4LL;
 v13 = 0LL;
 for ( i = v8; ; v8 = i )
 {
 v45 = v13;
 if ( v13 == 16 )
 break;
 v14 = v8;
 v15 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v8 + 8),
 *(_QWORD *)(v8 + 16),
 4 * v13,
 &off_105A3A8);
 v16 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v14 + 8),
 *(_QWORD *)(v14 + 16),
 4 * v13 + 1,
 &off_105A3C0);
 v17 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v14 + 8),
 *(_QWORD *)(v14 + 16),
 4 * v13 + 2,
 &off_105A3D8);
 v18 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v14 + 8),
 *(_QWORD *)(v14 + 16),
 4 * v13 + 3,
 &off_105A3F0);
 if ( v13 == (_QWORD)v44 )
 {
 alloc::
raw_vec::
RawVec::
grow_one_naga::
arena::
Handle_enum2__naga::
Expression____alloc::
alloc::
Global_(
 &v44,
 &off_105A408);
 v12 = *((_QWORD *)&v44 + 1);
 }
 z = v17 << 16;
 *(_DWORD *)(v12 + 4 * v13++) = (v18 << 24) | z | v15 | (v16 << 8);
 }

xxtea_sum_add: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner__bevy_ecs__system__query__Query_ref$_alictf__aspect__socket__Socket__tuple$______void_____bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner__bevy_ecs__system__query__Query_ref$_alictf__aspect__socket__Socket__tuple$______+281↑j
.text:
0000000000044DE1 mov rcx, qword ptr [rsp+158h+sum]
.text:
0000000000044DE6 add ecx, 6BC6121Dh
.text:
0000000000044DEC mov qword ptr [rsp+158h+sum], rcx
.text:
0000000000044DF1 mov ecx, 0E7B9CB0Dh
.text:
0000000000044DF6 jmp short loc_44E0C

5

解密

MULTIPLIER = 0x19660D
ADD_CONST = 0x3C6EF35F

def random(num):
 v44 = (MULTIPLIER * num) >> 64
 v46 = MULTIPLIER * num + ADD_CONST
 v49 = (v44 << 64) | v46
 v48 = ( MULTIPLIER * ((v49 >> 16) ^ v46) + ADD_CONST +
 ((MULTIPLIER * ((v44 >> 16) ^ v44)) << 64 +
 ADD_CONST
))
 v47 = ((v48 >> 16) ^ v48) & 2 **32 -1
 return v47

def xor_enc(plain,num):
 enc = (((num ^ plain) + (num >> 8) ) ^ (num >> 16)) + (num >> 24)
 enc = enc & 0xff
 return enc

def xor_dec(enc,num):
 c = enc - (num >> 24)
 b = c ^ (num >> 16)
 a = b - (num >> 8)
 plain = a ^ num
 plain = plain & 0xff
 return plain

def enc_start(plain):
 enc = []
 num = 0
 for i in range(len(plain)):
 num = random(num)
 enc.append(xor_enc(plain[i],num))
 return bytes(enc)

def dec_final(enc):
 dec = []
 num = 0
 for i in range(len(enc)):
 num = random(num)
 dec.append(xor_dec(enc[i],num))
 return dec

import struct

def xxtea_xor_decrypt(enc,key,delta=0x9E3779B9):
 enc_flag = [struct.unpack('> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ i) & 3] ^ z) + (sum ^ y))
 enc_flag[i] = (enc_flag[i] - MX) & ((1 << 32) -1)
 y = enc_flag[i]
 z = enc_flag[n-1]
 MX = ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ 0) & 3] ^ z) + (sum ^ y))
 enc_flag[0] = (enc_flag[0] - MX) & ((1 << 32) -1)
 y = enc_flag[0]
 sum = (sum - delta) & ((1 << 32) -1)
 rounds-=1

 for i in range(n):
 enc_flag[i] ^= 0x42E2B468

 return b''.join([struct.pack('> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ i) & 3] ^ z) + (sum ^ y))
 enc_flag[i] = (enc_flag[i] - MX) & ((1 << 32) -1)
 y = enc_flag[i]
 z = enc_flag[n-1]
 MX = ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ 0) & 3] ^ z) + (sum ^ y))
 enc_flag[0] = (enc_flag[0] - MX) & ((1 << 32) -1)
 y = enc_flag[0]
 sum = (sum - delta) & ((1 << 32) -1)
 rounds-=1
 return b''.join([struct.pack('>) {
 for mut transform in query.iter_mut() {
 transform.translation.x += 1.0; // 每帧移动玩家
 }
}

fn main() {
 App::
new()
 .add_plugins(DefaultPlugins)
 .add_system(move_player) // 添加系统
 .run();
}
use bevy::
prelude::*;

#[derive(Debug)] // 自定义事件
struct PlayerHitEvent {
 damage: f32,
}

fn detect_collision(
 mut ev_hit: EventWriter,
 query: Query<&Transform, With>,
) {
 for transform in query.iter() {
 if transform.translation.x > 100.0 {
 ev_hit.send(PlayerHitEvent { damage: 10.0 }); // 发送事件
 }
 }
}

fn handle_hit(mut ev_hit: EventReader) {
 for event in ev_hit.iter() {
 println!("玩家受到 {} 伤害", event.damage); // 处理事件
 }
}

fn main() {
 App::
new()
 .add_plugins(DefaultPlugins)
 .add_event::() // 注册事件
 .add_system(detect_collision) // 发送事件的系统
 .add_system(handle_hit) // 监听事件的系统
 .run();
}
impl Plugin for AspectCombinerPlugin {
 fn build(&self, app: &mut App) {
 app.add_systems(
 Update,
 (
 select_aspects,
 show_combiner_icon,
 select_combined_aspect,
 check_all_aspects_full,
 )
 .run_if(in_state(GameState::
Gaming)),
 )
 .init_resource::<Combiner>()
 .add_event::<CombinedAspect>();
 }
}
.text:
000000000004A33C mov eax, [rdi+78h]
.text:
000000000004A358 mov r11d, 0C57EE56Bh
.text:
000000000004A35E mov eax, 0EA433459h
case 11111：
enc_part_1
case 22222:
enc_part_3
case 22222:
enc_part_2
text:
000000000004A358 mov r11d, 0C57EE56Bh
.text:
000000000004A35E mov eax, 0EA433459h
.text:
000000000004A363 xor r14d, r14d
.text:
000000000004A366 xor esi, esi
.text:
000000000004A368 nop
.text:
000000000004A369 nop
.text:
000000000004A36A nop
.text:
000000000004A36B nop
.text:
000000000004A36C nop
.text:
000000000004A36D nop
.text:
000000000004A36E nop
.text:
000000000004A36F nop
.text:
000000000004A370 nop
.text:
000000000004A371 nop
.text:
000000000004A372 nop
.text:
000000000004A373 nop
.text:
000000000004A374 nop
.text:
000000000004A375 nop
.text:
000000000004A376 nop
.text:
000000000004A377 nop
.text:
000000000004A378 nop
.text:
000000000004A379 nop
.text:
000000000004A37A nop
.text:
000000000004A37B nop
.text:
000000000004A37C nop
.text:
000000000004A37D nop
.text:
000000000004A37E nop
.text:
000000000004A37F nop
.text:
000000000004A380 nop
.text:
000000000004A381 nop
.text:
000000000004A382 nop
.text:
000000000004A383 nop
.text:
000000000004A384 nop
.text:
000000000004A385 nop
.text:
000000000004A386 nop
.text:
000000000004A387 nop
.text:
000000000004A388 nop
.text:
000000000004A389 nop
.text:
000000000004A38A nop
.text:
000000000004A38B nop
.text:
000000000004A38C nop
.text:
000000000004A38D nop
.text:
000000000004A38E nop
.text:
000000000004A38F nop
.text:
000000000004A390 nop
.text:
000000000004A391 nop
.text:
000000000004A392 nop
.text:
000000000004A393 nop
.text:
000000000004A394 nop
.text:
000000000004A395 jmp short s_1
.text:
000000000004A397 ; ---------------------------------------------------------------------------
.text:
000000000004A397
.text:
000000000004A397 s_4: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8D5↓j
.text:
000000000004A397 mov rax, rsi
.text:
000000000004A39A shld rax, r14, 30h
.text:
000000000004A39F mov rdx, rsi
.text:
000000000004A3A2 shr rdx, 10h
.text:
000000000004A3A6 xor rsi, rdx
.text:
000000000004A3A9 xor r14, rax
.text:
000000000004A3AC mov eax, 4AD5EDBFh
.text:
000000000004A3B1 jmp short loc_4A403
.text:
000000000004A3B3 ; ---------------------------------------------------------------------------
.text:
000000000004A3B3
.text:
000000000004A3B3 s_3: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8F9↓j
.text:
000000000004A3B3 mov rax, r14
.text:
000000000004A3B6 mul r10
.text:
000000000004A3B9 imul rsi, 19660Dh
.text:
000000000004A3C0 mov r14, rax
.text:
000000000004A3C3 add r14, 3C6EF35Fh
.text:
000000000004A3CA adc rsi, rdx
.text:
000000000004A3CD mov eax, 6DFC18B3h
.text:
000000000004A3D2 jmp short s_4
.text:
000000000004A3D4 ; ---------------------------------------------------------------------------
.text:
000000000004A3D4
.text:
000000000004A3D4 s_1: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+898↑j
.text:
000000000004A3D4 mov eax, 3F551311h
.text:
000000000004A3D9 mov r14, rcx
.text:
000000000004A3DC mov rsi, r8
.text:
000000000004A3DF jmp short $+2
.text:
000000000004A3E1 ; ---------------------------------------------------------------------------
.text:
000000000004A3E1
.text:
000000000004A3E1 s_2: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8E2↑j
.text:
000000000004A3E1 mov rax, rsi
.text:
000000000004A3E4 shld rax, r14, 30h
.text:
000000000004A3E9 mov rdx, rsi
.text:
000000000004A3EC shr rdx, 10h
.text:
000000000004A3F0 xor rsi, rdx
.text:
000000000004A3F3 xor r14, rax
.text:
000000000004A3F6 jmp short s_3
.text:
000000000004A3F8 ; ---------------------------------------------------------------------------
.text:
000000000004A3F8 nop
.text:
000000000004A3F9 nop
.text:
000000000004A3FA nop
.text:
000000000004A3FB
.text:
000000000004A3FB loc_4A3FB:
.text:
000000000004A3FB nop
.text:
000000000004A3FC nop
.text:
000000000004A3FD nop
.text:
000000000004A3FE nop
.text:
000000000004A3FF nop
.text:
000000000004A400 nop
.text:
000000000004A401 nop
.text:
000000000004A402 nop
.text:
000000000004A403
.text:
000000000004A403 loc_4A403: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___void_____bevy_ecs__system__commands__Commands_bevy_ecs__change_detection__Res_bevy_yarnspinner__project__YarnProject__bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner___+8B4↑j
.text:
000000000004A403 cmp r9d, 0Ah
v44 = (0x19660D * (unsigned __int128)*(unsigned int *)(v6 + 0x78)) >> 64;
 v45 = *(_DWORD *)(v6 + 0x4C); // input
 v46 = 0x19660DLL * *(unsigned int *)(v6 + 0x78) + 0x3C6EF35F;
 *((_QWORD *)&v49 + 1) = v44;
 *(_QWORD *)&v49 = v46;
 v48 = 0x19660D * (unsigned __int128)((unsigned __int64)(v49 >> 16) ^ v46)// add ADD_CONST
 + __PAIR128__(0x19660D * ((v44 >> 16) ^ v44), 0x3C6EF35FLL);
 v47 = ((__int64)v48 >> 16) ^ v48;
 if ( *(_DWORD *)(v6 + 0x48) < 0xAu )
 v45 = *(_DWORD *)(v6 + 0x48);
 v50 = HIDWORD(v72);
 v51 = (_DWORD *)v72;
 *(_DWORD *)v72 = HIDWORD(v72);
 *(_DWORD *)(v6 + 0x78) = v47;
 if ( !*(_QWORD *)(v6 + 16) )
 {
 v52 = std::
time::
SystemTime::
now(v46, *((_QWORD *)&v48 + 1) >> 16, v44);
 std::
time::
SystemTime::
duration_since(&v73, v52, v53);
 if ( (_BYTE)v73 )
 v54 = 0LL;
 else
 v54 = v74;
 *(_QWORD *)(v6 + 0x70) = v54;
 }
 *v51 = v50;
 alloc::
vec::
Vec::
push_u8_alloc::
alloc::
Global_(
 v6,
 HIBYTE(v47) + (HIWORD(v47) ^ ((v47 >> 8) + (v47 ^ v45))),
 &off_1070390,
 HIBYTE(v47));
v48 = 0x19660D * (unsigned __int128)((unsigned __int64)(v49 >> 16) ^ v46)// add ADD_CONST
 + __PAIR128__(0x19660D * ((v44 >> 16) ^ v44), 0x3C6EF35FLL);
v48 = 0x19660D * (unsigned __int128)((unsigned __int64)(v49 >> 16) ^ v46 + 0x3C6EF35FLL)// add ADD_CONST
 + __PAIR128__(0x19660D * ((v44 >> 16) ^ v44), 0x3C6EF35FLL);
v6_120 = 0 # *(unsigned int *)(v6 + 120) last_random
v6_76 = 0x2c # *(unsigned int *)(v6 + 76) input

# 常量
MULTIPLIER = 0x19660D
ADD_CONST = 0x3C6EF35F

# 步骤 1: 计算 v44
v44 = (MULTIPLIER * v6_120) >> 64

# 步骤 2: 读取 v45
v45 = v6_76

# 步骤 3: 计算 v46
v46 = MULTIPLIER * v6_120 + ADD_CONST

# 步骤 4: 将 v44 和 v46 组合成 v49
v49 = (v44 << 64) | v46

# 步骤 5: 计算 v48
v48 = ( MULTIPLIER * ((v49 >> 16) ^ v46) + ADD_CONST +
 ((MULTIPLIER * ((v44 >> 16) ^ v44)) << 64 +
 ADD_CONST
))

# 步骤 6: 计算 v47
v47 = (v48 >> 16) ^ v48

# 输出结果
print(f"v44 = {hex(v44)}")
print(f"v45 = {hex(v45)}")
print(f"v46 = {hex(v46)}")
print(f"v49 = {hex(v49)}")
print(f"(v49 >> 16) ^ v46 = {hex((v49 >> 16) ^ v46)}")
print(f"v48 = {hex(v48 & 2**64 -1)}")
print(f"v47 = {hex(v47 & 2 ** 32 -1)}")

v47 = v47 & 2 ** 32 -1
a = (v47 ^ v45)
b = a + (v47 >> 8)
c = b ^ (v47 >> 16)
d = c + (v47 >> 24)
print(f"a = {hex(a)}")
print(f"b = {hex(b)}")
print(f"c = {hex(c)}")
print(f"d = {hex(d)}")

res = (((v47 ^ v45) + (v47 >> 8) ) ^ (v47 >> 16)) + (v47 >> 24)
print(f"res = {hex(res)}")
if ( result >= 0x40 && !*(_QWORD *)(v8 + 40) )
 {
 v39 = v10;
 v48 = v9;
 v49 = v4;
 v40 = v3;
 v47 = v8 + 24;
 *(_QWORD *)&v44 = 0LL;
 *((_QWORD *)&v44 + 1) = 4LL;
 v12 = 4LL;
 v13 = 0LL;
 for ( i = v8; ; v8 = i )
 {
 v45 = v13;
 if ( v13 == 16 )
 break;
 v14 = v8;
 v15 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v8 + 8),
 *(_QWORD *)(v8 + 16),
 4 * v13,
 &off_105A3A8);
 v16 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v14 + 8),
 *(_QWORD *)(v14 + 16),
 4 * v13 + 1,
 &off_105A3C0);
 v17 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v14 + 8),
 *(_QWORD *)(v14 + 16),
 4 * v13 + 2,
 &off_105A3D8);
 v18 = *(unsigned __int8 *)alloc::
vec::
impl_13::
index_bool_usize_alloc::
alloc::
Global_(
 *(_QWORD *)(v14 + 8),
 *(_QWORD *)(v14 + 16),
 4 * v13 + 3,
 &off_105A3F0);
 if ( v13 == (_QWORD)v44 )
 {
 alloc::
raw_vec::
RawVec::
grow_one_naga::
arena::
Handle_enum2__naga::
Expression____alloc::
alloc::
Global_(
 &v44,
 &off_105A408);
 v12 = *((_QWORD *)&v44 + 1);
 }
 z = v17 << 16;
 *(_DWORD *)(v12 + 4 * v13++) = (v18 << 24) | z | v15 | (v16 << 8);
 }
xxtea_sum_add: ; CODE XREF: bevy_ecs__system__function_system__impl$7__run_unsafe_void_____bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner__bevy_ecs__system__query__Query_ref$_alictf__aspect__socket__Socket__tuple$______void_____bevy_ecs__change_detection__ResMut_alictf__aspect__combiner__Combiner__bevy_ecs__system__query__Query_ref$_alictf__aspect__socket__Socket__tuple$______+281↑j
.text:
0000000000044DE1 mov rcx, qword ptr [rsp+158h+sum]
.text:
0000000000044DE6 add ecx, 6BC6121Dh
.text:
0000000000044DEC mov qword ptr [rsp+158h+sum], rcx
.text:
0000000000044DF1 mov ecx, 0E7B9CB0Dh
.text:
0000000000044DF6 jmp short loc_44E0C
MULTIPLIER = 0x19660D
ADD_CONST = 0x3C6EF35F

def random(num):
 v44 = (MULTIPLIER * num) >> 64
 v46 = MULTIPLIER * num + ADD_CONST
 v49 = (v44 << 64) | v46
 v48 = ( MULTIPLIER * ((v49 >> 16) ^ v46) + ADD_CONST +
 ((MULTIPLIER * ((v44 >> 16) ^ v44)) << 64 +
 ADD_CONST
))
 v47 = ((v48 >> 16) ^ v48) & 2 **32 -1
 return v47

def xor_enc(plain,num):
 enc = (((num ^ plain) + (num >> 8) ) ^ (num >> 16)) + (num >> 24)
 enc = enc & 0xff
 return enc

def xor_dec(enc,num):
 c = enc - (num >> 24)
 b = c ^ (num >> 16)
 a = b - (num >> 8)
 plain = a ^ num
 plain = plain & 0xff
 return plain

def enc_start(plain):
 enc = []
 num = 0
 for i in range(len(plain)):
 num = random(num)
 enc.append(xor_enc(plain[i],num))
 return bytes(enc)

def dec_final(enc):
 dec = []
 num = 0
 for i in range(len(enc)):
 num = random(num)
 dec.append(xor_dec(enc[i],num))
 return dec

import struct

def xxtea_xor_decrypt(enc,key,delta=0x9E3779B9):
 enc_flag = [struct.unpack('> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ i) & 3] ^ z) + (sum ^ y))
 enc_flag[i] = (enc_flag[i] - MX) & ((1 << 32) -1)
 y = enc_flag[i]
 z = enc_flag[n-1]
 MX = ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ 0) & 3] ^ z) + (sum ^ y))
 enc_flag[0] = (enc_flag[0] - MX) & ((1 << 32) -1)
 y = enc_flag[0]
 sum = (sum - delta) & ((1 << 32) -1)
 rounds-=1

 for i in range(n):
 enc_flag[i] ^= 0x42E2B468

 return b''.join([struct.pack('> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ i) & 3] ^ z) + (sum ^ y))
 enc_flag[i] = (enc_flag[i] - MX) & ((1 << 32) -1)
 y = enc_flag[i]
 z = enc_flag[n-1]
 MX = ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((key[((sum >> 2) ^ 0) & 3] ^ z) + (sum ^ y))
 enc_flag[0] = (enc_flag[0] - MX) & ((1 << 32) -1)
 y = enc_flag[0]
 sum = (sum - delta) & ((1 << 32) -1)
 rounds-=1
 return b''.join([struct.pack('<I', num) for num in enc_flag])

enc = bytes([0xA2, 0xB7, 0x9C, 0xC3, 0xB6, 0xF2, 0xB4, 0xE3, 0x2A, 0xE6,
 0x96, 0x55, 0xF8, 0xD0, 0x0E, 0xAD, 0x65, 0xB0, 0xAE, 0xB3,
 0x9D, 0x7E, 0x6A, 0x49, 0x46, 0x6E, 0x0E, 0x41, 0x35, 0x22,
 0xF7, 0x02, 0x4F, 0x86, 0xD6, 0x11, 0xC3, 0x86, 0xA6, 0x8F,
 0xDC, 0x03, 0xFE, 0x72, 0xC5, 0xE2, 0x9F, 0x0B, 0xE3, 0x4D,
 0x09, 0x80, 0x95, 0xA6, 0xA2, 0xF6, 0x93, 0xD7, 0xAC, 0xA9,
 0x53, 0x42, 0x61, 0x0F])

xxtea_key1 = [0x41661F49, 0xDFC12FCF, 0x1FE0F1A2, 0x71168786]
dec_1 = xxtea_xor_decrypt(enc,xxtea_key1,0x98D846DC)
enc = dec_1

xxtea_key2 = bytes([0x80, 0xE5, 0x51, 0x9E, 0x00, 0x60, 0x49, 0xF4, 0xED, 0x8E,
 0x16, 0x64, 0xBF, 0x55, 0x6E, 0x49])
dec_2 = xxtea_decrypt(enc,xxtea_key2,0xB72908F9)
enc = dec_2

xxtea_key3 = bytes([0x62, 0x76, 0x65, 0xAF, 0x4B, 0x14, 0x6F, 0xFC, 0x6C, 0x2B,
 0xAB, 0x22, 0xCB, 0x2D, 0x7D, 0x36])
dec_3 = xxtea_decrypt(enc,xxtea_key3,0x6BC6121D)
enc = dec_3

print(enc)
flag = dec_final(enc)
print(flag)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c67b739a0522062a0dbed255a23feb4c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c67b739a0522062a0dbed255a23feb4c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c67b739a0522062a0dbed255a23feb4c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c67b739a0522062a0dbed255a23feb4c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-a4c4c116024faf0c7b51ae6fd8d4f48e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-4d3eeb1a4ad5b2f4ab39cfebc12513bf.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-4d3eeb1a4ad5b2f4ab39cfebc12513bf.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-4d3eeb1a4ad5b2f4ab39cfebc12513bf.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-9f0ddad50d2813bad6dff59cc6c73471.gif)