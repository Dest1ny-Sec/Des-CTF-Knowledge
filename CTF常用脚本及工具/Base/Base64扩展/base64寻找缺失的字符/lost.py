import string

s = "JASGBWcQPRXEFLbCDIlmnHUVKTYZdMovwipatNOefghq56rs****kxyz012789+/"

for i in string.ascii_letters + string.digits:
    if(i not in s):
        print(i)
# ju35