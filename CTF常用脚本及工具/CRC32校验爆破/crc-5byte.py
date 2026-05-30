import binascii
import string

def crack_crc():
    print('-------------Start Crack CRC-------------')
    crc_list = [0x05dec988]#文件的CRC32值列表，注意顺序
    comment = ''
    chars = 'abcdefghijklmnopqrstuvwxyz\{\}'
    for crc_value in crc_list:
        for char1 in chars:
            for char2 in chars:
                for char3 in chars:
                    for char4 in chars:
                        for char5 in chars:
                            res_char = char1 + char2 + char3 + char4 + char5#获取遍历的任意5Byte字符
                            char_crc = binascii.crc32(res_char.encode())#获取遍历字符的CRC32值
                            calc_crc = char_crc & 0xffffffff#将遍历的字符的CRC32值与0xffffffff进行与运算
                            if calc_crc == crc_value:#将获取字符的CRC32值与每个文件的CRC32值进行匹配
                                print('[+] {}: {}'.format(hex(crc_value),res_char))
                                comment += res_char
    print('-----------CRC Crack Completed-----------')
    print('Result: {}'.format(comment))

if __name__ == '__main__':
    crack_crc()
