import gmpy2 as gp

def exgcd(a, b):
    if b==0:
        return 1, 0, a
    x2, y2, r = exgcd(b, a%b)
    x1 = y2
    y1 = x2-(a//b)*y2
    return x1, y1, r

def get_flag(string):
    flag=''
    i=0
    j=1
    while i < len(string):
        if int(string[i:i+j]) >= 33 and int(string[i:i+j]) <=126:
            flag+=chr(int(string[i:i+j]))
            i=i+j
            j=1
        else:
            j+=1
    print(flag)

if __name__ == '__main__':

    e1=773
    e2=839
    n=6266565720726907265997241358331585417095726146341989755538017122981360742813498401533594757088796536341941659691259323065631249
    message1=3453520592723443935451151545245025864232388871721682326408915024349804062041976702364728660682912396903968193981131553111537349
    message2=5672818026816293344070119332536629619457163570036305296869053532293105379690793386019065754465292867769521736414170803238309535
    r1, r2, t = exgcd(e1, e2)
    m = gp.powmod(message1, r1, n) * gp.powmod(message2, r2, n) % n
    get_flag(str(m))
