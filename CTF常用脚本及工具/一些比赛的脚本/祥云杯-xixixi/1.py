# -*- coding: utf-8 -*-
# @Project: Hello Python!
# @File   : exp
# @Author : Tr0jAn <Tr0jAn@birkenwald.cn>
# @Date   : 2020-11-22
import struct
import binascii

class FAT32Parser(object):
  def __init__(self, vhdFileName):
    with open(vhdFileName, 'rb') as f:
      self.diskData = f.read()
    self.DBR_off = self.GetDBRoff()
    self.newData = ''.join(str(self.diskData))


  def GetDBRoff(self):
    DPT_off = 0x1BE
    target = self.diskData[DPT_off+8:DPT_off+12]
    DBR_sector_off, = struct.unpack("<I", target)
    return DBR_sector_off * 512


  def GetFAT1off(self):
    target = self.diskData[self.DBR_off+0xE:self.DBR_off+0x10]
    FAT1_sector_off, = struct.unpack("<H", target)
    return self.DBR_off + FAT1_sector_off * 512


  def GetFATlength(self):
    target = self.diskData[self.DBR_off+0x24:self.DBR_off+0x28]
    FAT_sectors, = struct.unpack("<I", target)
    return FAT_sectors * 512


  def GetRootoff(self):
    FAT_length = self.GetFATlength()
    FAT2_off = self.GetFAT1off() + FAT_length
    return FAT2_off + FAT_length


  def Cluster2FAToff(self, cluster):
    FAT1_off = self.GetFAT1off()
    return FAT1_off + cluster * 4


  def Cluster2DataOff(self, cluster):
    rootDir_off = self.GetRootoff()
    return rootDir_off + (cluster - 2) * 512

    
def read(n):
    global key
    binary = b''
    for i in vhd.read(n):
        binary += (i ^ (key & 0xFE)).to_bytes(length=1, byteorder='big', signed=False)
    return binary


FAT = FAT32Parser("new.vhd")
vhd = open("new.vhd", "rb")
vhd.seek(0x27bae00)  # 定位磁盘中图片位置
flag = open("flag.png", "wb")
flag.write(vhd.read(8))  # 写入png头
key = 0
while True:
    d = read(8)
    length, cType = struct.unpack(">I4s", d)
    print(length, cType)  # length为数据长度，cType为数据块类型
    data = read(length)
    CRC = struct.unpack(">I", read(4))[0]
    print(CRC)
    rCRC = binascii.crc32(cType + data) & 0xffffffff
    print(rCRC)
    rDATA = struct.pack(">I", length) + cType + data + struct.pack(">I", rCRC)
    flag.write(rDATA)
    if CRC != rCRC:  # CRC错误的IDAT数据块
        b_endian = struct.pack(">I", CRC)
        clusterList = struct.unpack("<I", b_endian)[0]
        print(clusterList)
        vhd.seek(FAT.Cluster2DataOff(clusterList))
        key = clusterList & 0xFE
    if cType == b"IEND":
        break