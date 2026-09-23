---
title: 2025 腾讯游戏安全技术竞赛 - 安卓初赛
contest: 腾讯游戏安全
year: 2025
difficulty: medium
vuln_type: reverse
tags:
- Unreal Engine
- Frida
- UE4
- GWorld
- GName
- GObjects
- UObject
- FName
- Rotator
- Actor偏移
- '0x288'
- '0x500'
- '0x212'
- RenderCustomDepth
- 自瞄
- 锁头
attack_chain:
- 用 Frida 找到 GWorld (0xAFAC398) / GName (0xADF07C0) / GUObject (0xAE34A98) 三个全局
- 解析 GName 池 FNamePool + FNameEntry (FNameStride=0x2, offset_FNamePool_Blocks=0x10, LenBit=6)
- '解析 UObject: ClassPrivate 0x10 / FNameIndex 0x18 / OuterPrivate 0x20'
- 拿到 FirstPersonCharacter_C 0x500 偏移写 GunOffset → 自瞄
- 拿到 PlayerController 0x288 偏移写 ControlRotation → 锁头
- hook moduleBase+0x8D2ED80 函数 (CameraUpdate?) 用 PlayerController 的 rotation 覆盖 args[3]
- RenderCustomDepth 0x212 第 3 bit 控制透视 → 全 actor 遍历打开
key_payload: '''GWorld=0xAFAC398 / GName=0xADF07C0 / GObjects=0xAE34A98 / 0x288=ControlRotation / 0x500=GunOffset / 0x212=RenderCustomDepth'''
one_liner: 虚幻引擎 4 安卓手游 — Frida 写 GWorld/GName/GObjects 全局+解析 UObject+改 FirstPersonCharacter GunOffset + PlayerController Rotation + 透视 RenderCustomDepth bit3。
lesson: UE4 安卓游戏逆向需先定位三大全局 (GWorld/GName/GObjects)；UObject 通过 FNameIndex 走 GName 池；Actor 偏移 0x288/0x500 是 ControlRotation 和 GunOffset 经典位置。
quality: high
full_path: 2025腾讯游戏安全技术竞赛_安卓初赛.full.md
meta_path: 2025腾讯游戏安全技术竞赛_安卓初赛.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 2025 腾讯游戏安全技术竞赛 - 安卓初赛。虚幻引擎 4 安卓手游 — Frida 写 GWorld/GName/GObjects 全局+解析 UObject+改 FirstPersonCharacter GunOffset + PlayerController Rotation + 透视 RenderCustomDepth bit3。。关键路径：用 Frida 找到 GWorld (0x...
category: reverse
subcategory: reverse
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/240788.html
reasoning_chain:
- 触发点：UE4 安卓手游 → Frida 找 GWorld=0xAFAC398 / GName=0xADF07C0 / GObjects=0xAE34A98 三个全局 → 假设：UObject 反射起点
- 动作：解析 GName 池 FNamePool + FNameEntry（FNameStride=0x2, offset_FNamePool_Blocks=0x10, LenBit=6）→ 下一步：Block = index >> 16; Offset = index & 65535
- 下一步：UObject 字段 InternalIndex=0xC, ClassPrivate=0x10, FNameIndex=0x18, OuterPrivate=0x20 → 通过 FNameIndex 走 GName 池
- 触发点：FirstPersonCharacter_C + 0x500 偏移 → 假设：GunOffset 字段 → 动作：写 (0,0,20) 抬高枪口 +20 → 实现自瞄
- 观察：PlayerController + 0x288 是 ControlRotation → 假设：Pitch/Yaw/Roll 3 float → 动作：hook moduleBase+0x8D2ED80 函数用 PlayerController.rotation 覆盖 args[3] → 锁头
- 触发点：actor + 0x212 字段 bit 3 → 假设：RenderCustomDepth 透视 bit → 动作：遍历 actor 集合打开 bit 3 → 透视全场景
failed_attempts:
- 试图 hook update 写入 fixed rotation → 失败：必须先找 ControlRotation 在 PlayerController 内的偏移 (0x288)
- 试图查字符串常量拿 GWorld 偏移 → 失败：必须 memory scan 或 .so 段特征
- 试图写 lock 玩家基址 → 失败：要先解析 GObjects 拿 UObject 句柄
key_observations:
- UE4 安卓游戏逆向需先定位三大全局 GWorld/GName/GObjects
- UObject 通过 FNameIndex 走 GName 池 (Block/Offset 算法)
- Actor 偏移 0x288=ControlRotation / 0x500=GunOffset 是经典位置
- RenderCustomDepth bit3 控制透视是 UE4 feature flag
- Frida hook native 关键函数是写工具而非写代码的核心思路
prerequisites:
- UE4 引擎结构 (GWorld/GName/GObjects/UObject)
- Frida hook + Interceptor.attach
- FName 池解析
- 安卓 .so moduleBase 偏移定位
---
# 2025腾讯游戏安全技术竞赛 安卓初赛

> 原文: https://www.ctfiot.com/240788.html
> ID: 240788

作者论坛账号：lrhtony

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
GWorld 0xAFAC398
GName 0xADF07C0
GUObject 0xAE34A98
复制代码 隐藏代码
class Rotator {
    constructor(Pitch, Yaw, Roll) {
        this.Pitch = Pitch;
        this.Yaw = Yaw;
        this.Roll = Roll;
    }
    toString() {
        return`(${this.Pitch}, ${this.Yaw}, ${this.Roll})`;
    }
}

functiondumpRotator(rotatorAddr){
    const values = Memory.readByteArray(rotatorAddr, 3 * 4);
    const rot = newRotator(
        newFloat32Array(values, 0, 1)[0], 
        newFloat32Array(values, 4, 1)[0], 
        newFloat32Array(values, 8, 1)[0] 
    );
    console.log("dump rot", rot);
    return rot;
}

functiongetControlRotation(actorAddr){
    var data_addr = ptr(actorAddr).add(0x288);
    var rot = dumpRotator(data_addr);
    return rot;
}

functionwriteControlRotation(actorAddr, a, b, c){
    ptr(actorAddr).add(0x288).writeFloat(a);
    ptr(actorAddr).add(0x288+4).writeFloat(b);
    ptr(actorAddr).add(0x288+8).writeFloat(c);
}
复制代码 隐藏代码
function getGunOffset(actorAddr){
    var data_addr = ptr(actorAddr).add(0x500);
    dumpVector(data_addr);
}

function writeGunOffset(actorAddr, x, y, z){
    ptr(actorAddr).add(0x500).writeFloat(x);
    ptr(actorAddr).add(0x500+4).writeFloat(y);
    ptr(actorAddr).add(0x500+8).writeFloat(z);
}

writeGunOffset(actorAddrs["FirstPersonCharacter_C"], 0, 0, 20);
复制代码 隐藏代码
    var func_addr = moduleBase.add(0x8D2ED80)
    Interceptor.attach(func_addr, {
        onEnter: function (args) {
            dumpRotator(ptr(args[3]));
            var playerRotation = getControlRotation(actorAddrs["PlayerController"]);
            ptr(args[3]).writeFloat(playerRotation.Pitch);
            ptr(args[3]).add(4).writeFloat(playerRotation.Yaw);

        },
        onLeave: function (retval) {
        }
    });
复制代码 隐藏代码
function getRenderCustomDepth(actorAddr){
    var value = ptr(actorAddr).add(0x212).readU8();
    var bitValue = (value >> 3) & 1;
    return bitValue;
}

functiongetAllRenderCustomDepth(){
    const actors = getActorsAddr();
    for (const actorName in actors) {
        if (actors.hasOwnProperty(actorName)) {
            const actorAddr = actors[actorName];
            try {
                var value = getRenderCustomDepth(actorAddr);
                console.log(`RenderCustomDepth of ${actorName} at ${actorAddr}: ${value}`);
            } catch (e) {
                console.error(`Failed to get RenderCustomDepth of ${actorName} at ${actorAddr}: ${e}`);
            }
        }
    }
}
复制代码 隐藏代码
var moduleBase;
varGWorld;
varGWorld_Ptr_Offset = 0xAFAC398;
varGName;
varGName_Offset = 0xADF07C0;
varGObjects;
varGObjects_Offset = 0xAE34A98;
var actorAddrs

var offset_UObject_InternalIndex = 0xC;
var offset_UObject_ClassPrivate = 0x10;
var offset_UObject_FNameIndex = 0x18;
var offset_UObject_OuterPrivate = 0x20;

varGUObject = {
    getClass: function (obj) {
        returnptr(obj).add(offset_UObject_ClassPrivate).readPointer();
    },
    getNameId: function (obj) {
        try {
            returnptr(obj).add(offset_UObject_FNameIndex).readU32();
        }
        catch (e) {
            return0;
        }
    },
    getName: function(obj) {
        if (this.isValid(obj)){
            returngetFNameFromID(this.getNameId(obj));
        } else {
            return"None";
        }
    },
    getClassName: function(obj) {
        if (this.isValid(obj)) {
            var classPrivate = this.getClass(obj);
            returnthis.getName(classPrivate);
        } else {
            return"None";
        }
    },
    isValid: function(obj) {
        return (ptr(obj) > 0 && this.getNameId(obj) > 0 && this.getClass(obj) > 0);
    }
}

functiongetFNameFromID(index) {
    varFNameStride = 0x2
    var offset_GName_FNamePool = 0x30;
    var offset_FNamePool_Blocks = 0x10;

    var offset_FNameEntry_Info = 0;
    varFNameEntry_LenBit = 6;
    var offset_FNameEntry_String = 0x2;

    varBlock = index >> 16;
    varOffset = index & 65535;

    varFNamePool = GName.add(offset_GName_FNamePool);
    varNamePoolChunk = FNamePool.add(offset_FNamePool_Blocks + Block * 8).readPointer();
    varFNameEntry = NamePoolChunk.add(FNameStride * Offset);

    try {
        if (offset_FNameEntry_Info !== 0) {
            varFNameEntryHeader = FNameEntry.add(offset_FNameEntry_Info).readU16();    
        } else {
            varFNameEntryHeader = FNameEntry.readU16();
        }
    } catch(e) {
        return"";
    }

    var str_addr = FNameEntry.add(offset_FNameEntry_String);
    var str_length = FNameEntryHeader >> FNameEntry_LenBit;
    var wide = FNameEntryHeader & 1;
    if (wide) return"widestr";

    if (str_length > 0 && str_length < 250) {
        var str = str_addr.readUtf8String(str_length);
        return str;
    } else {
        return"None";
    }
}

functionset(modulename) {
    moduleBase = Module.findBaseAddress(modulename);
    GWorld = moduleBase.add(GWorld_Ptr_Offset).readPointer();
    GName = moduleBase.add(GName_Offset);
    GObjects = moduleBase.add(GObjects_Offset);
}

functiongetActorsAddr(){
    varLevel_Offset = 0x30
    varActors_Offset = 0x98

    varLevel = GWorld.add(Level_Offset).readPointer()
    varActors = Level.add(Actors_Offset).readPointer()
    varActors_Num = Level.add(Actors_Offset).add(8).readU32()
    var actorsAddr = {};
    for(var index = 0; index < Actors_Num; index++){
        var actor_addr = Actors.add(index * 8).readPointer()
        var actorName = GUObject.getName(actor_addr)
        actorsAddr[actorName] = actor_addr;    
    }
    return actorsAddr;
}

classVector {
    constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }
    toString() {
        return`(${this.x}, ${this.y}, ${this.z})`;
    }
}

classRotator {
    constructor(Pitch, Yaw, Roll) {
        this.Pitch = Pitch;
        this.Yaw = Yaw;
        this.Roll = Roll;
    }
    toString() {
        return`(${this.Pitch}, ${this.Yaw}, ${this.Roll})`;
    }
}

functiondumpVector(vectorAddr){
    const values = Memory.readByteArray(vectorAddr, 3 * 4);
    const vec = newVector(
        newFloat32Array(values, 0, 1)[0], 
        newFloat32Array(values, 4, 1)[0], 
        newFloat32Array(values, 8, 1)[0] 
    );
    console.log("dump vec", vec);
    return vec;
}

functiondumpRotator(rotatorAddr){
    const values = Memory.readByteArray(rotatorAddr, 3 * 4);
    const rot = newRotator(
        newFloat32Array(values, 0, 1)[0], 
        newFloat32Array(values, 4, 1)[0], 
        newFloat32Array(values, 8, 1)[0] 
    );
    console.log("dump rot", rot);
    return rot;
}

functiongetActorLocation(actorAddr){
    var functionAddr = moduleBase.add(0x92e16b4);
    var getActorLocationFunc = newNativeFunction(functionAddr, 'void', ['pointer', 'pointer', 'pointer']);
    var location = Memory.alloc(0x100);
    try{
        getActorLocationFunc(ptr(actorAddr), location, location);
        dumpVector(location);
        return location;
    }
    catch(e){
    }
}

functiongetActorRotation(actorAddr){
    var functionAddr = moduleBase.add(0x937BB14);
    var getActorRotationFunc = newNativeFunction(functionAddr, 'void', ['pointer', 'pointer', 'pointer']);
    var rotation = Memory.alloc(0x100);
    try{
        getActorRotationFunc(ptr(actorAddr), rotation, rotation);
        dumpRotator(rotation);
        return rotation;
    }
    catch(e){
    }
}

// function getVector(actorAddr){
//     var data_addr = ptr(actorAddr).add(0x500);
//     dumpVector(data_addr);
// }

// function writeVector(actorAddr, x, y, z){
//     ptr(actorAddr).add(0x500).writeFloat(x);
//     ptr(actorAddr).add(0x500+4).writeFloat(y);
//     ptr(actorAddr).add(0x500+8).writeFloat(z);
// }

functiongetGunOffset(actorAddr){
    var data_addr = ptr(actorAddr).add(0x500);
    dumpVector(data_addr);
}

functionwriteGunOffset(actorAddr, x, y, z){
    ptr(actorAddr).add(0x500).writeFloat(x);
    ptr(actorAddr).add(0x500+4).writeFloat(y);
    ptr(actorAddr).add(0x500+8).writeFloat(z);
}

functiongetControlRotation(actorAddr){
    var data_addr = ptr(actorAddr).add(0x288);
    var rot = dumpRotator(data_addr);
    return rot;
}

functionwriteControlRotation(actorAddr, a, b, c){
    ptr(actorAddr).add(0x288).writeFloat(a);
    ptr(actorAddr).add(0x288+4).writeFloat(b);
    ptr(actorAddr).add(0x288+8).writeFloat(c);
}

// function getFloat(actorAddr){
//     var data_addr = ptr(actorAddr).add(0x1a0);
//     const values = Memory.readByteArray(data_addr, 4);
//     console.log(new Float32Array(values, 0, 1)[0]);
// }

// function writeFloat(actorAddr, value){
//     ptr(actorAddr).add(0x52c).writeFloat(value);
// }

functiongetProjectil(){
    // 判断actorAddrs是否有FirstPersonProjectile_C
    actorAddrs = getActorsAddr();
    if (actorAddrs.hasOwnProperty("FirstPersonProjectile_C")) {
        var actorAddr = actorAddrs["FirstPersonProjectile_C"];
        var projectileMovement_addr = ptr(actorAddr).add(0x228).readPointer();
        console.log(projectileMovement_addr.add(0xec).readFloat());
    }

}

functionsetRenderCustomDepth(actorAddr, bEnabled){
    var functionAddr = moduleBase.add(0x8AB9DE8);
    var setRenderCustomDepthFunc = newNativeFunction(functionAddr, 'void', ['pointer', 'char']);
    setRenderCustomDepthFunc(ptr(actorAddr), bEnabled);
}

functionapplyCustomDepthToAllActors(bEnabled) {
    const actors = getActorsAddr(); // 获取所有Actor地址
    for (const actorName in actors) {
        if (actors.hasOwnProperty(actorName)) {
            const actorAddr = actors[actorName];
            try {
                setRenderCustomDepth(actorAddr, bEnabled); // 调用函数设置CustomDepth
                console.log(`Applied CustomDepth to ${actorName} at ${actorAddr}`);
            } catch (e) {
                console.error(`Failed to apply CustomDepth to ${actorName} at ${actorAddr}: ${e}`);
            }
        }
    }
}

functionsetCustomDepthStencilValue(actorAddr, value){
    var functionAddr = moduleBase.add(0x8AB9E0C);
    var setCustomDepthStencilValueFunc = newNativeFunction(functionAddr, 'void', ['pointer', 'int']);
    setCustomDepthStencilValueFunc(ptr(actorAddr), value);
}

functiongetRenderCustomDepth(actorAddr){
    var value = ptr(actorAddr).add(0x212).readU8();
    var bitValue = (value >> 3) & 1;
    return bitValue;
}

functiongetAllRenderCustomDepth(){
    const actors = getActorsAddr();
    for (const actorName in actors) {
        if (actors.hasOwnProperty(actorName)) {
            const actorAddr = actors[actorName];
            try {
                var value = getRenderCustomDepth(actorAddr);
                console.log(`RenderCustomDepth of ${actorName} at ${actorAddr}: ${value}`);
            } catch (e) {
                console.error(`Failed to get RenderCustomDepth of ${actorName} at ${actorAddr}: ${e}`);
            }
        }
    }
}

functionmain(){
    Java.perform(function(){
        set("libUE4.so");
        actorAddrs = getActorsAddr();
        writeGunOffset(actorAddrs["FirstPersonCharacter_C"], 0, 0, 20);
    });

    var func_addr = moduleBase.add(0x8D2ED80)
    Interceptor.attach(func_addr, {
        onEnter: function (args) {
            dumpRotator(ptr(args[3]));
            var playerRotation = getControlRotation(actorAddrs["PlayerController"]);
            ptr(args[3]).writeFloat(playerRotation.Pitch);
            ptr(args[3]).add(4).writeFloat(playerRotation.Yaw);

        },
        onLeave: function (retval) {
        }
    });

}

setImmediate(main);
```


---
## 附图

[图片已移除]
[图片已移除]