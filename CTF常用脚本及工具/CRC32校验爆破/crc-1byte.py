import binascii
import string

def crack_crc():
    print('-------------Start Crack CRC-------------')
    crc_list = [0xda6fd2a0, 0xf6a70, 0x70659eff, 0x862575d]#文件的CRC32值列表，注意顺序
    comment = ''
    chars = string.printable
    for crc_value in crc_list:
        for char1 in chars:
            char_crc = binascii.crc32(char1.encode())#获取遍历字符的CRC32值
            calc_crc = char_crc & 0xffffffff#将获取到的字符的CRC32值与0xffffffff进行与运算
            if calc_crc == crc_value:#将每个字符的CRC32值与每个文件的CRC32值进行匹配
                print('[+] {}: {}'.format(hex(crc_value),char1))
                comment += char1
    print('-----------CRC Crack Completed-----------')
    print('Result: {}'.format(comment))

if __name__ == '__main__':
    crack_crc()
