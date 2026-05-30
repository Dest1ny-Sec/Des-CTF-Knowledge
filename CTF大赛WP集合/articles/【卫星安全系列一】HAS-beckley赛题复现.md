# 【卫星安全系列一】HAS-beckley赛题复现

> 原文: https://www.ctfiot.com/148373.html
> ID: 148373

题目介绍
题目名：beckley

大概意思是利用Google Earth软件和给出的KML文件找到flag。

题目源码链接：https://github.com/cromulencellc/hackasat-qualifier-2020

由于网络问题，需要对源Dockerfile文件进行一些修改，

修改后的Dockerfile文件如下：

编译challenge环境

运行一个beckley挑战题服务端容器：

运行之后，nc设定的ip和端口，即可开始做题。

直接使用nc 172.17.0.1 19020开启

我们需要根据给出的satellite的信息和利用KML文件模拟卫星的拍摄角度，要完成这些需要对kml文件和python的Skyfield库进行学习。

可以在static文件夹下找到题目给出remote.kml文件，完整代码如下。

我们只需要关注<NetworkLink>、<LookAt>和<Link>元素即可。

用于指定本地或者远程的kml文件，在remote.kml文件里就是<Link>标签中的<href>元素引用的文件。

<LookAt> 元素用于指定地球上正被查看的点、景点与视点间的距离以及视图的角度。该元素的语法如下：

下图展示了 <LookAt> 视点的构建方式：

<LookAt> 元素可指定以下问题的答案：

问题
<LookAt> 中的规范

当前在查看什么目标？
<longitude>、<latitude>、<altitude>、<altitudeMode>

视点距景点有多远？
<range>

视图方向是否是北面朝上？
如果是，则使用默认的 <heading> 值0。如果不是，请指定一个0（不含）到360°的 <heading> 旋转值

视图方向是否直指地球？
如果是，则使用默认的 <tilt> 值。如果不是，镜头将向上朝着地平线；请指定一个不大于90°的 <tilt> 旋转值。 90°表示直接沿着地平线看过去（如果您离地球表面很远，而且 <tilt> 值为90°，那么您可能看不到地球表面）。

上面说过可以用于指定kml文件。

深入了解，请参考KML 教程 | “Keyhole 标记语言” | Google for Developers

使用 pip install Skyfield 即可

查询卫星某一刻的x,y,z坐标，代码如下：

运行结果

查询卫星相对于观察者的位置，可以通过构建一个Topos对象来表示观察者的纬度和经度，再结合矢量减法来确定，代码如下：

现在我们可以回到解题要求上了，我们需要计算出<LookAt>元素的几个属性值，定义一个虚拟相机来模拟卫星的拍摄角度。

计算出<longitude>、<latitude>、<altitude>、<heading>、<tilt>和<range>的值

<longitude>、<latitude>可以在2HSCKML.py文件中找到，如下所示：

因为<altitudeMode>是clampToGround,表示可以忽略高度，因此 <altitude> 是 0

下面的python代码可以计算出剩下的属性的值：

构造payload

最后成功显示了flag

卫星安全不同于传统的安全，涉及到很多数学和物理知识；本题是较为简单的一题，适合用来入门卫星安全。


```
Fire up your Google Earth and brush up on your KML tutorials, we're going to make it look at things!
```



```
FROM ubuntu:16.04
#Install Apache, Python, Curl. Enable CGI. Install PIP, use PIP to install skyfield
RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list; 
    apt-get update -y; 
    apt-get install -y apache2 python curl;
    a2enmod cgi; 
    curl -O https://bootstrap.pypa.io/pip/2.7/get-pip.py; 
    python2 get-pip.py; 
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple;
    pip install skyfield;

COPY errors /etc/apache2/sites-enabled/000-default.conf 
COPY custom_50x.html /var/www/html/custom_50x.html

WORKDIR /usr/lib/cgi-bin

# Upload all files to cgi-bin directory
COPY *.py ./
COPY entrypoint.sh ./
COPY deltat.* ./
COPY Leap_Second.dat ./
RUN chmod +x challenge.py 
# Suppress error output
RUN echo "ServerName beckley.mydomain.com" >> /etc/apache2/apache2.conf
#ENV FLAG=flag{Hungry_For_Apples}
# RUN
ENTRYPOINT ./entrypoint.sh
```



```
make challenge
```



```
socat -v tcp-listen:19020,reuseaddr exec:"docker run --rm -i -e SERVICE_HOST=172.17.0.1 -e SERVICE_PORT=19021 -e SEED=1000 -e FLAG=flag{test_beckley} -p 19021:80 beckley:challenge"
```



```
yjp@ubuntu:~$ nc 172.17.0.1 19020
We've captured data from a satellite that shows a flag located at the base of the Washington Monument.
The image was taken on March 26th, 2020, at 21:53:13
The satellite we used was: 

REDACT
1 13337U 98067A   20087.38052801 -.00000452  00000-0  00000+0 0  9995
2 13337  51.6460  33.2488 0005270  61.9928  83.3154 15.48919755219337

Use a Google Earth Pro KML file to 'Link' to http://172.17.0.1:19021/cgi-bin/HSCKML.py
and 'LookAt' that spot from where the satellite when it took the photo and get us that flag!
```



```
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
 <Folder>
 <name>HackASatCompetition</name>
 <visibility>0</visibility>
 <open>0</open>
 <description>HackASatComp1</description>
 <NetworkLink>
 <name>View Centered Placemark</name>
 <visibility>0</visibility>
 <open>0</open>
 <description>This is where the satellite was located when we saw it.</description>
 <refreshVisibility>0</refreshVisibility>
 <flyToView>0</flyToView>
 <LookAt id="ID">
 <!-- specific to LookAt -->
 <longitude>FILL ME IN</longitude> <!-- kml:angle180 -->
 <latitude>FILL ME IN TOO</latitude> <!-- kml:angle90 -->
 <altitude>FILL ME IN AS WELL</altitude> <!-- double -->
 <heading>FILL IN THIS VALUE</heading> <!-- kml:angle360 -->
 <tilt>FILL IN THIS VALUE TOO</tilt> <!-- kml:anglepos90 -->
 <range>FILL IN THIS VALUE ALSO</range> <!-- double -->
 <altitudeMode>clampToGround</altitudeMode>
 </LookAt>
 <Link>
 <href>http://FILL ME IN:FILL ME IN/cgi-bin/HSCKML.py</href>
 <refreshInterval>1</refreshInterval>
 <viewRefreshMode>onStop</viewRefreshMode>
 <viewRefreshTime>1</viewRefreshTime>
 <viewFormat>BBOX=[bboxWest],[bboxSouth],[bboxEast],[bboxNorth];CAMERA=[lookatLon],[lookatLat],[lookatRange],[lookatTilt],[lookatHeading];VIEW=[horizFov],[vertFov],[horizPixels],[vertPixels],[terrainEnabled]</viewFormat>
 </Link>
 </NetworkLink>
 </Folder>
</kml>
```



```
<LookAt id="ID">
  <longitude></longitude>                       <!-- kml:angle180 -->   
  <latitude></latitude>                         <!-- kml:angle90 -->   
  <altitude>0</altitude>                        <!-- double -->    
  <range></range>                               <!-- double -->   
  <tilt>0</tilt>                                <!-- float -->   
  <heading>0</heading>                          <!-- float -->   
  <altitudeMode>clampToGround</altitudeMode>    
           <!--kml:altitudeModeEnum:clampToGround, relativeToGround, absolute --> 
           <!-- or, gx:altitudeMode can be substituted: clampToSeaFloor, relativeToSeaFloor -->
</LookAt>
```



```
from skyfield.api import EarthSatellite
from skyfield.api import load

ts = load.timescale()
line1 = '1 25544U 98067A   14020.93268519  .00009878  00000-0  18200-3 0  5082'
line2 = '2 25544  51.6498 109.4756 0003572  55.9686 274.8005 15.49815350868473'
#从TLE数据中加载卫星轨道元素
satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)', ts)
print(satellite)
t = ts.utc(2014, 1, 23, 11, 18, 7)
geocentric = satellite.at(t)
print(geocentric.position.km)
```



```
ISS (ZARYA) catalog #25544 epoch 2014-01-20 22:23:04 UTC
[-3918.87650458 -1887.64838745  5209.08801512]
```



```
from skyfield.api import Topos
bluffton = Topos('38.8894838 N', '77.0352791 W')
difference = satellite - bluffton
topocentric = difference.at(t)
alt, az, distance = topocentric.altaz()
print("(alt, az, distance)=",(alt, az, distance))
# (alt, az, distance)= (<Angle 49deg 37' 40.9">, <Angle 243deg 31' 48.1">, <Distance 3.60007e-06 au>)
```



```
from skyfield.api import EarthSatellite
from skyfield.api import load
from skyfield.api import Topos

ts = load.timescale()
line1 = '1 13337U 98067A   20087.38052801 -.00000452  00000-0  00000+0 0  9995'
line2 = '2 13337  51.6460  33.2488 0005270  61.9928  83.3154 15.48919755219337'

satellite = EarthSatellite(line1, line2, 'REDACT', ts)
t = ts.utc(2020, 3, 26, 21, 53, 13)
photo = Topos('38.889100 N', '77.0354 W')
difference = satellite - photo
topocentric = difference.at(t)
alt, az, distance = topocentric.altaz()

print('Altitude(deg): %f' % alt.degrees)
print('Azimuth(def): %f' % az.degrees)
print('Range(m): %d' % int(distance.m))

tilt = 90 - alt.degrees

print('Tilt(deg): %f' % tilt)

heading = (180 + az.degrees) % 360

print('Heading(deg): %f' % heading)
```



```
curl http://172.17.0.1:19021/cgi-bin/HSCKML.py?CAMERA=-77.03,38.89,538544,40.369421,63.535801 -H 'User-Agent: GoogleEarth/7.3.2.5815(X11;Linux (5.2.0.0);en;kml:2.2;client:Pro;type:default)' -H 'Accept: application/vnd.google-earth.kml+xml, application/vnd.google-earth.kmz, image/*, */*' -H 'Accept-Language: en-US, *' -H 'Connection: keep-alive'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/4-1701349278.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/5-1701349279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/5-1701349279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/0-1701349280.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/5-1701349281.png)