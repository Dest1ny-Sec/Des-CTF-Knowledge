import hashlib


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


for i in range(10000000):
    if(md5(str(i)).startswith('deadbeef')):
        print(i)
        # break
