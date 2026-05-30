# BCTF自动驾驶-WriteUp

> 原文: https://www.ctfiot.com/1441.html
> ID: 1441

demo

Lane Detection: targeted attack

ADC Programming: interception

解题过程
planning.py

#!/usr/bin/env python3

import random
import cv2
import numpy as np
from collections import Counter
from simple_pid import PID
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, deltaE_cie76
from PIL import Image

# Stanley controller parameters
k_e = 0.3
k_v = 0.01
delta_steer_per_iter = 0.1

#########################################################
# Some utility functions. Define new ones as needed.
#########################################################

def waypoint_distance(waypt1: list, waypt2: list) -> float:
    return np.sqrt(np.sum((np.array(waypt1) - np.array(waypt2))**2))

def normalize_angle(angle: float) -> float:
    while angle > np.pi:
        angle -= 2.0*np.pi
    while angle < -np.pi:
        angle += 2.0*np.pi
    return angle

def preprocess_image(cv_img: np.ndarray) -> np.ndarray:
    # resize to have less pixels
    cv_img = cv2.resize(cv_img, (416, 416), interpolation=cv2.INTER_AREA)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    if cv_img.shape[0] == 3:
        rgb_img = np.transpose(cv_img, (1, 2, 0))
    else:
        rgb_img = cv_img
    return rgb_img

#########################################################
# Main control logic for the Autonomous Driving Car (ADC)
#########################################################

class Controller:
    def __init__(self):
        self.speed_pid = PID(1.0, 0.1, 0.01, setpoint=5)
        self.speed_pid.sample_time = 0.01
        self.speed_pid.output_limits = (-1, 1)
        self.counter = 0
        self.last_steering = 0
        self.last_throttle = 0
        self.plan_waypts = []

    #########################################################
    # TODO: Players should implement get_control() with their
    # own control logic to achieve the attack goal
    #########################################################

    def get_control(self, adc_pose: list, adc_speed: float, adc_yaw: float, adc_frame: np.ndarray, npc_poses: list) -> (float, float):
        """
        Control logic for ADC. This function will be invoked at each control iteration.
        @param self
        @param adc_pose list: ADC's current 2D position in east and north directions
        @param adc_speed float: ADC's current speed
        @param adc_yaw float: ADC's current heading in radians
        @param adc_frame numpy.ndarray: ADC's front camera frame, shape=(1080, 1920, 3)
        @param npc_poses list(list): The positions of NPCs as an array of 2D arrays
        """
        # Note: Below is a sample implementation, you are free to modify it and
        #       add new functions as needed as long as this function will return
        #       and only returns steering and throttle

        # sample usages of functions and inputs
        adc_frame_preprocessed = preprocess_image(adc_frame)
        for i in range(len(npc_poses)):
            dist = waypoint_distance(adc_pose, npc_poses[i])
            print("ADC distance to {}th NPC is {}m".format(i, dist))

        if len(npc_poses) > 0:
            self.plan_waypts = [adc_pose, npc_poses[0]]
        steering = self.lateral_control(self.plan_waypts, adc_pose, adc_speed, adc_yaw, self.last_steering)
        if dist > 150:
          dist = 150
        throttle = self.longitudinal_control(adc_speed, dist)
        #steering = 0.0
        #throttle = 0.05

        self.counter += 1
        self.last_steering = steering
        self.last_throttle = throttle

        # Note: steering: +: steer to right, -: steer to left
        #       throttle: +: speed up, -: slow down
        #       both are limited in the range (-1, 1)
        return steering, throttle

    def lateral_control(self, plan_waypts: list, curr_waypt: list, v: float, yaw: float, pre_steer: float, is_return: bool = False) -> float:
        """
        create lateral controller.
        @param self
        @param plan_waypts list: planned trajectory, i.e., a list of waypoints, should contain at least two waypoints
        @param curr_waypt list: ADC's current 2D position
        @param v float: ADC speed
        @param yaw float: ADC yaw in radians
        @param pre_steer float: previous steering
        @param is_return bool: if the ADC is returning the starting point
        """
        # Ref: https://www.ri.cmu.edu/pub_files/2009/2/Automatic_Steering_Methods_for_Autonomous_Automobile_Path_Tracking.pdf
        yaw_path = np.arctan2(plan_waypts[-1][1] - plan_waypts[0][1], plan_waypts[-1][0] - plan_waypts[0][0])
        yaw_diff = normalize_angle(yaw_path - yaw)
        crosstrack_error = np.sqrt(
            np.min(np.sum((np.array(curr_waypt) - np.array(plan_waypts)) ** 2, axis=1)))
        yaw_crosstrack = np.arctan2(curr_waypt[1] - plan_waypts[0][1], curr_waypt[0] - plan_waypts[0][0])
        yaw_path2ct = normalize_angle(yaw_path - yaw_crosstrack)
        if yaw_path2ct > 0:
            crosstrack_error = abs(crosstrack_error)
        else:
            crosstrack_error = -abs(crosstrack_error)
        yaw_diff_crosstrack = np.arctan(k_e * crosstrack_error / (k_v + v))
        steer = normalize_angle(yaw_diff + yaw_diff_crosstrack)
        steer = -np.clip(steer, -1., 1.)
        if is_return:
            steer_limited = np.clip(steer, pre_steer - 3*delta_steer_per_iter, pre_steer + 3*delta_steer_per_iter)
        else:
            steer_limited = np.clip(steer, pre_steer - delta_steer_per_iter, pre_steer + delta_steer_per_iter)
        return steer_limited

    def longitudinal_control(self, v: float, t_v: float) -> float:
        """
        create longitudinal controller.
        @param self
        @param v float: input ADC speed
        @param t_v float: target speed
        """
        self.speed_pid.setpoint = t_v
        throttle = self.speed_pid(v)
        return throttle

Adversarial NPC: single box

解题过程
gps.py

f = open('npc_benign.json', 'r')
gps = f.read()
f.close()
gpslines = gps.split('n')
pos = []
for line in gpslines:
  i0 = line.find('timestamp')
  if i0 >= 0:
    ti = line[i0+12:-1]
  i1 = line.find('latitude')
  if i1 >= 0:
    la = float(line[i1+11:-1])
  i2 = line.find('longitude')
  if i2 >= 0:
    lo = float(line[i2+12:-1])
  i3 = line.find('altitude')
  if i3 >= 0:
    al = float(line[i3+11:-1])
  i3 = line.find('roll')
  if i3 >= 0:
    ro = float(line[i3+7:-1])
  i3 = line.find('pitch')
  if i3 >= 0:
    pi = line[i3+8:-1]
  i3 = line.find('yaw')
  if i3 >= 0:
    ya = line[i3+6:-1]
  i3 = line.find('speed')
  if i3 >= 0:
    sp = line[i3+8:]
    pos.append( [la, lo, al, ti, ro, pi, ya, sp] )

rate = 1.2
print rate
for i in range(len(pos) - 120):
  pos[120 + i][0] = rate*(pos[120][0] - pos[399][0]) + pos[120 + i][0]
f = open('gps_new.json', 'w')
f.write('[n')
for i in range(len(pos)):
  f.write('  {n')
  f.write('    "timestamp": %s,n' % pos[i][3])
  f.write('    "latitude": %.12f,n' % pos[i][0])
  f.write('    "longitude": %s,n' % pos[i][1])
  f.write('    "altitude": %s,n' % pos[i][2])
  f.write('    "roll": %s,n' % pos[i][4])
  f.write('    "pitch": %s,n' % pos[i][5])
  f.write('    "yaw": %s,n' % pos[i][6])
  f.write('    "speed": %sn' % pos[i][7])
  if i == len(pos) - 1:
    f.write('  }n')
  else:
    f.write('  },n')
f.write(']')
f.close()

gps_new.json

[
  {
    "timestamp": 0.0,
    "latitude": 37.789961912203,
    "longitude": -122.401553978,
    "altitude": 10.2880001068,
    "roll": 0.0,
    "pitch": 0,
    "yaw": 1.00179122455302e-05,
    "speed": 20.0
  },
  {
    "timestamp": 0.05,
    "latitude": 37.789961854541,
    "longitude": -122.401542626,
    "altitude": 10.2728290558,
    "roll": 0.00087853212608,
    "pitch": 4.37385324403294e-06,
    "yaw": 1.08999765870976e-05,
    "speed": 19.986112009053592
  },
  {
    "timestamp": 0.1,
    "latitude": 37.789961797602,
    "longitude": -122.401531416,
    "altitude": 10.245757103,
    "roll": 0.0404979214072,
    "pitch": 0.000107885905890726,
    "yaw": -0.000273296143859625,
    "speed": 19.53953417980725
  },
  {
    "timestamp": 0.15,
    "latitude": 37.789961741532,
    "longitude": -122.401520378,
    "altitude": 10.2186584473,
    "roll": 0.0877417102456,
    "pitch": 0.000613974640145898,
    "yaw": 0.0023149426560849,
    "speed": 19.458443954458264
  },
  {
    "timestamp": 0.2,
    "latitude": 37.789961685130,
    "longitude": -122.401509302,
    "altitude": 10.1946020126,
    "roll": 0.083763346076,
    "pitch": 0.00211690412834287,
    "yaw": 0.00415488658472896,
    "speed": 19.555836055796547
  },
  {
    "timestamp": 0.25,
    "latitude": 37.789961628374,
    "longitude": -122.401498156,
    "altitude": 10.1744937897,
    "roll": 0.0497044585645,
    "pitch": 0.00419731345027685,
    "yaw": 0.00471088895574212,
    "speed": 19.678308862186125
  },
  {
    "timestamp": 0.3,
    "latitude": 37.789961571419,
    "longitude": -122.401486944,
    "altitude": 10.1585912704,
    "roll": 0.00784304458648,
    "pitch": 0.00621826434507966,
    "yaw": 0.00434521911665797,
    "speed": 19.779648523152936
  },
  {
    "timestamp": 0.35,
    "latitude": 37.789961513677,
    "longitude": -122.401475686,
    "altitude": 10.1464471817,
    "roll": 359.972473145,
    "pitch": 0.00776536809280515,
    "yaw": 0.0035081971436739,
    "speed": 19.849717576884554
  },
  {
    "timestamp": 0.4,
    "latitude": 37.789961455639,
    "longitude": -122.401464397,
    "altitude": 10.1374406815,
    "roll": 359.948364258,
    "pitch": 0.00868796184659004,
    "yaw": 0.00251324544660747,
    "speed": 19.89642120146336
  },
  {
    "timestamp": 0.45,
    "latitude": 37.789961397359,
    "longitude": -122.401453087,
    "altitude": 10.1309347153,
    "roll": 359.935058594,
    "pitch": 0.0090014636516571,
    "yaw": 0.00152538309339434,
    "speed": 19.927312974287453
  },
  {
    "timestamp": 0.5,
    "latitude": 37.789961339155,
    "longitude": -122.401441766,
    "altitude": 10.1262254715,
    "roll": 359.930297852,
    "pitch": 0.008848219178617,
    "yaw": 0.000618399993982166,
    "speed": 19.94533976993406
  },
  {
    "timestamp": 0.55,
    "latitude": 37.789961281179,
    "longitude": -122.401430435,
    "altitude": 10.1230268478,
    "roll": 359.931060791,
    "pitch": 0.00836139172315598,
    "yaw": -0.000185332421096973,
    "speed": 19.96002497668345
  },
  {
    "timestamp": 0.6,
    "latitude": 37.789961223581,
    "longitude": -122.401419098,
    "altitude": 10.1209049225,
    "roll": 359.934997559,
    "pitch": 0.00766501389443874,
    "yaw": -0.000895189994480461,
    "speed": 19.971443679571472
  },
  {
    "timestamp": 0.65,
    "latitude": 37.789961165952,
    "longitude": -122.401407755,
    "altitude": 10.1195383072,
    "roll": 359.940490723,
    "pitch": 0.006865537725389,
    "yaw": -0.00152462569531053,
    "speed": 19.980237728104957
  },
  {
    "timestamp": 0.7,
    "latitude": 37.789961108438,
    "longitude": -122.401396408,
    "altitude": 10.1186876297,
    "roll": 359.946502686,
    "pitch": 0.00605636136606336,
    "yaw": -0.00208621425554156,
    "speed": 19.98697477269317
  },
  {
    "timestamp": 0.75,
    "latitude": 37.789961050775,
    "longitude": -122.401385058,
    "altitude": 10.1180534363,
    "roll": 359.952514648,
    "pitch": 0.00531605770811439,
    "yaw": -0.00259051029570401,
    "speed": 19.989631499553205
  },
  {
    "timestamp": 0.8,
    "latitude": 37.789960993101,
    "longitude": -122.401373707,
    "altitude": 10.1177206039,
    "roll": 359.95803833,
    "pitch": 0.00465651554986835,
    "yaw": -0.00304309162311256,
    "speed": 19.992138222000087
  },
  {
    "timestamp": 0.85,
    "latitude": 37.789960935424,
    "longitude": -122.401362355,
    "altitude": 10.1175680161,
    "roll": 359.963134766,
    "pitch": 0.00408577406778932,
    "yaw": -0.00344746187329292,
    "speed": 19.992563261676434
  },
  {
    "timestamp": 0.9,
    "latitude": 37.789960877885,
    "longitude": -122.401351004,
    "altitude": 10.1175193787,
    "roll": 359.96774292,
    "pitch": 0.00361152645200491,
    "yaw": -0.00380691210739315,
    "speed": 19.991148027605753
  },
  {
    "timestamp": 0.95,
    "latitude": 37.789960820212,
    "longitude": -122.401339654,
    "altitude": 10.1175270081,
    "roll": 359.971862793,
    "pitch": 0.00322462385520339,
    "yaw": -0.00412555923685431,
    "speed": 19.988266090103252
  },
  {
    "timestamp": 1.0,
    "latitude": 37.789960763237,
    "longitude": -122.401328306,
    "altitude": 10.117562294,
    "roll": 359.975494385,
    "pitch": 0.00291407643817365,
    "yaw": -0.00440777745097876,
    "speed": 19.984203483323423
  },
  {
    "timestamp": 1.05,
    "latitude": 37.789960706273,
    "longitude": -122.40131696,
    "altitude": 10.117606163,
    "roll": 359.978637695,
    "pitch": 0.00267567718401551,
    "yaw": -0.00465807551518083,
    "speed": 19.97910515475458
  },
  {
    "timestamp": 1.1,
    "latitude": 37.789960649325,
    "longitude": -122.401305618,
    "altitude": 10.1176509857,
    "roll": 359.981292725,
    "pitch": 0.00250738835893571,
    "yaw": -0.00488132331520319,
    "speed": 19.973785565312706
  },
  {
    "timestamp": 1.15,
    "latitude": 37.789960592389,
    "longitude": -122.401294278,
    "altitude": 10.1176919937,
    "roll": 359.983337402,
    "pitch": 0.00239476445131004,
    "yaw": -0.00508645363152027,
    "speed": 19.969312829104958
  },
  {
    "timestamp": 1.2,
    "latitude": 37.789960535463,
    "longitude": -122.40128294,
    "altitude": 10.117726326,
    "roll": 359.984741211,
    "pitch": 0.00231496570631862,
    "yaw": -0.00528392428532243,
    "speed": 19.965778502837836
  },
  {
    "timestamp": 1.25,
    "latitude": 37.789960478545,
    "longitude": -122.401271604,
    "altitude": 10.1177530289,
    "roll": 359.985595703,
    "pitch": 0.00226673320867121,
    "yaw": -0.00548101216554642,
    "speed": 19.963094857810283
  },
  {
    "timestamp": 1.3,
    "latitude": 37.789960421638,
    "longitude": -122.401260271,
    "altitude": 10.1176490784,
    "roll": 359.986053467,
    "pitch": 0.00226743193343282,
    "yaw": -0.00568257411941886,
    "speed": 19.958982534039922
  },
  {
    "timestamp": 1.35,
    "latitude": 37.789960364740,
    "longitude": -122.401248939,
    "altitude": 10.1174964905,
    "roll": 359.986114502,
    "pitch": 0.00230335025116801,
    "yaw": 359.994110107422,
    "speed": 19.95570381378949
  },
  {
    "timestamp": 1.4,
    "latitude": 37.789960307843,
    "longitude": -122.401237608,
    "altitude": 10.1174621582,
    "roll": 359.985748291,
    "pitch": 0.0023405384272337,
    "yaw": 359.993896484375,
    "speed": 19.95549023573878
  },
  {
    "timestamp": 1.45,
    "latitude": 37.789960250944,
    "longitude": -122.401226277,
    "altitude": 10.1174850464,
    "roll": 359.985229492,
    "pitch": 0.00236273277550936,
    "yaw": 359.99365234375,
    "speed": 19.95587559769856
  },
  {
    "timestamp": 1.5,
    "latitude": 37.789960194042,
    "longitude": -122.401214945,
    "altitude": 10.1175336838,
    "roll": 359.984619141,
    "pitch": 0.00237292191013694,
    "yaw": 359.993408203125,
    "speed": 19.956577547265994
  },
  {
    "timestamp": 1.55,
    "latitude": 37.789960137136,
    "longitude": -122.401203613,
    "altitude": 10.1175880432,
    "roll": 359.984069824,
    "pitch": 0.00236266059800982,
    "yaw": 359.9931640625,
    "speed": 19.957517881738802
  },
  {
    "timestamp": 1.6,
    "latitude": 37.789960080232,
    "longitude": -122.401192281,
    "altitude": 10.1175165176,
    "roll": 359.983612061,
    "pitch": 0.00237421225756407,
    "yaw": 359.992919921875,
    "speed": 19.956472523193977
  },
  {
    "timestamp": 1.65,
    "latitude": 37.789960023323,
    "longitude": -122.401180949,
    "altitude": 10.117518425,
    "roll": 359.983123779,
    "pitch": 0.00238050473853946,
    "yaw": 359.992645263672,
    "speed": 19.957933625617486
  },
  {
    "timestamp": 1.7,
    "latitude": 37.789959966553,
    "longitude": -122.401169617,
    "altitude": 10.1174278259,
    "roll": 359.982696533,
    "pitch": 0.00238894182257354,
    "yaw": 359.992370605469,
    "speed": 19.95748724579294
  },
  {
    "timestamp": 1.75,
    "latitude": 37.789959910333,
    "longitude": -122.401158286,
    "altitude": 10.1173057556,
    "roll": 359.982299805,
    "pitch": 0.00242291716858745,
    "yaw": 359.992095947266,
    "speed": 19.957285069593514
  },
  {
    "timestamp": 1.8,
    "latitude": 37.789959854105,
    "longitude": -122.401146953,
    "altitude": 10.1173048019,
    "roll": 359.981811523,
    "pitch": 0.00244475179351866,
    "yaw": 359.991821289063,
    "speed": 19.95961786464248
  },
  {
    "timestamp": 1.85,
    "latitude": 37.789959797876,
    "longitude": -122.40113562,
    "altitude": 10.1172361374,
    "roll": 359.981445312,
    "pitch": 0.00246058404445648,
    "yaw": 359.991516113281,
    "speed": 19.959898189511442
  },
  {
    "timestamp": 1.9,
    "latitude": 37.789959741637,
    "longitude": -122.401124285,
    "altitude": 10.117269516,
    "roll": 359.981018066,
    "pitch": 0.00246267067268491,
    "yaw": 359.991241455078,
    "speed": 19.962477064661208
  },
  {
    "timestamp": 1.95,
    "latitude": 37.789959685391,
    "longitude": -122.401112949,
    "altitude": 10.1173448563,
    "roll": 359.980682373,
    "pitch": 0.00245036277920008,
    "yaw": 359.990936279297,
    "speed": 19.965116928987015
  },
  {
    "timestamp": 2.0,
    "latitude": 37.789959629142,
    "longitude": -122.401101613,
    "altitude": 10.1173095703,
    "roll": 359.980529785,
    "pitch": 0.00243124924600124,
    "yaw": 359.990631103516,
    "speed": 19.96543910293284
  },
  {
    "timestamp": 2.05,
    "latitude": 37.789959572885,
    "longitude": -122.401090275,
    "altitude": 10.1173496246,
    "roll": 359.98034668,
    "pitch": 0.00241344003006816,
    "yaw": 359.990325927734,
    "speed": 19.967977901361348
  },
  {
    "timestamp": 2.1,
    "latitude": 37.789959516619,
    "longitude": -122.401078936,
    "altitude": 10.1174201965,
    "roll": 359.980194092,
    "pitch": 0.00238355016335845,
    "yaw": 359.990020751953,
    "speed": 19.97052236735932
  },
  {
    "timestamp": 2.15,
    "latitude": 37.789959460346,
    "longitude": -122.401067595,
    "altitude": 10.1174974442,
    "roll": 359.980133057,
    "pitch": 0.00234452867880464,
    "yaw": 359.989715576172,
    "speed": 19.972898943121464
  },
  {
    "timestamp": 2.2,
    "latitude": 37.789959404064,
    "longitude": -122.401056253,
    "altitude": 10.1175699234,
    "roll": 359.980133057,
    "pitch": 0.00230431067757308,
    "yaw": 359.989410400391,
    "speed": 19.975096200299582
  },
  {
    "timestamp": 2.25,
    "latitude": 37.789959347775,
    "longitude": -122.40104491,
    "altitude": 10.1176309586,
    "roll": 359.980194092,
    "pitch": 0.00226445542648435,
    "yaw": 359.989105224609,
    "speed": 19.977125605200175
  },
  {
    "timestamp": 2.3,
    "latitude": 37.789959291481,
    "longitude": -122.401033566,
    "altitude": 10.1176815033,
    "roll": 359.980285645,
    "pitch": 0.00223197950981557,
    "yaw": 359.988830566406,
    "speed": 19.979010055870532
  },
  {
    "timestamp": 2.35,
    "latitude": 37.789959235179,
    "longitude": -122.401022221,
    "altitude": 10.1177196503,
    "roll": 359.980407715,
    "pitch": 0.00220701354555786,
    "yaw": 359.988525390625,
    "speed": 19.980743832224416
  },
  {
    "timestamp": 2.4,
    "latitude": 37.789959178871,
    "longitude": -122.401010875,
    "altitude": 10.1177473068,
    "roll": 359.980560303,
    "pitch": 0.00218956684693694,
    "yaw": 359.988220214844,
    "speed": 19.98234600440188
  },
  {
    "timestamp": 2.45,
    "latitude": 37.789959122557,
    "longitude": -122.400999528,
    "altitude": 10.117767334,
    "roll": 359.980712891,
    "pitch": 0.00217794580385089,
    "yaw": 359.987915039063,
    "speed": 19.983822300586546
  },
  {
    "timestamp": 2.5,
    "latitude": 37.789959066789,
    "longitude": -122.40098818,
    "altitude": 10.1177816391,
    "roll": 359.980865479,
    "pitch": 0.00216638017445803,
    "yaw": 359.987640380859,
    "speed": 19.985176528428337
  },
  {
    "timestamp": 2.55,
    "latitude": 37.789959011155,
    "longitude": -122.400976832,
    "altitude": 10.1177911758,
    "roll": 359.980987549,
    "pitch": 0.00216149282641709,
    "yaw": 359.987335205078,
    "speed": 19.98642013257847
  },
  {
    "timestamp": 2.6,
    "latitude": 37.789958955515,
    "longitude": -122.400965483,
    "altitude": 10.1177978516,
    "roll": 359.981140137,
    "pitch": 0.00216195499524474,
    "yaw": 359.987060546875,
    "speed": 19.987568372971005
  },
  {
    "timestamp": 2.65,
    "latitude": 37.789958899873,
    "longitude": -122.400954133,
    "altitude": 10.1178016663,
    "roll": 359.981292725,
    "pitch": 0.00215979758650064,
    "yaw": 359.986785888672,
    "speed": 19.98862697113305
  },
  {
    "timestamp": 2.7,
    "latitude": 37.789958844225,
    "longitude": -122.400942783,
    "altitude": 10.1178035736,
    "roll": 359.981414795,
    "pitch": 0.00215980270877481,
    "yaw": 359.986480712891,
    "speed": 19.98960355319131
  },
  {
    "timestamp": 2.75,
    "latitude": 37.789958788573,
    "longitude": -122.400931432,
    "altitude": 10.117805481,
    "roll": 359.981536865,
    "pitch": 0.00216565770097077,
    "yaw": 359.986206054688,
    "speed": 19.9904962126573
  },
  {
    "timestamp": 2.8,
    "latitude": 37.789958732917,
    "longitude": -122.400920081,
    "altitude": 10.1178064346,
    "roll": 359.981628418,
    "pitch": 0.00216430006548762,
    "yaw": 359.985931396484,
    "speed": 19.991320208214937
  },
  {
    "timestamp": 2.85,
    "latitude": 37.789958677259,
    "longitude": -122.400908729,
    "altitude": 10.1178064346,
    "roll": 359.981750488,
    "pitch": 0.00216319272294641,
    "yaw": 359.985656738281,
    "speed": 19.99206218807896
  },
  {
    "timestamp": 2.9,
    "latitude": 37.789958621597,
    "longitude": -122.400897377,
    "altitude": 10.117805481,
    "roll": 359.981842041,
    "pitch": 0.00216986192390323,
    "yaw": 359.985382080078,
    "speed": 19.992746949304763
  },
  {
    "timestamp": 2.95,
    "latitude": 37.789958565933,
    "longitude": -122.400886024,
    "altitude": 10.117805481,
    "roll": 359.981933594,
    "pitch": 0.0021744011901319,
    "yaw": 359.985107421875,
    "speed": 19.993376397195743
  },
  {
    "timestamp": 3.0,
    "latitude": 37.789958510266,
    "longitude": -122.400874672,
    "altitude": 10.1178045273,
    "roll": 359.982025146,
    "pitch": 0.00217310898005962,
    "yaw": 359.984832763672,
    "speed": 19.993950533069413
  },
  {
    "timestamp": 3.05,
    "latitude": 37.789958454596,
    "longitude": -122.400863318,
    "altitude": 10.1178035736,
    "roll": 359.982116699,
    "pitch": 0.00217565940693021,
    "yaw": 359.984558105469,
    "speed": 19.99447317122369
  },
  {
    "timestamp": 3.1,
    "latitude": 37.789958398923,
    "longitude": -122.400851965,
    "altitude": 10.1178035736,
    "roll": 359.982177734,
    "pitch": 0.00217900006100535,
    "yaw": 359.984283447266,
    "speed": 19.994957661546973
  },
  {
    "timestamp": 3.15,
    "latitude": 37.789958343248,
    "longitude": -122.400840611,
    "altitude": 10.1178026199,
    "roll": 359.98223877,
    "pitch": 0.00218631443567574,
    "yaw": 359.984008789063,
    "speed": 19.995402098863437
  },
  {
    "timestamp": 3.2,
    "latitude": 37.789958287577,
    "longitude": -122.400829259,
    "altitude": 10.1176776886,
    "roll": 359.982391357,
    "pitch": 0.0022147276904434,
    "yaw": 359.983734130859,
    "speed": 19.993618707926068
  },
  {
    "timestamp": 3.25,
    "latitude": 37.789958232178,
    "longitude": -122.400817905,
    "altitude": 10.1176328659,
    "roll": 359.982391357,
    "pitch": 0.00225040432997048,
    "yaw": 359.983489990234,
    "speed": 19.994171883641393
  },
  {
    "timestamp": 3.3,
    "latitude": 37.789958177189,
    "longitude": -122.400806552,
    "altitude": 10.1176290512,
    "roll": 359.982330322,
    "pitch": 0.00226510548964143,
    "yaw": 359.983215332031,
    "speed": 19.99484524164348
  },
  {
    "timestamp": 3.35,
    "latitude": 37.789958122198,
    "longitude": -122.400795198,
    "altitude": 10.1176462173,
    "roll": 359.982299805,
    "pitch": 0.00227254838682711,
    "yaw": 359.982940673828,
    "speed": 19.995468995394283
  },
  {
    "timestamp": 3.4,
    "latitude": 37.789958067210,
    "longitude": -122.400783846,
    "altitude": 10.1175470352,
    "roll": 359.982330322,
    "pitch": 0.00229224772192538,
    "yaw": 359.982666015625,
    "speed": 19.993851508270716
  },
  {
    "timestamp": 3.45,
    "latitude": 37.789958012219,
    "longitude": -122.400772493,
    "altitude": 10.1175289154,
    "roll": 359.982299805,
    "pitch": 0.00230890652164817,
    "yaw": 359.982391357422,
    "speed": 19.994540138011274
  },
  {
    "timestamp": 3.5,
    "latitude": 37.789957957224,
    "longitude": -122.400761139,
    "altitude": 10.1175498962,
    "roll": 359.982208252,
    "pitch": 0.00231484672985971,
    "yaw": 359.982116699219,
    "speed": 19.99532794580767
  },
  {
    "timestamp": 3.55,
    "latitude": 37.789957902226,
    "longitude": -122.400749785,
    "altitude": 10.1175870895,
    "roll": 359.982177734,
    "pitch": 0.00231113587506115,
    "yaw": 359.981872558594,
    "speed": 19.99604325500918
  },
  {
    "timestamp": 3.6,
    "latitude": 37.789957847225,
    "longitude": -122.40073843,
    "altitude": 10.1176271439,
    "roll": 359.982147217,
    "pitch": 0.0022966181859374,
    "yaw": 359.981597900391,
    "speed": 19.996674617560263
  },
  {
    "timestamp": 3.65,
    "latitude": 37.789957792222,
    "longitude": -122.400727076,
    "altitude": 10.1176662445,
    "roll": 359.982177734,
    "pitch": 0.00228655361570418,
    "yaw": 359.981323242188,
    "speed": 19.997225862447213
  },
  {
    "timestamp": 3.7,
    "latitude": 37.789957737215,
    "longitude": -122.400715721,
    "altitude": 10.1176996231,
    "roll": 359.982208252,
    "pitch": 0.00226253946311772,
    "yaw": 359.981048583984,
    "speed": 19.997706527301016
  },
  {
    "timestamp": 3.75,
    "latitude": 37.789957682207,
    "longitude": -122.400704365,
    "altitude": 10.117726326,
    "roll": 359.982269287,
    "pitch": 0.00225397362373769,
    "yaw": 359.980773925781,
    "speed": 19.998131882327776
  },
  {
    "timestamp": 3.8,
    "latitude": 37.789957627196,
    "longitude": -122.40069301,
    "altitude": 10.1177482605,
    "roll": 359.982330322,
    "pitch": 0.00224139168858528,
    "yaw": 359.980499267578,
    "speed": 19.998500020370336
  },
  {
    "timestamp": 3.85,
    "latitude": 37.789957572183,
    "longitude": -122.400681654,
    "altitude": 10.1177635193,
    "roll": 359.982391357,
    "pitch": 0.00222704815678298,
    "yaw": 359.980224609375,
    "speed": 19.998814754039056
  },
  {
    "timestamp": 3.9,
    "latitude": 37.789957517175,
    "longitude": -122.400670299,
    "altitude": 10.1176490784,
    "roll": 359.982543945,
    "pitch": 0.00224490719847381,
    "yaw": 359.97998046875,
    "speed": 19.996899738800995
  },
  {
    "timestamp": 3.95,
    "latitude": 37.789957462165,
    "longitude": -122.400658945,
    "altitude": 10.1176137924,
    "roll": 359.982543945,
    "pitch": 0.00226453295908868,
    "yaw": 359.979705810547,
    "speed": 19.997315599850594
  },
  {
    "timestamp": 4.0,
    "latitude": 37.789957407151,
    "longitude": -122.40064759,
    "altitude": 10.1176166534,
    "roll": 359.982513428,
    "pitch": 0.00227938196621835,
    "yaw": 359.979431152344,
    "speed": 19.99785926441077
  },
  {
    "timestamp": 4.05,
    "latitude": 37.789957352273,
    "longitude": -122.400636234,
    "altitude": 10.1176376343,
    "roll": 359.982452393,
    "pitch": 0.00228417618200183,
    "yaw": 359.979187011719,
    "speed": 19.998349508526218
  },
  {
    "timestamp": 4.1,
    "latitude": 37.789957297943,
    "longitude": -122.400624878,
    "altitude": 10.1176652908,
    "roll": 359.982452393,
    "pitch": 0.00227569113485515,
    "yaw": 359.978912353516,
    "speed": 19.998774886877484
  },
  {
    "timestamp": 4.15,
    "latitude": 37.789957243610,
    "longitude": -122.400613523,
    "altitude": 10.1176929474,
    "roll": 359.982452393,
    "pitch": 0.00226509454660118,
    "yaw": 359.978637695313,
    "speed": 19.999143034192922
  },
  {
    "timestamp": 4.2,
    "latitude": 37.789957189282,
    "longitude": -122.400602168,
    "altitude": 10.1175928116,
    "roll": 359.982543945,
    "pitch": 0.00227732583880425,
    "yaw": 359.978363037109,
    "speed": 19.99726995824648
  },
  {
    "timestamp": 4.25,
    "latitude": 37.789957134957,
    "longitude": -122.400590814,
    "altitude": 10.1174459457,
    "roll": 359.98260498,
    "pitch": 0.0023152781650424,
    "yaw": 359.978088378906,
    "speed": 19.995534306292747
  },
  {
    "timestamp": 4.3,
    "latitude": 37.789957080630,
    "longitude": -122.40057946,
    "altitude": 10.1174154282,
    "roll": 359.98248291,
    "pitch": 0.00235050567425787,
    "yaw": 359.977844238281,
    "speed": 19.99627443820035
  },
  {
    "timestamp": 4.35,
    "latitude": 37.789957026299,
    "longitude": -122.400568105,
    "altitude": 10.117442131,
    "roll": 359.98236084,
    "pitch": 0.00236308155581355,
    "yaw": 359.977569580078,
    "speed": 19.99711950233096
  },
  {
    "timestamp": 4.4,
    "latitude": 37.789956971972,
    "longitude": -122.400556751,
    "altitude": 10.1173677444,
    "roll": 359.982299805,
    "pitch": 0.00237932452000678,
    "yaw": 359.977294921875,
    "speed": 19.995685107191612
  },
  {
    "timestamp": 4.45,
    "latitude": 37.789956917641,
    "longitude": -122.400545397,
    "altitude": 10.1173820496,
    "roll": 359.982177734,
    "pitch": 0.00239856215193868,
    "yaw": 359.977020263672,
    "speed": 19.996520651574873
  },
  {
    "timestamp": 4.5,
    "latitude": 37.789956863312,
    "longitude": -122.400534044,
    "altitude": 10.1173095703,
    "roll": 359.982147217,
    "pitch": 0.00240716710686684,
    "yaw": 359.976745605469,
    "speed": 19.995229324889383
  },
  {
    "timestamp": 4.55,
    "latitude": 37.789956808980,
    "longitude": -122.400522689,
    "altitude": 10.1173315048,
    "roll": 359.982055664,
    "pitch": 0.00241197925060987,
    "yaw": 359.976470947266,
    "speed": 19.996194584461385
  },
  {
    "timestamp": 4.6,
    "latitude": 37.789956754644,
    "longitude": -122.400511335,
    "altitude": 10.1173915863,
    "roll": 359.981933594,
    "pitch": 0.00240230374038219,
    "yaw": 359.976196289063,
    "speed": 19.99721130381621
  },
  {
    "timestamp": 4.65,
    "latitude": 37.789956700310,
    "longitude": -122.400499981,
    "altitude": 10.1173400879,
    "roll": 359.981933594,
    "pitch": 0.00239455397240818,
    "yaw": 359.975921630859,
    "speed": 19.995914190502475
  },
  {
    "timestamp": 4.7,
    "latitude": 37.789956645973,
    "longitude": -122.400488626,
    "altitude": 10.1173677444,
    "roll": 359.981903076,
    "pitch": 0.00239040981978178,
    "yaw": 359.975646972656,
    "speed": 19.99686227746864
  },
  {
    "timestamp": 4.75,
    "latitude": 37.789956591638,
    "longitude": -122.400477273,
    "altitude": 10.1173019409,
    "roll": 359.981903076,
    "pitch": 0.00239842780865729,
    "yaw": 359.975372314453,
    "speed": 19.99566630327579
  },
  {
    "timestamp": 4.8,
    "latitude": 37.789956537299,
    "longitude": -122.400465918,
    "altitude": 10.1173286438,
    "roll": 359.981811523,
    "pitch": 0.00240119895897806,
    "yaw": 359.97509765625,
    "speed": 19.99671739982832
  },
  {
    "timestamp": 4.85,
    "latitude": 37.789956482955,
    "longitude": -122.400454563,
    "altitude": 10.1173915863,
    "roll": 359.981750488,
    "pitch": 0.00238885823637247,
    "yaw": 359.974822998047,
    "speed": 19.997798964368638
  },
  {
    "timestamp": 4.9,
    "latitude": 37.789956429296,
    "longitude": -122.400443208,
    "altitude": 10.1174659729,
    "roll": 359.981719971,
    "pitch": 0.00236097443848848,
    "yaw": 359.974548339844,
    "speed": 19.998746972912585
  },
  {
    "timestamp": 4.95,
    "latitude": 37.789956375633,
    "longitude": -122.400431852,
    "altitude": 10.1175384521,
    "roll": 359.981750488,
    "pitch": 0.00233252346515656,
    "yaw": 359.974273681641,
    "speed": 19.999544268791468
  },
  {
    "timestamp": 5.0,
    "latitude": 37.789956321972,
    "longitude": -122.400420497,
    "altitude": 10.1174764633,
    "roll": 359.981872559,
    "pitch": 0.00232315249741077,
    "yaw": 359.973999023438,
    "speed": 19.99802970224967
  },
  {
    "timestamp": 5.05,
    "latitude": 37.789956268316,
    "longitude": -122.400409142,
    "altitude": 10.1173591614,
    "roll": 359.981994629,
    "pitch": 0.00234956433996558,
    "yaw": 359.973724365234,
    "speed": 19.996585862924658
  },
  {
    "timestamp": 5.1,
    "latitude": 37.789956214656,
    "longitude": -122.400397788,
    "altitude": 10.1173524857,
    "roll": 359.981964111,
    "pitch": 0.00237329164519906,
    "yaw": 359.973449707031,
    "speed": 19.997575901996804
  },
  {
    "timestamp": 5.15,
    "latitude": 37.789956160991,
    "longitude": -122.400386432,
    "altitude": 10.117398262,
    "roll": 359.981872559,
    "pitch": 0.00237422715872526,
    "yaw": 359.973175048828,
    "speed": 19.99861552425624
  },
  {
    "timestamp": 5.2,
    "latitude": 37.789956107322,
    "longitude": -122.400375076,
    "altitude": 10.1174640656,
    "roll": 359.981842041,
    "pitch": 0.00235716160386801,
    "yaw": 359.972900390625,
    "speed": 19.99951396040015
  },
  {
    "timestamp": 5.25,
    "latitude": 37.789956053650,
    "longitude": -122.40036372,
    "altitude": 10.1175327301,
    "roll": 359.981842041,
    "pitch": 0.00232994090765715,
    "yaw": 359.972625732422,
    "speed": 20.000280754234854
  },
  {
    "timestamp": 5.3,
    "latitude": 37.789955999975,
    "longitude": -122.400352363,
    "altitude": 10.1175947189,
    "roll": 359.981872559,
    "pitch": 0.0023032205644995,
    "yaw": 359.972351074219,
    "speed": 20.00091592159934
  },
  {
    "timestamp": 5.35,
    "latitude": 37.789955946298,
    "longitude": -122.400341006,
    "altitude": 10.1176462173,
    "roll": 359.981964111,
    "pitch": 0.00227461545728147,
    "yaw": 359.972076416016,
    "speed": 20.001444275448648
  },
  {
    "timestamp": 5.4,
    "latitude": 37.789955892624,
    "longitude": -122.40032965,
    "altitude": 10.117562294,
    "roll": 359.982147217,
    "pitch": 0.00227690651081502,
    "yaw": 359.971801757813,
    "speed": 19.999681801528673
  },
  {
    "timestamp": 5.45,
    "latitude": 37.789955838948,
    "longitude": -122.400318293,
    "altitude": 10.1175498962,
    "roll": 359.982208252,
    "pitch": 0.00229195225983858,
    "yaw": 359.971527099609,
    "speed": 20.000200695871854
  },
  {
    "timestamp": 5.5,
    "latitude": 37.789955785269,
    "longitude": -122.400306936,
    "altitude": 10.1175718307,
    "roll": 359.982208252,
    "pitch": 0.00229026167653501,
    "yaw": 359.971252441406,
    "speed": 20.000801595972714
  },
  {
    "timestamp": 5.55,
    "latitude": 37.789955731587,
    "longitude": -122.400295579,
    "altitude": 10.117606163,
    "roll": 359.98223877,
    "pitch": 0.00228784885257483,
    "yaw": 359.970977783203,
    "speed": 20.001318554032075
  },
  {
    "timestamp": 5.6,
    "latitude": 37.789955677903,
    "longitude": -122.400284222,
    "altitude": 10.11764431,
    "roll": 359.982269287,
    "pitch": 0.00227135908789933,
    "yaw": 359.970703125,
    "speed": 20.001742031610263
  },
  {
    "timestamp": 5.65,
    "latitude": 37.789955624355,
    "longitude": -122.400272864,
    "altitude": 10.1176786423,
    "roll": 359.982330322,
    "pitch": 0.00226039462722838,
    "yaw": 359.970428466797,
    "speed": 20.002079669298713
  },
  {
    "timestamp": 5.7,
    "latitude": 37.789955571360,
    "longitude": -122.400261508,
    "altitude": 10.1175832748,
    "roll": 359.982452393,
    "pitch": 0.00227055652067065,
    "yaw": 359.970184326172,
    "speed": 20.000166542344466
  },
  {
    "timestamp": 5.75,
    "latitude": 37.789955518364,
    "longitude": -122.400250151,
    "altitude": 10.117562294,
    "roll": 359.98248291,
    "pitch": 0.0022855440620333,
    "yaw": 359.969909667969,
    "speed": 20.00055764171059
  },
  {
    "timestamp": 5.8,
    "latitude": 37.789955465365,
    "longitude": -122.400238794,
    "altitude": 10.1175785065,
    "roll": 359.982452393,
    "pitch": 0.00229357182979584,
    "yaw": 359.969635009766,
    "speed": 20.001049823120706
  },
  {
    "timestamp": 5.85,
    "latitude": 37.789955412363,
    "longitude": -122.400227437,
    "altitude": 10.1176109314,
    "roll": 359.982452393,
    "pitch": 0.00229317275807261,
    "yaw": 359.969360351563,
    "speed": 20.001471416959955
  },
  {
    "timestamp": 5.9,
    "latitude": 37.789955359360,
    "longitude": -122.40021608,
    "altitude": 10.1176452637,
    "roll": 359.982452393,
    "pitch": 0.00228287372738123,
    "yaw": 359.969116210938,
    "speed": 20.00181288621869
  },
  {
    "timestamp": 5.95,
    "latitude": 37.789955306355,
    "longitude": -122.400204722,
    "altitude": 10.1176786423,
    "roll": 359.98248291,
    "pitch": 0.00227211997844279,
    "yaw": 359.968841552734,
    "speed": 20.00207995507401
  },
  {
    "timestamp": 6.0,
    "latitude": 37.789971120626,
    "longitude": -122.400193364,
    "altitude": 10.1177072525,
    "roll": 359.982513428,
    "pitch": 0.00225184787996113,
    "yaw": 359.968566894531,
    "speed": 20.002291709157717
  },
  {
    "timestamp": 6.05,
    "latitude": 37.789990108351,
    "longitude": -122.400182007,
    "altitude": 10.1177310944,
    "roll": 359.982574463,
    "pitch": 0.00224795402027667,
    "yaw": 359.968292236328,
    "speed": 20.002450058437937
  },
  {
    "timestamp": 6.1,
    "latitude": 37.789990055341,
    "longitude": -122.400170649,
    "altitude": 10.1177501678,
    "roll": 359.982635498,
    "pitch": 0.00223951344378293,
    "yaw": 359.968048095703,
    "speed": 20.002558820064028
  },
  {
    "timestamp": 6.15,
    "latitude": 37.789990002336,
    "longitude": -122.400159292,
    "altitude": 10.1176395416,
    "roll": 359.982788086,
    "pitch": 0.00225848727859557,
    "yaw": 359.9677734375,
    "speed": 20.000447358917423
  },
  {
    "timestamp": 6.2,
    "latitude": 37.789989949329,
    "longitude": -122.400147935,
    "altitude": 10.117606163,
    "roll": 359.982788086,
    "pitch": 0.00228144880384207,
    "yaw": 359.967529296875,
    "speed": 20.000676323141658
  },
  {
    "timestamp": 6.25,
    "latitude": 37.789989896320,
    "longitude": -122.400136578,
    "altitude": 10.1176099777,
    "roll": 359.982727051,
    "pitch": 0.0022915608715266,
    "yaw": 359.967254638672,
    "speed": 20.001031180193525
  },
  {
    "timestamp": 6.3,
    "latitude": 37.789989843309,
    "longitude": -122.400125221,
    "altitude": 10.1176328659,
    "roll": 359.982696533,
    "pitch": 0.00229341792874038,
    "yaw": 359.966979980469,
    "speed": 20.001334519004907
  },
  {
    "timestamp": 6.35,
    "latitude": 37.789989790297,
    "longitude": -122.400113864,
    "altitude": 10.1176605225,
    "roll": 359.982666016,
    "pitch": 0.00229113316163421,
    "yaw": 359.966735839844,
    "speed": 20.00158444362864
  },
  {
    "timestamp": 6.4,
    "latitude": 37.789989737289,
    "longitude": -122.400102508,
    "altitude": 10.1175642014,
    "roll": 359.982757568,
    "pitch": 0.00230021099559963,
    "yaw": 359.966461181641,
    "speed": 19.999595032704118
  },
  {
    "timestamp": 6.45,
    "latitude": 37.789989684279,
    "longitude": -122.400091151,
    "altitude": 10.1175460815,
    "roll": 359.982727051,
    "pitch": 0.00231211213395,
    "yaw": 359.966186523438,
    "speed": 19.999927011283063
  },
  {
    "timestamp": 6.5,
    "latitude": 37.789989631816,
    "longitude": -122.400079795,
    "altitude": 10.1175642014,
    "roll": 359.982635498,
    "pitch": 0.00231424765661359,
    "yaw": 359.965942382813,
    "speed": 20.000371520024427
  },
  {
    "timestamp": 6.55,
    "latitude": 37.789989579496,
    "longitude": -122.400068439,
    "altitude": 10.1174736023,
    "roll": 359.982666016,
    "pitch": 0.00233938451856375,
    "yaw": 359.965667724609,
    "speed": 19.998576671108733
  },
  {
    "timestamp": 6.6,
    "latitude": 37.789989527179,
    "longitude": -122.400057085,
    "altitude": 10.1173419952,
    "roll": 359.982635498,
    "pitch": 0.00237708981148899,
    "yaw": 359.965393066406,
    "speed": 19.996892529353634
  },
  {
    "timestamp": 6.65,
    "latitude": 37.789989474866,
    "longitude": -122.400045731,
    "altitude": 10.1172056198,
    "roll": 359.982574463,
    "pitch": 0.00242323777638376,
    "yaw": 359.965148925781,
    "speed": 19.99548305521831
  },
  {
    "timestamp": 6.7,
    "latitude": 37.789989422555,
    "longitude": -122.400034378,
    "altitude": 10.1170816422,
    "roll": 359.982421875,
    "pitch": 0.00247634085826576,
    "yaw": 359.964874267578,
    "speed": 19.99435014961911
  },
  {
    "timestamp": 6.75,
    "latitude": 37.789989370246,
    "longitude": -122.400023026,
    "altitude": 10.1169776917,
    "roll": 359.982208252,
    "pitch": 0.00252237636595964,
    "yaw": 359.964599609375,
    "speed": 19.99344422783567
  },
  {
    "timestamp": 6.8,
    "latitude": 37.789989317937,
    "longitude": -122.400011674,
    "altitude": 10.1168937683,
    "roll": 359.981964111,
    "pitch": 0.00257128826342523,
    "yaw": 359.964324951172,
    "speed": 19.99274812369883
  },
  {
    "timestamp": 6.85,
    "latitude": 37.789989265624,
    "longitude": -122.400000321,
    "altitude": 10.1169548035,
    "roll": 359.981658936,
    "pitch": 0.00258542923256755,
    "yaw": 359.964050292969,
    "speed": 19.994402082002583
  },
  {
    "timestamp": 6.9,
    "latitude": 37.789989213304,
    "longitude": -122.399988967,
    "altitude": 10.1170768738,
    "roll": 359.981414795,
    "pitch": 0.00255335262045264,
    "yaw": 359.963745117188,
    "speed": 19.996027341145446
  },
  {
    "timestamp": 6.95,
    "latitude": 37.789989160980,
    "longitude": -122.399977612,
    "altitude": 10.1172142029,
    "roll": 359.981292725,
    "pitch": 0.00250799837522209,
    "yaw": 359.963470458984,
    "speed": 19.997438855809712
  },
  {
    "timestamp": 7.0,
    "latitude": 37.789989108650,
    "longitude": -122.399966257,
    "altitude": 10.1173448563,
    "roll": 359.981262207,
    "pitch": 0.00245027500204742,
    "yaw": 359.963195800781,
    "speed": 19.998638579999614
  },
  {
    "timestamp": 7.05,
    "latitude": 37.789989056316,
    "longitude": -122.399954901,
    "altitude": 10.1174573898,
    "roll": 359.981323242,
    "pitch": 0.00239869230426848,
    "yaw": 359.962890625,
    "speed": 19.999660900114428
  },
  {
    "timestamp": 7.1,
    "latitude": 37.789989003978,
    "longitude": -122.399943544,
    "altitude": 10.1175489426,
    "roll": 359.981414795,
    "pitch": 0.0023397624026984,
    "yaw": 359.962615966797,
    "speed": 20.000509669562263
  },
  {
    "timestamp": 7.15,
    "latitude": 37.789988951644,
    "longitude": -122.399932188,
    "altitude": 10.1174945831,
    "roll": 359.981628418,
    "pitch": 0.0023113121278584,
    "yaw": 359.962341308594,
    "speed": 19.999035142377497
  },
  {
    "timestamp": 7.2,
    "latitude": 37.789988899306,
    "longitude": -122.399920832,
    "altitude": 10.1175041199,
    "roll": 359.981750488,
    "pitch": 0.0023055556230247,
    "yaw": 359.962066650391,
    "speed": 19.999794391233014
  },
  {
    "timestamp": 7.25,
    "latitude": 37.789988846964,
    "longitude": -122.399909476,
    "altitude": 10.1175413132,
    "roll": 359.981811523,
    "pitch": 0.00229959702119231,
    "yaw": 359.961791992188,
    "speed": 20.000608932936796
  },
  {
    "timestamp": 7.3,
    "latitude": 37.789988795170,
    "longitude": -122.399898119,
    "altitude": 10.1175870895,
    "roll": 359.981872559,
    "pitch": 0.00228049186989665,
    "yaw": 359.961517333984,
    "speed": 20.001297553583523
  },
  {
    "timestamp": 7.35,
    "latitude": 37.789988743510,
    "longitude": -122.399886761,
    "altitude": 10.1176319122,
    "roll": 359.981933594,
    "pitch": 0.00226696976460516,
    "yaw": 359.961242675781,
    "speed": 20.00186791139159
  },
  {
    "timestamp": 7.4,
    "latitude": 37.789988691847,
    "longitude": -122.399875403,
    "altitude": 10.1176710129,
    "roll": 359.982025146,
    "pitch": 0.00224693724885583,
    "yaw": 359.960968017578,
    "speed": 20.002327633568214
  },
  {
    "timestamp": 7.45,
    "latitude": 37.789988640183,
    "longitude": -122.399864046,
    "altitude": 10.1177034378,
    "roll": 359.982147217,
    "pitch": 0.0022373185493052,
    "yaw": 359.960693359375,
    "speed": 20.002693893605056
  },
  {
    "timestamp": 7.5,
    "latitude": 37.789988588522,
    "longitude": -122.399852689,
    "altitude": 10.117603302,
    "roll": 359.982330322,
    "pitch": 0.0022485142108053,
    "yaw": 359.960418701172,
    "speed": 20.000790324878086
  },
  {
    "timestamp": 7.55,
    "latitude": 37.789988536866,
    "longitude": -122.399841333,
    "altitude": 10.1174545288,
    "roll": 359.982452393,
    "pitch": 0.00228825118392706,
    "yaw": 359.960144042969,
    "speed": 19.999005113216075
  },
  {
    "timestamp": 7.6,
    "latitude": 37.789988485214,
    "longitude": -122.399829978,
    "altitude": 10.1172981262,
    "roll": 359.982452393,
    "pitch": 0.00234563183039427,
    "yaw": 359.959899902344,
    "speed": 19.997494559945128
  },
  {
    "timestamp": 7.65,
    "latitude": 37.789988433558,
    "longitude": -122.399818623,
    "altitude": 10.1172790527,
    "roll": 359.982299805,
    "pitch": 0.00238940073177218,
    "yaw": 359.959625244141,
    "speed": 19.998431201513785
  },
  {
    "timestamp": 7.7,
    "latitude": 37.789988381898,
    "longitude": -122.399807267,
    "altitude": 10.1173257828,
    "roll": 359.982147217,
    "pitch": 0.00240586930885911,
    "yaw": 359.959350585938,
    "speed": 19.9994212800657
  },
  {
    "timestamp": 7.75,
    "latitude": 37.789988330234,
    "longitude": -122.39979591,
    "altitude": 10.1174001694,
    "roll": 359.982025146,
    "pitch": 0.00239031342789531,
    "yaw": 359.959075927734,
    "speed": 20.000285419941413
  },
  {
    "timestamp": 7.8,
    "latitude": 37.789988278567,
    "longitude": -122.399784554,
    "altitude": 10.1174783707,
    "roll": 359.981994629,
    "pitch": 0.00236720219254494,
    "yaw": 359.958801269531,
    "speed": 20.00100646282777
  },
  {
    "timestamp": 7.85,
    "latitude": 37.789988226897,
    "longitude": -122.399773196,
    "altitude": 10.1175508499,
    "roll": 359.981994629,
    "pitch": 0.00233327387832105,
    "yaw": 359.958526611328,
    "speed": 20.001597781186465
  },
  {
    "timestamp": 7.9,
    "latitude": 37.789988175225,
    "longitude": -122.399761839,
    "altitude": 10.1176137924,
    "roll": 359.982055664,
    "pitch": 0.00230844947509468,
    "yaw": 359.958251953125,
    "speed": 20.002084189481305
  },
  {
    "timestamp": 7.95,
    "latitude": 37.789988123550,
    "longitude": -122.399750481,
    "altitude": 10.1176643372,
    "roll": 359.982147217,
    "pitch": 0.00228154635988176,
    "yaw": 359.957977294922,
    "speed": 20.002465695485903
  },
  {
    "timestamp": 8.0,
    "latitude": 37.789988071873,
    "longitude": -122.399739123,
    "altitude": 10.1177024841,
    "roll": 359.982269287,
    "pitch": 0.00226069381460547,
    "yaw": 359.957702636719,
    "speed": 20.00277091936438
  },
  {
    "timestamp": 8.05,
    "latitude": 37.789988020200,
    "longitude": -122.399727766,
    "altitude": 10.117606163,
    "roll": 359.982421875,
    "pitch": 0.0022625932469964,
    "yaw": 359.957458496094,
    "speed": 20.00082347859325
  },
  {
    "timestamp": 8.1,
    "latitude": 37.789987969082,
    "longitude": -122.39971641,
    "altitude": 10.1174573898,
    "roll": 359.982543945,
    "pitch": 0.00229711225256324,
    "yaw": 359.957183837891,
    "speed": 19.998992494224826
  },
  {
    "timestamp": 8.15,
    "latitude": 37.789987918106,
    "longitude": -122.399705056,
    "altitude": 10.1173009872,
    "roll": 359.982543945,
    "pitch": 0.00235476298257709,
    "yaw": 359.956909179688,
    "speed": 19.99745333255886
  },
  {
    "timestamp": 8.2,
    "latitude": 37.789987867125,
    "longitude": -122.3996937,
    "altitude": 10.1172819138,
    "roll": 359.982391357,
    "pitch": 0.00239433464594185,
    "yaw": 359.956634521484,
    "speed": 19.99836518184796
  },
  {
    "timestamp": 8.25,
    "latitude": 37.789987816141,
    "longitude": -122.399682344,
    "altitude": 10.1173276901,
    "roll": 359.982208252,
    "pitch": 0.00240939576178789,
    "yaw": 359.956359863281,
    "speed": 19.999328564262015
  },
  {
    "timestamp": 8.3,
    "latitude": 37.789987765154,
    "longitude": -122.399670988,
    "altitude": 10.117401123,
    "roll": 359.982086182,
    "pitch": 0.0023988289758563,
    "yaw": 359.956115722656,
    "speed": 20.000166008001734
  },
  {
    "timestamp": 8.35,
    "latitude": 37.789987714162,
    "longitude": -122.399659631,
    "altitude": 10.1174793243,
    "roll": 359.982025146,
    "pitch": 0.00237702787853777,
    "yaw": 359.955841064453,
    "speed": 20.000866074504707
  },
  {
    "timestamp": 8.4,
    "latitude": 37.789987663168,
    "longitude": -122.399648274,
    "altitude": 10.1175527573,
    "roll": 359.982055664,
    "pitch": 0.00234598689712584,
    "yaw": 359.95556640625,
    "speed": 20.001444043539596
  },
  {
    "timestamp": 8.45,
    "latitude": 37.789987612172,
    "longitude": -122.399636917,
    "altitude": 10.1176137924,
    "roll": 359.982116699,
    "pitch": 0.00230577378533781,
    "yaw": 359.955291748047,
    "speed": 20.00191901310635
  },
  {
    "timestamp": 8.5,
    "latitude": 37.789987561173,
    "longitude": -122.399625559,
    "altitude": 10.1176652908,
    "roll": 359.982177734,
    "pitch": 0.00228631100617349,
    "yaw": 359.955017089844,
    "speed": 20.002298616328677
  },
  {
    "timestamp": 8.55,
    "latitude": 37.789987510172,
    "longitude": -122.399614201,
    "altitude": 10.1177034378,
    "roll": 359.982299805,
    "pitch": 0.00225589447654784,
    "yaw": 359.954742431641,
    "speed": 20.002592399776802
  },
  {
    "timestamp": 8.6,
    "latitude": 37.789987459169,
    "longitude": -122.399602843,
    "altitude": 10.1177310944,
    "roll": 359.982391357,
    "pitch": 0.00223811133764684,
    "yaw": 359.954467773438,
    "speed": 20.002823242887356
  },
  {
    "timestamp": 8.65,
    "latitude": 37.789987408165,
    "longitude": -122.399591485,
    "altitude": 10.1177530289,
    "roll": 359.98248291,
    "pitch": 0.00222805724479258,
    "yaw": 359.954223632813,
    "speed": 20.002991153771895
  },
  {
    "timestamp": 8.7,
    "latitude": 37.789987357159,
    "longitude": -122.399580127,
    "altitude": 10.117767334,
    "roll": 359.982574463,
    "pitch": 0.00222179992124438,
    "yaw": 359.953948974609,
    "speed": 20.003105656970106
  },
  {
    "timestamp": 8.75,
    "latitude": 37.789987306152,
    "longitude": -122.399568768,
    "altitude": 10.1177778244,
    "roll": 359.982666016,
    "pitch": 0.00222219713032246,
    "yaw": 359.953674316406,
    "speed": 20.003180108504854
  },
  {
    "timestamp": 8.8,
    "latitude": 37.789987255143,
    "longitude": -122.39955741,
    "altitude": 10.1177854538,
    "roll": 359.982727051,
    "pitch": 0.00222051865421236,
    "yaw": 359.953430175781,
    "speed": 20.00322023405055
  },
  {
    "timestamp": 8.85,
    "latitude": 37.789987204134,
    "longitude": -122.399546052,
    "altitude": 10.1177892685,
    "roll": 359.982788086,
    "pitch": 0.00222124718129635,
    "yaw": 359.953155517578,
    "speed": 20.003231749875305
  },
  {
    "timestamp": 8.9,
    "latitude": 37.789987153535,
    "longitude": -122.399534693,
    "altitude": 10.1177921295,
    "roll": 359.982849121,
    "pitch": 0.00220920611172915,
    "yaw": 359.952880859375,
    "speed": 20.003216562479086
  },
  {
    "timestamp": 8.95,
    "latitude": 37.789987103211,
    "longitude": -122.399523335,
    "altitude": 10.1177940369,
    "roll": 359.982910156,
    "pitch": 0.00221220147795975,
    "yaw": 359.95263671875,
    "speed": 20.003180397246446
  },
  {
    "timestamp": 9.0,
    "latitude": 37.789987052886,
    "longitude": -122.399511977,
    "altitude": 10.1177959442,
    "roll": 359.982940674,
    "pitch": 0.00221756170503795,
    "yaw": 359.952362060547,
    "speed": 20.00312897030958
  },
  {
    "timestamp": 9.05,
    "latitude": 37.789987002560,
    "longitude": -122.399500619,
    "altitude": 10.1177959442,
    "roll": 359.982971191,
    "pitch": 0.00222146604210138,
    "yaw": 359.952117919922,
    "speed": 20.003066102996314
  },
  {
    "timestamp": 9.1,
    "latitude": 37.789986952240,
    "longitude": -122.399489262,
    "altitude": 10.1176710129,
    "roll": 359.983093262,
    "pitch": 0.00223860167898238,
    "yaw": 359.951843261719,
    "speed": 20.000805922234747
  },
  {
    "timestamp": 9.15,
    "latitude": 37.789986901918,
    "longitude": -122.399477905,
    "altitude": 10.1176271439,
    "roll": 359.983032227,
    "pitch": 0.00226616091094911,
    "yaw": 359.951599121094,
    "speed": 20.000901386106875
  },
  {
    "timestamp": 9.2,
    "latitude": 37.789986851595,
    "longitude": -122.399466548,
    "altitude": 10.1176233292,
    "roll": 359.982971191,
    "pitch": 0.00228307861834764,
    "yaw": 359.951324462891,
    "speed": 20.001147545888422
  },
  {
    "timestamp": 9.25,
    "latitude": 37.789986801270,
    "longitude": -122.399455191,
    "altitude": 10.117641449,
    "roll": 359.982910156,
    "pitch": 0.00229295808821917,
    "yaw": 359.951080322266,
    "speed": 20.001359362999747
  },
  {
    "timestamp": 9.3,
    "latitude": 37.789986750943,
    "longitude": -122.399443833,
    "altitude": 10.1176671982,
    "roll": 359.982849121,
    "pitch": 0.00229064980521798,
    "yaw": 359.950805664063,
    "speed": 20.001533013991125
  },
  {
    "timestamp": 9.35,
    "latitude": 37.789986700614,
    "longitude": -122.399432476,
    "altitude": 10.1176929474,
    "roll": 359.982818604,
    "pitch": 0.00228314311243594,
    "yaw": 359.950561523438,
    "speed": 20.001664698622935
  },
  {
    "timestamp": 9.4,
    "latitude": 37.789986650285,
    "longitude": -122.399421118,
    "altitude": 10.1177167892,
    "roll": 359.982818604,
    "pitch": 0.0022710224147886,
    "yaw": 359.950286865234,
    "speed": 20.00176776409029
  },
  {
    "timestamp": 9.45,
    "latitude": 37.789986599954,
    "longitude": -122.399409761,
    "altitude": 10.1177377701,
    "roll": 359.982849121,
    "pitch": 0.00226512574590743,
    "yaw": 359.950042724609,
    "speed": 20.001834595153
  },
  {
    "timestamp": 9.5,
    "latitude": 37.789986549621,
    "longitude": -122.399398403,
    "altitude": 10.1177549362,
    "roll": 359.982879639,
    "pitch": 0.0022502806968987,
    "yaw": 359.949768066406,
    "speed": 20.00188043996686
  },
  {
    "timestamp": 9.55,
    "latitude": 37.789986499288,
    "longitude": -122.399387046,
    "altitude": 10.117767334,
    "roll": 359.982879639,
    "pitch": 0.00224536680616438,
    "yaw": 359.949523925781,
    "speed": 20.001903401109065
  },
  {
    "timestamp": 9.6,
    "latitude": 37.789986448953,
    "longitude": -122.399375688,
    "altitude": 10.1177759171,
    "roll": 359.982910156,
    "pitch": 0.00223907828330994,
    "yaw": 359.949249267578,
    "speed": 20.001905380935252
  },
  {
    "timestamp": 9.65,
    "latitude": 37.789986398617,
    "longitude": -122.399364331,
    "altitude": 10.1177835464,
    "roll": 359.982940674,
    "pitch": 0.00223272456787527,
    "yaw": 359.949005126953,
    "speed": 20.001892106128604
  },
  {
    "timestamp": 9.7,
    "latitude": 37.789986348281,
    "longitude": -122.399352973,
    "altitude": 10.1177883148,
    "roll": 359.982971191,
    "pitch": 0.0022344458848238,
    "yaw": 359.94873046875,
    "speed": 20.001871201377558
  },
  {
    "timestamp": 9.75,
    "latitude": 37.789986298493,
    "longitude": -122.399341616,
    "altitude": 10.1177911758,
    "roll": 359.983001709,
    "pitch": 0.00223176018334925,
    "yaw": 359.948486328125,
    "speed": 20.001835042067338
  },
  {
    "timestamp": 9.8,
    "latitude": 37.789986248842,
    "longitude": -122.399330258,
    "altitude": 10.1177930832,
    "roll": 359.983001709,
    "pitch": 0.00223211525008082,
    "yaw": 359.948211669922,
    "speed": 20.00179315803253
  },
  {
    "timestamp": 9.85,
    "latitude": 37.789986199190,
    "longitude": -122.399318901,
    "altitude": 10.1177949905,
    "roll": 359.983032227,
    "pitch": 0.0022289277985692,
    "yaw": 359.947967529297,
    "speed": 20.001745555384414
  },
  {
    "timestamp": 9.9,
    "latitude": 37.789986149537,
    "longitude": -122.399307543,
    "altitude": 10.1177968979,
    "roll": 359.983032227,
    "pitch": 0.00223221210762858,
    "yaw": 359.947692871094,
    "speed": 20.001696041778846
  },
  {
    "timestamp": 9.95,
    "latitude": 37.789986099883,
    "longitude": -122.399296186,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00222878041677177,
    "yaw": 359.947448730469,
    "speed": 20.001650347272363
  },
  {
    "timestamp": 10.0,
    "latitude": 37.789986050228,
    "longitude": -122.399284828,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00222932756878436,
    "yaw": 359.947174072266,
    "speed": 20.001593206488508
  },
  {
    "timestamp": 10.05,
    "latitude": 37.789986000572,
    "longitude": -122.399273471,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00223075482062995,
    "yaw": 359.946929931641,
    "speed": 20.00153797703571
  },
  {
    "timestamp": 10.1,
    "latitude": 37.789985950915,
    "longitude": -122.399262114,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00222972803749144,
    "yaw": 359.946655273438,
    "speed": 20.001482744053057
  },
  {
    "timestamp": 10.15,
    "latitude": 37.789985901257,
    "longitude": -122.399250756,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223257206380367,
    "yaw": 359.946411132813,
    "speed": 20.0014237006983
  },
  {
    "timestamp": 10.2,
    "latitude": 37.789985851599,
    "longitude": -122.399239399,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223213690333068,
    "yaw": 359.946136474609,
    "speed": 20.00136274547202
  },
  {
    "timestamp": 10.25,
    "latitude": 37.789985801939,
    "longitude": -122.399228042,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223233038559556,
    "yaw": 359.945892333984,
    "speed": 20.001299887566788
  },
  {
    "timestamp": 10.3,
    "latitude": 37.789985752279,
    "longitude": -122.399216685,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00222982303239405,
    "yaw": 359.945617675781,
    "speed": 20.001242749162667
  },
  {
    "timestamp": 10.35,
    "latitude": 37.789985702617,
    "longitude": -122.399205328,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.0022344512399286,
    "yaw": 359.945373535156,
    "speed": 20.001189428861483
  },
  {
    "timestamp": 10.4,
    "latitude": 37.789985652955,
    "longitude": -122.39919397,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.0022326682228595,
    "yaw": 359.945129394531,
    "speed": 20.001132294107286
  },
  {
    "timestamp": 10.45,
    "latitude": 37.789985603292,
    "longitude": -122.399182613,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223428593017161,
    "yaw": 359.944854736328,
    "speed": 20.001077063742773
  },
  {
    "timestamp": 10.5,
    "latitude": 37.789985553627,
    "longitude": -122.399171256,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223252805881202,
    "yaw": 359.944610595703,
    "speed": 20.001021837308926
  },
  {
    "timestamp": 10.55,
    "latitude": 37.789985503962,
    "longitude": -122.399159899,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223416928201914,
    "yaw": 359.9443359375,
    "speed": 20.000972329689013
  },
  {
    "timestamp": 10.6,
    "latitude": 37.789985454846,
    "longitude": -122.399148542,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223253876902163,
    "yaw": 359.944091796875,
    "speed": 20.000922826291156
  },
  {
    "timestamp": 10.65,
    "latitude": 37.789985405867,
    "longitude": -122.399137185,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223451689817011,
    "yaw": 359.943817138672,
    "speed": 20.00087331962157
  },
  {
    "timestamp": 10.7,
    "latitude": 37.789985356886,
    "longitude": -122.399125828,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223346031270921,
    "yaw": 359.943572998047,
    "speed": 20.00082572408819
  },
  {
    "timestamp": 10.75,
    "latitude": 37.789985307905,
    "longitude": -122.399114471,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223269034177065,
    "yaw": 359.943298339844,
    "speed": 20.000781940396447
  },
  {
    "timestamp": 10.8,
    "latitude": 37.789985258922,
    "longitude": -122.399103114,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223556067794561,
    "yaw": 359.943054199219,
    "speed": 20.000740067679505
  },
  {
    "timestamp": 10.85,
    "latitude": 37.789985209939,
    "longitude": -122.399091757,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223547476343811,
    "yaw": 359.942779541016,
    "speed": 20.000700099345718
  },
  {
    "timestamp": 10.9,
    "latitude": 37.789985160955,
    "longitude": -122.399080401,
    "altitude": 10.1177968979,
    "roll": 359.983093262,
    "pitch": 0.00223225657828152,
    "yaw": 359.942535400391,
    "speed": 20.000662043625432
  },
  {
    "timestamp": 10.95,
    "latitude": 37.789985111970,
    "longitude": -122.399069044,
    "altitude": 10.1177968979,
    "roll": 359.983093262,
    "pitch": 0.00223602331243455,
    "yaw": 359.942291259766,
    "speed": 20.000622080048196
  },
  {
    "timestamp": 11.0,
    "latitude": 37.789985062983,
    "longitude": -122.399057687,
    "altitude": 10.1177968979,
    "roll": 359.983093262,
    "pitch": 0.00223650084808469,
    "yaw": 359.942016601563,
    "speed": 20.000584020296376
  },
  {
    "timestamp": 11.05,
    "latitude": 37.789985013996,
    "longitude": -122.39904633,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223638094030321,
    "yaw": 359.941772460938,
    "speed": 20.00054596486567
  },
  {
    "timestamp": 11.1,
    "latitude": 37.789984965008,
    "longitude": -122.399034973,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223557790741324,
    "yaw": 359.941497802734,
    "speed": 20.000509812135263
  },
  {
    "timestamp": 11.15,
    "latitude": 37.789984916025,
    "longitude": -122.399023618,
    "altitude": 10.1176729202,
    "roll": 359.983123779,
    "pitch": 0.00225197849795222,
    "yaw": 359.941253662109,
    "speed": 19.998285890840762
  },
  {
    "timestamp": 11.2,
    "latitude": 37.789984867047,
    "longitude": -122.399012264,
    "altitude": 10.1175031662,
    "roll": 359.983154297,
    "pitch": 0.00230385945178568,
    "yaw": 359.940979003906,
    "speed": 19.996252758595663
  },
  {
    "timestamp": 11.25,
    "latitude": 37.789984818074,
    "longitude": -122.39900091,
    "altitude": 10.1173305511,
    "roll": 359.983062744,
    "pitch": 0.00237184087745845,
    "yaw": 359.940734863281,
    "speed": 19.99455530680235
  },
  {
    "timestamp": 11.3,
    "latitude": 37.789984769097,
    "longitude": -122.398989557,
    "altitude": 10.1173019409,
    "roll": 359.982818604,
    "pitch": 0.00241863704286516,
    "yaw": 359.940460205078,
    "speed": 19.995366071362962
  },
  {
    "timestamp": 11.35,
    "latitude": 37.789984720117,
    "longitude": -122.398978202,
    "altitude": 10.1173410416,
    "roll": 359.982543945,
    "pitch": 0.00243473658338189,
    "yaw": 359.940185546875,
    "speed": 19.99626271476258
  },
  {
    "timestamp": 11.4,
    "latitude": 37.789984671133,
    "longitude": -122.398966848,
    "altitude": 10.1174097061,
    "roll": 359.98236084,
    "pitch": 0.00242731487378478,
    "yaw": 359.939910888672,
    "speed": 19.99706012710748
  },
  {
    "timestamp": 11.45,
    "latitude": 37.789984622833,
    "longitude": -122.398955493,
    "altitude": 10.1174850464,
    "roll": 359.98223877,
    "pitch": 0.00239316001534462,
    "yaw": 359.939666748047,
    "speed": 19.997756409163227
  },
  {
    "timestamp": 11.5,
    "latitude": 37.789984574531,
    "longitude": -122.398944137,
    "altitude": 10.117556572,
    "roll": 359.982208252,
    "pitch": 0.00236164266243577,
    "yaw": 359.939392089844,
    "speed": 19.998359203866958
  },
  {
    "timestamp": 11.55,
    "latitude": 37.789984526226,
    "longitude": -122.398932782,
    "altitude": 10.1176176071,
    "roll": 359.982208252,
    "pitch": 0.0023259453009814,
    "yaw": 359.939117431641,
    "speed": 19.998870436850424
  },
  {
    "timestamp": 11.6,
    "latitude": 37.789984477918,
    "longitude": -122.398921426,
    "altitude": 10.1176671982,
    "roll": 359.982269287,
    "pitch": 0.00229865685105324,
    "yaw": 359.938842773438,
    "speed": 19.999297751757247
  },
  {
    "timestamp": 11.65,
    "latitude": 37.789984429609,
    "longitude": -122.398910069,
    "altitude": 10.1177043915,
    "roll": 359.982330322,
    "pitch": 0.0022755665704608,
    "yaw": 359.938568115234,
    "speed": 19.99966976395208
  },
  {
    "timestamp": 11.7,
    "latitude": 37.789984381297,
    "longitude": -122.398898713,
    "altitude": 10.1177330017,
    "roll": 359.982391357,
    "pitch": 0.00225544068962336,
    "yaw": 359.938293457031,
    "speed": 19.999978832918806
  },
  {
    "timestamp": 11.75,
    "latitude": 37.789984332983,
    "longitude": -122.398887356,
    "altitude": 10.1177549362,
    "roll": 359.982452393,
    "pitch": 0.00224031764082611,
    "yaw": 359.938049316406,
    "speed": 20.00024213892229
  },
  {
    "timestamp": 11.8,
    "latitude": 37.789984284668,
    "longitude": -122.398876,
    "altitude": 10.1177692413,
    "roll": 359.982543945,
    "pitch": 0.00222994270734489,
    "yaw": 359.937774658203,
    "speed": 20.000457756893155
  },
  {
    "timestamp": 11.85,
    "latitude": 37.789984236350,
    "longitude": -122.398864643,
    "altitude": 10.1177806854,
    "roll": 359.98260498,
    "pitch": 0.00222775992006063,
    "yaw": 359.9375,
    "speed": 20.000637137918275
  },
  {
    "timestamp": 11.9,
    "latitude": 37.789984188032,
    "longitude": -122.398853286,
    "altitude": 10.1177873611,
    "roll": 359.982666016,
    "pitch": 0.00220926431939006,
    "yaw": 359.937255859375,
    "speed": 20.000776472569434
  },
  {
    "timestamp": 11.95,
    "latitude": 37.789984139712,
    "longitude": -122.398841929,
    "altitude": 10.1177911758,
    "roll": 359.982727051,
    "pitch": 0.00221366086043417,
    "yaw": 359.936981201172,
    "speed": 20.000891011986518
  },
  {
    "timestamp": 12.0,
    "latitude": 37.789984091390,
    "longitude": -122.398830572,
    "altitude": 10.1177940369,
    "roll": 359.982757568,
    "pitch": 0.00221553677693009,
    "yaw": 359.936706542969,
    "speed": 20.00097503259773
  },
  {
    "timestamp": 12.05,
    "latitude": 37.789984043067,
    "longitude": -122.398819215,
    "altitude": 10.1177959442,
    "roll": 359.982818604,
    "pitch": 0.0022086575627327,
    "yaw": 359.936462402344,
    "speed": 20.001038076872064
  },
  {
    "timestamp": 12.1,
    "latitude": 37.789983994744,
    "longitude": -122.398807858,
    "altitude": 10.1177978516,
    "roll": 359.982849121,
    "pitch": 0.00221044546924531,
    "yaw": 359.936187744141,
    "speed": 20.00108395121187
  },
  {
    "timestamp": 12.15,
    "latitude": 37.789983946418,
    "longitude": -122.398796501,
    "altitude": 10.1177978516,
    "roll": 359.982879639,
    "pitch": 0.00221742386929691,
    "yaw": 359.935943603516,
    "speed": 20.001114571056686
  },
  {
    "timestamp": 12.2,
    "latitude": 37.789983898092,
    "longitude": -122.398785144,
    "altitude": 10.1177978516,
    "roll": 359.982910156,
    "pitch": 0.00222268328070641,
    "yaw": 359.935668945313,
    "speed": 20.00112992895242
  },
  {
    "timestamp": 12.25,
    "latitude": 37.789983850177,
    "longitude": -122.398773787,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.0022226138971746,
    "yaw": 359.935424804688,
    "speed": 20.001137661767444
  },
  {
    "timestamp": 12.3,
    "latitude": 37.789983802536,
    "longitude": -122.398762429,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.00222027860581875,
    "yaw": 359.935150146484,
    "speed": 20.0011396686152
  },
  {
    "timestamp": 12.35,
    "latitude": 37.789983754893,
    "longitude": -122.398751072,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.0022227056324482,
    "yaw": 359.934906005859,
    "speed": 20.001128328455646
  },
  {
    "timestamp": 12.4,
    "latitude": 37.789983707250,
    "longitude": -122.398739715,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222329492680728,
    "yaw": 359.934631347656,
    "speed": 20.001107447302843
  },
  {
    "timestamp": 12.45,
    "latitude": 37.789983659606,
    "longitude": -122.398728358,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222819414921105,
    "yaw": 359.934387207031,
    "speed": 20.00107703386006
  },
  {
    "timestamp": 12.5,
    "latitude": 37.789983611961,
    "longitude": -122.398717001,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222740601748228,
    "yaw": 359.934112548828,
    "speed": 20.001046616667185
  },
  {
    "timestamp": 12.55,
    "latitude": 37.789983564315,
    "longitude": -122.398705644,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222426978871226,
    "yaw": 359.933868408203,
    "speed": 20.001018111377554
  },
  {
    "timestamp": 12.6,
    "latitude": 37.789983516667,
    "longitude": -122.398694287,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223220558837056,
    "yaw": 359.93359375,
    "speed": 20.00099150904176
  },
  {
    "timestamp": 12.65,
    "latitude": 37.789983469019,
    "longitude": -122.39868293,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223063421435654,
    "yaw": 359.933349609375,
    "speed": 20.00095728198265
  },
  {
    "timestamp": 12.7,
    "latitude": 37.789983421370,
    "longitude": -122.398671573,
    "altitude": 10.1177968979,
    "roll": 359.983032227,
    "pitch": 0.00222963094711304,
    "yaw": 359.933074951172,
    "speed": 20.000921145087386
  },
  {
    "timestamp": 12.75,
    "latitude": 37.789983373720,
    "longitude": -122.398660216,
    "altitude": 10.1177968979,
    "roll": 359.983032227,
    "pitch": 0.00223269034177065,
    "yaw": 359.932830810547,
    "speed": 20.00089073388436
  },
  {
    "timestamp": 12.8,
    "latitude": 37.789983326069,
    "longitude": -122.398648859,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00223281770013273,
    "yaw": 359.932556152344,
    "speed": 20.000856503881458
  },
  {
    "timestamp": 12.85,
    "latitude": 37.789983278417,
    "longitude": -122.398637502,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223010359331965,
    "yaw": 359.932312011719,
    "speed": 20.00082609338223
  },
  {
    "timestamp": 12.9,
    "latitude": 37.789983230764,
    "longitude": -122.398626145,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223103747703135,
    "yaw": 359.932037353516,
    "speed": 20.000789955785624
  },
  {
    "timestamp": 12.95,
    "latitude": 37.789983183109,
    "longitude": -122.398614788,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223221001215279,
    "yaw": 359.931793212891,
    "speed": 20.000751916185678
  },
  {
    "timestamp": 13.0,
    "latitude": 37.789983135461,
    "longitude": -122.398603432,
    "altitude": 10.1176729202,
    "roll": 359.983123779,
    "pitch": 0.00225414498709142,
    "yaw": 359.931518554688,
    "speed": 19.998524191204403
  },
  {
    "timestamp": 13.05,
    "latitude": 37.789983087811,
    "longitude": -122.398592077,
    "altitude": 10.1176280975,
    "roll": 359.983062744,
    "pitch": 0.00228103692643344,
    "yaw": 359.931274414063,
    "speed": 19.998680721517452
  },
  {
    "timestamp": 13.1,
    "latitude": 37.789983040571,
    "longitude": -122.398580721,
    "altitude": 10.1176252365,
    "roll": 359.982971191,
    "pitch": 0.00229854043573141,
    "yaw": 359.930999755859,
    "speed": 19.998991762976708
  },
  {
    "timestamp": 13.15,
    "latitude": 37.789982993605,
    "longitude": -122.398569365,
    "altitude": 10.1176424026,
    "roll": 359.982879639,
    "pitch": 0.00230004079639912,
    "yaw": 359.930755615234,
    "speed": 19.99927609143151
  },
  {
    "timestamp": 13.2,
    "latitude": 37.789982946637,
    "longitude": -122.398558009,
    "altitude": 10.1176681519,
    "roll": 359.982818604,
    "pitch": 0.00229158368892968,
    "yaw": 359.930480957031,
    "speed": 19.999522252985603
  },
  {
    "timestamp": 13.25,
    "latitude": 37.789982899668,
    "longitude": -122.398546652,
    "altitude": 10.1176948547,
    "roll": 359.982788086,
    "pitch": 0.00228723417967558,
    "yaw": 359.930236816406,
    "speed": 19.999737892585923
  },
  {
    "timestamp": 13.3,
    "latitude": 37.789982852696,
    "longitude": -122.398535296,
    "altitude": 10.1177186966,
    "roll": 359.982788086,
    "pitch": 0.00227309949696064,
    "yaw": 359.929962158203,
    "speed": 19.99991347019116
  },
  {
    "timestamp": 13.35,
    "latitude": 37.789982805729,
    "longitude": -122.398523941,
    "altitude": 10.1176137924,
    "roll": 359.982849121,
    "pitch": 0.00228499481454492,
    "yaw": 359.9296875,
    "speed": 19.997872630922792
  },
  {
    "timestamp": 13.4,
    "latitude": 37.789982758768,
    "longitude": -122.398512587,
    "altitude": 10.1174612045,
    "roll": 359.982879639,
    "pitch": 0.00232336740009487,
    "yaw": 359.929443359375,
    "speed": 19.99599210316249
  },
  {
    "timestamp": 13.45,
    "latitude": 37.789982711803,
    "longitude": -122.398501232,
    "altitude": 10.1174259186,
    "roll": 359.982757568,
    "pitch": 0.00236295000649989,
    "yaw": 359.929168701172,
    "speed": 19.99661023294477
  },
  {
    "timestamp": 13.5,
    "latitude": 37.789982664835,
    "longitude": -122.398489877,
    "altitude": 10.1174497604,
    "roll": 359.982574463,
    "pitch": 0.0023738972377032,
    "yaw": 359.928924560547,
    "speed": 19.997337123383062
  },
  {
    "timestamp": 13.55,
    "latitude": 37.789982617864,
    "longitude": -122.398478522,
    "altitude": 10.1174993515,
    "roll": 359.982452393,
    "pitch": 0.0023706411011517,
    "yaw": 359.928649902344,
    "speed": 19.997987673057114
  },
  {
    "timestamp": 13.6,
    "latitude": 37.789982570890,
    "longitude": -122.398467167,
    "altitude": 10.117556572,
    "roll": 359.98236084,
    "pitch": 0.00235155737027526,
    "yaw": 359.928375244141,
    "speed": 19.998544733915228
  },
  {
    "timestamp": 13.65,
    "latitude": 37.789982523914,
    "longitude": -122.398455811,
    "altitude": 10.1176099777,
    "roll": 359.982330322,
    "pitch": 0.00232770619913936,
    "yaw": 359.928100585938,
    "speed": 19.999027395400553
  },
  {
    "timestamp": 13.7,
    "latitude": 37.789982476935,
    "longitude": -122.398444455,
    "altitude": 10.1176567078,
    "roll": 359.98236084,
    "pitch": 0.00230229622684419,
    "yaw": 359.927825927734,
    "speed": 19.99942994237591
  },
  {
    "timestamp": 13.75,
    "latitude": 37.789982429955,
    "longitude": -122.398433099,
    "altitude": 10.1176939011,
    "roll": 359.982391357,
    "pitch": 0.00227904715575278,
    "yaw": 359.927581787109,
    "speed": 19.999782903574022
  },
  {
    "timestamp": 13.8,
    "latitude": 37.789982382972,
    "longitude": -122.398421742,
    "altitude": 10.1177244186,
    "roll": 359.982452393,
    "pitch": 0.00226229894906282,
    "yaw": 359.927307128906,
    "speed": 20.0000729152055
  },
  {
    "timestamp": 13.85,
    "latitude": 37.789982335987,
    "longitude": -122.398410385,
    "altitude": 10.1177463531,
    "roll": 359.982513428,
    "pitch": 0.00225284323096275,
    "yaw": 359.927032470703,
    "speed": 20.00030571604535
  },
  {
    "timestamp": 13.9,
    "latitude": 37.789982289001,
    "longitude": -122.398399029,
    "altitude": 10.1177635193,
    "roll": 359.982574463,
    "pitch": 0.00224081170745194,
    "yaw": 359.9267578125,
    "speed": 20.000502279591267
  },
  {
    "timestamp": 13.95,
    "latitude": 37.789982242700,
    "longitude": -122.398387672,
    "altitude": 10.1177759171,
    "roll": 359.982635498,
    "pitch": 0.00222576316446066,
    "yaw": 359.926513671875,
    "speed": 20.000664517161233
  },
  {
    "timestamp": 14.0,
    "latitude": 37.789982196399,
    "longitude": -122.398376315,
    "altitude": 10.1177835464,
    "roll": 359.982696533,
    "pitch": 0.00222680834122002,
    "yaw": 359.926239013672,
    "speed": 20.000796234818925
  },
  {
    "timestamp": 14.05,
    "latitude": 37.789982150095,
    "longitude": -122.398364958,
    "altitude": 10.1177892685,
    "roll": 359.982727051,
    "pitch": 0.00221645087003708,
    "yaw": 359.925964355469,
    "speed": 20.000901252925672
  },
  {
    "timestamp": 14.1,
    "latitude": 37.789982103791,
    "longitude": -122.398353601,
    "altitude": 10.1177921295,
    "roll": 359.982788086,
    "pitch": 0.00221889070235193,
    "yaw": 359.925720214844,
    "speed": 20.00097766684151
  },
  {
    "timestamp": 14.15,
    "latitude": 37.789982057484,
    "longitude": -122.398342244,
    "altitude": 10.1177940369,
    "roll": 359.982818604,
    "pitch": 0.00221892702393234,
    "yaw": 359.925445556641,
    "speed": 20.001038817659172
  },
  {
    "timestamp": 14.2,
    "latitude": 37.789982011177,
    "longitude": -122.398330887,
    "altitude": 10.1177959442,
    "roll": 359.982849121,
    "pitch": 0.00221337238326669,
    "yaw": 359.925201416016,
    "speed": 20.001080898620266
  },
  {
    "timestamp": 14.25,
    "latitude": 37.789981964869,
    "longitude": -122.39831953,
    "altitude": 10.1177978516,
    "roll": 359.982879639,
    "pitch": 0.00221557286567986,
    "yaw": 359.924926757813,
    "speed": 20.00111534578646
  },
  {
    "timestamp": 14.3,
    "latitude": 37.789981918560,
    "longitude": -122.398308173,
    "altitude": 10.1177978516,
    "roll": 359.982910156,
    "pitch": 0.00221909210085869,
    "yaw": 359.924682617188,
    "speed": 20.00112881729406
  },
  {
    "timestamp": 14.35,
    "latitude": 37.789981872249,
    "longitude": -122.398296815,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.00222738808952272,
    "yaw": 359.924407958984,
    "speed": 20.001134655593976
  },
  {
    "timestamp": 14.4,
    "latitude": 37.789981825938,
    "longitude": -122.398285458,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222678948193789,
    "yaw": 359.924163818359,
    "speed": 20.00113096216267
  },
  {
    "timestamp": 14.45,
    "latitude": 37.789981779625,
    "longitude": -122.398274101,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222344836220145,
    "yaw": 359.923889160156,
    "speed": 20.00112154233745
  },
  {
    "timestamp": 14.5,
    "latitude": 37.789981733311,
    "longitude": -122.398262744,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222464581020176,
    "yaw": 359.923645019531,
    "speed": 20.001102590691083
  },
  {
    "timestamp": 14.55,
    "latitude": 37.789981686996,
    "longitude": -122.398251387,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00223012850619853,
    "yaw": 359.923370361328,
    "speed": 20.001079819587062
  },
  {
    "timestamp": 14.6,
    "latitude": 37.789981640680,
    "longitude": -122.39824003,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222636689431965,
    "yaw": 359.923126220703,
    "speed": 20.001051331772377
  },
  {
    "timestamp": 14.65,
    "latitude": 37.789981594363,
    "longitude": -122.398228673,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222669937647879,
    "yaw": 359.9228515625,
    "speed": 20.00102093158219
  },
  {
    "timestamp": 14.7,
    "latitude": 37.789981548045,
    "longitude": -122.398217316,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222462601959705,
    "yaw": 359.922607421875,
    "speed": 20.000988629404798
  },
  {
    "timestamp": 14.75,
    "latitude": 37.789981502001,
    "longitude": -122.398205959,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222673965618014,
    "yaw": 359.922332763672,
    "speed": 20.00095441523442
  },
  {
    "timestamp": 14.8,
    "latitude": 37.789981456369,
    "longitude": -122.398194602,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222971546463668,
    "yaw": 359.922088623047,
    "speed": 20.00092020691533
  },
  {
    "timestamp": 14.85,
    "latitude": 37.789981410736,
    "longitude": -122.398183245,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223331991583109,
    "yaw": 359.921813964844,
    "speed": 20.000885993292986
  },
  {
    "timestamp": 14.9,
    "latitude": 37.789981365102,
    "longitude": -122.398171888,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223399861715734,
    "yaw": 359.921569824219,
    "speed": 20.000853692431136
  },
  {
    "timestamp": 14.95,
    "latitude": 37.789981319467,
    "longitude": -122.398160531,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223155017010868,
    "yaw": 359.921295166016,
    "speed": 20.000819479829048
  },
  {
    "timestamp": 15.0,
    "latitude": 37.789981273831,
    "longitude": -122.398149174,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223252503201365,
    "yaw": 359.921051025391,
    "speed": 20.000781457748342
  },
  {
    "timestamp": 15.05,
    "latitude": 37.789981228193,
    "longitude": -122.398137817,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223337928764522,
    "yaw": 359.920776367188,
    "speed": 20.000745338347123
  },
  {
    "timestamp": 15.1,
    "latitude": 37.789981182555,
    "longitude": -122.39812646,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223091524094343,
    "yaw": 359.920532226563,
    "speed": 20.00071113149576
  },
  {
    "timestamp": 15.15,
    "latitude": 37.789981136915,
    "longitude": -122.398115103,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223192060366273,
    "yaw": 359.920257568359,
    "speed": 20.000678827557675
  },
  {
    "timestamp": 15.2,
    "latitude": 37.789981091275,
    "longitude": -122.398103746,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223312503658235,
    "yaw": 359.920013427734,
    "speed": 20.000650343933184
  },
  {
    "timestamp": 15.25,
    "latitude": 37.789981045634,
    "longitude": -122.398092389,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223117205314338,
    "yaw": 359.919738769531,
    "speed": 20.00061804070603
  },
  {
    "timestamp": 15.3,
    "latitude": 37.789980999992,
    "longitude": -122.398081032,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223269360139966,
    "yaw": 359.919494628906,
    "speed": 20.000591464929727
  },
  {
    "timestamp": 15.35,
    "latitude": 37.789980954348,
    "longitude": -122.398069676,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.0022344880271703,
    "yaw": 359.919250488281,
    "speed": 20.00056488987194
  },
  {
    "timestamp": 15.4,
    "latitude": 37.789980908704,
    "longitude": -122.398058319,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223303982056677,
    "yaw": 359.918975830078,
    "speed": 20.000536402503542
  },
  {
    "timestamp": 15.45,
    "latitude": 37.789980863059,
    "longitude": -122.398046962,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.0022346880286932,
    "yaw": 359.918731689453,
    "speed": 20.000507920761546
  },
  {
    "timestamp": 15.5,
    "latitude": 37.789980817412,
    "longitude": -122.398035605,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223287753760815,
    "yaw": 359.91845703125,
    "speed": 20.00048134161994
  },
  {
    "timestamp": 15.55,
    "latitude": 37.789980771765,
    "longitude": -122.398024249,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.0022342384327203,
    "yaw": 359.918212890625,
    "speed": 20.000454768299356
  },
  {
    "timestamp": 15.6,
    "latitude": 37.789980726530,
    "longitude": -122.398012892,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223219743929803,
    "yaw": 359.917938232422,
    "speed": 20.000428189780145
  },
  {
    "timestamp": 15.65,
    "latitude": 37.789980681569,
    "longitude": -122.398001535,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223029823973775,
    "yaw": 359.917694091797,
    "speed": 20.000411153636573
  },
  {
    "timestamp": 15.7,
    "latitude": 37.789980636606,
    "longitude": -122.397990179,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223225448280573,
    "yaw": 359.917419433594,
    "speed": 20.000399834923584
  },
  {
    "timestamp": 15.75,
    "latitude": 37.789980591642,
    "longitude": -122.397978822,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223157997243106,
    "yaw": 359.917175292969,
    "speed": 20.00038089258159
  },
  {
    "timestamp": 15.8,
    "latitude": 37.789980546684,
    "longitude": -122.397967466,
    "altitude": 10.1176719666,
    "roll": 359.983123779,
    "pitch": 0.00225535733625293,
    "yaw": 359.916900634766,
    "speed": 19.998168448273994
  },
  {
    "timestamp": 15.85,
    "latitude": 37.789980501724,
    "longitude": -122.397956111,
    "altitude": 10.1176280975,
    "roll": 359.983062744,
    "pitch": 0.00228413660079241,
    "yaw": 359.916656494141,
    "speed": 19.998330724891375
  },
  {
    "timestamp": 15.9,
    "latitude": 37.789980456762,
    "longitude": -122.397944755,
    "altitude": 10.1176242828,
    "roll": 359.982971191,
    "pitch": 0.00229926127940416,
    "yaw": 359.916381835938,
    "speed": 19.998647510656856
  },
  {
    "timestamp": 15.95,
    "latitude": 37.789980411799,
    "longitude": -122.397933399,
    "altitude": 10.1176424026,
    "roll": 359.982879639,
    "pitch": 0.00230474676936865,
    "yaw": 359.916137695313,
    "speed": 19.998947122469215
  },
  {
    "timestamp": 16.0,
    "latitude": 37.789980366833,
    "longitude": -122.397922043,
    "altitude": 10.1176681519,
    "roll": 359.982788086,
    "pitch": 0.00229955301620066,
    "yaw": 359.915863037109,
    "speed": 19.999206657983194
  },
  {
    "timestamp": 16.05,
    "latitude": 37.789980321867,
    "longitude": -122.397910687,
    "altitude": 10.1176939011,
    "roll": 359.982757568,
    "pitch": 0.00228793569840491,
    "yaw": 359.915618896484,
    "speed": 19.999424229911565
  },
  {
    "timestamp": 16.1,
    "latitude": 37.789980276897,
    "longitude": -122.397899331,
    "altitude": 10.1177177429,
    "roll": 359.982757568,
    "pitch": 0.00228012190200388,
    "yaw": 359.915344238281,
    "speed": 19.999607458230965
  },
  {
    "timestamp": 16.15,
    "latitude": 37.789980231926,
    "longitude": -122.397887975,
    "altitude": 10.1177396774,
    "roll": 359.982757568,
    "pitch": 0.00226402841508389,
    "yaw": 359.915069580078,
    "speed": 19.99977542918457
  },
  {
    "timestamp": 16.2,
    "latitude": 37.789980186954,
    "longitude": -122.397876618,
    "altitude": 10.1177558899,
    "roll": 359.982788086,
    "pitch": 0.00224838824942708,
    "yaw": 359.914825439453,
    "speed": 19.999905259279508
  },
  {
    "timestamp": 16.25,
    "latitude": 37.789980141980,
    "longitude": -122.397865262,
    "altitude": 10.1177682877,
    "roll": 359.982788086,
    "pitch": 0.00224931328557432,
    "yaw": 359.91455078125,
    "speed": 20.000016010798095
  },
  {
    "timestamp": 16.3,
    "latitude": 37.789980097005,
    "longitude": -122.397853905,
    "altitude": 10.1177778244,
    "roll": 359.982818604,
    "pitch": 0.002238116459921,
    "yaw": 359.914306640625,
    "speed": 20.00010960296106
  },
  {
    "timestamp": 16.35,
    "latitude": 37.789980052029,
    "longitude": -122.397842549,
    "altitude": 10.1177845001,
    "roll": 359.982849121,
    "pitch": 0.00223604519851506,
    "yaw": 359.914031982422,
    "speed": 20.00018984022735
  },
  {
    "timestamp": 16.4,
    "latitude": 37.789980007052,
    "longitude": -122.397831192,
    "altitude": 10.1177892685,
    "roll": 359.982879639,
    "pitch": 0.00222854083403945,
    "yaw": 359.913757324219,
    "speed": 20.000256730728037
  },
  {
    "timestamp": 16.45,
    "latitude": 37.789979962624,
    "longitude": -122.397819836,
    "altitude": 10.1177930832,
    "roll": 359.982910156,
    "pitch": 0.00223252573050559,
    "yaw": 359.913513183594,
    "speed": 20.000312180177506
  },
  {
    "timestamp": 16.5,
    "latitude": 37.789979918332,
    "longitude": -122.397808479,
    "altitude": 10.1177949905,
    "roll": 359.982910156,
    "pitch": 0.00222557131201029,
    "yaw": 359.913238525391,
    "speed": 20.000359997202395
  },
  {
    "timestamp": 16.55,
    "latitude": 37.789979874044,
    "longitude": -122.397797124,
    "altitude": 10.1176710129,
    "roll": 359.983001709,
    "pitch": 0.0022486203815788,
    "yaw": 359.912994384766,
    "speed": 19.9982047829773
  },
  {
    "timestamp": 16.6,
    "latitude": 37.789979829756,
    "longitude": -122.397785768,
    "altitude": 10.1176271439,
    "roll": 359.982971191,
    "pitch": 0.00227682269178331,
    "yaw": 359.912719726563,
    "speed": 19.9984109329835
  },
  {
    "timestamp": 16.65,
    "latitude": 37.789979785465,
    "longitude": -122.397774412,
    "altitude": 10.1176242828,
    "roll": 359.982879639,
    "pitch": 0.00229516997933388,
    "yaw": 359.912475585938,
    "speed": 19.99876587839288
  },
  {
    "timestamp": 16.7,
    "latitude": 37.789979741172,
    "longitude": -122.397763056,
    "altitude": 10.1176424026,
    "roll": 359.982788086,
    "pitch": 0.00230081053450704,
    "yaw": 359.912200927734,
    "speed": 19.99909028670778
  },
  {
    "timestamp": 16.75,
    "latitude": 37.789979696878,
    "longitude": -122.3977517,
    "altitude": 10.1176681519,
    "roll": 359.982757568,
    "pitch": 0.00229269987903535,
    "yaw": 359.911926269531,
    "speed": 19.999370810700228
  },
  {
    "timestamp": 16.8,
    "latitude": 37.789979652580,
    "longitude": -122.397740344,
    "altitude": 10.1176939011,
    "roll": 359.982727051,
    "pitch": 0.00228843558579683,
    "yaw": 359.911682128906,
    "speed": 19.999599834069333
  },
  {
    "timestamp": 16.85,
    "latitude": 37.789979608282,
    "longitude": -122.397728988,
    "altitude": 10.1177177429,
    "roll": 359.982727051,
    "pitch": 0.00227168202400208,
    "yaw": 359.911407470703,
    "speed": 19.99980214333621
  },
  {
    "timestamp": 16.9,
    "latitude": 37.789979563982,
    "longitude": -122.397717631,
    "altitude": 10.1177396774,
    "roll": 359.982727051,
    "pitch": 0.00226365402340889,
    "yaw": 359.911163330078,
    "speed": 19.999973941521798
  },
  {
    "timestamp": 16.95,
    "latitude": 37.789979519680,
    "longitude": -122.397706275,
    "altitude": 10.1177568436,
    "roll": 359.982757568,
    "pitch": 0.00224294327199459,
    "yaw": 359.910888671875,
    "speed": 20.00011712276976
  },
  {
    "timestamp": 17.0,
    "latitude": 37.789979475378,
    "longitude": -122.397694918,
    "altitude": 10.1177692413,
    "roll": 359.982788086,
    "pitch": 0.002239138353616,
    "yaw": 359.910614013672,
    "speed": 20.0002316960222
  },
  {
    "timestamp": 17.05,
    "latitude": 37.789979431074,
    "longitude": -122.397683562,
    "altitude": 10.1177778244,
    "roll": 359.982818604,
    "pitch": 0.00223426730372012,
    "yaw": 359.910369873047,
    "speed": 20.00032720363976
  },
  {
    "timestamp": 17.1,
    "latitude": 37.789979386769,
    "longitude": -122.397672205,
    "altitude": 10.1177845001,
    "roll": 359.982849121,
    "pitch": 0.00222696596756577,
    "yaw": 359.910095214844,
    "speed": 20.000399819706395
  },
  {
    "timestamp": 17.15,
    "latitude": 37.789979342462,
    "longitude": -122.397660848,
    "altitude": 10.1177892685,
    "roll": 359.982879639,
    "pitch": 0.00223442306742072,
    "yaw": 359.909851074219,
    "speed": 20.000468628521247
  },
  {
    "timestamp": 17.2,
    "latitude": 37.789979298153,
    "longitude": -122.397649492,
    "altitude": 10.1177921295,
    "roll": 359.982879639,
    "pitch": 0.00223075109533966,
    "yaw": 359.909576416016,
    "speed": 20.000522172519823
  },
  {
    "timestamp": 17.25,
    "latitude": 37.789979253843,
    "longitude": -122.397638135,
    "altitude": 10.1177940369,
    "roll": 359.982910156,
    "pitch": 0.00222637876868248,
    "yaw": 359.909332275391,
    "speed": 20.000558557453083
  },
  {
    "timestamp": 17.3,
    "latitude": 37.789979210220,
    "longitude": -122.397626778,
    "altitude": 10.1177959442,
    "roll": 359.982940674,
    "pitch": 0.0022288728505373,
    "yaw": 359.909057617188,
    "speed": 20.000581584747284
  },
  {
    "timestamp": 17.35,
    "latitude": 37.789979166596,
    "longitude": -122.397615421,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.0022279042750597,
    "yaw": 359.908782958984,
    "speed": 20.00060270401583
  },
  {
    "timestamp": 17.4,
    "latitude": 37.789979122970,
    "longitude": -122.397604064,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222681765444577,
    "yaw": 359.908538818359,
    "speed": 20.000608571593066
  },
  {
    "timestamp": 17.45,
    "latitude": 37.789979079344,
    "longitude": -122.397592707,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222628144547343,
    "yaw": 359.908264160156,
    "speed": 20.00061634214145
  },
  {
    "timestamp": 17.5,
    "latitude": 37.789979035716,
    "longitude": -122.39758135,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222354591824114,
    "yaw": 359.908020019531,
    "speed": 20.000622211363908
  },
  {
    "timestamp": 17.55,
    "latitude": 37.789978992087,
    "longitude": -122.397569993,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222520320676267,
    "yaw": 359.907745361328,
    "speed": 20.000614723196836
  },
  {
    "timestamp": 17.6,
    "latitude": 37.789978948458,
    "longitude": -122.397558637,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00223093805834651,
    "yaw": 359.907501220703,
    "speed": 20.00060724159069
  },
  {
    "timestamp": 17.65,
    "latitude": 37.789978904827,
    "longitude": -122.39754728,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00223053386434913,
    "yaw": 359.9072265625,
    "speed": 20.000590217249567
  },
  {
    "timestamp": 17.7,
    "latitude": 37.789978861195,
    "longitude": -122.397535923,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223054806701839,
    "yaw": 359.906982421875,
    "speed": 20.000582736452376
  },
  {
    "timestamp": 17.75,
    "latitude": 37.789978817562,
    "longitude": -122.397524566,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223427941091359,
    "yaw": 359.906707763672,
    "speed": 20.000563805009875
  },
  {
    "timestamp": 17.8,
    "latitude": 37.789978773927,
    "longitude": -122.397513209,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.0022313327062875,
    "yaw": 359.906463623047,
    "speed": 20.000546787760037
  },
  {
    "timestamp": 17.85,
    "latitude": 37.789978730292,
    "longitude": -122.397501852,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223175506107509,
    "yaw": 359.906219482422,
    "speed": 20.000529770361204
  },
  {
    "timestamp": 17.9,
    "latitude": 37.789978686656,
    "longitude": -122.397490495,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223246612586081,
    "yaw": 359.905944824219,
    "speed": 20.00050893293071
  },
  {
    "timestamp": 17.95,
    "latitude": 37.789978643019,
    "longitude": -122.397479139,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223644892685115,
    "yaw": 359.905700683594,
    "speed": 20.000484287047968
  },
  {
    "timestamp": 18.0,
    "latitude": 37.789978599381,
    "longitude": -122.397467782,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223346636630595,
    "yaw": 359.905426025391,
    "speed": 20.000459635483754
  },
  {
    "timestamp": 18.05,
    "latitude": 37.789978555743,
    "longitude": -122.397456425,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223336229100823,
    "yaw": 359.905181884766,
    "speed": 20.000434990379066
  },
  {
    "timestamp": 18.1,
    "latitude": 37.789978512240,
    "longitude": -122.397445069,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222995225340128,
    "yaw": 359.904907226563,
    "speed": 20.000421783557872
  },
  {
    "timestamp": 18.15,
    "latitude": 37.789978469287,
    "longitude": -122.397433712,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223004445433617,
    "yaw": 359.904663085938,
    "speed": 20.000408583901635
  },
  {
    "timestamp": 18.2,
    "latitude": 37.789978426332,
    "longitude": -122.397422355,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223068031482399,
    "yaw": 359.904388427734,
    "speed": 20.000393470604145
  },
  {
    "timestamp": 18.25,
    "latitude": 37.789978383377,
    "longitude": -122.397410999,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223187124356627,
    "yaw": 359.904144287109,
    "speed": 20.000378363887325
  },
  {
    "timestamp": 18.3,
    "latitude": 37.789978340420,
    "longitude": -122.397399642,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223335647024214,
    "yaw": 359.903869628906,
    "speed": 20.00036325140071
  },
  {
    "timestamp": 18.35,
    "latitude": 37.789978297462,
    "longitude": -122.397388285,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223472039215267,
    "yaw": 359.903625488281,
    "speed": 20.000348143906695
  },
  {
    "timestamp": 18.4,
    "latitude": 37.789978254504,
    "longitude": -122.397376928,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223277066834271,
    "yaw": 359.903350830078,
    "speed": 20.00033303212198
  },
  {
    "timestamp": 18.45,
    "latitude": 37.789978211544,
    "longitude": -122.397365572,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223416718654335,
    "yaw": 359.903106689453,
    "speed": 20.000317926640882
  },
  {
    "timestamp": 18.5,
    "latitude": 37.789978168583,
    "longitude": -122.397354215,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223243981599808,
    "yaw": 359.90283203125,
    "speed": 20.000306631533466
  },
  {
    "timestamp": 18.55,
    "latitude": 37.789978125621,
    "longitude": -122.397342859,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223423959687352,
    "yaw": 359.902587890625,
    "speed": 20.000289619836064
  },
  {
    "timestamp": 18.6,
    "latitude": 37.789978082659,
    "longitude": -122.397331502,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223296275362372,
    "yaw": 359.902313232422,
    "speed": 20.00027260210313
  },
  {
    "timestamp": 18.65,
    "latitude": 37.789978039696,
    "longitude": -122.397320146,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223173177801073,
    "yaw": 359.902069091797,
    "speed": 20.00025940602324
  },
  {
    "timestamp": 18.7,
    "latitude": 37.789977996731,
    "longitude": -122.397308789,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223068334162235,
    "yaw": 359.901824951172,
    "speed": 20.000246210273435
  },
  {
    "timestamp": 18.75,
    "latitude": 37.789977953766,
    "longitude": -122.397297432,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222984119318426,
    "yaw": 359.901550292969,
    "speed": 20.00023300875237
  },
  {
    "timestamp": 18.8,
    "latitude": 37.789977910799,
    "longitude": -122.397286076,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222929939627647,
    "yaw": 359.901306152344,
    "speed": 20.000219814006428
  },
  {
    "timestamp": 18.85,
    "latitude": 37.789977867831,
    "longitude": -122.397274719,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.0022323455195874,
    "yaw": 359.901031494141,
    "speed": 20.000202798826777
  },
  {
    "timestamp": 18.9,
    "latitude": 37.789977824862,
    "longitude": -122.397263363,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223184167407453,
    "yaw": 359.900787353516,
    "speed": 20.000195326964043
  },
  {
    "timestamp": 18.95,
    "latitude": 37.789977782167,
    "longitude": -122.397252006,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.0022346309851855,
    "yaw": 359.900512695313,
    "speed": 20.000187848356497
  },
  {
    "timestamp": 19.0,
    "latitude": 37.789977739884,
    "longitude": -122.39724065,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223374646157026,
    "yaw": 359.900268554688,
    "speed": 20.000180377352777
  },
  {
    "timestamp": 19.05,
    "latitude": 37.789977697599,
    "longitude": -122.397229293,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223588570952415,
    "yaw": 359.899993896484,
    "speed": 20.000176714847136
  },
  {
    "timestamp": 19.1,
    "latitude": 37.789977655314,
    "longitude": -122.397217937,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223418907262385,
    "yaw": 359.899749755859,
    "speed": 20.000167337372304
  },
  {
    "timestamp": 19.15,
    "latitude": 37.789977613027,
    "longitude": -122.39720658,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223207916133106,
    "yaw": 359.899475097656,
    "speed": 20.000159861004608
  },
  {
    "timestamp": 19.2,
    "latitude": 37.789977570739,
    "longitude": -122.397195224,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223633414134383,
    "yaw": 359.899230957031,
    "speed": 20.000156206284306
  },
  {
    "timestamp": 19.25,
    "latitude": 37.789977528450,
    "longitude": -122.397183867,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223689968697727,
    "yaw": 359.898956298828,
    "speed": 20.00015254549959
  },
  {
    "timestamp": 19.3,
    "latitude": 37.789977486160,
    "longitude": -122.397172511,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223388220183551,
    "yaw": 359.898712158203,
    "speed": 20.000148891744697
  },
  {
    "timestamp": 19.35,
    "latitude": 37.789977443869,
    "longitude": -122.397161154,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223375926725566,
    "yaw": 359.8984375,
    "speed": 20.000139509821096
  },
  {
    "timestamp": 19.4,
    "latitude": 37.789977401577,
    "longitude": -122.397149798,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223662261851132,
    "yaw": 359.898193359375,
    "speed": 20.000132041827225
  },
  {
    "timestamp": 19.45,
    "latitude": 37.789977359283,
    "longitude": -122.397138441,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223557627759874,
    "yaw": 359.897918701172,
    "speed": 20.000124567003667
  },
  {
    "timestamp": 19.5,
    "latitude": 37.789977316989,
    "longitude": -122.397127085,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223398604430258,
    "yaw": 359.897674560547,
    "speed": 20.000117099719166
  },
  {
    "timestamp": 19.55,
    "latitude": 37.789977274693,
    "longitude": -122.397115728,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223206309601665,
    "yaw": 359.897399902344,
    "speed": 20.00010962682543
  },
  {
    "timestamp": 19.6,
    "latitude": 37.789977232397,
    "longitude": -122.397104372,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.0022332591470331,
    "yaw": 359.897155761719,
    "speed": 20.0001040678841
  },
  {
    "timestamp": 19.65,
    "latitude": 37.789977190099,
    "longitude": -122.397093015,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223139091394842,
    "yaw": 359.896881103516,
    "speed": 20.000098502868916
  },
  {
    "timestamp": 19.7,
    "latitude": 37.789977147800,
    "longitude": -122.397081658,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00222964980639517,
    "yaw": 359.896636962891,
    "speed": 20.000092944927516
  },
  {
    "timestamp": 19.75,
    "latitude": 37.789977105500,
    "longitude": -122.397070302,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222856434993446,
    "yaw": 359.896362304688,
    "speed": 20.000089289384828
  },
  {
    "timestamp": 19.8,
    "latitude": 37.789977063474,
    "longitude": -122.397058945,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223132572136819,
    "yaw": 359.896118164063,
    "speed": 20.000083732672547
  },
  {
    "timestamp": 19.85,
    "latitude": 37.789977021860,
    "longitude": -122.397047589,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222804327495396,
    "yaw": 359.895874023438,
    "speed": 20.00007817617314
  },
  {
    "timestamp": 19.9,
    "latitude": 37.789976980244,
    "longitude": -122.397036232,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222878437489271,
    "yaw": 359.895599365234,
    "speed": 20.000074520861027
  },
  {
    "timestamp": 19.95,
    "latitude": 37.789976938628,
    "longitude": -122.397024876,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223023095168173,
    "yaw": 359.895355224609,
    "speed": 20.00007087268931
  },
  {
    "timestamp": 20.0,
    "latitude": 37.789935007395,
    "longitude": -122.397013519,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222910335287452,
    "yaw": 359.895080566406,
    "speed": 20.000069125585753
  }
]

GPS Spoofing: GPS is all you got

解题过程
gps.py

f = open('gps.json', 'r')
gps = f.read()
f.close()
gpslines = gps.split('n')
pos = []
for line in gpslines:
  i0 = line.find('timestamp')
  if i0 >= 0:
    ti = line[i0+12:-1]
  i1 = line.find('latitude')
  if i1 >= 0:
    la = float(line[i1+11:-1])
  i2 = line.find('longitude')
  if i2 >= 0:
    lo = float(line[i2+12:-1])
  i3 = line.find('altitude')
  if i3 >= 0:
    al = float(line[i3+11:-1])
    pos.append( [la, lo, al, ti] )

rate = (0.0107700551979-0.000017) / 0.0107700551979
print rate
for i in range(len(pos) - 1):
  pos[1 + i][0] = rate*(pos[1+i][0] - pos[0][0]) + pos[i][0]

f = open('gps_new.json', 'w')
f.write('[n')
for i in range(len(pos)):
  f.write('  {n')
  f.write('    "timestamp": %s,n' % pos[i][3])
  f.write('    "latitude": %.13f,n' % pos[i][0])
  f.write('    "longitude": %.12f,n' % pos[i][1])
  f.write('    "altitude": %.13fn' % pos[i][2])
  if i == len(pos) - 1:
    f.write('  }n')
  else:
    f.write('  },n')
f.write(']')
f.close()

gps_new.json

[
  {
    "timestamp": 0.0,
    "latitude": 37.7899753693032,
    "longitude": -122.397121279501,
    "altitude": 10.1277933120720
  },
  {
    "timestamp": 0.05,
    "latitude": 37.7899754265434,
    "longitude": -122.397132214792,
    "altitude": 10.1244440078730
  },
  {
    "timestamp": 0.1,
    "latitude": 37.7899755414654,
    "longitude": -122.397143236731,
    "altitude": 10.1220254898070
  },
  {
    "timestamp": 0.15,
    "latitude": 37.7899757143859,
    "longitude": -122.397154347742,
    "altitude": 10.1203002929680
  },
  {
    "timestamp": 0.2,
    "latitude": 37.7899759458176,
    "longitude": -122.397165532403,
    "altitude": 10.1192083358760
  },
  {
    "timestamp": 0.25,
    "latitude": 37.7899762360459,
    "longitude": -122.397176773210,
    "altitude": 10.1185302734370
  },
  {
    "timestamp": 0.3,
    "latitude": 37.7899765851408,
    "longitude": -122.397188054742,
    "altitude": 10.1180019378660
  },
  {
    "timestamp": 0.35,
    "latitude": 37.7899769933924,
    "longitude": -122.397199366426,
    "altitude": 10.1177244186400
  },
  {
    "timestamp": 0.4,
    "latitude": 37.7899774602113,
    "longitude": -122.397210697351,
    "altitude": 10.1174736022940
  },
  {
    "timestamp": 0.45,
    "latitude": 37.7899779856691,
    "longitude": -122.397222042486,
    "altitude": 10.1173887252800
  },
  {
    "timestamp": 0.5,
    "latitude": 37.7899785698098,
    "longitude": -122.397233396459,
    "altitude": 10.1173906326290
  },
  {
    "timestamp": 0.55,
    "latitude": 37.7899792122478,
    "longitude": -122.397244755808,
    "altitude": 10.1174354553220
  },
  {
    "timestamp": 0.6,
    "latitude": 37.7899799127243,
    "longitude": -122.397256118452,
    "altitude": 10.1174955368040
  },
  {
    "timestamp": 0.65,
    "latitude": 37.7899806712363,
    "longitude": -122.397267480749,
    "altitude": 10.1174316406200
  },
  {
    "timestamp": 0.7,
    "latitude": 37.7899814876491,
    "longitude": -122.397278843740,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 0.75,
    "latitude": 37.7899823615452,
    "longitude": -122.397290205868,
    "altitude": 10.1173601150510
  },
  {
    "timestamp": 0.8,
    "latitude": 37.7899832927887,
    "longitude": -122.397301568517,
    "altitude": 10.1173706054680
  },
  {
    "timestamp": 0.85,
    "latitude": 37.7899842815179,
    "longitude": -122.397312931512,
    "altitude": 10.1174211502070
  },
  {
    "timestamp": 0.9,
    "latitude": 37.7899853275968,
    "longitude": -122.397324295028,
    "altitude": 10.1174869537350
  },
  {
    "timestamp": 0.95,
    "latitude": 37.7899864310199,
    "longitude": -122.397335657677,
    "altitude": 10.1174249649040
  },
  {
    "timestamp": 1.0,
    "latitude": 37.7899875917800,
    "longitude": -122.397347019113,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 1.05,
    "latitude": 37.7899888098787,
    "longitude": -122.397358381069,
    "altitude": 10.1173133850090
  },
  {
    "timestamp": 1.1,
    "latitude": 37.7899900847674,
    "longitude": -122.397369743377,
    "altitude": 10.1173658370970
  },
  {
    "timestamp": 1.15,
    "latitude": 37.7899914163023,
    "longitude": -122.397381104645,
    "altitude": 10.1173114776610
  },
  {
    "timestamp": 1.2,
    "latitude": 37.7899928044823,
    "longitude": -122.397392465914,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 1.25,
    "latitude": 37.7899942493082,
    "longitude": -122.397403827529,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 1.3,
    "latitude": 37.7899957507807,
    "longitude": -122.397415189491,
    "altitude": 10.1174774169920
  },
  {
    "timestamp": 1.35,
    "latitude": 37.7899973088924,
    "longitude": -122.397426550240,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 1.4,
    "latitude": 37.7899989236441,
    "longitude": -122.397437911336,
    "altitude": 10.1174364089960
  },
  {
    "timestamp": 1.45,
    "latitude": 37.7900005950354,
    "longitude": -122.397449272604,
    "altitude": 10.1174831390380
  },
  {
    "timestamp": 1.5,
    "latitude": 37.7900023230663,
    "longitude": -122.397460634047,
    "altitude": 10.1175384521480
  },
  {
    "timestamp": 1.55,
    "latitude": 37.7900041077364,
    "longitude": -122.397471995662,
    "altitude": 10.1175937652580
  },
  {
    "timestamp": 1.6,
    "latitude": 37.7900059490447,
    "longitude": -122.397483357278,
    "altitude": 10.1176424026480
  },
  {
    "timestamp": 1.65,
    "latitude": 37.7900078469830,
    "longitude": -122.397494717507,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 1.7,
    "latitude": 37.7900098015504,
    "longitude": -122.397506077736,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 1.75,
    "latitude": 37.7900118127473,
    "longitude": -122.397517438312,
    "altitude": 10.1175651550290
  },
  {
    "timestamp": 1.8,
    "latitude": 37.7900138805727,
    "longitude": -122.397528798888,
    "altitude": 10.1175994873040
  },
  {
    "timestamp": 1.85,
    "latitude": 37.7900160043389,
    "longitude": -122.397540159470,
    "altitude": 10.1176385879510
  },
  {
    "timestamp": 1.9,
    "latitude": 37.7900181840450,
    "longitude": -122.397551520051,
    "altitude": 10.1176729202270
  },
  {
    "timestamp": 1.95,
    "latitude": 37.7900204196836,
    "longitude": -122.397562879420,
    "altitude": 10.1175775527950
  },
  {
    "timestamp": 2.0,
    "latitude": 37.7900227112465,
    "longitude": -122.397574237402,
    "altitude": 10.1174325942990
  },
  {
    "timestamp": 2.05,
    "latitude": 37.7900250587336,
    "longitude": -122.397585595557,
    "altitude": 10.1174049377440
  },
  {
    "timestamp": 2.1,
    "latitude": 37.7900274621393,
    "longitude": -122.397596952847,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 2.15,
    "latitude": 37.7900299214635,
    "longitude": -122.397608310309,
    "altitude": 10.1173181533810
  },
  {
    "timestamp": 2.2,
    "latitude": 37.7900324367004,
    "longitude": -122.397619666905,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 2.25,
    "latitude": 37.7900350078510,
    "longitude": -122.397631023848,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 2.3,
    "latitude": 37.7900376349166,
    "longitude": -122.397642381310,
    "altitude": 10.1173467636100
  },
  {
    "timestamp": 2.35,
    "latitude": 37.7900403178919,
    "longitude": -122.397653737906,
    "altitude": 10.1173048019400
  },
  {
    "timestamp": 2.4,
    "latitude": 37.7900430567774,
    "longitude": -122.397665094849,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 2.45,
    "latitude": 37.7900458515678,
    "longitude": -122.397676450925,
    "altitude": 10.1172819137570
  },
  {
    "timestamp": 2.5,
    "latitude": 37.7900487022645,
    "longitude": -122.397687807521,
    "altitude": 10.1173124313350
  },
  {
    "timestamp": 2.55,
    "latitude": 37.7900516088691,
    "longitude": -122.397699164638,
    "altitude": 10.1173801422110
  },
  {
    "timestamp": 2.6,
    "latitude": 37.7900545713823,
    "longitude": -122.397710522100,
    "altitude": 10.1174583435050
  },
  {
    "timestamp": 2.65,
    "latitude": 37.7900575895309,
    "longitude": -122.397721880085,
    "altitude": 10.1175317764280
  },
  {
    "timestamp": 2.7,
    "latitude": 37.7900606628968,
    "longitude": -122.397733237034,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 2.75,
    "latitude": 37.7900637914735,
    "longitude": -122.397744592943,
    "altitude": 10.1173553466790
  },
  {
    "timestamp": 2.8,
    "latitude": 37.7900669752625,
    "longitude": -122.397755949371,
    "altitude": 10.1173486709590
  },
  {
    "timestamp": 2.85,
    "latitude": 37.7900702142654,
    "longitude": -122.397767306320,
    "altitude": 10.1173944473260
  },
  {
    "timestamp": 2.9,
    "latitude": 37.7900735084767,
    "longitude": -122.397778662402,
    "altitude": 10.1173362731930
  },
  {
    "timestamp": 2.95,
    "latitude": 37.7900768578972,
    "longitude": -122.397790018831,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 3.0,
    "latitude": 37.7900802625282,
    "longitude": -122.397801375779,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 3.05,
    "latitude": 37.7900837223706,
    "longitude": -122.397812733075,
    "altitude": 10.1174898147580
  },
  {
    "timestamp": 3.1,
    "latitude": 37.7900872374250,
    "longitude": -122.397824090717,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 3.15,
    "latitude": 37.7900908076859,
    "longitude": -122.397835447492,
    "altitude": 10.1174907684320
  },
  {
    "timestamp": 3.2,
    "latitude": 37.7900944331540,
    "longitude": -122.397846804614,
    "altitude": 10.1174936294550
  },
  {
    "timestamp": 3.25,
    "latitude": 37.7900981138227,
    "longitude": -122.397858160697,
    "altitude": 10.1174030303950
  },
  {
    "timestamp": 3.3,
    "latitude": 37.7901018496929,
    "longitude": -122.397869517126,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 3.35,
    "latitude": 37.7901056407599,
    "longitude": -122.397880872861,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 3.4,
    "latitude": 37.7901094870182,
    "longitude": -122.397892227731,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 3.45,
    "latitude": 37.7901133881886,
    "longitude": -122.397903581909,
    "altitude": 10.1171007156370
  },
  {
    "timestamp": 3.5,
    "latitude": 37.7901173438544,
    "longitude": -122.397914935398,
    "altitude": 10.1169986724850
  },
  {
    "timestamp": 3.55,
    "latitude": 37.7901213540128,
    "longitude": -122.397926288540,
    "altitude": 10.1169157028190
  },
  {
    "timestamp": 3.6,
    "latitude": 37.7901254186603,
    "longitude": -122.397937641163,
    "altitude": 10.1168479919430
  },
  {
    "timestamp": 3.65,
    "latitude": 37.7901295377954,
    "longitude": -122.397948993785,
    "altitude": 10.1167964935300
  },
  {
    "timestamp": 3.7,
    "latitude": 37.7901337114227,
    "longitude": -122.397960347447,
    "altitude": 10.1168823242180
  },
  {
    "timestamp": 3.75,
    "latitude": 37.7901379395461,
    "longitude": -122.397971702149,
    "altitude": 10.1170234680170
  },
  {
    "timestamp": 3.8,
    "latitude": 37.7901422221700,
    "longitude": -122.397983057891,
    "altitude": 10.1171770095820
  },
  {
    "timestamp": 3.85,
    "latitude": 37.7901465592959,
    "longitude": -122.397994414152,
    "altitude": 10.1173191070550
  },
  {
    "timestamp": 3.9,
    "latitude": 37.7901509509200,
    "longitude": -122.398005769894,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 3.95,
    "latitude": 37.7901553970439,
    "longitude": -122.398017126156,
    "altitude": 10.1173677444450
  },
  {
    "timestamp": 4.0,
    "latitude": 37.7901598976691,
    "longitude": -122.398028482938,
    "altitude": 10.1174392700190
  },
  {
    "timestamp": 4.05,
    "latitude": 37.7901644527987,
    "longitude": -122.398039840499,
    "altitude": 10.1175127029410
  },
  {
    "timestamp": 4.1,
    "latitude": 37.7901690624332,
    "longitude": -122.398051198407,
    "altitude": 10.1175804138180
  },
  {
    "timestamp": 4.15,
    "latitude": 37.7901737265738,
    "longitude": -122.398062556748,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 4.2,
    "latitude": 37.7901784452210,
    "longitude": -122.398073915436,
    "altitude": 10.1176815032950
  },
  {
    "timestamp": 4.25,
    "latitude": 37.7901832178247,
    "longitude": -122.398085274129,
    "altitude": 10.1177158355710
  },
  {
    "timestamp": 4.3,
    "latitude": 37.7901880442420,
    "longitude": -122.398096631956,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 4.35,
    "latitude": 37.7901929244722,
    "longitude": -122.398107989870,
    "altitude": 10.1175899505610
  },
  {
    "timestamp": 4.4,
    "latitude": 37.7901978585161,
    "longitude": -122.398119348130,
    "altitude": 10.1175985336300
  },
  {
    "timestamp": 4.45,
    "latitude": 37.7902028463666,
    "longitude": -122.398130705264,
    "altitude": 10.1174993515010
  },
  {
    "timestamp": 4.5,
    "latitude": 37.7902078880181,
    "longitude": -122.398142061445,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.55,
    "latitude": 37.7902129834647,
    "longitude": -122.398153416760,
    "altitude": 10.1172180175780
  },
  {
    "timestamp": 4.6,
    "latitude": 37.7902181327083,
    "longitude": -122.398164772594,
    "altitude": 10.1172151565550
  },
  {
    "timestamp": 4.65,
    "latitude": 37.7902233357502,
    "longitude": -122.398176128949,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 4.7,
    "latitude": 37.7902285925861,
    "longitude": -122.398187484610,
    "altitude": 10.1172380447380
  },
  {
    "timestamp": 4.75,
    "latitude": 37.7902339032172,
    "longitude": -122.398198840791,
    "altitude": 10.1172828674310
  },
  {
    "timestamp": 4.8,
    "latitude": 37.7902392676462,
    "longitude": -122.398210197665,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.85,
    "latitude": 37.7902446858735,
    "longitude": -122.398221554886,
    "altitude": 10.1174459457390
  },
  {
    "timestamp": 4.9,
    "latitude": 37.7902501578997,
    "longitude": -122.398232912367,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 4.95,
    "latitude": 37.7902556837195,
    "longitude": -122.398244269068,
    "altitude": 10.1174678802400
  },
  {
    "timestamp": 5.0,
    "latitude": 37.7902612633335,
    "longitude": -122.398255626116,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 5.05,
    "latitude": 37.7902668961933,
    "longitude": -122.398266983515,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 5.1,
    "latitude": 37.7902725821561,
    "longitude": -122.398278340048,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 5.15,
    "latitude": 37.7902783212225,
    "longitude": -122.398289696929,
    "altitude": 10.1174468994140
  },
  {
    "timestamp": 5.2,
    "latitude": 37.7902841133799,
    "longitude": -122.398301051556,
    "altitude": 10.1172370910640
  },
  {
    "timestamp": 5.25,
    "latitude": 37.7902899586237,
    "longitude": -122.398312405490,
    "altitude": 10.1170768737790
  },
  {
    "timestamp": 5.3,
    "latitude": 37.7902958569563,
    "longitude": -122.398323760117,
    "altitude": 10.1170806884760
  },
  {
    "timestamp": 5.35,
    "latitude": 37.7903018083750,
    "longitude": -122.398335114398,
    "altitude": 10.1170358657830
  },
  {
    "timestamp": 5.4,
    "latitude": 37.7903078128825,
    "longitude": -122.398346469459,
    "altitude": 10.1170988082880
  },
  {
    "timestamp": 5.45,
    "latitude": 37.7903138704808,
    "longitude": -122.398357825126,
    "altitude": 10.1172056198100
  },
  {
    "timestamp": 5.5,
    "latitude": 37.7903199811726,
    "longitude": -122.398369181487,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 5.55,
    "latitude": 37.7903261449596,
    "longitude": -122.398380538454,
    "altitude": 10.1174306869500
  },
  {
    "timestamp": 5.6,
    "latitude": 37.7903323618431,
    "longitude": -122.398391895854,
    "altitude": 10.1175231933590
  },
  {
    "timestamp": 5.65,
    "latitude": 37.7903386318175,
    "longitude": -122.398403252388,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 5.7,
    "latitude": 37.7903449548840,
    "longitude": -122.398414609355,
    "altitude": 10.1174850463860
  },
  {
    "timestamp": 5.75,
    "latitude": 37.7903513310431,
    "longitude": -122.398425966669,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 5.8,
    "latitude": 37.7903577602899,
    "longitude": -122.398437323203,
    "altitude": 10.1174497604300
  },
  {
    "timestamp": 5.85,
    "latitude": 37.7903642420630,
    "longitude": -122.398448677575,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 5.9,
    "latitude": 37.7903707762270,
    "longitude": -122.398460032555,
    "altitude": 10.1171531677240
  },
  {
    "timestamp": 5.95,
    "latitude": 37.7903773627769,
    "longitude": -122.398471386755,
    "altitude": 10.1170740127560
  },
  {
    "timestamp": 6.0,
    "latitude": 37.7903840017165,
    "longitude": -122.398482741908,
    "altitude": 10.1171169281000
  },
  {
    "timestamp": 6.05,
    "latitude": 37.7903906930487,
    "longitude": -122.398494097842,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 6.1,
    "latitude": 37.7903974367754,
    "longitude": -122.398505454381,
    "altitude": 10.1173210144040
  },
  {
    "timestamp": 6.15,
    "latitude": 37.7904042328987,
    "longitude": -122.398516811528,
    "altitude": 10.1174259185790
  },
  {
    "timestamp": 6.2,
    "latitude": 37.7904110814197,
    "longitude": -122.398528169107,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 6.25,
    "latitude": 37.7904179823390,
    "longitude": -122.398539527033,
    "altitude": 10.1175928115840
  },
  {
    "timestamp": 6.3,
    "latitude": 37.7904249356573,
    "longitude": -122.398550885306,
    "altitude": 10.1176500320430
  },
  {
    "timestamp": 6.35,
    "latitude": 37.7904319413739,
    "longitude": -122.398562243665,
    "altitude": 10.1176948547360
  },
  {
    "timestamp": 6.4,
    "latitude": 37.7904389994896,
    "longitude": -122.398573602371,
    "altitude": 10.1177272796630
  },
  {
    "timestamp": 6.45,
    "latitude": 37.7904461100037,
    "longitude": -122.398584961164,
    "altitude": 10.1177511215200
  },
  {
    "timestamp": 6.5,
    "latitude": 37.7904532729160,
    "longitude": -122.398596320130,
    "altitude": 10.1177663803100
  },
  {
    "timestamp": 6.55,
    "latitude": 37.7904604882192,
    "longitude": -122.398607677883,
    "altitude": 10.1176519393920
  },
  {
    "timestamp": 6.6,
    "latitude": 37.7904677559127,
    "longitude": -122.398619035723,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 6.65,
    "latitude": 37.7904750753096,
    "longitude": -122.398630393742,
    "altitude": 10.1176176071160
  },
  {
    "timestamp": 6.7,
    "latitude": 37.7904824464103,
    "longitude": -122.398641752020,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 6.75,
    "latitude": 37.7904898692140,
    "longitude": -122.398653110385,
    "altitude": 10.1176633834830
  },
  {
    "timestamp": 6.8,
    "latitude": 37.7904973437199,
    "longitude": -122.398664468751,
    "altitude": 10.1176910400390
  },
  {
    "timestamp": 6.85,
    "latitude": 37.7905048699274,
    "longitude": -122.398675827289,
    "altitude": 10.1177148818900
  },
  {
    "timestamp": 6.9,
    "latitude": 37.7905124478357,
    "longitude": -122.398687185828,
    "altitude": 10.1177368164060
  },
  {
    "timestamp": 6.95,
    "latitude": 37.7905200774373,
    "longitude": -122.398698543154,
    "altitude": 10.1176271438590
  },
  {
    "timestamp": 7.0,
    "latitude": 37.7905277587251,
    "longitude": -122.398709899266,
    "altitude": 10.1174707412700
  },
  {
    "timestamp": 7.05,
    "latitude": 37.7905354916931,
    "longitude": -122.398721254426,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 7.1,
    "latitude": 37.7905432763353,
    "longitude": -122.398732608632,
    "altitude": 10.1171607971190
  },
  {
    "timestamp": 7.15,
    "latitude": 37.7905511126414,
    "longitude": -122.398743961019,
    "altitude": 10.1169099807730
  },
  {
    "timestamp": 7.2,
    "latitude": 37.7905590006064,
    "longitude": -122.398755312626,
    "altitude": 10.1167659759520
  },
  {
    "timestamp": 7.25,
    "latitude": 37.7905669402349,
    "longitude": -122.398766665403,
    "altitude": 10.1168107986400
  },
  {
    "timestamp": 7.3,
    "latitude": 37.7905749315314,
    "longitude": -122.398778019220,
    "altitude": 10.1169395446770
  },
  {
    "timestamp": 7.35,
    "latitude": 37.7905829744989,
    "longitude": -122.398789373859,
    "altitude": 10.1170969009390
  },
  {
    "timestamp": 7.4,
    "latitude": 37.7905910691405,
    "longitude": -122.398800729322,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 7.45,
    "latitude": 37.7905992150465,
    "longitude": -122.398812085439,
    "altitude": 10.1173830032340
  },
  {
    "timestamp": 7.5,
    "latitude": 37.7906074119440,
    "longitude": -122.398823442120,
    "altitude": 10.1174917221060
  },
  {
    "timestamp": 7.55,
    "latitude": 37.7906156598279,
    "longitude": -122.398834797979,
    "altitude": 10.1174545288080
  },
  {
    "timestamp": 7.6,
    "latitude": 37.7906239586991,
    "longitude": -122.398846154271,
    "altitude": 10.1174764633170
  },
  {
    "timestamp": 7.65,
    "latitude": 37.7906323085531,
    "longitude": -122.398857509869,
    "altitude": 10.1173954010000
  },
  {
    "timestamp": 7.7,
    "latitude": 37.7906407093911,
    "longitude": -122.398868865945,
    "altitude": 10.1174020767210
  },
  {
    "timestamp": 7.75,
    "latitude": 37.7906491612148,
    "longitude": -122.398880222540,
    "altitude": 10.1174488067620
  },
  {
    "timestamp": 7.8,
    "latitude": 37.7906576640255,
    "longitude": -122.398891579612,
    "altitude": 10.1175098419180
  },
  {
    "timestamp": 7.85,
    "latitude": 37.7906662178243,
    "longitude": -122.398902937117,
    "altitude": 10.1175699234000
  },
  {
    "timestamp": 7.9,
    "latitude": 37.7906748226116,
    "longitude": -122.398914294925,
    "altitude": 10.1176242828360
  },
  {
    "timestamp": 7.95,
    "latitude": 37.7906834783813,
    "longitude": -122.398925651737,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 8.0,
    "latitude": 37.7906921851336,
    "longitude": -122.398937008809,
    "altitude": 10.1175346374510
  },
  {
    "timestamp": 8.05,
    "latitude": 37.7907009428628,
    "longitude": -122.398948364971,
    "altitude": 10.1174345016470
  },
  {
    "timestamp": 8.1,
    "latitude": 37.7907097515698,
    "longitude": -122.398959721523,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.15,
    "latitude": 37.7907186112557,
    "longitude": -122.398971078508,
    "altitude": 10.1174640655510
  },
  {
    "timestamp": 8.2,
    "latitude": 37.7907275219209,
    "longitude": -122.398982435797,
    "altitude": 10.1175184249870
  },
  {
    "timestamp": 8.25,
    "latitude": 37.7907364830171,
    "longitude": -122.398993793480,
    "altitude": 10.1175756454460
  },
  {
    "timestamp": 8.3,
    "latitude": 37.7907454944005,
    "longitude": -122.399005150081,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.35,
    "latitude": 37.7907545560716,
    "longitude": -122.399016507029,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.4,
    "latitude": 37.7907636680312,
    "longitude": -122.399027864323,
    "altitude": 10.1175327301020
  },
  {
    "timestamp": 8.45,
    "latitude": 37.7907728302797,
    "longitude": -122.399039221921,
    "altitude": 10.1175765991210
  },
  {
    "timestamp": 8.5,
    "latitude": 37.7907820428170,
    "longitude": -122.399050579735,
    "altitude": 10.1176214218100
  },
  {
    "timestamp": 8.55,
    "latitude": 37.7907913056367,
    "longitude": -122.399061936466,
    "altitude": 10.1175374984740
  },
  {
    "timestamp": 8.6,
    "latitude": 37.7908006187389,
    "longitude": -122.399073293457,
    "altitude": 10.1175270080560
  },
  {
    "timestamp": 8.65,
    "latitude": 37.7908099821174,
    "longitude": -122.399084649452,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.7,
    "latitude": 37.7908193957730,
    "longitude": -122.399096005794,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 8.75,
    "latitude": 37.7908288597004,
    "longitude": -122.399107361312,
    "altitude": 10.1173334121700
  },
  {
    "timestamp": 8.8,
    "latitude": 37.7908383739004,
    "longitude": -122.399118717220,
    "altitude": 10.1173448562620
  },
  {
    "timestamp": 8.85,
    "latitude": 37.7908479383745,
    "longitude": -122.399130073648,
    "altitude": 10.1174001693720
  },
  {
    "timestamp": 8.9,
    "latitude": 37.7908575531238,
    "longitude": -122.399141430466,
    "altitude": 10.1174697875970
  },
  {
    "timestamp": 8.95,
    "latitude": 37.7908672181426,
    "longitude": -122.399152786418,
    "altitude": 10.1174125671380
  },
  {
    "timestamp": 9.0,
    "latitude": 37.7908769334252,
    "longitude": -122.399164141460,
    "altitude": 10.1173057556150
  },
  {
    "timestamp": 9.05,
    "latitude": 37.7908866985547,
    "longitude": -122.399175495704,
    "altitude": 10.1171846389770
  },
  {
    "timestamp": 9.1,
    "latitude": 37.7908965132520,
    "longitude": -122.399186849321,
    "altitude": 10.1170701980590
  },
  {
    "timestamp": 9.15,
    "latitude": 37.7909063775135,
    "longitude": -122.399198202441,
    "altitude": 10.1169719696040
  },
  {
    "timestamp": 9.2,
    "latitude": 37.7909162913360,
    "longitude": -122.399209555128,
    "altitude": 10.1168909072870
  },
  {
    "timestamp": 9.25,
    "latitude": 37.7909262547167,
    "longitude": -122.399220907511,
    "altitude": 10.1168279647820
  },
  {
    "timestamp": 9.3,
    "latitude": 37.7909362676598,
    "longitude": -122.399232260890,
    "altitude": 10.1169061660760
  },
  {
    "timestamp": 9.35,
    "latitude": 37.7909463301693,
    "longitude": -122.399243615310,
    "altitude": 10.1170415878290
  },
  {
    "timestamp": 9.4,
    "latitude": 37.7909564422487,
    "longitude": -122.399254970596,
    "altitude": 10.1171903610220
  },
  {
    "timestamp": 9.45,
    "latitude": 37.7909666038942,
    "longitude": -122.399266325384,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 9.5,
    "latitude": 37.7909768151018,
    "longitude": -122.399277679587,
    "altitude": 10.1171512603700
  },
  {
    "timestamp": 9.55,
    "latitude": 37.7909870758744,
    "longitude": -122.399289034569,
    "altitude": 10.1171989440910
  },
  {
    "timestamp": 9.6,
    "latitude": 37.7909973862150,
    "longitude": -122.399300390375,
    "altitude": 10.1172876358030
  },
  {
    "timestamp": 9.65,
    "latitude": 37.7910077461262,
    "longitude": -122.399311746896,
    "altitude": 10.1173849105830
  },
  {
    "timestamp": 9.7,
    "latitude": 37.7910181556101,
    "longitude": -122.399323104023,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 9.75,
    "latitude": 37.7910286146679,
    "longitude": -122.399334461617,
    "altitude": 10.1175584793090
  },
  {
    "timestamp": 9.8,
    "latitude": 37.7910391233006,
    "longitude": -122.399345819621,
    "altitude": 10.1176233291620
  },
  {
    "timestamp": 9.85,
    "latitude": 37.7910496808222,
    "longitude": -122.399357177957,
    "altitude": 10.1176738739010
  },
  {
    "timestamp": 9.9,
    "latitude": 37.7910602872266,
    "longitude": -122.399368535295,
    "altitude": 10.1175851821890
  },
  {
    "timestamp": 9.95,
    "latitude": 37.7910709425141,
    "longitude": -122.399379892916,
    "altitude": 10.1175680160520
  },
  {
    "timestamp": 10.0,
    "latitude": 37.7910816466851,
    "longitude": -122.399391250861,
    "altitude": 10.1175842285150
  },
  {
    "timestamp": 10.05,
    "latitude": 37.7910923997403,
    "longitude": -122.399402609105,
    "altitude": 10.1176166534420
  }
]

Adventure

Basic

解题思路
5

Expensive Sensor

解题思路
LIDAR

Google it

解题思路
330-320直接的某个数字，都尝试一下

Try it

解题思路
LGSVL

Lane Detection

Lane Detection: free drawing

解题思路

GPS Spoofing

GPS Spoofing: GPS is all you got

解题思路
gps.py

f = open('gps.json', 'r')
gps = f.read()
f.close()
gpslines = gps.split('n')
pos = []
for line in gpslines:
  i0 = line.find('timestamp')
  if i0 >= 0:
    ti = line[i0+12:-1]
  i1 = line.find('latitude')
  if i1 >= 0:
    la = float(line[i1+11:-1])
  i2 = line.find('longitude')
  if i2 >= 0:
    lo = float(line[i2+12:-1])
  i3 = line.find('altitude')
  if i3 >= 0:
    al = float(line[i3+11:-1])
    pos.append( [la, lo, al, ti] )

rate = (0.0107700551979-0.000017) / 0.0107700551979
print rate
for i in range(len(pos) - 1):
  pos[1 + i][0] = rate*(pos[1+i][0] - pos[0][0]) + pos[i][0]

f = open('gps_new.json', 'w')
f.write('[n')
for i in range(len(pos)):
  f.write('  {n')
  f.write('    "timestamp": %s,n' % pos[i][3])
  f.write('    "latitude": %.13f,n' % pos[i][0])
  f.write('    "longitude": %.12f,n' % pos[i][1])
  f.write('    "altitude": %.13fn' % pos[i][2])
  if i == len(pos) - 1:
    f.write('  }n')
  else:
    f.write('  },n')
f.write(']')
f.close()

gps_new.json

[
  {
    "timestamp": 0.0,
    "latitude": 37.7899753693032,
    "longitude": -122.397121279501,
    "altitude": 10.1277933120720
  },
  {
    "timestamp": 0.05,
    "latitude": 37.7899754265434,
    "longitude": -122.397132214792,
    "altitude": 10.1244440078730
  },
  {
    "timestamp": 0.1,
    "latitude": 37.7899755414654,
    "longitude": -122.397143236731,
    "altitude": 10.1220254898070
  },
  {
    "timestamp": 0.15,
    "latitude": 37.7899757143859,
    "longitude": -122.397154347742,
    "altitude": 10.1203002929680
  },
  {
    "timestamp": 0.2,
    "latitude": 37.7899759458176,
    "longitude": -122.397165532403,
    "altitude": 10.1192083358760
  },
  {
    "timestamp": 0.25,
    "latitude": 37.7899762360459,
    "longitude": -122.397176773210,
    "altitude": 10.1185302734370
  },
  {
    "timestamp": 0.3,
    "latitude": 37.7899765851408,
    "longitude": -122.397188054742,
    "altitude": 10.1180019378660
  },
  {
    "timestamp": 0.35,
    "latitude": 37.7899769933924,
    "longitude": -122.397199366426,
    "altitude": 10.1177244186400
  },
  {
    "timestamp": 0.4,
    "latitude": 37.7899774602113,
    "longitude": -122.397210697351,
    "altitude": 10.1174736022940
  },
  {
    "timestamp": 0.45,
    "latitude": 37.7899779856691,
    "longitude": -122.397222042486,
    "altitude": 10.1173887252800
  },
  {
    "timestamp": 0.5,
    "latitude": 37.7899785698098,
    "longitude": -122.397233396459,
    "altitude": 10.1173906326290
  },
  {
    "timestamp": 0.55,
    "latitude": 37.7899792122478,
    "longitude": -122.397244755808,
    "altitude": 10.1174354553220
  },
  {
    "timestamp": 0.6,
    "latitude": 37.7899799127243,
    "longitude": -122.397256118452,
    "altitude": 10.1174955368040
  },
  {
    "timestamp": 0.65,
    "latitude": 37.7899806712363,
    "longitude": -122.397267480749,
    "altitude": 10.1174316406200
  },
  {
    "timestamp": 0.7,
    "latitude": 37.7899814876491,
    "longitude": -122.397278843740,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 0.75,
    "latitude": 37.7899823615452,
    "longitude": -122.397290205868,
    "altitude": 10.1173601150510
  },
  {
    "timestamp": 0.8,
    "latitude": 37.7899832927887,
    "longitude": -122.397301568517,
    "altitude": 10.1173706054680
  },
  {
    "timestamp": 0.85,
    "latitude": 37.7899842815179,
    "longitude": -122.397312931512,
    "altitude": 10.1174211502070
  },
  {
    "timestamp": 0.9,
    "latitude": 37.7899853275968,
    "longitude": -122.397324295028,
    "altitude": 10.1174869537350
  },
  {
    "timestamp": 0.95,
    "latitude": 37.7899864310199,
    "longitude": -122.397335657677,
    "altitude": 10.1174249649040
  },
  {
    "timestamp": 1.0,
    "latitude": 37.7899875917800,
    "longitude": -122.397347019113,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 1.05,
    "latitude": 37.7899888098787,
    "longitude": -122.397358381069,
    "altitude": 10.1173133850090
  },
  {
    "timestamp": 1.1,
    "latitude": 37.7899900847674,
    "longitude": -122.397369743377,
    "altitude": 10.1173658370970
  },
  {
    "timestamp": 1.15,
    "latitude": 37.7899914163023,
    "longitude": -122.397381104645,
    "altitude": 10.1173114776610
  },
  {
    "timestamp": 1.2,
    "latitude": 37.7899928044823,
    "longitude": -122.397392465914,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 1.25,
    "latitude": 37.7899942493082,
    "longitude": -122.397403827529,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 1.3,
    "latitude": 37.7899957507807,
    "longitude": -122.397415189491,
    "altitude": 10.1174774169920
  },
  {
    "timestamp": 1.35,
    "latitude": 37.7899973088924,
    "longitude": -122.397426550240,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 1.4,
    "latitude": 37.7899989236441,
    "longitude": -122.397437911336,
    "altitude": 10.1174364089960
  },
  {
    "timestamp": 1.45,
    "latitude": 37.7900005950354,
    "longitude": -122.397449272604,
    "altitude": 10.1174831390380
  },
  {
    "timestamp": 1.5,
    "latitude": 37.7900023230663,
    "longitude": -122.397460634047,
    "altitude": 10.1175384521480
  },
  {
    "timestamp": 1.55,
    "latitude": 37.7900041077364,
    "longitude": -122.397471995662,
    "altitude": 10.1175937652580
  },
  {
    "timestamp": 1.6,
    "latitude": 37.7900059490447,
    "longitude": -122.397483357278,
    "altitude": 10.1176424026480
  },
  {
    "timestamp": 1.65,
    "latitude": 37.7900078469830,
    "longitude": -122.397494717507,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 1.7,
    "latitude": 37.7900098015504,
    "longitude": -122.397506077736,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 1.75,
    "latitude": 37.7900118127473,
    "longitude": -122.397517438312,
    "altitude": 10.1175651550290
  },
  {
    "timestamp": 1.8,
    "latitude": 37.7900138805727,
    "longitude": -122.397528798888,
    "altitude": 10.1175994873040
  },
  {
    "timestamp": 1.85,
    "latitude": 37.7900160043389,
    "longitude": -122.397540159470,
    "altitude": 10.1176385879510
  },
  {
    "timestamp": 1.9,
    "latitude": 37.7900181840450,
    "longitude": -122.397551520051,
    "altitude": 10.1176729202270
  },
  {
    "timestamp": 1.95,
    "latitude": 37.7900204196836,
    "longitude": -122.397562879420,
    "altitude": 10.1175775527950
  },
  {
    "timestamp": 2.0,
    "latitude": 37.7900227112465,
    "longitude": -122.397574237402,
    "altitude": 10.1174325942990
  },
  {
    "timestamp": 2.05,
    "latitude": 37.7900250587336,
    "longitude": -122.397585595557,
    "altitude": 10.1174049377440
  },
  {
    "timestamp": 2.1,
    "latitude": 37.7900274621393,
    "longitude": -122.397596952847,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 2.15,
    "latitude": 37.7900299214635,
    "longitude": -122.397608310309,
    "altitude": 10.1173181533810
  },
  {
    "timestamp": 2.2,
    "latitude": 37.7900324367004,
    "longitude": -122.397619666905,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 2.25,
    "latitude": 37.7900350078510,
    "longitude": -122.397631023848,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 2.3,
    "latitude": 37.7900376349166,
    "longitude": -122.397642381310,
    "altitude": 10.1173467636100
  },
  {
    "timestamp": 2.35,
    "latitude": 37.7900403178919,
    "longitude": -122.397653737906,
    "altitude": 10.1173048019400
  },
  {
    "timestamp": 2.4,
    "latitude": 37.7900430567774,
    "longitude": -122.397665094849,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 2.45,
    "latitude": 37.7900458515678,
    "longitude": -122.397676450925,
    "altitude": 10.1172819137570
  },
  {
    "timestamp": 2.5,
    "latitude": 37.7900487022645,
    "longitude": -122.397687807521,
    "altitude": 10.1173124313350
  },
  {
    "timestamp": 2.55,
    "latitude": 37.7900516088691,
    "longitude": -122.397699164638,
    "altitude": 10.1173801422110
  },
  {
    "timestamp": 2.6,
    "latitude": 37.7900545713823,
    "longitude": -122.397710522100,
    "altitude": 10.1174583435050
  },
  {
    "timestamp": 2.65,
    "latitude": 37.7900575895309,
    "longitude": -122.397721880085,
    "altitude": 10.1175317764280
  },
  {
    "timestamp": 2.7,
    "latitude": 37.7900606628968,
    "longitude": -122.397733237034,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 2.75,
    "latitude": 37.7900637914735,
    "longitude": -122.397744592943,
    "altitude": 10.1173553466790
  },
  {
    "timestamp": 2.8,
    "latitude": 37.7900669752625,
    "longitude": -122.397755949371,
    "altitude": 10.1173486709590
  },
  {
    "timestamp": 2.85,
    "latitude": 37.7900702142654,
    "longitude": -122.397767306320,
    "altitude": 10.1173944473260
  },
  {
    "timestamp": 2.9,
    "latitude": 37.7900735084767,
    "longitude": -122.397778662402,
    "altitude": 10.1173362731930
  },
  {
    "timestamp": 2.95,
    "latitude": 37.7900768578972,
    "longitude": -122.397790018831,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 3.0,
    "latitude": 37.7900802625282,
    "longitude": -122.397801375779,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 3.05,
    "latitude": 37.7900837223706,
    "longitude": -122.397812733075,
    "altitude": 10.1174898147580
  },
  {
    "timestamp": 3.1,
    "latitude": 37.7900872374250,
    "longitude": -122.397824090717,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 3.15,
    "latitude": 37.7900908076859,
    "longitude": -122.397835447492,
    "altitude": 10.1174907684320
  },
  {
    "timestamp": 3.2,
    "latitude": 37.7900944331540,
    "longitude": -122.397846804614,
    "altitude": 10.1174936294550
  },
  {
    "timestamp": 3.25,
    "latitude": 37.7900981138227,
    "longitude": -122.397858160697,
    "altitude": 10.1174030303950
  },
  {
    "timestamp": 3.3,
    "latitude": 37.7901018496929,
    "longitude": -122.397869517126,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 3.35,
    "latitude": 37.7901056407599,
    "longitude": -122.397880872861,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 3.4,
    "latitude": 37.7901094870182,
    "longitude": -122.397892227731,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 3.45,
    "latitude": 37.7901133881886,
    "longitude": -122.397903581909,
    "altitude": 10.1171007156370
  },
  {
    "timestamp": 3.5,
    "latitude": 37.7901173438544,
    "longitude": -122.397914935398,
    "altitude": 10.1169986724850
  },
  {
    "timestamp": 3.55,
    "latitude": 37.7901213540128,
    "longitude": -122.397926288540,
    "altitude": 10.1169157028190
  },
  {
    "timestamp": 3.6,
    "latitude": 37.7901254186603,
    "longitude": -122.397937641163,
    "altitude": 10.1168479919430
  },
  {
    "timestamp": 3.65,
    "latitude": 37.7901295377954,
    "longitude": -122.397948993785,
    "altitude": 10.1167964935300
  },
  {
    "timestamp": 3.7,
    "latitude": 37.7901337114227,
    "longitude": -122.397960347447,
    "altitude": 10.1168823242180
  },
  {
    "timestamp": 3.75,
    "latitude": 37.7901379395461,
    "longitude": -122.397971702149,
    "altitude": 10.1170234680170
  },
  {
    "timestamp": 3.8,
    "latitude": 37.7901422221700,
    "longitude": -122.397983057891,
    "altitude": 10.1171770095820
  },
  {
    "timestamp": 3.85,
    "latitude": 37.7901465592959,
    "longitude": -122.397994414152,
    "altitude": 10.1173191070550
  },
  {
    "timestamp": 3.9,
    "latitude": 37.7901509509200,
    "longitude": -122.398005769894,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 3.95,
    "latitude": 37.7901553970439,
    "longitude": -122.398017126156,
    "altitude": 10.1173677444450
  },
  {
    "timestamp": 4.0,
    "latitude": 37.7901598976691,
    "longitude": -122.398028482938,
    "altitude": 10.1174392700190
  },
  {
    "timestamp": 4.05,
    "latitude": 37.7901644527987,
    "longitude": -122.398039840499,
    "altitude": 10.1175127029410
  },
  {
    "timestamp": 4.1,
    "latitude": 37.7901690624332,
    "longitude": -122.398051198407,
    "altitude": 10.1175804138180
  },
  {
    "timestamp": 4.15,
    "latitude": 37.7901737265738,
    "longitude": -122.398062556748,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 4.2,
    "latitude": 37.7901784452210,
    "longitude": -122.398073915436,
    "altitude": 10.1176815032950
  },
  {
    "timestamp": 4.25,
    "latitude": 37.7901832178247,
    "longitude": -122.398085274129,
    "altitude": 10.1177158355710
  },
  {
    "timestamp": 4.3,
    "latitude": 37.7901880442420,
    "longitude": -122.398096631956,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 4.35,
    "latitude": 37.7901929244722,
    "longitude": -122.398107989870,
    "altitude": 10.1175899505610
  },
  {
    "timestamp": 4.4,
    "latitude": 37.7901978585161,
    "longitude": -122.398119348130,
    "altitude": 10.1175985336300
  },
  {
    "timestamp": 4.45,
    "latitude": 37.7902028463666,
    "longitude": -122.398130705264,
    "altitude": 10.1174993515010
  },
  {
    "timestamp": 4.5,
    "latitude": 37.7902078880181,
    "longitude": -122.398142061445,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.55,
    "latitude": 37.7902129834647,
    "longitude": -122.398153416760,
    "altitude": 10.1172180175780
  },
  {
    "timestamp": 4.6,
    "latitude": 37.7902181327083,
    "longitude": -122.398164772594,
    "altitude": 10.1172151565550
  },
  {
    "timestamp": 4.65,
    "latitude": 37.7902233357502,
    "longitude": -122.398176128949,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 4.7,
    "latitude": 37.7902285925861,
    "longitude": -122.398187484610,
    "altitude": 10.1172380447380
  },
  {
    "timestamp": 4.75,
    "latitude": 37.7902339032172,
    "longitude": -122.398198840791,
    "altitude": 10.1172828674310
  },
  {
    "timestamp": 4.8,
    "latitude": 37.7902392676462,
    "longitude": -122.398210197665,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.85,
    "latitude": 37.7902446858735,
    "longitude": -122.398221554886,
    "altitude": 10.1174459457390
  },
  {
    "timestamp": 4.9,
    "latitude": 37.7902501578997,
    "longitude": -122.398232912367,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 4.95,
    "latitude": 37.7902556837195,
    "longitude": -122.398244269068,
    "altitude": 10.1174678802400
  },
  {
    "timestamp": 5.0,
    "latitude": 37.7902612633335,
    "longitude": -122.398255626116,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 5.05,
    "latitude": 37.7902668961933,
    "longitude": -122.398266983515,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 5.1,
    "latitude": 37.7902725821561,
    "longitude": -122.398278340048,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 5.15,
    "latitude": 37.7902783212225,
    "longitude": -122.398289696929,
    "altitude": 10.1174468994140
  },
  {
    "timestamp": 5.2,
    "latitude": 37.7902841133799,
    "longitude": -122.398301051556,
    "altitude": 10.1172370910640
  },
  {
    "timestamp": 5.25,
    "latitude": 37.7902899586237,
    "longitude": -122.398312405490,
    "altitude": 10.1170768737790
  },
  {
    "timestamp": 5.3,
    "latitude": 37.7902958569563,
    "longitude": -122.398323760117,
    "altitude": 10.1170806884760
  },
  {
    "timestamp": 5.35,
    "latitude": 37.7903018083750,
    "longitude": -122.398335114398,
    "altitude": 10.1170358657830
  },
  {
    "timestamp": 5.4,
    "latitude": 37.7903078128825,
    "longitude": -122.398346469459,
    "altitude": 10.1170988082880
  },
  {
    "timestamp": 5.45,
    "latitude": 37.7903138704808,
    "longitude": -122.398357825126,
    "altitude": 10.1172056198100
  },
  {
    "timestamp": 5.5,
    "latitude": 37.7903199811726,
    "longitude": -122.398369181487,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 5.55,
    "latitude": 37.7903261449596,
    "longitude": -122.398380538454,
    "altitude": 10.1174306869500
  },
  {
    "timestamp": 5.6,
    "latitude": 37.7903323618431,
    "longitude": -122.398391895854,
    "altitude": 10.1175231933590
  },
  {
    "timestamp": 5.65,
    "latitude": 37.7903386318175,
    "longitude": -122.398403252388,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 5.7,
    "latitude": 37.7903449548840,
    "longitude": -122.398414609355,
    "altitude": 10.1174850463860
  },
  {
    "timestamp": 5.75,
    "latitude": 37.7903513310431,
    "longitude": -122.398425966669,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 5.8,
    "latitude": 37.7903577602899,
    "longitude": -122.398437323203,
    "altitude": 10.1174497604300
  },
  {
    "timestamp": 5.85,
    "latitude": 37.7903642420630,
    "longitude": -122.398448677575,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 5.9,
    "latitude": 37.7903707762270,
    "longitude": -122.398460032555,
    "altitude": 10.1171531677240
  },
  {
    "timestamp": 5.95,
    "latitude": 37.7903773627769,
    "longitude": -122.398471386755,
    "altitude": 10.1170740127560
  },
  {
    "timestamp": 6.0,
    "latitude": 37.7903840017165,
    "longitude": -122.398482741908,
    "altitude": 10.1171169281000
  },
  {
    "timestamp": 6.05,
    "latitude": 37.7903906930487,
    "longitude": -122.398494097842,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 6.1,
    "latitude": 37.7903974367754,
    "longitude": -122.398505454381,
    "altitude": 10.1173210144040
  },
  {
    "timestamp": 6.15,
    "latitude": 37.7904042328987,
    "longitude": -122.398516811528,
    "altitude": 10.1174259185790
  },
  {
    "timestamp": 6.2,
    "latitude": 37.7904110814197,
    "longitude": -122.398528169107,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 6.25,
    "latitude": 37.7904179823390,
    "longitude": -122.398539527033,
    "altitude": 10.1175928115840
  },
  {
    "timestamp": 6.3,
    "latitude": 37.7904249356573,
    "longitude": -122.398550885306,
    "altitude": 10.1176500320430
  },
  {
    "timestamp": 6.35,
    "latitude": 37.7904319413739,
    "longitude": -122.398562243665,
    "altitude": 10.1176948547360
  },
  {
    "timestamp": 6.4,
    "latitude": 37.7904389994896,
    "longitude": -122.398573602371,
    "altitude": 10.1177272796630
  },
  {
    "timestamp": 6.45,
    "latitude": 37.7904461100037,
    "longitude": -122.398584961164,
    "altitude": 10.1177511215200
  },
  {
    "timestamp": 6.5,
    "latitude": 37.7904532729160,
    "longitude": -122.398596320130,
    "altitude": 10.1177663803100
  },
  {
    "timestamp": 6.55,
    "latitude": 37.7904604882192,
    "longitude": -122.398607677883,
    "altitude": 10.1176519393920
  },
  {
    "timestamp": 6.6,
    "latitude": 37.7904677559127,
    "longitude": -122.398619035723,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 6.65,
    "latitude": 37.7904750753096,
    "longitude": -122.398630393742,
    "altitude": 10.1176176071160
  },
  {
    "timestamp": 6.7,
    "latitude": 37.7904824464103,
    "longitude": -122.398641752020,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 6.75,
    "latitude": 37.7904898692140,
    "longitude": -122.398653110385,
    "altitude": 10.1176633834830
  },
  {
    "timestamp": 6.8,
    "latitude": 37.7904973437199,
    "longitude": -122.398664468751,
    "altitude": 10.1176910400390
  },
  {
    "timestamp": 6.85,
    "latitude": 37.7905048699274,
    "longitude": -122.398675827289,
    "altitude": 10.1177148818900
  },
  {
    "timestamp": 6.9,
    "latitude": 37.7905124478357,
    "longitude": -122.398687185828,
    "altitude": 10.1177368164060
  },
  {
    "timestamp": 6.95,
    "latitude": 37.7905200774373,
    "longitude": -122.398698543154,
    "altitude": 10.1176271438590
  },
  {
    "timestamp": 7.0,
    "latitude": 37.7905277587251,
    "longitude": -122.398709899266,
    "altitude": 10.1174707412700
  },
  {
    "timestamp": 7.05,
    "latitude": 37.7905354916931,
    "longitude": -122.398721254426,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 7.1,
    "latitude": 37.7905432763353,
    "longitude": -122.398732608632,
    "altitude": 10.1171607971190
  },
  {
    "timestamp": 7.15,
    "latitude": 37.7905511126414,
    "longitude": -122.398743961019,
    "altitude": 10.1169099807730
  },
  {
    "timestamp": 7.2,
    "latitude": 37.7905590006064,
    "longitude": -122.398755312626,
    "altitude": 10.1167659759520
  },
  {
    "timestamp": 7.25,
    "latitude": 37.7905669402349,
    "longitude": -122.398766665403,
    "altitude": 10.1168107986400
  },
  {
    "timestamp": 7.3,
    "latitude": 37.7905749315314,
    "longitude": -122.398778019220,
    "altitude": 10.1169395446770
  },
  {
    "timestamp": 7.35,
    "latitude": 37.7905829744989,
    "longitude": -122.398789373859,
    "altitude": 10.1170969009390
  },
  {
    "timestamp": 7.4,
    "latitude": 37.7905910691405,
    "longitude": -122.398800729322,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 7.45,
    "latitude": 37.7905992150465,
    "longitude": -122.398812085439,
    "altitude": 10.1173830032340
  },
  {
    "timestamp": 7.5,
    "latitude": 37.7906074119440,
    "longitude": -122.398823442120,
    "altitude": 10.1174917221060
  },
  {
    "timestamp": 7.55,
    "latitude": 37.7906156598279,
    "longitude": -122.398834797979,
    "altitude": 10.1174545288080
  },
  {
    "timestamp": 7.6,
    "latitude": 37.7906239586991,
    "longitude": -122.398846154271,
    "altitude": 10.1174764633170
  },
  {
    "timestamp": 7.65,
    "latitude": 37.7906323085531,
    "longitude": -122.398857509869,
    "altitude": 10.1173954010000
  },
  {
    "timestamp": 7.7,
    "latitude": 37.7906407093911,
    "longitude": -122.398868865945,
    "altitude": 10.1174020767210
  },
  {
    "timestamp": 7.75,
    "latitude": 37.7906491612148,
    "longitude": -122.398880222540,
    "altitude": 10.1174488067620
  },
  {
    "timestamp": 7.8,
    "latitude": 37.7906576640255,
    "longitude": -122.398891579612,
    "altitude": 10.1175098419180
  },
  {
    "timestamp": 7.85,
    "latitude": 37.7906662178243,
    "longitude": -122.398902937117,
    "altitude": 10.1175699234000
  },
  {
    "timestamp": 7.9,
    "latitude": 37.7906748226116,
    "longitude": -122.398914294925,
    "altitude": 10.1176242828360
  },
  {
    "timestamp": 7.95,
    "latitude": 37.7906834783813,
    "longitude": -122.398925651737,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 8.0,
    "latitude": 37.7906921851336,
    "longitude": -122.398937008809,
    "altitude": 10.1175346374510
  },
  {
    "timestamp": 8.05,
    "latitude": 37.7907009428628,
    "longitude": -122.398948364971,
    "altitude": 10.1174345016470
  },
  {
    "timestamp": 8.1,
    "latitude": 37.7907097515698,
    "longitude": -122.398959721523,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.15,
    "latitude": 37.7907186112557,
    "longitude": -122.398971078508,
    "altitude": 10.1174640655510
  },
  {
    "timestamp": 8.2,
    "latitude": 37.7907275219209,
    "longitude": -122.398982435797,
    "altitude": 10.1175184249870
  },
  {
    "timestamp": 8.25,
    "latitude": 37.7907364830171,
    "longitude": -122.398993793480,
    "altitude": 10.1175756454460
  },
  {
    "timestamp": 8.3,
    "latitude": 37.7907454944005,
    "longitude": -122.399005150081,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.35,
    "latitude": 37.7907545560716,
    "longitude": -122.399016507029,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.4,
    "latitude": 37.7907636680312,
    "longitude": -122.399027864323,
    "altitude": 10.1175327301020
  },
  {
    "timestamp": 8.45,
    "latitude": 37.7907728302797,
    "longitude": -122.399039221921,
    "altitude": 10.1175765991210
  },
  {
    "timestamp": 8.5,
    "latitude": 37.7907820428170,
    "longitude": -122.399050579735,
    "altitude": 10.1176214218100
  },
  {
    "timestamp": 8.55,
    "latitude": 37.7907913056367,
    "longitude": -122.399061936466,
    "altitude": 10.1175374984740
  },
  {
    "timestamp": 8.6,
    "latitude": 37.7908006187389,
    "longitude": -122.399073293457,
    "altitude": 10.1175270080560
  },
  {
    "timestamp": 8.65,
    "latitude": 37.7908099821174,
    "longitude": -122.399084649452,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.7,
    "latitude": 37.7908193957730,
    "longitude": -122.399096005794,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 8.75,
    "latitude": 37.7908288597004,
    "longitude": -122.399107361312,
    "altitude": 10.1173334121700
  },
  {
    "timestamp": 8.8,
    "latitude": 37.7908383739004,
    "longitude": -122.399118717220,
    "altitude": 10.1173448562620
  },
  {
    "timestamp": 8.85,
    "latitude": 37.7908479383745,
    "longitude": -122.399130073648,
    "altitude": 10.1174001693720
  },
  {
    "timestamp": 8.9,
    "latitude": 37.7908575531238,
    "longitude": -122.399141430466,
    "altitude": 10.1174697875970
  },
  {
    "timestamp": 8.95,
    "latitude": 37.7908672181426,
    "longitude": -122.399152786418,
    "altitude": 10.1174125671380
  },
  {
    "timestamp": 9.0,
    "latitude": 37.7908769334252,
    "longitude": -122.399164141460,
    "altitude": 10.1173057556150
  },
  {
    "timestamp": 9.05,
    "latitude": 37.7908866985547,
    "longitude": -122.399175495704,
    "altitude": 10.1171846389770
  },
  {
    "timestamp": 9.1,
    "latitude": 37.7908965132520,
    "longitude": -122.399186849321,
    "altitude": 10.1170701980590
  },
  {
    "timestamp": 9.15,
    "latitude": 37.7909063775135,
    "longitude": -122.399198202441,
    "altitude": 10.1169719696040
  },
  {
    "timestamp": 9.2,
    "latitude": 37.7909162913360,
    "longitude": -122.399209555128,
    "altitude": 10.1168909072870
  },
  {
    "timestamp": 9.25,
    "latitude": 37.7909262547167,
    "longitude": -122.399220907511,
    "altitude": 10.1168279647820
  },
  {
    "timestamp": 9.3,
    "latitude": 37.7909362676598,
    "longitude": -122.399232260890,
    "altitude": 10.1169061660760
  },
  {
    "timestamp": 9.35,
    "latitude": 37.7909463301693,
    "longitude": -122.399243615310,
    "altitude": 10.1170415878290
  },
  {
    "timestamp": 9.4,
    "latitude": 37.7909564422487,
    "longitude": -122.399254970596,
    "altitude": 10.1171903610220
  },
  {
    "timestamp": 9.45,
    "latitude": 37.7909666038942,
    "longitude": -122.399266325384,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 9.5,
    "latitude": 37.7909768151018,
    "longitude": -122.399277679587,
    "altitude": 10.1171512603700
  },
  {
    "timestamp": 9.55,
    "latitude": 37.7909870758744,
    "longitude": -122.399289034569,
    "altitude": 10.1171989440910
  },
  {
    "timestamp": 9.6,
    "latitude": 37.7909973862150,
    "longitude": -122.399300390375,
    "altitude": 10.1172876358030
  },
  {
    "timestamp": 9.65,
    "latitude": 37.7910077461262,
    "longitude": -122.399311746896,
    "altitude": 10.1173849105830
  },
  {
    "timestamp": 9.7,
    "latitude": 37.7910181556101,
    "longitude": -122.399323104023,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 9.75,
    "latitude": 37.7910286146679,
    "longitude": -122.399334461617,
    "altitude": 10.1175584793090
  },
  {
    "timestamp": 9.8,
    "latitude": 37.7910391233006,
    "longitude": -122.399345819621,
    "altitude": 10.1176233291620
  },
  {
    "timestamp": 9.85,
    "latitude": 37.7910496808222,
    "longitude": -122.399357177957,
    "altitude": 10.1176738739010
  },
  {
    "timestamp": 9.9,
    "latitude": 37.7910602872266,
    "longitude": -122.399368535295,
    "altitude": 10.1175851821890
  },
  {
    "timestamp": 9.95,
    "latitude": 37.7910709425141,
    "longitude": -122.399379892916,
    "altitude": 10.1175680160520
  },
  {
    "timestamp": 10.0,
    "latitude": 37.7910816466851,
    "longitude": -122.399391250861,
    "altitude": 10.1175842285150
  },
  {
    "timestamp": 10.05,
    "latitude": 37.7910923997403,
    "longitude": -122.399402609105,
    "altitude": 10.1176166534420
  }
]

Lane Detection: dirty road patch

解题思路
1111

Lane Detection: targeted attack

解题思路
答案和上一题一样

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
#!/usr/bin/env python3

import random
import cv2
import numpy as np
from collections import Counter
from simple_pid import PID
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, deltaE_cie76
from PIL import Image

# Stanley controller parameters
k_e = 0.3
k_v = 0.01
delta_steer_per_iter = 0.1

#########################################################
# Some utility functions. Define new ones as needed.
#########################################################

def waypoint_distance(waypt1: list, waypt2: list) -> float:
    return np.sqrt(np.sum((np.array(waypt1) - np.array(waypt2))**2))

def normalize_angle(angle: float) -> float:
    while angle > np.pi:
        angle -= 2.0*np.pi
    while angle < -np.pi:
        angle += 2.0*np.pi
    return angle

def preprocess_image(cv_img: np.ndarray) -> np.ndarray:
    # resize to have less pixels
    cv_img = cv2.resize(cv_img, (416, 416), interpolation=cv2.INTER_AREA)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    if cv_img.shape[0] == 3:
        rgb_img = np.transpose(cv_img, (1, 2, 0))
    else:
        rgb_img = cv_img
    return rgb_img

#########################################################
# Main control logic for the Autonomous Driving Car (ADC)
#########################################################

class Controller:
    def __init__(self):
        self.speed_pid = PID(1.0, 0.1, 0.01, setpoint=5)
        self.speed_pid.sample_time = 0.01
        self.speed_pid.output_limits = (-1, 1)
        self.counter = 0
        self.last_steering = 0
        self.last_throttle = 0
        self.plan_waypts = []

    #########################################################
    # TODO: Players should implement get_control() with their
    # own control logic to achieve the attack goal
    #########################################################

    def get_control(self, adc_pose: list, adc_speed: float, adc_yaw: float, adc_frame: np.ndarray, npc_poses: list) -> (float, float):
        """
        Control logic for ADC. This function will be invoked at each control iteration.
        @param self
        @param adc_pose list: ADC's current 2D position in east and north directions
        @param adc_speed float: ADC's current speed
        @param adc_yaw float: ADC's current heading in radians
        @param adc_frame numpy.ndarray: ADC's front camera frame, shape=(1080, 1920, 3)
        @param npc_poses list(list): The positions of NPCs as an array of 2D arrays
        """
        # Note: Below is a sample implementation, you are free to modify it and
        #       add new functions as needed as long as this function will return
        #       and only returns steering and throttle

        # sample usages of functions and inputs
        adc_frame_preprocessed = preprocess_image(adc_frame)
        for i in range(len(npc_poses)):
            dist = waypoint_distance(adc_pose, npc_poses[i])
            print("ADC distance to {}th NPC is {}m".format(i, dist))

        if len(npc_poses) > 0:
            self.plan_waypts = [adc_pose, npc_poses[0]]
        steering = self.lateral_control(self.plan_waypts, adc_pose, adc_speed, adc_yaw, self.last_steering)
        if dist > 150:
          dist = 150
        throttle = self.longitudinal_control(adc_speed, dist)
        #steering = 0.0
        #throttle = 0.05

        self.counter += 1
        self.last_steering = steering
        self.last_throttle = throttle

        # Note: steering: +: steer to right, -: steer to left
        #       throttle: +: speed up, -: slow down
        #       both are limited in the range (-1, 1)
        return steering, throttle

    def lateral_control(self, plan_waypts: list, curr_waypt: list, v: float, yaw: float, pre_steer: float, is_return: bool = False) -> float:
        """
        create lateral controller.
        @param self
        @param plan_waypts list: planned trajectory, i.e., a list of waypoints, should contain at least two waypoints
        @param curr_waypt list: ADC's current 2D position
        @param v float: ADC speed
        @param yaw float: ADC yaw in radians
        @param pre_steer float: previous steering
        @param is_return bool: if the ADC is returning the starting point
        """
        # Ref: https://www.ri.cmu.edu/pub_files/2009/2/Automatic_Steering_Methods_for_Autonomous_Automobile_Path_Tracking.pdf
        yaw_path = np.arctan2(plan_waypts[-1][1] - plan_waypts[0][1], plan_waypts[-1][0] - plan_waypts[0][0])
        yaw_diff = normalize_angle(yaw_path - yaw)
        crosstrack_error = np.sqrt(
            np.min(np.sum((np.array(curr_waypt) - np.array(plan_waypts)) ** 2, axis=1)))
        yaw_crosstrack = np.arctan2(curr_waypt[1] - plan_waypts[0][1], curr_waypt[0] - plan_waypts[0][0])
        yaw_path2ct = normalize_angle(yaw_path - yaw_crosstrack)
        if yaw_path2ct > 0:
            crosstrack_error = abs(crosstrack_error)
        else:
            crosstrack_error = -abs(crosstrack_error)
        yaw_diff_crosstrack = np.arctan(k_e * crosstrack_error / (k_v + v))
        steer = normalize_angle(yaw_diff + yaw_diff_crosstrack)
        steer = -np.clip(steer, -1., 1.)
        if is_return:
            steer_limited = np.clip(steer, pre_steer - 3*delta_steer_per_iter, pre_steer + 3*delta_steer_per_iter)
        else:
            steer_limited = np.clip(steer, pre_steer - delta_steer_per_iter, pre_steer + delta_steer_per_iter)
        return steer_limited

    def longitudinal_control(self, v: float, t_v: float) -> float:
        """
        create longitudinal controller.
        @param self
        @param v float: input ADC speed
        @param t_v float: target speed
        """
        self.speed_pid.setpoint = t_v
        throttle = self.speed_pid(v)
        return throttle
```



```
f = open('npc_benign.json', 'r')
gps = f.read()
f.close()
gpslines = gps.split('n')
pos = []
for line in gpslines:
  i0 = line.find('timestamp')
  if i0 >= 0:
    ti = line[i0+12:-1]
  i1 = line.find('latitude')
  if i1 >= 0:
    la = float(line[i1+11:-1])
  i2 = line.find('longitude')
  if i2 >= 0:
    lo = float(line[i2+12:-1])
  i3 = line.find('altitude')
  if i3 >= 0:
    al = float(line[i3+11:-1])
  i3 = line.find('roll')
  if i3 >= 0:
    ro = float(line[i3+7:-1])
  i3 = line.find('pitch')
  if i3 >= 0:
    pi = line[i3+8:-1]
  i3 = line.find('yaw')
  if i3 >= 0:
    ya = line[i3+6:-1]
  i3 = line.find('speed')
  if i3 >= 0:
    sp = line[i3+8:]
    pos.append( [la, lo, al, ti, ro, pi, ya, sp] )

rate = 1.2
print rate
for i in range(len(pos) - 120):
  pos[120 + i][0] = rate*(pos[120][0] - pos[399][0]) + pos[120 + i][0]
f = open('gps_new.json', 'w')
f.write('[n')
for i in range(len(pos)):
  f.write('  {n')
  f.write('    "timestamp": %s,n' % pos[i][3])
  f.write('    "latitude": %.12f,n' % pos[i][0])
  f.write('    "longitude": %s,n' % pos[i][1])
  f.write('    "altitude": %s,n' % pos[i][2])
  f.write('    "roll": %s,n' % pos[i][4])
  f.write('    "pitch": %s,n' % pos[i][5])
  f.write('    "yaw": %s,n' % pos[i][6])
  f.write('    "speed": %sn' % pos[i][7])
  if i == len(pos) - 1:
    f.write('  }n')
  else:
    f.write('  },n')
f.write(']')
f.close()
```



```
[
  {
    "timestamp": 0.0,
    "latitude": 37.789961912203,
    "longitude": -122.401553978,
    "altitude": 10.2880001068,
    "roll": 0.0,
    "pitch": 0,
    "yaw": 1.00179122455302e-05,
    "speed": 20.0
  },
  {
    "timestamp": 0.05,
    "latitude": 37.789961854541,
    "longitude": -122.401542626,
    "altitude": 10.2728290558,
    "roll": 0.00087853212608,
    "pitch": 4.37385324403294e-06,
    "yaw": 1.08999765870976e-05,
    "speed": 19.986112009053592
  },
  {
    "timestamp": 0.1,
    "latitude": 37.789961797602,
    "longitude": -122.401531416,
    "altitude": 10.245757103,
    "roll": 0.0404979214072,
    "pitch": 0.000107885905890726,
    "yaw": -0.000273296143859625,
    "speed": 19.53953417980725
  },
  {
    "timestamp": 0.15,
    "latitude": 37.789961741532,
    "longitude": -122.401520378,
    "altitude": 10.2186584473,
    "roll": 0.0877417102456,
    "pitch": 0.000613974640145898,
    "yaw": 0.0023149426560849,
    "speed": 19.458443954458264
  },
  {
    "timestamp": 0.2,
    "latitude": 37.789961685130,
    "longitude": -122.401509302,
    "altitude": 10.1946020126,
    "roll": 0.083763346076,
    "pitch": 0.00211690412834287,
    "yaw": 0.00415488658472896,
    "speed": 19.555836055796547
  },
  {
    "timestamp": 0.25,
    "latitude": 37.789961628374,
    "longitude": -122.401498156,
    "altitude": 10.1744937897,
    "roll": 0.0497044585645,
    "pitch": 0.00419731345027685,
    "yaw": 0.00471088895574212,
    "speed": 19.678308862186125
  },
  {
    "timestamp": 0.3,
    "latitude": 37.789961571419,
    "longitude": -122.401486944,
    "altitude": 10.1585912704,
    "roll": 0.00784304458648,
    "pitch": 0.00621826434507966,
    "yaw": 0.00434521911665797,
    "speed": 19.779648523152936
  },
  {
    "timestamp": 0.35,
    "latitude": 37.789961513677,
    "longitude": -122.401475686,
    "altitude": 10.1464471817,
    "roll": 359.972473145,
    "pitch": 0.00776536809280515,
    "yaw": 0.0035081971436739,
    "speed": 19.849717576884554
  },
  {
    "timestamp": 0.4,
    "latitude": 37.789961455639,
    "longitude": -122.401464397,
    "altitude": 10.1374406815,
    "roll": 359.948364258,
    "pitch": 0.00868796184659004,
    "yaw": 0.00251324544660747,
    "speed": 19.89642120146336
  },
  {
    "timestamp": 0.45,
    "latitude": 37.789961397359,
    "longitude": -122.401453087,
    "altitude": 10.1309347153,
    "roll": 359.935058594,
    "pitch": 0.0090014636516571,
    "yaw": 0.00152538309339434,
    "speed": 19.927312974287453
  },
  {
    "timestamp": 0.5,
    "latitude": 37.789961339155,
    "longitude": -122.401441766,
    "altitude": 10.1262254715,
    "roll": 359.930297852,
    "pitch": 0.008848219178617,
    "yaw": 0.000618399993982166,
    "speed": 19.94533976993406
  },
  {
    "timestamp": 0.55,
    "latitude": 37.789961281179,
    "longitude": -122.401430435,
    "altitude": 10.1230268478,
    "roll": 359.931060791,
    "pitch": 0.00836139172315598,
    "yaw": -0.000185332421096973,
    "speed": 19.96002497668345
  },
  {
    "timestamp": 0.6,
    "latitude": 37.789961223581,
    "longitude": -122.401419098,
    "altitude": 10.1209049225,
    "roll": 359.934997559,
    "pitch": 0.00766501389443874,
    "yaw": -0.000895189994480461,
    "speed": 19.971443679571472
  },
  {
    "timestamp": 0.65,
    "latitude": 37.789961165952,
    "longitude": -122.401407755,
    "altitude": 10.1195383072,
    "roll": 359.940490723,
    "pitch": 0.006865537725389,
    "yaw": -0.00152462569531053,
    "speed": 19.980237728104957
  },
  {
    "timestamp": 0.7,
    "latitude": 37.789961108438,
    "longitude": -122.401396408,
    "altitude": 10.1186876297,
    "roll": 359.946502686,
    "pitch": 0.00605636136606336,
    "yaw": -0.00208621425554156,
    "speed": 19.98697477269317
  },
  {
    "timestamp": 0.75,
    "latitude": 37.789961050775,
    "longitude": -122.401385058,
    "altitude": 10.1180534363,
    "roll": 359.952514648,
    "pitch": 0.00531605770811439,
    "yaw": -0.00259051029570401,
    "speed": 19.989631499553205
  },
  {
    "timestamp": 0.8,
    "latitude": 37.789960993101,
    "longitude": -122.401373707,
    "altitude": 10.1177206039,
    "roll": 359.95803833,
    "pitch": 0.00465651554986835,
    "yaw": -0.00304309162311256,
    "speed": 19.992138222000087
  },
  {
    "timestamp": 0.85,
    "latitude": 37.789960935424,
    "longitude": -122.401362355,
    "altitude": 10.1175680161,
    "roll": 359.963134766,
    "pitch": 0.00408577406778932,
    "yaw": -0.00344746187329292,
    "speed": 19.992563261676434
  },
  {
    "timestamp": 0.9,
    "latitude": 37.789960877885,
    "longitude": -122.401351004,
    "altitude": 10.1175193787,
    "roll": 359.96774292,
    "pitch": 0.00361152645200491,
    "yaw": -0.00380691210739315,
    "speed": 19.991148027605753
  },
  {
    "timestamp": 0.95,
    "latitude": 37.789960820212,
    "longitude": -122.401339654,
    "altitude": 10.1175270081,
    "roll": 359.971862793,
    "pitch": 0.00322462385520339,
    "yaw": -0.00412555923685431,
    "speed": 19.988266090103252
  },
  {
    "timestamp": 1.0,
    "latitude": 37.789960763237,
    "longitude": -122.401328306,
    "altitude": 10.117562294,
    "roll": 359.975494385,
    "pitch": 0.00291407643817365,
    "yaw": -0.00440777745097876,
    "speed": 19.984203483323423
  },
  {
    "timestamp": 1.05,
    "latitude": 37.789960706273,
    "longitude": -122.40131696,
    "altitude": 10.117606163,
    "roll": 359.978637695,
    "pitch": 0.00267567718401551,
    "yaw": -0.00465807551518083,
    "speed": 19.97910515475458
  },
  {
    "timestamp": 1.1,
    "latitude": 37.789960649325,
    "longitude": -122.401305618,
    "altitude": 10.1176509857,
    "roll": 359.981292725,
    "pitch": 0.00250738835893571,
    "yaw": -0.00488132331520319,
    "speed": 19.973785565312706
  },
  {
    "timestamp": 1.15,
    "latitude": 37.789960592389,
    "longitude": -122.401294278,
    "altitude": 10.1176919937,
    "roll": 359.983337402,
    "pitch": 0.00239476445131004,
    "yaw": -0.00508645363152027,
    "speed": 19.969312829104958
  },
  {
    "timestamp": 1.2,
    "latitude": 37.789960535463,
    "longitude": -122.40128294,
    "altitude": 10.117726326,
    "roll": 359.984741211,
    "pitch": 0.00231496570631862,
    "yaw": -0.00528392428532243,
    "speed": 19.965778502837836
  },
  {
    "timestamp": 1.25,
    "latitude": 37.789960478545,
    "longitude": -122.401271604,
    "altitude": 10.1177530289,
    "roll": 359.985595703,
    "pitch": 0.00226673320867121,
    "yaw": -0.00548101216554642,
    "speed": 19.963094857810283
  },
  {
    "timestamp": 1.3,
    "latitude": 37.789960421638,
    "longitude": -122.401260271,
    "altitude": 10.1176490784,
    "roll": 359.986053467,
    "pitch": 0.00226743193343282,
    "yaw": -0.00568257411941886,
    "speed": 19.958982534039922
  },
  {
    "timestamp": 1.35,
    "latitude": 37.789960364740,
    "longitude": -122.401248939,
    "altitude": 10.1174964905,
    "roll": 359.986114502,
    "pitch": 0.00230335025116801,
    "yaw": 359.994110107422,
    "speed": 19.95570381378949
  },
  {
    "timestamp": 1.4,
    "latitude": 37.789960307843,
    "longitude": -122.401237608,
    "altitude": 10.1174621582,
    "roll": 359.985748291,
    "pitch": 0.0023405384272337,
    "yaw": 359.993896484375,
    "speed": 19.95549023573878
  },
  {
    "timestamp": 1.45,
    "latitude": 37.789960250944,
    "longitude": -122.401226277,
    "altitude": 10.1174850464,
    "roll": 359.985229492,
    "pitch": 0.00236273277550936,
    "yaw": 359.99365234375,
    "speed": 19.95587559769856
  },
  {
    "timestamp": 1.5,
    "latitude": 37.789960194042,
    "longitude": -122.401214945,
    "altitude": 10.1175336838,
    "roll": 359.984619141,
    "pitch": 0.00237292191013694,
    "yaw": 359.993408203125,
    "speed": 19.956577547265994
  },
  {
    "timestamp": 1.55,
    "latitude": 37.789960137136,
    "longitude": -122.401203613,
    "altitude": 10.1175880432,
    "roll": 359.984069824,
    "pitch": 0.00236266059800982,
    "yaw": 359.9931640625,
    "speed": 19.957517881738802
  },
  {
    "timestamp": 1.6,
    "latitude": 37.789960080232,
    "longitude": -122.401192281,
    "altitude": 10.1175165176,
    "roll": 359.983612061,
    "pitch": 0.00237421225756407,
    "yaw": 359.992919921875,
    "speed": 19.956472523193977
  },
  {
    "timestamp": 1.65,
    "latitude": 37.789960023323,
    "longitude": -122.401180949,
    "altitude": 10.117518425,
    "roll": 359.983123779,
    "pitch": 0.00238050473853946,
    "yaw": 359.992645263672,
    "speed": 19.957933625617486
  },
  {
    "timestamp": 1.7,
    "latitude": 37.789959966553,
    "longitude": -122.401169617,
    "altitude": 10.1174278259,
    "roll": 359.982696533,
    "pitch": 0.00238894182257354,
    "yaw": 359.992370605469,
    "speed": 19.95748724579294
  },
  {
    "timestamp": 1.75,
    "latitude": 37.789959910333,
    "longitude": -122.401158286,
    "altitude": 10.1173057556,
    "roll": 359.982299805,
    "pitch": 0.00242291716858745,
    "yaw": 359.992095947266,
    "speed": 19.957285069593514
  },
  {
    "timestamp": 1.8,
    "latitude": 37.789959854105,
    "longitude": -122.401146953,
    "altitude": 10.1173048019,
    "roll": 359.981811523,
    "pitch": 0.00244475179351866,
    "yaw": 359.991821289063,
    "speed": 19.95961786464248
  },
  {
    "timestamp": 1.85,
    "latitude": 37.789959797876,
    "longitude": -122.40113562,
    "altitude": 10.1172361374,
    "roll": 359.981445312,
    "pitch": 0.00246058404445648,
    "yaw": 359.991516113281,
    "speed": 19.959898189511442
  },
  {
    "timestamp": 1.9,
    "latitude": 37.789959741637,
    "longitude": -122.401124285,
    "altitude": 10.117269516,
    "roll": 359.981018066,
    "pitch": 0.00246267067268491,
    "yaw": 359.991241455078,
    "speed": 19.962477064661208
  },
  {
    "timestamp": 1.95,
    "latitude": 37.789959685391,
    "longitude": -122.401112949,
    "altitude": 10.1173448563,
    "roll": 359.980682373,
    "pitch": 0.00245036277920008,
    "yaw": 359.990936279297,
    "speed": 19.965116928987015
  },
  {
    "timestamp": 2.0,
    "latitude": 37.789959629142,
    "longitude": -122.401101613,
    "altitude": 10.1173095703,
    "roll": 359.980529785,
    "pitch": 0.00243124924600124,
    "yaw": 359.990631103516,
    "speed": 19.96543910293284
  },
  {
    "timestamp": 2.05,
    "latitude": 37.789959572885,
    "longitude": -122.401090275,
    "altitude": 10.1173496246,
    "roll": 359.98034668,
    "pitch": 0.00241344003006816,
    "yaw": 359.990325927734,
    "speed": 19.967977901361348
  },
  {
    "timestamp": 2.1,
    "latitude": 37.789959516619,
    "longitude": -122.401078936,
    "altitude": 10.1174201965,
    "roll": 359.980194092,
    "pitch": 0.00238355016335845,
    "yaw": 359.990020751953,
    "speed": 19.97052236735932
  },
  {
    "timestamp": 2.15,
    "latitude": 37.789959460346,
    "longitude": -122.401067595,
    "altitude": 10.1174974442,
    "roll": 359.980133057,
    "pitch": 0.00234452867880464,
    "yaw": 359.989715576172,
    "speed": 19.972898943121464
  },
  {
    "timestamp": 2.2,
    "latitude": 37.789959404064,
    "longitude": -122.401056253,
    "altitude": 10.1175699234,
    "roll": 359.980133057,
    "pitch": 0.00230431067757308,
    "yaw": 359.989410400391,
    "speed": 19.975096200299582
  },
  {
    "timestamp": 2.25,
    "latitude": 37.789959347775,
    "longitude": -122.40104491,
    "altitude": 10.1176309586,
    "roll": 359.980194092,
    "pitch": 0.00226445542648435,
    "yaw": 359.989105224609,
    "speed": 19.977125605200175
  },
  {
    "timestamp": 2.3,
    "latitude": 37.789959291481,
    "longitude": -122.401033566,
    "altitude": 10.1176815033,
    "roll": 359.980285645,
    "pitch": 0.00223197950981557,
    "yaw": 359.988830566406,
    "speed": 19.979010055870532
  },
  {
    "timestamp": 2.35,
    "latitude": 37.789959235179,
    "longitude": -122.401022221,
    "altitude": 10.1177196503,
    "roll": 359.980407715,
    "pitch": 0.00220701354555786,
    "yaw": 359.988525390625,
    "speed": 19.980743832224416
  },
  {
    "timestamp": 2.4,
    "latitude": 37.789959178871,
    "longitude": -122.401010875,
    "altitude": 10.1177473068,
    "roll": 359.980560303,
    "pitch": 0.00218956684693694,
    "yaw": 359.988220214844,
    "speed": 19.98234600440188
  },
  {
    "timestamp": 2.45,
    "latitude": 37.789959122557,
    "longitude": -122.400999528,
    "altitude": 10.117767334,
    "roll": 359.980712891,
    "pitch": 0.00217794580385089,
    "yaw": 359.987915039063,
    "speed": 19.983822300586546
  },
  {
    "timestamp": 2.5,
    "latitude": 37.789959066789,
    "longitude": -122.40098818,
    "altitude": 10.1177816391,
    "roll": 359.980865479,
    "pitch": 0.00216638017445803,
    "yaw": 359.987640380859,
    "speed": 19.985176528428337
  },
  {
    "timestamp": 2.55,
    "latitude": 37.789959011155,
    "longitude": -122.400976832,
    "altitude": 10.1177911758,
    "roll": 359.980987549,
    "pitch": 0.00216149282641709,
    "yaw": 359.987335205078,
    "speed": 19.98642013257847
  },
  {
    "timestamp": 2.6,
    "latitude": 37.789958955515,
    "longitude": -122.400965483,
    "altitude": 10.1177978516,
    "roll": 359.981140137,
    "pitch": 0.00216195499524474,
    "yaw": 359.987060546875,
    "speed": 19.987568372971005
  },
  {
    "timestamp": 2.65,
    "latitude": 37.789958899873,
    "longitude": -122.400954133,
    "altitude": 10.1178016663,
    "roll": 359.981292725,
    "pitch": 0.00215979758650064,
    "yaw": 359.986785888672,
    "speed": 19.98862697113305
  },
  {
    "timestamp": 2.7,
    "latitude": 37.789958844225,
    "longitude": -122.400942783,
    "altitude": 10.1178035736,
    "roll": 359.981414795,
    "pitch": 0.00215980270877481,
    "yaw": 359.986480712891,
    "speed": 19.98960355319131
  },
  {
    "timestamp": 2.75,
    "latitude": 37.789958788573,
    "longitude": -122.400931432,
    "altitude": 10.117805481,
    "roll": 359.981536865,
    "pitch": 0.00216565770097077,
    "yaw": 359.986206054688,
    "speed": 19.9904962126573
  },
  {
    "timestamp": 2.8,
    "latitude": 37.789958732917,
    "longitude": -122.400920081,
    "altitude": 10.1178064346,
    "roll": 359.981628418,
    "pitch": 0.00216430006548762,
    "yaw": 359.985931396484,
    "speed": 19.991320208214937
  },
  {
    "timestamp": 2.85,
    "latitude": 37.789958677259,
    "longitude": -122.400908729,
    "altitude": 10.1178064346,
    "roll": 359.981750488,
    "pitch": 0.00216319272294641,
    "yaw": 359.985656738281,
    "speed": 19.99206218807896
  },
  {
    "timestamp": 2.9,
    "latitude": 37.789958621597,
    "longitude": -122.400897377,
    "altitude": 10.117805481,
    "roll": 359.981842041,
    "pitch": 0.00216986192390323,
    "yaw": 359.985382080078,
    "speed": 19.992746949304763
  },
  {
    "timestamp": 2.95,
    "latitude": 37.789958565933,
    "longitude": -122.400886024,
    "altitude": 10.117805481,
    "roll": 359.981933594,
    "pitch": 0.0021744011901319,
    "yaw": 359.985107421875,
    "speed": 19.993376397195743
  },
  {
    "timestamp": 3.0,
    "latitude": 37.789958510266,
    "longitude": -122.400874672,
    "altitude": 10.1178045273,
    "roll": 359.982025146,
    "pitch": 0.00217310898005962,
    "yaw": 359.984832763672,
    "speed": 19.993950533069413
  },
  {
    "timestamp": 3.05,
    "latitude": 37.789958454596,
    "longitude": -122.400863318,
    "altitude": 10.1178035736,
    "roll": 359.982116699,
    "pitch": 0.00217565940693021,
    "yaw": 359.984558105469,
    "speed": 19.99447317122369
  },
  {
    "timestamp": 3.1,
    "latitude": 37.789958398923,
    "longitude": -122.400851965,
    "altitude": 10.1178035736,
    "roll": 359.982177734,
    "pitch": 0.00217900006100535,
    "yaw": 359.984283447266,
    "speed": 19.994957661546973
  },
  {
    "timestamp": 3.15,
    "latitude": 37.789958343248,
    "longitude": -122.400840611,
    "altitude": 10.1178026199,
    "roll": 359.98223877,
    "pitch": 0.00218631443567574,
    "yaw": 359.984008789063,
    "speed": 19.995402098863437
  },
  {
    "timestamp": 3.2,
    "latitude": 37.789958287577,
    "longitude": -122.400829259,
    "altitude": 10.1176776886,
    "roll": 359.982391357,
    "pitch": 0.0022147276904434,
    "yaw": 359.983734130859,
    "speed": 19.993618707926068
  },
  {
    "timestamp": 3.25,
    "latitude": 37.789958232178,
    "longitude": -122.400817905,
    "altitude": 10.1176328659,
    "roll": 359.982391357,
    "pitch": 0.00225040432997048,
    "yaw": 359.983489990234,
    "speed": 19.994171883641393
  },
  {
    "timestamp": 3.3,
    "latitude": 37.789958177189,
    "longitude": -122.400806552,
    "altitude": 10.1176290512,
    "roll": 359.982330322,
    "pitch": 0.00226510548964143,
    "yaw": 359.983215332031,
    "speed": 19.99484524164348
  },
  {
    "timestamp": 3.35,
    "latitude": 37.789958122198,
    "longitude": -122.400795198,
    "altitude": 10.1176462173,
    "roll": 359.982299805,
    "pitch": 0.00227254838682711,
    "yaw": 359.982940673828,
    "speed": 19.995468995394283
  },
  {
    "timestamp": 3.4,
    "latitude": 37.789958067210,
    "longitude": -122.400783846,
    "altitude": 10.1175470352,
    "roll": 359.982330322,
    "pitch": 0.00229224772192538,
    "yaw": 359.982666015625,
    "speed": 19.993851508270716
  },
  {
    "timestamp": 3.45,
    "latitude": 37.789958012219,
    "longitude": -122.400772493,
    "altitude": 10.1175289154,
    "roll": 359.982299805,
    "pitch": 0.00230890652164817,
    "yaw": 359.982391357422,
    "speed": 19.994540138011274
  },
  {
    "timestamp": 3.5,
    "latitude": 37.789957957224,
    "longitude": -122.400761139,
    "altitude": 10.1175498962,
    "roll": 359.982208252,
    "pitch": 0.00231484672985971,
    "yaw": 359.982116699219,
    "speed": 19.99532794580767
  },
  {
    "timestamp": 3.55,
    "latitude": 37.789957902226,
    "longitude": -122.400749785,
    "altitude": 10.1175870895,
    "roll": 359.982177734,
    "pitch": 0.00231113587506115,
    "yaw": 359.981872558594,
    "speed": 19.99604325500918
  },
  {
    "timestamp": 3.6,
    "latitude": 37.789957847225,
    "longitude": -122.40073843,
    "altitude": 10.1176271439,
    "roll": 359.982147217,
    "pitch": 0.0022966181859374,
    "yaw": 359.981597900391,
    "speed": 19.996674617560263
  },
  {
    "timestamp": 3.65,
    "latitude": 37.789957792222,
    "longitude": -122.400727076,
    "altitude": 10.1176662445,
    "roll": 359.982177734,
    "pitch": 0.00228655361570418,
    "yaw": 359.981323242188,
    "speed": 19.997225862447213
  },
  {
    "timestamp": 3.7,
    "latitude": 37.789957737215,
    "longitude": -122.400715721,
    "altitude": 10.1176996231,
    "roll": 359.982208252,
    "pitch": 0.00226253946311772,
    "yaw": 359.981048583984,
    "speed": 19.997706527301016
  },
  {
    "timestamp": 3.75,
    "latitude": 37.789957682207,
    "longitude": -122.400704365,
    "altitude": 10.117726326,
    "roll": 359.982269287,
    "pitch": 0.00225397362373769,
    "yaw": 359.980773925781,
    "speed": 19.998131882327776
  },
  {
    "timestamp": 3.8,
    "latitude": 37.789957627196,
    "longitude": -122.40069301,
    "altitude": 10.1177482605,
    "roll": 359.982330322,
    "pitch": 0.00224139168858528,
    "yaw": 359.980499267578,
    "speed": 19.998500020370336
  },
  {
    "timestamp": 3.85,
    "latitude": 37.789957572183,
    "longitude": -122.400681654,
    "altitude": 10.1177635193,
    "roll": 359.982391357,
    "pitch": 0.00222704815678298,
    "yaw": 359.980224609375,
    "speed": 19.998814754039056
  },
  {
    "timestamp": 3.9,
    "latitude": 37.789957517175,
    "longitude": -122.400670299,
    "altitude": 10.1176490784,
    "roll": 359.982543945,
    "pitch": 0.00224490719847381,
    "yaw": 359.97998046875,
    "speed": 19.996899738800995
  },
  {
    "timestamp": 3.95,
    "latitude": 37.789957462165,
    "longitude": -122.400658945,
    "altitude": 10.1176137924,
    "roll": 359.982543945,
    "pitch": 0.00226453295908868,
    "yaw": 359.979705810547,
    "speed": 19.997315599850594
  },
  {
    "timestamp": 4.0,
    "latitude": 37.789957407151,
    "longitude": -122.40064759,
    "altitude": 10.1176166534,
    "roll": 359.982513428,
    "pitch": 0.00227938196621835,
    "yaw": 359.979431152344,
    "speed": 19.99785926441077
  },
  {
    "timestamp": 4.05,
    "latitude": 37.789957352273,
    "longitude": -122.400636234,
    "altitude": 10.1176376343,
    "roll": 359.982452393,
    "pitch": 0.00228417618200183,
    "yaw": 359.979187011719,
    "speed": 19.998349508526218
  },
  {
    "timestamp": 4.1,
    "latitude": 37.789957297943,
    "longitude": -122.400624878,
    "altitude": 10.1176652908,
    "roll": 359.982452393,
    "pitch": 0.00227569113485515,
    "yaw": 359.978912353516,
    "speed": 19.998774886877484
  },
  {
    "timestamp": 4.15,
    "latitude": 37.789957243610,
    "longitude": -122.400613523,
    "altitude": 10.1176929474,
    "roll": 359.982452393,
    "pitch": 0.00226509454660118,
    "yaw": 359.978637695313,
    "speed": 19.999143034192922
  },
  {
    "timestamp": 4.2,
    "latitude": 37.789957189282,
    "longitude": -122.400602168,
    "altitude": 10.1175928116,
    "roll": 359.982543945,
    "pitch": 0.00227732583880425,
    "yaw": 359.978363037109,
    "speed": 19.99726995824648
  },
  {
    "timestamp": 4.25,
    "latitude": 37.789957134957,
    "longitude": -122.400590814,
    "altitude": 10.1174459457,
    "roll": 359.98260498,
    "pitch": 0.0023152781650424,
    "yaw": 359.978088378906,
    "speed": 19.995534306292747
  },
  {
    "timestamp": 4.3,
    "latitude": 37.789957080630,
    "longitude": -122.40057946,
    "altitude": 10.1174154282,
    "roll": 359.98248291,
    "pitch": 0.00235050567425787,
    "yaw": 359.977844238281,
    "speed": 19.99627443820035
  },
  {
    "timestamp": 4.35,
    "latitude": 37.789957026299,
    "longitude": -122.400568105,
    "altitude": 10.117442131,
    "roll": 359.98236084,
    "pitch": 0.00236308155581355,
    "yaw": 359.977569580078,
    "speed": 19.99711950233096
  },
  {
    "timestamp": 4.4,
    "latitude": 37.789956971972,
    "longitude": -122.400556751,
    "altitude": 10.1173677444,
    "roll": 359.982299805,
    "pitch": 0.00237932452000678,
    "yaw": 359.977294921875,
    "speed": 19.995685107191612
  },
  {
    "timestamp": 4.45,
    "latitude": 37.789956917641,
    "longitude": -122.400545397,
    "altitude": 10.1173820496,
    "roll": 359.982177734,
    "pitch": 0.00239856215193868,
    "yaw": 359.977020263672,
    "speed": 19.996520651574873
  },
  {
    "timestamp": 4.5,
    "latitude": 37.789956863312,
    "longitude": -122.400534044,
    "altitude": 10.1173095703,
    "roll": 359.982147217,
    "pitch": 0.00240716710686684,
    "yaw": 359.976745605469,
    "speed": 19.995229324889383
  },
  {
    "timestamp": 4.55,
    "latitude": 37.789956808980,
    "longitude": -122.400522689,
    "altitude": 10.1173315048,
    "roll": 359.982055664,
    "pitch": 0.00241197925060987,
    "yaw": 359.976470947266,
    "speed": 19.996194584461385
  },
  {
    "timestamp": 4.6,
    "latitude": 37.789956754644,
    "longitude": -122.400511335,
    "altitude": 10.1173915863,
    "roll": 359.981933594,
    "pitch": 0.00240230374038219,
    "yaw": 359.976196289063,
    "speed": 19.99721130381621
  },
  {
    "timestamp": 4.65,
    "latitude": 37.789956700310,
    "longitude": -122.400499981,
    "altitude": 10.1173400879,
    "roll": 359.981933594,
    "pitch": 0.00239455397240818,
    "yaw": 359.975921630859,
    "speed": 19.995914190502475
  },
  {
    "timestamp": 4.7,
    "latitude": 37.789956645973,
    "longitude": -122.400488626,
    "altitude": 10.1173677444,
    "roll": 359.981903076,
    "pitch": 0.00239040981978178,
    "yaw": 359.975646972656,
    "speed": 19.99686227746864
  },
  {
    "timestamp": 4.75,
    "latitude": 37.789956591638,
    "longitude": -122.400477273,
    "altitude": 10.1173019409,
    "roll": 359.981903076,
    "pitch": 0.00239842780865729,
    "yaw": 359.975372314453,
    "speed": 19.99566630327579
  },
  {
    "timestamp": 4.8,
    "latitude": 37.789956537299,
    "longitude": -122.400465918,
    "altitude": 10.1173286438,
    "roll": 359.981811523,
    "pitch": 0.00240119895897806,
    "yaw": 359.97509765625,
    "speed": 19.99671739982832
  },
  {
    "timestamp": 4.85,
    "latitude": 37.789956482955,
    "longitude": -122.400454563,
    "altitude": 10.1173915863,
    "roll": 359.981750488,
    "pitch": 0.00238885823637247,
    "yaw": 359.974822998047,
    "speed": 19.997798964368638
  },
  {
    "timestamp": 4.9,
    "latitude": 37.789956429296,
    "longitude": -122.400443208,
    "altitude": 10.1174659729,
    "roll": 359.981719971,
    "pitch": 0.00236097443848848,
    "yaw": 359.974548339844,
    "speed": 19.998746972912585
  },
  {
    "timestamp": 4.95,
    "latitude": 37.789956375633,
    "longitude": -122.400431852,
    "altitude": 10.1175384521,
    "roll": 359.981750488,
    "pitch": 0.00233252346515656,
    "yaw": 359.974273681641,
    "speed": 19.999544268791468
  },
  {
    "timestamp": 5.0,
    "latitude": 37.789956321972,
    "longitude": -122.400420497,
    "altitude": 10.1174764633,
    "roll": 359.981872559,
    "pitch": 0.00232315249741077,
    "yaw": 359.973999023438,
    "speed": 19.99802970224967
  },
  {
    "timestamp": 5.05,
    "latitude": 37.789956268316,
    "longitude": -122.400409142,
    "altitude": 10.1173591614,
    "roll": 359.981994629,
    "pitch": 0.00234956433996558,
    "yaw": 359.973724365234,
    "speed": 19.996585862924658
  },
  {
    "timestamp": 5.1,
    "latitude": 37.789956214656,
    "longitude": -122.400397788,
    "altitude": 10.1173524857,
    "roll": 359.981964111,
    "pitch": 0.00237329164519906,
    "yaw": 359.973449707031,
    "speed": 19.997575901996804
  },
  {
    "timestamp": 5.15,
    "latitude": 37.789956160991,
    "longitude": -122.400386432,
    "altitude": 10.117398262,
    "roll": 359.981872559,
    "pitch": 0.00237422715872526,
    "yaw": 359.973175048828,
    "speed": 19.99861552425624
  },
  {
    "timestamp": 5.2,
    "latitude": 37.789956107322,
    "longitude": -122.400375076,
    "altitude": 10.1174640656,
    "roll": 359.981842041,
    "pitch": 0.00235716160386801,
    "yaw": 359.972900390625,
    "speed": 19.99951396040015
  },
  {
    "timestamp": 5.25,
    "latitude": 37.789956053650,
    "longitude": -122.40036372,
    "altitude": 10.1175327301,
    "roll": 359.981842041,
    "pitch": 0.00232994090765715,
    "yaw": 359.972625732422,
    "speed": 20.000280754234854
  },
  {
    "timestamp": 5.3,
    "latitude": 37.789955999975,
    "longitude": -122.400352363,
    "altitude": 10.1175947189,
    "roll": 359.981872559,
    "pitch": 0.0023032205644995,
    "yaw": 359.972351074219,
    "speed": 20.00091592159934
  },
  {
    "timestamp": 5.35,
    "latitude": 37.789955946298,
    "longitude": -122.400341006,
    "altitude": 10.1176462173,
    "roll": 359.981964111,
    "pitch": 0.00227461545728147,
    "yaw": 359.972076416016,
    "speed": 20.001444275448648
  },
  {
    "timestamp": 5.4,
    "latitude": 37.789955892624,
    "longitude": -122.40032965,
    "altitude": 10.117562294,
    "roll": 359.982147217,
    "pitch": 0.00227690651081502,
    "yaw": 359.971801757813,
    "speed": 19.999681801528673
  },
  {
    "timestamp": 5.45,
    "latitude": 37.789955838948,
    "longitude": -122.400318293,
    "altitude": 10.1175498962,
    "roll": 359.982208252,
    "pitch": 0.00229195225983858,
    "yaw": 359.971527099609,
    "speed": 20.000200695871854
  },
  {
    "timestamp": 5.5,
    "latitude": 37.789955785269,
    "longitude": -122.400306936,
    "altitude": 10.1175718307,
    "roll": 359.982208252,
    "pitch": 0.00229026167653501,
    "yaw": 359.971252441406,
    "speed": 20.000801595972714
  },
  {
    "timestamp": 5.55,
    "latitude": 37.789955731587,
    "longitude": -122.400295579,
    "altitude": 10.117606163,
    "roll": 359.98223877,
    "pitch": 0.00228784885257483,
    "yaw": 359.970977783203,
    "speed": 20.001318554032075
  },
  {
    "timestamp": 5.6,
    "latitude": 37.789955677903,
    "longitude": -122.400284222,
    "altitude": 10.11764431,
    "roll": 359.982269287,
    "pitch": 0.00227135908789933,
    "yaw": 359.970703125,
    "speed": 20.001742031610263
  },
  {
    "timestamp": 5.65,
    "latitude": 37.789955624355,
    "longitude": -122.400272864,
    "altitude": 10.1176786423,
    "roll": 359.982330322,
    "pitch": 0.00226039462722838,
    "yaw": 359.970428466797,
    "speed": 20.002079669298713
  },
  {
    "timestamp": 5.7,
    "latitude": 37.789955571360,
    "longitude": -122.400261508,
    "altitude": 10.1175832748,
    "roll": 359.982452393,
    "pitch": 0.00227055652067065,
    "yaw": 359.970184326172,
    "speed": 20.000166542344466
  },
  {
    "timestamp": 5.75,
    "latitude": 37.789955518364,
    "longitude": -122.400250151,
    "altitude": 10.117562294,
    "roll": 359.98248291,
    "pitch": 0.0022855440620333,
    "yaw": 359.969909667969,
    "speed": 20.00055764171059
  },
  {
    "timestamp": 5.8,
    "latitude": 37.789955465365,
    "longitude": -122.400238794,
    "altitude": 10.1175785065,
    "roll": 359.982452393,
    "pitch": 0.00229357182979584,
    "yaw": 359.969635009766,
    "speed": 20.001049823120706
  },
  {
    "timestamp": 5.85,
    "latitude": 37.789955412363,
    "longitude": -122.400227437,
    "altitude": 10.1176109314,
    "roll": 359.982452393,
    "pitch": 0.00229317275807261,
    "yaw": 359.969360351563,
    "speed": 20.001471416959955
  },
  {
    "timestamp": 5.9,
    "latitude": 37.789955359360,
    "longitude": -122.40021608,
    "altitude": 10.1176452637,
    "roll": 359.982452393,
    "pitch": 0.00228287372738123,
    "yaw": 359.969116210938,
    "speed": 20.00181288621869
  },
  {
    "timestamp": 5.95,
    "latitude": 37.789955306355,
    "longitude": -122.400204722,
    "altitude": 10.1176786423,
    "roll": 359.98248291,
    "pitch": 0.00227211997844279,
    "yaw": 359.968841552734,
    "speed": 20.00207995507401
  },
  {
    "timestamp": 6.0,
    "latitude": 37.789971120626,
    "longitude": -122.400193364,
    "altitude": 10.1177072525,
    "roll": 359.982513428,
    "pitch": 0.00225184787996113,
    "yaw": 359.968566894531,
    "speed": 20.002291709157717
  },
  {
    "timestamp": 6.05,
    "latitude": 37.789990108351,
    "longitude": -122.400182007,
    "altitude": 10.1177310944,
    "roll": 359.982574463,
    "pitch": 0.00224795402027667,
    "yaw": 359.968292236328,
    "speed": 20.002450058437937
  },
  {
    "timestamp": 6.1,
    "latitude": 37.789990055341,
    "longitude": -122.400170649,
    "altitude": 10.1177501678,
    "roll": 359.982635498,
    "pitch": 0.00223951344378293,
    "yaw": 359.968048095703,
    "speed": 20.002558820064028
  },
  {
    "timestamp": 6.15,
    "latitude": 37.789990002336,
    "longitude": -122.400159292,
    "altitude": 10.1176395416,
    "roll": 359.982788086,
    "pitch": 0.00225848727859557,
    "yaw": 359.9677734375,
    "speed": 20.000447358917423
  },
  {
    "timestamp": 6.2,
    "latitude": 37.789989949329,
    "longitude": -122.400147935,
    "altitude": 10.117606163,
    "roll": 359.982788086,
    "pitch": 0.00228144880384207,
    "yaw": 359.967529296875,
    "speed": 20.000676323141658
  },
  {
    "timestamp": 6.25,
    "latitude": 37.789989896320,
    "longitude": -122.400136578,
    "altitude": 10.1176099777,
    "roll": 359.982727051,
    "pitch": 0.0022915608715266,
    "yaw": 359.967254638672,
    "speed": 20.001031180193525
  },
  {
    "timestamp": 6.3,
    "latitude": 37.789989843309,
    "longitude": -122.400125221,
    "altitude": 10.1176328659,
    "roll": 359.982696533,
    "pitch": 0.00229341792874038,
    "yaw": 359.966979980469,
    "speed": 20.001334519004907
  },
  {
    "timestamp": 6.35,
    "latitude": 37.789989790297,
    "longitude": -122.400113864,
    "altitude": 10.1176605225,
    "roll": 359.982666016,
    "pitch": 0.00229113316163421,
    "yaw": 359.966735839844,
    "speed": 20.00158444362864
  },
  {
    "timestamp": 6.4,
    "latitude": 37.789989737289,
    "longitude": -122.400102508,
    "altitude": 10.1175642014,
    "roll": 359.982757568,
    "pitch": 0.00230021099559963,
    "yaw": 359.966461181641,
    "speed": 19.999595032704118
  },
  {
    "timestamp": 6.45,
    "latitude": 37.789989684279,
    "longitude": -122.400091151,
    "altitude": 10.1175460815,
    "roll": 359.982727051,
    "pitch": 0.00231211213395,
    "yaw": 359.966186523438,
    "speed": 19.999927011283063
  },
  {
    "timestamp": 6.5,
    "latitude": 37.789989631816,
    "longitude": -122.400079795,
    "altitude": 10.1175642014,
    "roll": 359.982635498,
    "pitch": 0.00231424765661359,
    "yaw": 359.965942382813,
    "speed": 20.000371520024427
  },
  {
    "timestamp": 6.55,
    "latitude": 37.789989579496,
    "longitude": -122.400068439,
    "altitude": 10.1174736023,
    "roll": 359.982666016,
    "pitch": 0.00233938451856375,
    "yaw": 359.965667724609,
    "speed": 19.998576671108733
  },
  {
    "timestamp": 6.6,
    "latitude": 37.789989527179,
    "longitude": -122.400057085,
    "altitude": 10.1173419952,
    "roll": 359.982635498,
    "pitch": 0.00237708981148899,
    "yaw": 359.965393066406,
    "speed": 19.996892529353634
  },
  {
    "timestamp": 6.65,
    "latitude": 37.789989474866,
    "longitude": -122.400045731,
    "altitude": 10.1172056198,
    "roll": 359.982574463,
    "pitch": 0.00242323777638376,
    "yaw": 359.965148925781,
    "speed": 19.99548305521831
  },
  {
    "timestamp": 6.7,
    "latitude": 37.789989422555,
    "longitude": -122.400034378,
    "altitude": 10.1170816422,
    "roll": 359.982421875,
    "pitch": 0.00247634085826576,
    "yaw": 359.964874267578,
    "speed": 19.99435014961911
  },
  {
    "timestamp": 6.75,
    "latitude": 37.789989370246,
    "longitude": -122.400023026,
    "altitude": 10.1169776917,
    "roll": 359.982208252,
    "pitch": 0.00252237636595964,
    "yaw": 359.964599609375,
    "speed": 19.99344422783567
  },
  {
    "timestamp": 6.8,
    "latitude": 37.789989317937,
    "longitude": -122.400011674,
    "altitude": 10.1168937683,
    "roll": 359.981964111,
    "pitch": 0.00257128826342523,
    "yaw": 359.964324951172,
    "speed": 19.99274812369883
  },
  {
    "timestamp": 6.85,
    "latitude": 37.789989265624,
    "longitude": -122.400000321,
    "altitude": 10.1169548035,
    "roll": 359.981658936,
    "pitch": 0.00258542923256755,
    "yaw": 359.964050292969,
    "speed": 19.994402082002583
  },
  {
    "timestamp": 6.9,
    "latitude": 37.789989213304,
    "longitude": -122.399988967,
    "altitude": 10.1170768738,
    "roll": 359.981414795,
    "pitch": 0.00255335262045264,
    "yaw": 359.963745117188,
    "speed": 19.996027341145446
  },
  {
    "timestamp": 6.95,
    "latitude": 37.789989160980,
    "longitude": -122.399977612,
    "altitude": 10.1172142029,
    "roll": 359.981292725,
    "pitch": 0.00250799837522209,
    "yaw": 359.963470458984,
    "speed": 19.997438855809712
  },
  {
    "timestamp": 7.0,
    "latitude": 37.789989108650,
    "longitude": -122.399966257,
    "altitude": 10.1173448563,
    "roll": 359.981262207,
    "pitch": 0.00245027500204742,
    "yaw": 359.963195800781,
    "speed": 19.998638579999614
  },
  {
    "timestamp": 7.05,
    "latitude": 37.789989056316,
    "longitude": -122.399954901,
    "altitude": 10.1174573898,
    "roll": 359.981323242,
    "pitch": 0.00239869230426848,
    "yaw": 359.962890625,
    "speed": 19.999660900114428
  },
  {
    "timestamp": 7.1,
    "latitude": 37.789989003978,
    "longitude": -122.399943544,
    "altitude": 10.1175489426,
    "roll": 359.981414795,
    "pitch": 0.0023397624026984,
    "yaw": 359.962615966797,
    "speed": 20.000509669562263
  },
  {
    "timestamp": 7.15,
    "latitude": 37.789988951644,
    "longitude": -122.399932188,
    "altitude": 10.1174945831,
    "roll": 359.981628418,
    "pitch": 0.0023113121278584,
    "yaw": 359.962341308594,
    "speed": 19.999035142377497
  },
  {
    "timestamp": 7.2,
    "latitude": 37.789988899306,
    "longitude": -122.399920832,
    "altitude": 10.1175041199,
    "roll": 359.981750488,
    "pitch": 0.0023055556230247,
    "yaw": 359.962066650391,
    "speed": 19.999794391233014
  },
  {
    "timestamp": 7.25,
    "latitude": 37.789988846964,
    "longitude": -122.399909476,
    "altitude": 10.1175413132,
    "roll": 359.981811523,
    "pitch": 0.00229959702119231,
    "yaw": 359.961791992188,
    "speed": 20.000608932936796
  },
  {
    "timestamp": 7.3,
    "latitude": 37.789988795170,
    "longitude": -122.399898119,
    "altitude": 10.1175870895,
    "roll": 359.981872559,
    "pitch": 0.00228049186989665,
    "yaw": 359.961517333984,
    "speed": 20.001297553583523
  },
  {
    "timestamp": 7.35,
    "latitude": 37.789988743510,
    "longitude": -122.399886761,
    "altitude": 10.1176319122,
    "roll": 359.981933594,
    "pitch": 0.00226696976460516,
    "yaw": 359.961242675781,
    "speed": 20.00186791139159
  },
  {
    "timestamp": 7.4,
    "latitude": 37.789988691847,
    "longitude": -122.399875403,
    "altitude": 10.1176710129,
    "roll": 359.982025146,
    "pitch": 0.00224693724885583,
    "yaw": 359.960968017578,
    "speed": 20.002327633568214
  },
  {
    "timestamp": 7.45,
    "latitude": 37.789988640183,
    "longitude": -122.399864046,
    "altitude": 10.1177034378,
    "roll": 359.982147217,
    "pitch": 0.0022373185493052,
    "yaw": 359.960693359375,
    "speed": 20.002693893605056
  },
  {
    "timestamp": 7.5,
    "latitude": 37.789988588522,
    "longitude": -122.399852689,
    "altitude": 10.117603302,
    "roll": 359.982330322,
    "pitch": 0.0022485142108053,
    "yaw": 359.960418701172,
    "speed": 20.000790324878086
  },
  {
    "timestamp": 7.55,
    "latitude": 37.789988536866,
    "longitude": -122.399841333,
    "altitude": 10.1174545288,
    "roll": 359.982452393,
    "pitch": 0.00228825118392706,
    "yaw": 359.960144042969,
    "speed": 19.999005113216075
  },
  {
    "timestamp": 7.6,
    "latitude": 37.789988485214,
    "longitude": -122.399829978,
    "altitude": 10.1172981262,
    "roll": 359.982452393,
    "pitch": 0.00234563183039427,
    "yaw": 359.959899902344,
    "speed": 19.997494559945128
  },
  {
    "timestamp": 7.65,
    "latitude": 37.789988433558,
    "longitude": -122.399818623,
    "altitude": 10.1172790527,
    "roll": 359.982299805,
    "pitch": 0.00238940073177218,
    "yaw": 359.959625244141,
    "speed": 19.998431201513785
  },
  {
    "timestamp": 7.7,
    "latitude": 37.789988381898,
    "longitude": -122.399807267,
    "altitude": 10.1173257828,
    "roll": 359.982147217,
    "pitch": 0.00240586930885911,
    "yaw": 359.959350585938,
    "speed": 19.9994212800657
  },
  {
    "timestamp": 7.75,
    "latitude": 37.789988330234,
    "longitude": -122.39979591,
    "altitude": 10.1174001694,
    "roll": 359.982025146,
    "pitch": 0.00239031342789531,
    "yaw": 359.959075927734,
    "speed": 20.000285419941413
  },
  {
    "timestamp": 7.8,
    "latitude": 37.789988278567,
    "longitude": -122.399784554,
    "altitude": 10.1174783707,
    "roll": 359.981994629,
    "pitch": 0.00236720219254494,
    "yaw": 359.958801269531,
    "speed": 20.00100646282777
  },
  {
    "timestamp": 7.85,
    "latitude": 37.789988226897,
    "longitude": -122.399773196,
    "altitude": 10.1175508499,
    "roll": 359.981994629,
    "pitch": 0.00233327387832105,
    "yaw": 359.958526611328,
    "speed": 20.001597781186465
  },
  {
    "timestamp": 7.9,
    "latitude": 37.789988175225,
    "longitude": -122.399761839,
    "altitude": 10.1176137924,
    "roll": 359.982055664,
    "pitch": 0.00230844947509468,
    "yaw": 359.958251953125,
    "speed": 20.002084189481305
  },
  {
    "timestamp": 7.95,
    "latitude": 37.789988123550,
    "longitude": -122.399750481,
    "altitude": 10.1176643372,
    "roll": 359.982147217,
    "pitch": 0.00228154635988176,
    "yaw": 359.957977294922,
    "speed": 20.002465695485903
  },
  {
    "timestamp": 8.0,
    "latitude": 37.789988071873,
    "longitude": -122.399739123,
    "altitude": 10.1177024841,
    "roll": 359.982269287,
    "pitch": 0.00226069381460547,
    "yaw": 359.957702636719,
    "speed": 20.00277091936438
  },
  {
    "timestamp": 8.05,
    "latitude": 37.789988020200,
    "longitude": -122.399727766,
    "altitude": 10.117606163,
    "roll": 359.982421875,
    "pitch": 0.0022625932469964,
    "yaw": 359.957458496094,
    "speed": 20.00082347859325
  },
  {
    "timestamp": 8.1,
    "latitude": 37.789987969082,
    "longitude": -122.39971641,
    "altitude": 10.1174573898,
    "roll": 359.982543945,
    "pitch": 0.00229711225256324,
    "yaw": 359.957183837891,
    "speed": 19.998992494224826
  },
  {
    "timestamp": 8.15,
    "latitude": 37.789987918106,
    "longitude": -122.399705056,
    "altitude": 10.1173009872,
    "roll": 359.982543945,
    "pitch": 0.00235476298257709,
    "yaw": 359.956909179688,
    "speed": 19.99745333255886
  },
  {
    "timestamp": 8.2,
    "latitude": 37.789987867125,
    "longitude": -122.3996937,
    "altitude": 10.1172819138,
    "roll": 359.982391357,
    "pitch": 0.00239433464594185,
    "yaw": 359.956634521484,
    "speed": 19.99836518184796
  },
  {
    "timestamp": 8.25,
    "latitude": 37.789987816141,
    "longitude": -122.399682344,
    "altitude": 10.1173276901,
    "roll": 359.982208252,
    "pitch": 0.00240939576178789,
    "yaw": 359.956359863281,
    "speed": 19.999328564262015
  },
  {
    "timestamp": 8.3,
    "latitude": 37.789987765154,
    "longitude": -122.399670988,
    "altitude": 10.117401123,
    "roll": 359.982086182,
    "pitch": 0.0023988289758563,
    "yaw": 359.956115722656,
    "speed": 20.000166008001734
  },
  {
    "timestamp": 8.35,
    "latitude": 37.789987714162,
    "longitude": -122.399659631,
    "altitude": 10.1174793243,
    "roll": 359.982025146,
    "pitch": 0.00237702787853777,
    "yaw": 359.955841064453,
    "speed": 20.000866074504707
  },
  {
    "timestamp": 8.4,
    "latitude": 37.789987663168,
    "longitude": -122.399648274,
    "altitude": 10.1175527573,
    "roll": 359.982055664,
    "pitch": 0.00234598689712584,
    "yaw": 359.95556640625,
    "speed": 20.001444043539596
  },
  {
    "timestamp": 8.45,
    "latitude": 37.789987612172,
    "longitude": -122.399636917,
    "altitude": 10.1176137924,
    "roll": 359.982116699,
    "pitch": 0.00230577378533781,
    "yaw": 359.955291748047,
    "speed": 20.00191901310635
  },
  {
    "timestamp": 8.5,
    "latitude": 37.789987561173,
    "longitude": -122.399625559,
    "altitude": 10.1176652908,
    "roll": 359.982177734,
    "pitch": 0.00228631100617349,
    "yaw": 359.955017089844,
    "speed": 20.002298616328677
  },
  {
    "timestamp": 8.55,
    "latitude": 37.789987510172,
    "longitude": -122.399614201,
    "altitude": 10.1177034378,
    "roll": 359.982299805,
    "pitch": 0.00225589447654784,
    "yaw": 359.954742431641,
    "speed": 20.002592399776802
  },
  {
    "timestamp": 8.6,
    "latitude": 37.789987459169,
    "longitude": -122.399602843,
    "altitude": 10.1177310944,
    "roll": 359.982391357,
    "pitch": 0.00223811133764684,
    "yaw": 359.954467773438,
    "speed": 20.002823242887356
  },
  {
    "timestamp": 8.65,
    "latitude": 37.789987408165,
    "longitude": -122.399591485,
    "altitude": 10.1177530289,
    "roll": 359.98248291,
    "pitch": 0.00222805724479258,
    "yaw": 359.954223632813,
    "speed": 20.002991153771895
  },
  {
    "timestamp": 8.7,
    "latitude": 37.789987357159,
    "longitude": -122.399580127,
    "altitude": 10.117767334,
    "roll": 359.982574463,
    "pitch": 0.00222179992124438,
    "yaw": 359.953948974609,
    "speed": 20.003105656970106
  },
  {
    "timestamp": 8.75,
    "latitude": 37.789987306152,
    "longitude": -122.399568768,
    "altitude": 10.1177778244,
    "roll": 359.982666016,
    "pitch": 0.00222219713032246,
    "yaw": 359.953674316406,
    "speed": 20.003180108504854
  },
  {
    "timestamp": 8.8,
    "latitude": 37.789987255143,
    "longitude": -122.39955741,
    "altitude": 10.1177854538,
    "roll": 359.982727051,
    "pitch": 0.00222051865421236,
    "yaw": 359.953430175781,
    "speed": 20.00322023405055
  },
  {
    "timestamp": 8.85,
    "latitude": 37.789987204134,
    "longitude": -122.399546052,
    "altitude": 10.1177892685,
    "roll": 359.982788086,
    "pitch": 0.00222124718129635,
    "yaw": 359.953155517578,
    "speed": 20.003231749875305
  },
  {
    "timestamp": 8.9,
    "latitude": 37.789987153535,
    "longitude": -122.399534693,
    "altitude": 10.1177921295,
    "roll": 359.982849121,
    "pitch": 0.00220920611172915,
    "yaw": 359.952880859375,
    "speed": 20.003216562479086
  },
  {
    "timestamp": 8.95,
    "latitude": 37.789987103211,
    "longitude": -122.399523335,
    "altitude": 10.1177940369,
    "roll": 359.982910156,
    "pitch": 0.00221220147795975,
    "yaw": 359.95263671875,
    "speed": 20.003180397246446
  },
  {
    "timestamp": 9.0,
    "latitude": 37.789987052886,
    "longitude": -122.399511977,
    "altitude": 10.1177959442,
    "roll": 359.982940674,
    "pitch": 0.00221756170503795,
    "yaw": 359.952362060547,
    "speed": 20.00312897030958
  },
  {
    "timestamp": 9.05,
    "latitude": 37.789987002560,
    "longitude": -122.399500619,
    "altitude": 10.1177959442,
    "roll": 359.982971191,
    "pitch": 0.00222146604210138,
    "yaw": 359.952117919922,
    "speed": 20.003066102996314
  },
  {
    "timestamp": 9.1,
    "latitude": 37.789986952240,
    "longitude": -122.399489262,
    "altitude": 10.1176710129,
    "roll": 359.983093262,
    "pitch": 0.00223860167898238,
    "yaw": 359.951843261719,
    "speed": 20.000805922234747
  },
  {
    "timestamp": 9.15,
    "latitude": 37.789986901918,
    "longitude": -122.399477905,
    "altitude": 10.1176271439,
    "roll": 359.983032227,
    "pitch": 0.00226616091094911,
    "yaw": 359.951599121094,
    "speed": 20.000901386106875
  },
  {
    "timestamp": 9.2,
    "latitude": 37.789986851595,
    "longitude": -122.399466548,
    "altitude": 10.1176233292,
    "roll": 359.982971191,
    "pitch": 0.00228307861834764,
    "yaw": 359.951324462891,
    "speed": 20.001147545888422
  },
  {
    "timestamp": 9.25,
    "latitude": 37.789986801270,
    "longitude": -122.399455191,
    "altitude": 10.117641449,
    "roll": 359.982910156,
    "pitch": 0.00229295808821917,
    "yaw": 359.951080322266,
    "speed": 20.001359362999747
  },
  {
    "timestamp": 9.3,
    "latitude": 37.789986750943,
    "longitude": -122.399443833,
    "altitude": 10.1176671982,
    "roll": 359.982849121,
    "pitch": 0.00229064980521798,
    "yaw": 359.950805664063,
    "speed": 20.001533013991125
  },
  {
    "timestamp": 9.35,
    "latitude": 37.789986700614,
    "longitude": -122.399432476,
    "altitude": 10.1176929474,
    "roll": 359.982818604,
    "pitch": 0.00228314311243594,
    "yaw": 359.950561523438,
    "speed": 20.001664698622935
  },
  {
    "timestamp": 9.4,
    "latitude": 37.789986650285,
    "longitude": -122.399421118,
    "altitude": 10.1177167892,
    "roll": 359.982818604,
    "pitch": 0.0022710224147886,
    "yaw": 359.950286865234,
    "speed": 20.00176776409029
  },
  {
    "timestamp": 9.45,
    "latitude": 37.789986599954,
    "longitude": -122.399409761,
    "altitude": 10.1177377701,
    "roll": 359.982849121,
    "pitch": 0.00226512574590743,
    "yaw": 359.950042724609,
    "speed": 20.001834595153
  },
  {
    "timestamp": 9.5,
    "latitude": 37.789986549621,
    "longitude": -122.399398403,
    "altitude": 10.1177549362,
    "roll": 359.982879639,
    "pitch": 0.0022502806968987,
    "yaw": 359.949768066406,
    "speed": 20.00188043996686
  },
  {
    "timestamp": 9.55,
    "latitude": 37.789986499288,
    "longitude": -122.399387046,
    "altitude": 10.117767334,
    "roll": 359.982879639,
    "pitch": 0.00224536680616438,
    "yaw": 359.949523925781,
    "speed": 20.001903401109065
  },
  {
    "timestamp": 9.6,
    "latitude": 37.789986448953,
    "longitude": -122.399375688,
    "altitude": 10.1177759171,
    "roll": 359.982910156,
    "pitch": 0.00223907828330994,
    "yaw": 359.949249267578,
    "speed": 20.001905380935252
  },
  {
    "timestamp": 9.65,
    "latitude": 37.789986398617,
    "longitude": -122.399364331,
    "altitude": 10.1177835464,
    "roll": 359.982940674,
    "pitch": 0.00223272456787527,
    "yaw": 359.949005126953,
    "speed": 20.001892106128604
  },
  {
    "timestamp": 9.7,
    "latitude": 37.789986348281,
    "longitude": -122.399352973,
    "altitude": 10.1177883148,
    "roll": 359.982971191,
    "pitch": 0.0022344458848238,
    "yaw": 359.94873046875,
    "speed": 20.001871201377558
  },
  {
    "timestamp": 9.75,
    "latitude": 37.789986298493,
    "longitude": -122.399341616,
    "altitude": 10.1177911758,
    "roll": 359.983001709,
    "pitch": 0.00223176018334925,
    "yaw": 359.948486328125,
    "speed": 20.001835042067338
  },
  {
    "timestamp": 9.8,
    "latitude": 37.789986248842,
    "longitude": -122.399330258,
    "altitude": 10.1177930832,
    "roll": 359.983001709,
    "pitch": 0.00223211525008082,
    "yaw": 359.948211669922,
    "speed": 20.00179315803253
  },
  {
    "timestamp": 9.85,
    "latitude": 37.789986199190,
    "longitude": -122.399318901,
    "altitude": 10.1177949905,
    "roll": 359.983032227,
    "pitch": 0.0022289277985692,
    "yaw": 359.947967529297,
    "speed": 20.001745555384414
  },
  {
    "timestamp": 9.9,
    "latitude": 37.789986149537,
    "longitude": -122.399307543,
    "altitude": 10.1177968979,
    "roll": 359.983032227,
    "pitch": 0.00223221210762858,
    "yaw": 359.947692871094,
    "speed": 20.001696041778846
  },
  {
    "timestamp": 9.95,
    "latitude": 37.789986099883,
    "longitude": -122.399296186,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00222878041677177,
    "yaw": 359.947448730469,
    "speed": 20.001650347272363
  },
  {
    "timestamp": 10.0,
    "latitude": 37.789986050228,
    "longitude": -122.399284828,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00222932756878436,
    "yaw": 359.947174072266,
    "speed": 20.001593206488508
  },
  {
    "timestamp": 10.05,
    "latitude": 37.789986000572,
    "longitude": -122.399273471,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00223075482062995,
    "yaw": 359.946929931641,
    "speed": 20.00153797703571
  },
  {
    "timestamp": 10.1,
    "latitude": 37.789985950915,
    "longitude": -122.399262114,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00222972803749144,
    "yaw": 359.946655273438,
    "speed": 20.001482744053057
  },
  {
    "timestamp": 10.15,
    "latitude": 37.789985901257,
    "longitude": -122.399250756,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223257206380367,
    "yaw": 359.946411132813,
    "speed": 20.0014237006983
  },
  {
    "timestamp": 10.2,
    "latitude": 37.789985851599,
    "longitude": -122.399239399,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223213690333068,
    "yaw": 359.946136474609,
    "speed": 20.00136274547202
  },
  {
    "timestamp": 10.25,
    "latitude": 37.789985801939,
    "longitude": -122.399228042,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223233038559556,
    "yaw": 359.945892333984,
    "speed": 20.001299887566788
  },
  {
    "timestamp": 10.3,
    "latitude": 37.789985752279,
    "longitude": -122.399216685,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00222982303239405,
    "yaw": 359.945617675781,
    "speed": 20.001242749162667
  },
  {
    "timestamp": 10.35,
    "latitude": 37.789985702617,
    "longitude": -122.399205328,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.0022344512399286,
    "yaw": 359.945373535156,
    "speed": 20.001189428861483
  },
  {
    "timestamp": 10.4,
    "latitude": 37.789985652955,
    "longitude": -122.39919397,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.0022326682228595,
    "yaw": 359.945129394531,
    "speed": 20.001132294107286
  },
  {
    "timestamp": 10.45,
    "latitude": 37.789985603292,
    "longitude": -122.399182613,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223428593017161,
    "yaw": 359.944854736328,
    "speed": 20.001077063742773
  },
  {
    "timestamp": 10.5,
    "latitude": 37.789985553627,
    "longitude": -122.399171256,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223252805881202,
    "yaw": 359.944610595703,
    "speed": 20.001021837308926
  },
  {
    "timestamp": 10.55,
    "latitude": 37.789985503962,
    "longitude": -122.399159899,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223416928201914,
    "yaw": 359.9443359375,
    "speed": 20.000972329689013
  },
  {
    "timestamp": 10.6,
    "latitude": 37.789985454846,
    "longitude": -122.399148542,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223253876902163,
    "yaw": 359.944091796875,
    "speed": 20.000922826291156
  },
  {
    "timestamp": 10.65,
    "latitude": 37.789985405867,
    "longitude": -122.399137185,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223451689817011,
    "yaw": 359.943817138672,
    "speed": 20.00087331962157
  },
  {
    "timestamp": 10.7,
    "latitude": 37.789985356886,
    "longitude": -122.399125828,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223346031270921,
    "yaw": 359.943572998047,
    "speed": 20.00082572408819
  },
  {
    "timestamp": 10.75,
    "latitude": 37.789985307905,
    "longitude": -122.399114471,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223269034177065,
    "yaw": 359.943298339844,
    "speed": 20.000781940396447
  },
  {
    "timestamp": 10.8,
    "latitude": 37.789985258922,
    "longitude": -122.399103114,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223556067794561,
    "yaw": 359.943054199219,
    "speed": 20.000740067679505
  },
  {
    "timestamp": 10.85,
    "latitude": 37.789985209939,
    "longitude": -122.399091757,
    "altitude": 10.1177978516,
    "roll": 359.983093262,
    "pitch": 0.00223547476343811,
    "yaw": 359.942779541016,
    "speed": 20.000700099345718
  },
  {
    "timestamp": 10.9,
    "latitude": 37.789985160955,
    "longitude": -122.399080401,
    "altitude": 10.1177968979,
    "roll": 359.983093262,
    "pitch": 0.00223225657828152,
    "yaw": 359.942535400391,
    "speed": 20.000662043625432
  },
  {
    "timestamp": 10.95,
    "latitude": 37.789985111970,
    "longitude": -122.399069044,
    "altitude": 10.1177968979,
    "roll": 359.983093262,
    "pitch": 0.00223602331243455,
    "yaw": 359.942291259766,
    "speed": 20.000622080048196
  },
  {
    "timestamp": 11.0,
    "latitude": 37.789985062983,
    "longitude": -122.399057687,
    "altitude": 10.1177968979,
    "roll": 359.983093262,
    "pitch": 0.00223650084808469,
    "yaw": 359.942016601563,
    "speed": 20.000584020296376
  },
  {
    "timestamp": 11.05,
    "latitude": 37.789985013996,
    "longitude": -122.39904633,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223638094030321,
    "yaw": 359.941772460938,
    "speed": 20.00054596486567
  },
  {
    "timestamp": 11.1,
    "latitude": 37.789984965008,
    "longitude": -122.399034973,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223557790741324,
    "yaw": 359.941497802734,
    "speed": 20.000509812135263
  },
  {
    "timestamp": 11.15,
    "latitude": 37.789984916025,
    "longitude": -122.399023618,
    "altitude": 10.1176729202,
    "roll": 359.983123779,
    "pitch": 0.00225197849795222,
    "yaw": 359.941253662109,
    "speed": 19.998285890840762
  },
  {
    "timestamp": 11.2,
    "latitude": 37.789984867047,
    "longitude": -122.399012264,
    "altitude": 10.1175031662,
    "roll": 359.983154297,
    "pitch": 0.00230385945178568,
    "yaw": 359.940979003906,
    "speed": 19.996252758595663
  },
  {
    "timestamp": 11.25,
    "latitude": 37.789984818074,
    "longitude": -122.39900091,
    "altitude": 10.1173305511,
    "roll": 359.983062744,
    "pitch": 0.00237184087745845,
    "yaw": 359.940734863281,
    "speed": 19.99455530680235
  },
  {
    "timestamp": 11.3,
    "latitude": 37.789984769097,
    "longitude": -122.398989557,
    "altitude": 10.1173019409,
    "roll": 359.982818604,
    "pitch": 0.00241863704286516,
    "yaw": 359.940460205078,
    "speed": 19.995366071362962
  },
  {
    "timestamp": 11.35,
    "latitude": 37.789984720117,
    "longitude": -122.398978202,
    "altitude": 10.1173410416,
    "roll": 359.982543945,
    "pitch": 0.00243473658338189,
    "yaw": 359.940185546875,
    "speed": 19.99626271476258
  },
  {
    "timestamp": 11.4,
    "latitude": 37.789984671133,
    "longitude": -122.398966848,
    "altitude": 10.1174097061,
    "roll": 359.98236084,
    "pitch": 0.00242731487378478,
    "yaw": 359.939910888672,
    "speed": 19.99706012710748
  },
  {
    "timestamp": 11.45,
    "latitude": 37.789984622833,
    "longitude": -122.398955493,
    "altitude": 10.1174850464,
    "roll": 359.98223877,
    "pitch": 0.00239316001534462,
    "yaw": 359.939666748047,
    "speed": 19.997756409163227
  },
  {
    "timestamp": 11.5,
    "latitude": 37.789984574531,
    "longitude": -122.398944137,
    "altitude": 10.117556572,
    "roll": 359.982208252,
    "pitch": 0.00236164266243577,
    "yaw": 359.939392089844,
    "speed": 19.998359203866958
  },
  {
    "timestamp": 11.55,
    "latitude": 37.789984526226,
    "longitude": -122.398932782,
    "altitude": 10.1176176071,
    "roll": 359.982208252,
    "pitch": 0.0023259453009814,
    "yaw": 359.939117431641,
    "speed": 19.998870436850424
  },
  {
    "timestamp": 11.6,
    "latitude": 37.789984477918,
    "longitude": -122.398921426,
    "altitude": 10.1176671982,
    "roll": 359.982269287,
    "pitch": 0.00229865685105324,
    "yaw": 359.938842773438,
    "speed": 19.999297751757247
  },
  {
    "timestamp": 11.65,
    "latitude": 37.789984429609,
    "longitude": -122.398910069,
    "altitude": 10.1177043915,
    "roll": 359.982330322,
    "pitch": 0.0022755665704608,
    "yaw": 359.938568115234,
    "speed": 19.99966976395208
  },
  {
    "timestamp": 11.7,
    "latitude": 37.789984381297,
    "longitude": -122.398898713,
    "altitude": 10.1177330017,
    "roll": 359.982391357,
    "pitch": 0.00225544068962336,
    "yaw": 359.938293457031,
    "speed": 19.999978832918806
  },
  {
    "timestamp": 11.75,
    "latitude": 37.789984332983,
    "longitude": -122.398887356,
    "altitude": 10.1177549362,
    "roll": 359.982452393,
    "pitch": 0.00224031764082611,
    "yaw": 359.938049316406,
    "speed": 20.00024213892229
  },
  {
    "timestamp": 11.8,
    "latitude": 37.789984284668,
    "longitude": -122.398876,
    "altitude": 10.1177692413,
    "roll": 359.982543945,
    "pitch": 0.00222994270734489,
    "yaw": 359.937774658203,
    "speed": 20.000457756893155
  },
  {
    "timestamp": 11.85,
    "latitude": 37.789984236350,
    "longitude": -122.398864643,
    "altitude": 10.1177806854,
    "roll": 359.98260498,
    "pitch": 0.00222775992006063,
    "yaw": 359.9375,
    "speed": 20.000637137918275
  },
  {
    "timestamp": 11.9,
    "latitude": 37.789984188032,
    "longitude": -122.398853286,
    "altitude": 10.1177873611,
    "roll": 359.982666016,
    "pitch": 0.00220926431939006,
    "yaw": 359.937255859375,
    "speed": 20.000776472569434
  },
  {
    "timestamp": 11.95,
    "latitude": 37.789984139712,
    "longitude": -122.398841929,
    "altitude": 10.1177911758,
    "roll": 359.982727051,
    "pitch": 0.00221366086043417,
    "yaw": 359.936981201172,
    "speed": 20.000891011986518
  },
  {
    "timestamp": 12.0,
    "latitude": 37.789984091390,
    "longitude": -122.398830572,
    "altitude": 10.1177940369,
    "roll": 359.982757568,
    "pitch": 0.00221553677693009,
    "yaw": 359.936706542969,
    "speed": 20.00097503259773
  },
  {
    "timestamp": 12.05,
    "latitude": 37.789984043067,
    "longitude": -122.398819215,
    "altitude": 10.1177959442,
    "roll": 359.982818604,
    "pitch": 0.0022086575627327,
    "yaw": 359.936462402344,
    "speed": 20.001038076872064
  },
  {
    "timestamp": 12.1,
    "latitude": 37.789983994744,
    "longitude": -122.398807858,
    "altitude": 10.1177978516,
    "roll": 359.982849121,
    "pitch": 0.00221044546924531,
    "yaw": 359.936187744141,
    "speed": 20.00108395121187
  },
  {
    "timestamp": 12.15,
    "latitude": 37.789983946418,
    "longitude": -122.398796501,
    "altitude": 10.1177978516,
    "roll": 359.982879639,
    "pitch": 0.00221742386929691,
    "yaw": 359.935943603516,
    "speed": 20.001114571056686
  },
  {
    "timestamp": 12.2,
    "latitude": 37.789983898092,
    "longitude": -122.398785144,
    "altitude": 10.1177978516,
    "roll": 359.982910156,
    "pitch": 0.00222268328070641,
    "yaw": 359.935668945313,
    "speed": 20.00112992895242
  },
  {
    "timestamp": 12.25,
    "latitude": 37.789983850177,
    "longitude": -122.398773787,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.0022226138971746,
    "yaw": 359.935424804688,
    "speed": 20.001137661767444
  },
  {
    "timestamp": 12.3,
    "latitude": 37.789983802536,
    "longitude": -122.398762429,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.00222027860581875,
    "yaw": 359.935150146484,
    "speed": 20.0011396686152
  },
  {
    "timestamp": 12.35,
    "latitude": 37.789983754893,
    "longitude": -122.398751072,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.0022227056324482,
    "yaw": 359.934906005859,
    "speed": 20.001128328455646
  },
  {
    "timestamp": 12.4,
    "latitude": 37.789983707250,
    "longitude": -122.398739715,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222329492680728,
    "yaw": 359.934631347656,
    "speed": 20.001107447302843
  },
  {
    "timestamp": 12.45,
    "latitude": 37.789983659606,
    "longitude": -122.398728358,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222819414921105,
    "yaw": 359.934387207031,
    "speed": 20.00107703386006
  },
  {
    "timestamp": 12.5,
    "latitude": 37.789983611961,
    "longitude": -122.398717001,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222740601748228,
    "yaw": 359.934112548828,
    "speed": 20.001046616667185
  },
  {
    "timestamp": 12.55,
    "latitude": 37.789983564315,
    "longitude": -122.398705644,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222426978871226,
    "yaw": 359.933868408203,
    "speed": 20.001018111377554
  },
  {
    "timestamp": 12.6,
    "latitude": 37.789983516667,
    "longitude": -122.398694287,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223220558837056,
    "yaw": 359.93359375,
    "speed": 20.00099150904176
  },
  {
    "timestamp": 12.65,
    "latitude": 37.789983469019,
    "longitude": -122.39868293,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223063421435654,
    "yaw": 359.933349609375,
    "speed": 20.00095728198265
  },
  {
    "timestamp": 12.7,
    "latitude": 37.789983421370,
    "longitude": -122.398671573,
    "altitude": 10.1177968979,
    "roll": 359.983032227,
    "pitch": 0.00222963094711304,
    "yaw": 359.933074951172,
    "speed": 20.000921145087386
  },
  {
    "timestamp": 12.75,
    "latitude": 37.789983373720,
    "longitude": -122.398660216,
    "altitude": 10.1177968979,
    "roll": 359.983032227,
    "pitch": 0.00223269034177065,
    "yaw": 359.932830810547,
    "speed": 20.00089073388436
  },
  {
    "timestamp": 12.8,
    "latitude": 37.789983326069,
    "longitude": -122.398648859,
    "altitude": 10.1177968979,
    "roll": 359.983062744,
    "pitch": 0.00223281770013273,
    "yaw": 359.932556152344,
    "speed": 20.000856503881458
  },
  {
    "timestamp": 12.85,
    "latitude": 37.789983278417,
    "longitude": -122.398637502,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223010359331965,
    "yaw": 359.932312011719,
    "speed": 20.00082609338223
  },
  {
    "timestamp": 12.9,
    "latitude": 37.789983230764,
    "longitude": -122.398626145,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223103747703135,
    "yaw": 359.932037353516,
    "speed": 20.000789955785624
  },
  {
    "timestamp": 12.95,
    "latitude": 37.789983183109,
    "longitude": -122.398614788,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223221001215279,
    "yaw": 359.931793212891,
    "speed": 20.000751916185678
  },
  {
    "timestamp": 13.0,
    "latitude": 37.789983135461,
    "longitude": -122.398603432,
    "altitude": 10.1176729202,
    "roll": 359.983123779,
    "pitch": 0.00225414498709142,
    "yaw": 359.931518554688,
    "speed": 19.998524191204403
  },
  {
    "timestamp": 13.05,
    "latitude": 37.789983087811,
    "longitude": -122.398592077,
    "altitude": 10.1176280975,
    "roll": 359.983062744,
    "pitch": 0.00228103692643344,
    "yaw": 359.931274414063,
    "speed": 19.998680721517452
  },
  {
    "timestamp": 13.1,
    "latitude": 37.789983040571,
    "longitude": -122.398580721,
    "altitude": 10.1176252365,
    "roll": 359.982971191,
    "pitch": 0.00229854043573141,
    "yaw": 359.930999755859,
    "speed": 19.998991762976708
  },
  {
    "timestamp": 13.15,
    "latitude": 37.789982993605,
    "longitude": -122.398569365,
    "altitude": 10.1176424026,
    "roll": 359.982879639,
    "pitch": 0.00230004079639912,
    "yaw": 359.930755615234,
    "speed": 19.99927609143151
  },
  {
    "timestamp": 13.2,
    "latitude": 37.789982946637,
    "longitude": -122.398558009,
    "altitude": 10.1176681519,
    "roll": 359.982818604,
    "pitch": 0.00229158368892968,
    "yaw": 359.930480957031,
    "speed": 19.999522252985603
  },
  {
    "timestamp": 13.25,
    "latitude": 37.789982899668,
    "longitude": -122.398546652,
    "altitude": 10.1176948547,
    "roll": 359.982788086,
    "pitch": 0.00228723417967558,
    "yaw": 359.930236816406,
    "speed": 19.999737892585923
  },
  {
    "timestamp": 13.3,
    "latitude": 37.789982852696,
    "longitude": -122.398535296,
    "altitude": 10.1177186966,
    "roll": 359.982788086,
    "pitch": 0.00227309949696064,
    "yaw": 359.929962158203,
    "speed": 19.99991347019116
  },
  {
    "timestamp": 13.35,
    "latitude": 37.789982805729,
    "longitude": -122.398523941,
    "altitude": 10.1176137924,
    "roll": 359.982849121,
    "pitch": 0.00228499481454492,
    "yaw": 359.9296875,
    "speed": 19.997872630922792
  },
  {
    "timestamp": 13.4,
    "latitude": 37.789982758768,
    "longitude": -122.398512587,
    "altitude": 10.1174612045,
    "roll": 359.982879639,
    "pitch": 0.00232336740009487,
    "yaw": 359.929443359375,
    "speed": 19.99599210316249
  },
  {
    "timestamp": 13.45,
    "latitude": 37.789982711803,
    "longitude": -122.398501232,
    "altitude": 10.1174259186,
    "roll": 359.982757568,
    "pitch": 0.00236295000649989,
    "yaw": 359.929168701172,
    "speed": 19.99661023294477
  },
  {
    "timestamp": 13.5,
    "latitude": 37.789982664835,
    "longitude": -122.398489877,
    "altitude": 10.1174497604,
    "roll": 359.982574463,
    "pitch": 0.0023738972377032,
    "yaw": 359.928924560547,
    "speed": 19.997337123383062
  },
  {
    "timestamp": 13.55,
    "latitude": 37.789982617864,
    "longitude": -122.398478522,
    "altitude": 10.1174993515,
    "roll": 359.982452393,
    "pitch": 0.0023706411011517,
    "yaw": 359.928649902344,
    "speed": 19.997987673057114
  },
  {
    "timestamp": 13.6,
    "latitude": 37.789982570890,
    "longitude": -122.398467167,
    "altitude": 10.117556572,
    "roll": 359.98236084,
    "pitch": 0.00235155737027526,
    "yaw": 359.928375244141,
    "speed": 19.998544733915228
  },
  {
    "timestamp": 13.65,
    "latitude": 37.789982523914,
    "longitude": -122.398455811,
    "altitude": 10.1176099777,
    "roll": 359.982330322,
    "pitch": 0.00232770619913936,
    "yaw": 359.928100585938,
    "speed": 19.999027395400553
  },
  {
    "timestamp": 13.7,
    "latitude": 37.789982476935,
    "longitude": -122.398444455,
    "altitude": 10.1176567078,
    "roll": 359.98236084,
    "pitch": 0.00230229622684419,
    "yaw": 359.927825927734,
    "speed": 19.99942994237591
  },
  {
    "timestamp": 13.75,
    "latitude": 37.789982429955,
    "longitude": -122.398433099,
    "altitude": 10.1176939011,
    "roll": 359.982391357,
    "pitch": 0.00227904715575278,
    "yaw": 359.927581787109,
    "speed": 19.999782903574022
  },
  {
    "timestamp": 13.8,
    "latitude": 37.789982382972,
    "longitude": -122.398421742,
    "altitude": 10.1177244186,
    "roll": 359.982452393,
    "pitch": 0.00226229894906282,
    "yaw": 359.927307128906,
    "speed": 20.0000729152055
  },
  {
    "timestamp": 13.85,
    "latitude": 37.789982335987,
    "longitude": -122.398410385,
    "altitude": 10.1177463531,
    "roll": 359.982513428,
    "pitch": 0.00225284323096275,
    "yaw": 359.927032470703,
    "speed": 20.00030571604535
  },
  {
    "timestamp": 13.9,
    "latitude": 37.789982289001,
    "longitude": -122.398399029,
    "altitude": 10.1177635193,
    "roll": 359.982574463,
    "pitch": 0.00224081170745194,
    "yaw": 359.9267578125,
    "speed": 20.000502279591267
  },
  {
    "timestamp": 13.95,
    "latitude": 37.789982242700,
    "longitude": -122.398387672,
    "altitude": 10.1177759171,
    "roll": 359.982635498,
    "pitch": 0.00222576316446066,
    "yaw": 359.926513671875,
    "speed": 20.000664517161233
  },
  {
    "timestamp": 14.0,
    "latitude": 37.789982196399,
    "longitude": -122.398376315,
    "altitude": 10.1177835464,
    "roll": 359.982696533,
    "pitch": 0.00222680834122002,
    "yaw": 359.926239013672,
    "speed": 20.000796234818925
  },
  {
    "timestamp": 14.05,
    "latitude": 37.789982150095,
    "longitude": -122.398364958,
    "altitude": 10.1177892685,
    "roll": 359.982727051,
    "pitch": 0.00221645087003708,
    "yaw": 359.925964355469,
    "speed": 20.000901252925672
  },
  {
    "timestamp": 14.1,
    "latitude": 37.789982103791,
    "longitude": -122.398353601,
    "altitude": 10.1177921295,
    "roll": 359.982788086,
    "pitch": 0.00221889070235193,
    "yaw": 359.925720214844,
    "speed": 20.00097766684151
  },
  {
    "timestamp": 14.15,
    "latitude": 37.789982057484,
    "longitude": -122.398342244,
    "altitude": 10.1177940369,
    "roll": 359.982818604,
    "pitch": 0.00221892702393234,
    "yaw": 359.925445556641,
    "speed": 20.001038817659172
  },
  {
    "timestamp": 14.2,
    "latitude": 37.789982011177,
    "longitude": -122.398330887,
    "altitude": 10.1177959442,
    "roll": 359.982849121,
    "pitch": 0.00221337238326669,
    "yaw": 359.925201416016,
    "speed": 20.001080898620266
  },
  {
    "timestamp": 14.25,
    "latitude": 37.789981964869,
    "longitude": -122.39831953,
    "altitude": 10.1177978516,
    "roll": 359.982879639,
    "pitch": 0.00221557286567986,
    "yaw": 359.924926757813,
    "speed": 20.00111534578646
  },
  {
    "timestamp": 14.3,
    "latitude": 37.789981918560,
    "longitude": -122.398308173,
    "altitude": 10.1177978516,
    "roll": 359.982910156,
    "pitch": 0.00221909210085869,
    "yaw": 359.924682617188,
    "speed": 20.00112881729406
  },
  {
    "timestamp": 14.35,
    "latitude": 37.789981872249,
    "longitude": -122.398296815,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.00222738808952272,
    "yaw": 359.924407958984,
    "speed": 20.001134655593976
  },
  {
    "timestamp": 14.4,
    "latitude": 37.789981825938,
    "longitude": -122.398285458,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222678948193789,
    "yaw": 359.924163818359,
    "speed": 20.00113096216267
  },
  {
    "timestamp": 14.45,
    "latitude": 37.789981779625,
    "longitude": -122.398274101,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222344836220145,
    "yaw": 359.923889160156,
    "speed": 20.00112154233745
  },
  {
    "timestamp": 14.5,
    "latitude": 37.789981733311,
    "longitude": -122.398262744,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222464581020176,
    "yaw": 359.923645019531,
    "speed": 20.001102590691083
  },
  {
    "timestamp": 14.55,
    "latitude": 37.789981686996,
    "longitude": -122.398251387,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00223012850619853,
    "yaw": 359.923370361328,
    "speed": 20.001079819587062
  },
  {
    "timestamp": 14.6,
    "latitude": 37.789981640680,
    "longitude": -122.39824003,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222636689431965,
    "yaw": 359.923126220703,
    "speed": 20.001051331772377
  },
  {
    "timestamp": 14.65,
    "latitude": 37.789981594363,
    "longitude": -122.398228673,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222669937647879,
    "yaw": 359.9228515625,
    "speed": 20.00102093158219
  },
  {
    "timestamp": 14.7,
    "latitude": 37.789981548045,
    "longitude": -122.398217316,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222462601959705,
    "yaw": 359.922607421875,
    "speed": 20.000988629404798
  },
  {
    "timestamp": 14.75,
    "latitude": 37.789981502001,
    "longitude": -122.398205959,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222673965618014,
    "yaw": 359.922332763672,
    "speed": 20.00095441523442
  },
  {
    "timestamp": 14.8,
    "latitude": 37.789981456369,
    "longitude": -122.398194602,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222971546463668,
    "yaw": 359.922088623047,
    "speed": 20.00092020691533
  },
  {
    "timestamp": 14.85,
    "latitude": 37.789981410736,
    "longitude": -122.398183245,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223331991583109,
    "yaw": 359.921813964844,
    "speed": 20.000885993292986
  },
  {
    "timestamp": 14.9,
    "latitude": 37.789981365102,
    "longitude": -122.398171888,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223399861715734,
    "yaw": 359.921569824219,
    "speed": 20.000853692431136
  },
  {
    "timestamp": 14.95,
    "latitude": 37.789981319467,
    "longitude": -122.398160531,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223155017010868,
    "yaw": 359.921295166016,
    "speed": 20.000819479829048
  },
  {
    "timestamp": 15.0,
    "latitude": 37.789981273831,
    "longitude": -122.398149174,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223252503201365,
    "yaw": 359.921051025391,
    "speed": 20.000781457748342
  },
  {
    "timestamp": 15.05,
    "latitude": 37.789981228193,
    "longitude": -122.398137817,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223337928764522,
    "yaw": 359.920776367188,
    "speed": 20.000745338347123
  },
  {
    "timestamp": 15.1,
    "latitude": 37.789981182555,
    "longitude": -122.39812646,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223091524094343,
    "yaw": 359.920532226563,
    "speed": 20.00071113149576
  },
  {
    "timestamp": 15.15,
    "latitude": 37.789981136915,
    "longitude": -122.398115103,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223192060366273,
    "yaw": 359.920257568359,
    "speed": 20.000678827557675
  },
  {
    "timestamp": 15.2,
    "latitude": 37.789981091275,
    "longitude": -122.398103746,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223312503658235,
    "yaw": 359.920013427734,
    "speed": 20.000650343933184
  },
  {
    "timestamp": 15.25,
    "latitude": 37.789981045634,
    "longitude": -122.398092389,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223117205314338,
    "yaw": 359.919738769531,
    "speed": 20.00061804070603
  },
  {
    "timestamp": 15.3,
    "latitude": 37.789980999992,
    "longitude": -122.398081032,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223269360139966,
    "yaw": 359.919494628906,
    "speed": 20.000591464929727
  },
  {
    "timestamp": 15.35,
    "latitude": 37.789980954348,
    "longitude": -122.398069676,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.0022344880271703,
    "yaw": 359.919250488281,
    "speed": 20.00056488987194
  },
  {
    "timestamp": 15.4,
    "latitude": 37.789980908704,
    "longitude": -122.398058319,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223303982056677,
    "yaw": 359.918975830078,
    "speed": 20.000536402503542
  },
  {
    "timestamp": 15.45,
    "latitude": 37.789980863059,
    "longitude": -122.398046962,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.0022346880286932,
    "yaw": 359.918731689453,
    "speed": 20.000507920761546
  },
  {
    "timestamp": 15.5,
    "latitude": 37.789980817412,
    "longitude": -122.398035605,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223287753760815,
    "yaw": 359.91845703125,
    "speed": 20.00048134161994
  },
  {
    "timestamp": 15.55,
    "latitude": 37.789980771765,
    "longitude": -122.398024249,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.0022342384327203,
    "yaw": 359.918212890625,
    "speed": 20.000454768299356
  },
  {
    "timestamp": 15.6,
    "latitude": 37.789980726530,
    "longitude": -122.398012892,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223219743929803,
    "yaw": 359.917938232422,
    "speed": 20.000428189780145
  },
  {
    "timestamp": 15.65,
    "latitude": 37.789980681569,
    "longitude": -122.398001535,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223029823973775,
    "yaw": 359.917694091797,
    "speed": 20.000411153636573
  },
  {
    "timestamp": 15.7,
    "latitude": 37.789980636606,
    "longitude": -122.397990179,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223225448280573,
    "yaw": 359.917419433594,
    "speed": 20.000399834923584
  },
  {
    "timestamp": 15.75,
    "latitude": 37.789980591642,
    "longitude": -122.397978822,
    "altitude": 10.1177978516,
    "roll": 359.983062744,
    "pitch": 0.00223157997243106,
    "yaw": 359.917175292969,
    "speed": 20.00038089258159
  },
  {
    "timestamp": 15.8,
    "latitude": 37.789980546684,
    "longitude": -122.397967466,
    "altitude": 10.1176719666,
    "roll": 359.983123779,
    "pitch": 0.00225535733625293,
    "yaw": 359.916900634766,
    "speed": 19.998168448273994
  },
  {
    "timestamp": 15.85,
    "latitude": 37.789980501724,
    "longitude": -122.397956111,
    "altitude": 10.1176280975,
    "roll": 359.983062744,
    "pitch": 0.00228413660079241,
    "yaw": 359.916656494141,
    "speed": 19.998330724891375
  },
  {
    "timestamp": 15.9,
    "latitude": 37.789980456762,
    "longitude": -122.397944755,
    "altitude": 10.1176242828,
    "roll": 359.982971191,
    "pitch": 0.00229926127940416,
    "yaw": 359.916381835938,
    "speed": 19.998647510656856
  },
  {
    "timestamp": 15.95,
    "latitude": 37.789980411799,
    "longitude": -122.397933399,
    "altitude": 10.1176424026,
    "roll": 359.982879639,
    "pitch": 0.00230474676936865,
    "yaw": 359.916137695313,
    "speed": 19.998947122469215
  },
  {
    "timestamp": 16.0,
    "latitude": 37.789980366833,
    "longitude": -122.397922043,
    "altitude": 10.1176681519,
    "roll": 359.982788086,
    "pitch": 0.00229955301620066,
    "yaw": 359.915863037109,
    "speed": 19.999206657983194
  },
  {
    "timestamp": 16.05,
    "latitude": 37.789980321867,
    "longitude": -122.397910687,
    "altitude": 10.1176939011,
    "roll": 359.982757568,
    "pitch": 0.00228793569840491,
    "yaw": 359.915618896484,
    "speed": 19.999424229911565
  },
  {
    "timestamp": 16.1,
    "latitude": 37.789980276897,
    "longitude": -122.397899331,
    "altitude": 10.1177177429,
    "roll": 359.982757568,
    "pitch": 0.00228012190200388,
    "yaw": 359.915344238281,
    "speed": 19.999607458230965
  },
  {
    "timestamp": 16.15,
    "latitude": 37.789980231926,
    "longitude": -122.397887975,
    "altitude": 10.1177396774,
    "roll": 359.982757568,
    "pitch": 0.00226402841508389,
    "yaw": 359.915069580078,
    "speed": 19.99977542918457
  },
  {
    "timestamp": 16.2,
    "latitude": 37.789980186954,
    "longitude": -122.397876618,
    "altitude": 10.1177558899,
    "roll": 359.982788086,
    "pitch": 0.00224838824942708,
    "yaw": 359.914825439453,
    "speed": 19.999905259279508
  },
  {
    "timestamp": 16.25,
    "latitude": 37.789980141980,
    "longitude": -122.397865262,
    "altitude": 10.1177682877,
    "roll": 359.982788086,
    "pitch": 0.00224931328557432,
    "yaw": 359.91455078125,
    "speed": 20.000016010798095
  },
  {
    "timestamp": 16.3,
    "latitude": 37.789980097005,
    "longitude": -122.397853905,
    "altitude": 10.1177778244,
    "roll": 359.982818604,
    "pitch": 0.002238116459921,
    "yaw": 359.914306640625,
    "speed": 20.00010960296106
  },
  {
    "timestamp": 16.35,
    "latitude": 37.789980052029,
    "longitude": -122.397842549,
    "altitude": 10.1177845001,
    "roll": 359.982849121,
    "pitch": 0.00223604519851506,
    "yaw": 359.914031982422,
    "speed": 20.00018984022735
  },
  {
    "timestamp": 16.4,
    "latitude": 37.789980007052,
    "longitude": -122.397831192,
    "altitude": 10.1177892685,
    "roll": 359.982879639,
    "pitch": 0.00222854083403945,
    "yaw": 359.913757324219,
    "speed": 20.000256730728037
  },
  {
    "timestamp": 16.45,
    "latitude": 37.789979962624,
    "longitude": -122.397819836,
    "altitude": 10.1177930832,
    "roll": 359.982910156,
    "pitch": 0.00223252573050559,
    "yaw": 359.913513183594,
    "speed": 20.000312180177506
  },
  {
    "timestamp": 16.5,
    "latitude": 37.789979918332,
    "longitude": -122.397808479,
    "altitude": 10.1177949905,
    "roll": 359.982910156,
    "pitch": 0.00222557131201029,
    "yaw": 359.913238525391,
    "speed": 20.000359997202395
  },
  {
    "timestamp": 16.55,
    "latitude": 37.789979874044,
    "longitude": -122.397797124,
    "altitude": 10.1176710129,
    "roll": 359.983001709,
    "pitch": 0.0022486203815788,
    "yaw": 359.912994384766,
    "speed": 19.9982047829773
  },
  {
    "timestamp": 16.6,
    "latitude": 37.789979829756,
    "longitude": -122.397785768,
    "altitude": 10.1176271439,
    "roll": 359.982971191,
    "pitch": 0.00227682269178331,
    "yaw": 359.912719726563,
    "speed": 19.9984109329835
  },
  {
    "timestamp": 16.65,
    "latitude": 37.789979785465,
    "longitude": -122.397774412,
    "altitude": 10.1176242828,
    "roll": 359.982879639,
    "pitch": 0.00229516997933388,
    "yaw": 359.912475585938,
    "speed": 19.99876587839288
  },
  {
    "timestamp": 16.7,
    "latitude": 37.789979741172,
    "longitude": -122.397763056,
    "altitude": 10.1176424026,
    "roll": 359.982788086,
    "pitch": 0.00230081053450704,
    "yaw": 359.912200927734,
    "speed": 19.99909028670778
  },
  {
    "timestamp": 16.75,
    "latitude": 37.789979696878,
    "longitude": -122.3977517,
    "altitude": 10.1176681519,
    "roll": 359.982757568,
    "pitch": 0.00229269987903535,
    "yaw": 359.911926269531,
    "speed": 19.999370810700228
  },
  {
    "timestamp": 16.8,
    "latitude": 37.789979652580,
    "longitude": -122.397740344,
    "altitude": 10.1176939011,
    "roll": 359.982727051,
    "pitch": 0.00228843558579683,
    "yaw": 359.911682128906,
    "speed": 19.999599834069333
  },
  {
    "timestamp": 16.85,
    "latitude": 37.789979608282,
    "longitude": -122.397728988,
    "altitude": 10.1177177429,
    "roll": 359.982727051,
    "pitch": 0.00227168202400208,
    "yaw": 359.911407470703,
    "speed": 19.99980214333621
  },
  {
    "timestamp": 16.9,
    "latitude": 37.789979563982,
    "longitude": -122.397717631,
    "altitude": 10.1177396774,
    "roll": 359.982727051,
    "pitch": 0.00226365402340889,
    "yaw": 359.911163330078,
    "speed": 19.999973941521798
  },
  {
    "timestamp": 16.95,
    "latitude": 37.789979519680,
    "longitude": -122.397706275,
    "altitude": 10.1177568436,
    "roll": 359.982757568,
    "pitch": 0.00224294327199459,
    "yaw": 359.910888671875,
    "speed": 20.00011712276976
  },
  {
    "timestamp": 17.0,
    "latitude": 37.789979475378,
    "longitude": -122.397694918,
    "altitude": 10.1177692413,
    "roll": 359.982788086,
    "pitch": 0.002239138353616,
    "yaw": 359.910614013672,
    "speed": 20.0002316960222
  },
  {
    "timestamp": 17.05,
    "latitude": 37.789979431074,
    "longitude": -122.397683562,
    "altitude": 10.1177778244,
    "roll": 359.982818604,
    "pitch": 0.00223426730372012,
    "yaw": 359.910369873047,
    "speed": 20.00032720363976
  },
  {
    "timestamp": 17.1,
    "latitude": 37.789979386769,
    "longitude": -122.397672205,
    "altitude": 10.1177845001,
    "roll": 359.982849121,
    "pitch": 0.00222696596756577,
    "yaw": 359.910095214844,
    "speed": 20.000399819706395
  },
  {
    "timestamp": 17.15,
    "latitude": 37.789979342462,
    "longitude": -122.397660848,
    "altitude": 10.1177892685,
    "roll": 359.982879639,
    "pitch": 0.00223442306742072,
    "yaw": 359.909851074219,
    "speed": 20.000468628521247
  },
  {
    "timestamp": 17.2,
    "latitude": 37.789979298153,
    "longitude": -122.397649492,
    "altitude": 10.1177921295,
    "roll": 359.982879639,
    "pitch": 0.00223075109533966,
    "yaw": 359.909576416016,
    "speed": 20.000522172519823
  },
  {
    "timestamp": 17.25,
    "latitude": 37.789979253843,
    "longitude": -122.397638135,
    "altitude": 10.1177940369,
    "roll": 359.982910156,
    "pitch": 0.00222637876868248,
    "yaw": 359.909332275391,
    "speed": 20.000558557453083
  },
  {
    "timestamp": 17.3,
    "latitude": 37.789979210220,
    "longitude": -122.397626778,
    "altitude": 10.1177959442,
    "roll": 359.982940674,
    "pitch": 0.0022288728505373,
    "yaw": 359.909057617188,
    "speed": 20.000581584747284
  },
  {
    "timestamp": 17.35,
    "latitude": 37.789979166596,
    "longitude": -122.397615421,
    "altitude": 10.1177978516,
    "roll": 359.982940674,
    "pitch": 0.0022279042750597,
    "yaw": 359.908782958984,
    "speed": 20.00060270401583
  },
  {
    "timestamp": 17.4,
    "latitude": 37.789979122970,
    "longitude": -122.397604064,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222681765444577,
    "yaw": 359.908538818359,
    "speed": 20.000608571593066
  },
  {
    "timestamp": 17.45,
    "latitude": 37.789979079344,
    "longitude": -122.397592707,
    "altitude": 10.1177978516,
    "roll": 359.982971191,
    "pitch": 0.00222628144547343,
    "yaw": 359.908264160156,
    "speed": 20.00061634214145
  },
  {
    "timestamp": 17.5,
    "latitude": 37.789979035716,
    "longitude": -122.39758135,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222354591824114,
    "yaw": 359.908020019531,
    "speed": 20.000622211363908
  },
  {
    "timestamp": 17.55,
    "latitude": 37.789978992087,
    "longitude": -122.397569993,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00222520320676267,
    "yaw": 359.907745361328,
    "speed": 20.000614723196836
  },
  {
    "timestamp": 17.6,
    "latitude": 37.789978948458,
    "longitude": -122.397558637,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00223093805834651,
    "yaw": 359.907501220703,
    "speed": 20.00060724159069
  },
  {
    "timestamp": 17.65,
    "latitude": 37.789978904827,
    "longitude": -122.39754728,
    "altitude": 10.1177978516,
    "roll": 359.983001709,
    "pitch": 0.00223053386434913,
    "yaw": 359.9072265625,
    "speed": 20.000590217249567
  },
  {
    "timestamp": 17.7,
    "latitude": 37.789978861195,
    "longitude": -122.397535923,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223054806701839,
    "yaw": 359.906982421875,
    "speed": 20.000582736452376
  },
  {
    "timestamp": 17.75,
    "latitude": 37.789978817562,
    "longitude": -122.397524566,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223427941091359,
    "yaw": 359.906707763672,
    "speed": 20.000563805009875
  },
  {
    "timestamp": 17.8,
    "latitude": 37.789978773927,
    "longitude": -122.397513209,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.0022313327062875,
    "yaw": 359.906463623047,
    "speed": 20.000546787760037
  },
  {
    "timestamp": 17.85,
    "latitude": 37.789978730292,
    "longitude": -122.397501852,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223175506107509,
    "yaw": 359.906219482422,
    "speed": 20.000529770361204
  },
  {
    "timestamp": 17.9,
    "latitude": 37.789978686656,
    "longitude": -122.397490495,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223246612586081,
    "yaw": 359.905944824219,
    "speed": 20.00050893293071
  },
  {
    "timestamp": 17.95,
    "latitude": 37.789978643019,
    "longitude": -122.397479139,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223644892685115,
    "yaw": 359.905700683594,
    "speed": 20.000484287047968
  },
  {
    "timestamp": 18.0,
    "latitude": 37.789978599381,
    "longitude": -122.397467782,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223346636630595,
    "yaw": 359.905426025391,
    "speed": 20.000459635483754
  },
  {
    "timestamp": 18.05,
    "latitude": 37.789978555743,
    "longitude": -122.397456425,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223336229100823,
    "yaw": 359.905181884766,
    "speed": 20.000434990379066
  },
  {
    "timestamp": 18.1,
    "latitude": 37.789978512240,
    "longitude": -122.397445069,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222995225340128,
    "yaw": 359.904907226563,
    "speed": 20.000421783557872
  },
  {
    "timestamp": 18.15,
    "latitude": 37.789978469287,
    "longitude": -122.397433712,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223004445433617,
    "yaw": 359.904663085938,
    "speed": 20.000408583901635
  },
  {
    "timestamp": 18.2,
    "latitude": 37.789978426332,
    "longitude": -122.397422355,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223068031482399,
    "yaw": 359.904388427734,
    "speed": 20.000393470604145
  },
  {
    "timestamp": 18.25,
    "latitude": 37.789978383377,
    "longitude": -122.397410999,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223187124356627,
    "yaw": 359.904144287109,
    "speed": 20.000378363887325
  },
  {
    "timestamp": 18.3,
    "latitude": 37.789978340420,
    "longitude": -122.397399642,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223335647024214,
    "yaw": 359.903869628906,
    "speed": 20.00036325140071
  },
  {
    "timestamp": 18.35,
    "latitude": 37.789978297462,
    "longitude": -122.397388285,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223472039215267,
    "yaw": 359.903625488281,
    "speed": 20.000348143906695
  },
  {
    "timestamp": 18.4,
    "latitude": 37.789978254504,
    "longitude": -122.397376928,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223277066834271,
    "yaw": 359.903350830078,
    "speed": 20.00033303212198
  },
  {
    "timestamp": 18.45,
    "latitude": 37.789978211544,
    "longitude": -122.397365572,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223416718654335,
    "yaw": 359.903106689453,
    "speed": 20.000317926640882
  },
  {
    "timestamp": 18.5,
    "latitude": 37.789978168583,
    "longitude": -122.397354215,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223243981599808,
    "yaw": 359.90283203125,
    "speed": 20.000306631533466
  },
  {
    "timestamp": 18.55,
    "latitude": 37.789978125621,
    "longitude": -122.397342859,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223423959687352,
    "yaw": 359.902587890625,
    "speed": 20.000289619836064
  },
  {
    "timestamp": 18.6,
    "latitude": 37.789978082659,
    "longitude": -122.397331502,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223296275362372,
    "yaw": 359.902313232422,
    "speed": 20.00027260210313
  },
  {
    "timestamp": 18.65,
    "latitude": 37.789978039696,
    "longitude": -122.397320146,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223173177801073,
    "yaw": 359.902069091797,
    "speed": 20.00025940602324
  },
  {
    "timestamp": 18.7,
    "latitude": 37.789977996731,
    "longitude": -122.397308789,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223068334162235,
    "yaw": 359.901824951172,
    "speed": 20.000246210273435
  },
  {
    "timestamp": 18.75,
    "latitude": 37.789977953766,
    "longitude": -122.397297432,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222984119318426,
    "yaw": 359.901550292969,
    "speed": 20.00023300875237
  },
  {
    "timestamp": 18.8,
    "latitude": 37.789977910799,
    "longitude": -122.397286076,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222929939627647,
    "yaw": 359.901306152344,
    "speed": 20.000219814006428
  },
  {
    "timestamp": 18.85,
    "latitude": 37.789977867831,
    "longitude": -122.397274719,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.0022323455195874,
    "yaw": 359.901031494141,
    "speed": 20.000202798826777
  },
  {
    "timestamp": 18.9,
    "latitude": 37.789977824862,
    "longitude": -122.397263363,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223184167407453,
    "yaw": 359.900787353516,
    "speed": 20.000195326964043
  },
  {
    "timestamp": 18.95,
    "latitude": 37.789977782167,
    "longitude": -122.397252006,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.0022346309851855,
    "yaw": 359.900512695313,
    "speed": 20.000187848356497
  },
  {
    "timestamp": 19.0,
    "latitude": 37.789977739884,
    "longitude": -122.39724065,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223374646157026,
    "yaw": 359.900268554688,
    "speed": 20.000180377352777
  },
  {
    "timestamp": 19.05,
    "latitude": 37.789977697599,
    "longitude": -122.397229293,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223588570952415,
    "yaw": 359.899993896484,
    "speed": 20.000176714847136
  },
  {
    "timestamp": 19.1,
    "latitude": 37.789977655314,
    "longitude": -122.397217937,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223418907262385,
    "yaw": 359.899749755859,
    "speed": 20.000167337372304
  },
  {
    "timestamp": 19.15,
    "latitude": 37.789977613027,
    "longitude": -122.39720658,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223207916133106,
    "yaw": 359.899475097656,
    "speed": 20.000159861004608
  },
  {
    "timestamp": 19.2,
    "latitude": 37.789977570739,
    "longitude": -122.397195224,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223633414134383,
    "yaw": 359.899230957031,
    "speed": 20.000156206284306
  },
  {
    "timestamp": 19.25,
    "latitude": 37.789977528450,
    "longitude": -122.397183867,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223689968697727,
    "yaw": 359.898956298828,
    "speed": 20.00015254549959
  },
  {
    "timestamp": 19.3,
    "latitude": 37.789977486160,
    "longitude": -122.397172511,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223388220183551,
    "yaw": 359.898712158203,
    "speed": 20.000148891744697
  },
  {
    "timestamp": 19.35,
    "latitude": 37.789977443869,
    "longitude": -122.397161154,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223375926725566,
    "yaw": 359.8984375,
    "speed": 20.000139509821096
  },
  {
    "timestamp": 19.4,
    "latitude": 37.789977401577,
    "longitude": -122.397149798,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223662261851132,
    "yaw": 359.898193359375,
    "speed": 20.000132041827225
  },
  {
    "timestamp": 19.45,
    "latitude": 37.789977359283,
    "longitude": -122.397138441,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223557627759874,
    "yaw": 359.897918701172,
    "speed": 20.000124567003667
  },
  {
    "timestamp": 19.5,
    "latitude": 37.789977316989,
    "longitude": -122.397127085,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223398604430258,
    "yaw": 359.897674560547,
    "speed": 20.000117099719166
  },
  {
    "timestamp": 19.55,
    "latitude": 37.789977274693,
    "longitude": -122.397115728,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223206309601665,
    "yaw": 359.897399902344,
    "speed": 20.00010962682543
  },
  {
    "timestamp": 19.6,
    "latitude": 37.789977232397,
    "longitude": -122.397104372,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.0022332591470331,
    "yaw": 359.897155761719,
    "speed": 20.0001040678841
  },
  {
    "timestamp": 19.65,
    "latitude": 37.789977190099,
    "longitude": -122.397093015,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00223139091394842,
    "yaw": 359.896881103516,
    "speed": 20.000098502868916
  },
  {
    "timestamp": 19.7,
    "latitude": 37.789977147800,
    "longitude": -122.397081658,
    "altitude": 10.1177988052,
    "roll": 359.983032227,
    "pitch": 0.00222964980639517,
    "yaw": 359.896636962891,
    "speed": 20.000092944927516
  },
  {
    "timestamp": 19.75,
    "latitude": 37.789977105500,
    "longitude": -122.397070302,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222856434993446,
    "yaw": 359.896362304688,
    "speed": 20.000089289384828
  },
  {
    "timestamp": 19.8,
    "latitude": 37.789977063474,
    "longitude": -122.397058945,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223132572136819,
    "yaw": 359.896118164063,
    "speed": 20.000083732672547
  },
  {
    "timestamp": 19.85,
    "latitude": 37.789977021860,
    "longitude": -122.397047589,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222804327495396,
    "yaw": 359.895874023438,
    "speed": 20.00007817617314
  },
  {
    "timestamp": 19.9,
    "latitude": 37.789976980244,
    "longitude": -122.397036232,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222878437489271,
    "yaw": 359.895599365234,
    "speed": 20.000074520861027
  },
  {
    "timestamp": 19.95,
    "latitude": 37.789976938628,
    "longitude": -122.397024876,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00223023095168173,
    "yaw": 359.895355224609,
    "speed": 20.00007087268931
  },
  {
    "timestamp": 20.0,
    "latitude": 37.789935007395,
    "longitude": -122.397013519,
    "altitude": 10.1177978516,
    "roll": 359.983032227,
    "pitch": 0.00222910335287452,
    "yaw": 359.895080566406,
    "speed": 20.000069125585753
  }
]
```



```
f = open('gps.json', 'r')
gps = f.read()
f.close()
gpslines = gps.split('n')
pos = []
for line in gpslines:
  i0 = line.find('timestamp')
  if i0 >= 0:
    ti = line[i0+12:-1]
  i1 = line.find('latitude')
  if i1 >= 0:
    la = float(line[i1+11:-1])
  i2 = line.find('longitude')
  if i2 >= 0:
    lo = float(line[i2+12:-1])
  i3 = line.find('altitude')
  if i3 >= 0:
    al = float(line[i3+11:-1])
    pos.append( [la, lo, al, ti] )

rate = (0.0107700551979-0.000017) / 0.0107700551979
print rate
for i in range(len(pos) - 1):
  pos[1 + i][0] = rate*(pos[1+i][0] - pos[0][0]) + pos[i][0]

f = open('gps_new.json', 'w')
f.write('[n')
for i in range(len(pos)):
  f.write('  {n')
  f.write('    "timestamp": %s,n' % pos[i][3])
  f.write('    "latitude": %.13f,n' % pos[i][0])
  f.write('    "longitude": %.12f,n' % pos[i][1])
  f.write('    "altitude": %.13fn' % pos[i][2])
  if i == len(pos) - 1:
    f.write('  }n')
  else:
    f.write('  },n')
f.write(']')
f.close()
```



```
[
  {
    "timestamp": 0.0,
    "latitude": 37.7899753693032,
    "longitude": -122.397121279501,
    "altitude": 10.1277933120720
  },
  {
    "timestamp": 0.05,
    "latitude": 37.7899754265434,
    "longitude": -122.397132214792,
    "altitude": 10.1244440078730
  },
  {
    "timestamp": 0.1,
    "latitude": 37.7899755414654,
    "longitude": -122.397143236731,
    "altitude": 10.1220254898070
  },
  {
    "timestamp": 0.15,
    "latitude": 37.7899757143859,
    "longitude": -122.397154347742,
    "altitude": 10.1203002929680
  },
  {
    "timestamp": 0.2,
    "latitude": 37.7899759458176,
    "longitude": -122.397165532403,
    "altitude": 10.1192083358760
  },
  {
    "timestamp": 0.25,
    "latitude": 37.7899762360459,
    "longitude": -122.397176773210,
    "altitude": 10.1185302734370
  },
  {
    "timestamp": 0.3,
    "latitude": 37.7899765851408,
    "longitude": -122.397188054742,
    "altitude": 10.1180019378660
  },
  {
    "timestamp": 0.35,
    "latitude": 37.7899769933924,
    "longitude": -122.397199366426,
    "altitude": 10.1177244186400
  },
  {
    "timestamp": 0.4,
    "latitude": 37.7899774602113,
    "longitude": -122.397210697351,
    "altitude": 10.1174736022940
  },
  {
    "timestamp": 0.45,
    "latitude": 37.7899779856691,
    "longitude": -122.397222042486,
    "altitude": 10.1173887252800
  },
  {
    "timestamp": 0.5,
    "latitude": 37.7899785698098,
    "longitude": -122.397233396459,
    "altitude": 10.1173906326290
  },
  {
    "timestamp": 0.55,
    "latitude": 37.7899792122478,
    "longitude": -122.397244755808,
    "altitude": 10.1174354553220
  },
  {
    "timestamp": 0.6,
    "latitude": 37.7899799127243,
    "longitude": -122.397256118452,
    "altitude": 10.1174955368040
  },
  {
    "timestamp": 0.65,
    "latitude": 37.7899806712363,
    "longitude": -122.397267480749,
    "altitude": 10.1174316406200
  },
  {
    "timestamp": 0.7,
    "latitude": 37.7899814876491,
    "longitude": -122.397278843740,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 0.75,
    "latitude": 37.7899823615452,
    "longitude": -122.397290205868,
    "altitude": 10.1173601150510
  },
  {
    "timestamp": 0.8,
    "latitude": 37.7899832927887,
    "longitude": -122.397301568517,
    "altitude": 10.1173706054680
  },
  {
    "timestamp": 0.85,
    "latitude": 37.7899842815179,
    "longitude": -122.397312931512,
    "altitude": 10.1174211502070
  },
  {
    "timestamp": 0.9,
    "latitude": 37.7899853275968,
    "longitude": -122.397324295028,
    "altitude": 10.1174869537350
  },
  {
    "timestamp": 0.95,
    "latitude": 37.7899864310199,
    "longitude": -122.397335657677,
    "altitude": 10.1174249649040
  },
  {
    "timestamp": 1.0,
    "latitude": 37.7899875917800,
    "longitude": -122.397347019113,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 1.05,
    "latitude": 37.7899888098787,
    "longitude": -122.397358381069,
    "altitude": 10.1173133850090
  },
  {
    "timestamp": 1.1,
    "latitude": 37.7899900847674,
    "longitude": -122.397369743377,
    "altitude": 10.1173658370970
  },
  {
    "timestamp": 1.15,
    "latitude": 37.7899914163023,
    "longitude": -122.397381104645,
    "altitude": 10.1173114776610
  },
  {
    "timestamp": 1.2,
    "latitude": 37.7899928044823,
    "longitude": -122.397392465914,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 1.25,
    "latitude": 37.7899942493082,
    "longitude": -122.397403827529,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 1.3,
    "latitude": 37.7899957507807,
    "longitude": -122.397415189491,
    "altitude": 10.1174774169920
  },
  {
    "timestamp": 1.35,
    "latitude": 37.7899973088924,
    "longitude": -122.397426550240,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 1.4,
    "latitude": 37.7899989236441,
    "longitude": -122.397437911336,
    "altitude": 10.1174364089960
  },
  {
    "timestamp": 1.45,
    "latitude": 37.7900005950354,
    "longitude": -122.397449272604,
    "altitude": 10.1174831390380
  },
  {
    "timestamp": 1.5,
    "latitude": 37.7900023230663,
    "longitude": -122.397460634047,
    "altitude": 10.1175384521480
  },
  {
    "timestamp": 1.55,
    "latitude": 37.7900041077364,
    "longitude": -122.397471995662,
    "altitude": 10.1175937652580
  },
  {
    "timestamp": 1.6,
    "latitude": 37.7900059490447,
    "longitude": -122.397483357278,
    "altitude": 10.1176424026480
  },
  {
    "timestamp": 1.65,
    "latitude": 37.7900078469830,
    "longitude": -122.397494717507,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 1.7,
    "latitude": 37.7900098015504,
    "longitude": -122.397506077736,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 1.75,
    "latitude": 37.7900118127473,
    "longitude": -122.397517438312,
    "altitude": 10.1175651550290
  },
  {
    "timestamp": 1.8,
    "latitude": 37.7900138805727,
    "longitude": -122.397528798888,
    "altitude": 10.1175994873040
  },
  {
    "timestamp": 1.85,
    "latitude": 37.7900160043389,
    "longitude": -122.397540159470,
    "altitude": 10.1176385879510
  },
  {
    "timestamp": 1.9,
    "latitude": 37.7900181840450,
    "longitude": -122.397551520051,
    "altitude": 10.1176729202270
  },
  {
    "timestamp": 1.95,
    "latitude": 37.7900204196836,
    "longitude": -122.397562879420,
    "altitude": 10.1175775527950
  },
  {
    "timestamp": 2.0,
    "latitude": 37.7900227112465,
    "longitude": -122.397574237402,
    "altitude": 10.1174325942990
  },
  {
    "timestamp": 2.05,
    "latitude": 37.7900250587336,
    "longitude": -122.397585595557,
    "altitude": 10.1174049377440
  },
  {
    "timestamp": 2.1,
    "latitude": 37.7900274621393,
    "longitude": -122.397596952847,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 2.15,
    "latitude": 37.7900299214635,
    "longitude": -122.397608310309,
    "altitude": 10.1173181533810
  },
  {
    "timestamp": 2.2,
    "latitude": 37.7900324367004,
    "longitude": -122.397619666905,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 2.25,
    "latitude": 37.7900350078510,
    "longitude": -122.397631023848,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 2.3,
    "latitude": 37.7900376349166,
    "longitude": -122.397642381310,
    "altitude": 10.1173467636100
  },
  {
    "timestamp": 2.35,
    "latitude": 37.7900403178919,
    "longitude": -122.397653737906,
    "altitude": 10.1173048019400
  },
  {
    "timestamp": 2.4,
    "latitude": 37.7900430567774,
    "longitude": -122.397665094849,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 2.45,
    "latitude": 37.7900458515678,
    "longitude": -122.397676450925,
    "altitude": 10.1172819137570
  },
  {
    "timestamp": 2.5,
    "latitude": 37.7900487022645,
    "longitude": -122.397687807521,
    "altitude": 10.1173124313350
  },
  {
    "timestamp": 2.55,
    "latitude": 37.7900516088691,
    "longitude": -122.397699164638,
    "altitude": 10.1173801422110
  },
  {
    "timestamp": 2.6,
    "latitude": 37.7900545713823,
    "longitude": -122.397710522100,
    "altitude": 10.1174583435050
  },
  {
    "timestamp": 2.65,
    "latitude": 37.7900575895309,
    "longitude": -122.397721880085,
    "altitude": 10.1175317764280
  },
  {
    "timestamp": 2.7,
    "latitude": 37.7900606628968,
    "longitude": -122.397733237034,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 2.75,
    "latitude": 37.7900637914735,
    "longitude": -122.397744592943,
    "altitude": 10.1173553466790
  },
  {
    "timestamp": 2.8,
    "latitude": 37.7900669752625,
    "longitude": -122.397755949371,
    "altitude": 10.1173486709590
  },
  {
    "timestamp": 2.85,
    "latitude": 37.7900702142654,
    "longitude": -122.397767306320,
    "altitude": 10.1173944473260
  },
  {
    "timestamp": 2.9,
    "latitude": 37.7900735084767,
    "longitude": -122.397778662402,
    "altitude": 10.1173362731930
  },
  {
    "timestamp": 2.95,
    "latitude": 37.7900768578972,
    "longitude": -122.397790018831,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 3.0,
    "latitude": 37.7900802625282,
    "longitude": -122.397801375779,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 3.05,
    "latitude": 37.7900837223706,
    "longitude": -122.397812733075,
    "altitude": 10.1174898147580
  },
  {
    "timestamp": 3.1,
    "latitude": 37.7900872374250,
    "longitude": -122.397824090717,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 3.15,
    "latitude": 37.7900908076859,
    "longitude": -122.397835447492,
    "altitude": 10.1174907684320
  },
  {
    "timestamp": 3.2,
    "latitude": 37.7900944331540,
    "longitude": -122.397846804614,
    "altitude": 10.1174936294550
  },
  {
    "timestamp": 3.25,
    "latitude": 37.7900981138227,
    "longitude": -122.397858160697,
    "altitude": 10.1174030303950
  },
  {
    "timestamp": 3.3,
    "latitude": 37.7901018496929,
    "longitude": -122.397869517126,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 3.35,
    "latitude": 37.7901056407599,
    "longitude": -122.397880872861,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 3.4,
    "latitude": 37.7901094870182,
    "longitude": -122.397892227731,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 3.45,
    "latitude": 37.7901133881886,
    "longitude": -122.397903581909,
    "altitude": 10.1171007156370
  },
  {
    "timestamp": 3.5,
    "latitude": 37.7901173438544,
    "longitude": -122.397914935398,
    "altitude": 10.1169986724850
  },
  {
    "timestamp": 3.55,
    "latitude": 37.7901213540128,
    "longitude": -122.397926288540,
    "altitude": 10.1169157028190
  },
  {
    "timestamp": 3.6,
    "latitude": 37.7901254186603,
    "longitude": -122.397937641163,
    "altitude": 10.1168479919430
  },
  {
    "timestamp": 3.65,
    "latitude": 37.7901295377954,
    "longitude": -122.397948993785,
    "altitude": 10.1167964935300
  },
  {
    "timestamp": 3.7,
    "latitude": 37.7901337114227,
    "longitude": -122.397960347447,
    "altitude": 10.1168823242180
  },
  {
    "timestamp": 3.75,
    "latitude": 37.7901379395461,
    "longitude": -122.397971702149,
    "altitude": 10.1170234680170
  },
  {
    "timestamp": 3.8,
    "latitude": 37.7901422221700,
    "longitude": -122.397983057891,
    "altitude": 10.1171770095820
  },
  {
    "timestamp": 3.85,
    "latitude": 37.7901465592959,
    "longitude": -122.397994414152,
    "altitude": 10.1173191070550
  },
  {
    "timestamp": 3.9,
    "latitude": 37.7901509509200,
    "longitude": -122.398005769894,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 3.95,
    "latitude": 37.7901553970439,
    "longitude": -122.398017126156,
    "altitude": 10.1173677444450
  },
  {
    "timestamp": 4.0,
    "latitude": 37.7901598976691,
    "longitude": -122.398028482938,
    "altitude": 10.1174392700190
  },
  {
    "timestamp": 4.05,
    "latitude": 37.7901644527987,
    "longitude": -122.398039840499,
    "altitude": 10.1175127029410
  },
  {
    "timestamp": 4.1,
    "latitude": 37.7901690624332,
    "longitude": -122.398051198407,
    "altitude": 10.1175804138180
  },
  {
    "timestamp": 4.15,
    "latitude": 37.7901737265738,
    "longitude": -122.398062556748,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 4.2,
    "latitude": 37.7901784452210,
    "longitude": -122.398073915436,
    "altitude": 10.1176815032950
  },
  {
    "timestamp": 4.25,
    "latitude": 37.7901832178247,
    "longitude": -122.398085274129,
    "altitude": 10.1177158355710
  },
  {
    "timestamp": 4.3,
    "latitude": 37.7901880442420,
    "longitude": -122.398096631956,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 4.35,
    "latitude": 37.7901929244722,
    "longitude": -122.398107989870,
    "altitude": 10.1175899505610
  },
  {
    "timestamp": 4.4,
    "latitude": 37.7901978585161,
    "longitude": -122.398119348130,
    "altitude": 10.1175985336300
  },
  {
    "timestamp": 4.45,
    "latitude": 37.7902028463666,
    "longitude": -122.398130705264,
    "altitude": 10.1174993515010
  },
  {
    "timestamp": 4.5,
    "latitude": 37.7902078880181,
    "longitude": -122.398142061445,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.55,
    "latitude": 37.7902129834647,
    "longitude": -122.398153416760,
    "altitude": 10.1172180175780
  },
  {
    "timestamp": 4.6,
    "latitude": 37.7902181327083,
    "longitude": -122.398164772594,
    "altitude": 10.1172151565550
  },
  {
    "timestamp": 4.65,
    "latitude": 37.7902233357502,
    "longitude": -122.398176128949,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 4.7,
    "latitude": 37.7902285925861,
    "longitude": -122.398187484610,
    "altitude": 10.1172380447380
  },
  {
    "timestamp": 4.75,
    "latitude": 37.7902339032172,
    "longitude": -122.398198840791,
    "altitude": 10.1172828674310
  },
  {
    "timestamp": 4.8,
    "latitude": 37.7902392676462,
    "longitude": -122.398210197665,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.85,
    "latitude": 37.7902446858735,
    "longitude": -122.398221554886,
    "altitude": 10.1174459457390
  },
  {
    "timestamp": 4.9,
    "latitude": 37.7902501578997,
    "longitude": -122.398232912367,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 4.95,
    "latitude": 37.7902556837195,
    "longitude": -122.398244269068,
    "altitude": 10.1174678802400
  },
  {
    "timestamp": 5.0,
    "latitude": 37.7902612633335,
    "longitude": -122.398255626116,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 5.05,
    "latitude": 37.7902668961933,
    "longitude": -122.398266983515,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 5.1,
    "latitude": 37.7902725821561,
    "longitude": -122.398278340048,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 5.15,
    "latitude": 37.7902783212225,
    "longitude": -122.398289696929,
    "altitude": 10.1174468994140
  },
  {
    "timestamp": 5.2,
    "latitude": 37.7902841133799,
    "longitude": -122.398301051556,
    "altitude": 10.1172370910640
  },
  {
    "timestamp": 5.25,
    "latitude": 37.7902899586237,
    "longitude": -122.398312405490,
    "altitude": 10.1170768737790
  },
  {
    "timestamp": 5.3,
    "latitude": 37.7902958569563,
    "longitude": -122.398323760117,
    "altitude": 10.1170806884760
  },
  {
    "timestamp": 5.35,
    "latitude": 37.7903018083750,
    "longitude": -122.398335114398,
    "altitude": 10.1170358657830
  },
  {
    "timestamp": 5.4,
    "latitude": 37.7903078128825,
    "longitude": -122.398346469459,
    "altitude": 10.1170988082880
  },
  {
    "timestamp": 5.45,
    "latitude": 37.7903138704808,
    "longitude": -122.398357825126,
    "altitude": 10.1172056198100
  },
  {
    "timestamp": 5.5,
    "latitude": 37.7903199811726,
    "longitude": -122.398369181487,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 5.55,
    "latitude": 37.7903261449596,
    "longitude": -122.398380538454,
    "altitude": 10.1174306869500
  },
  {
    "timestamp": 5.6,
    "latitude": 37.7903323618431,
    "longitude": -122.398391895854,
    "altitude": 10.1175231933590
  },
  {
    "timestamp": 5.65,
    "latitude": 37.7903386318175,
    "longitude": -122.398403252388,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 5.7,
    "latitude": 37.7903449548840,
    "longitude": -122.398414609355,
    "altitude": 10.1174850463860
  },
  {
    "timestamp": 5.75,
    "latitude": 37.7903513310431,
    "longitude": -122.398425966669,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 5.8,
    "latitude": 37.7903577602899,
    "longitude": -122.398437323203,
    "altitude": 10.1174497604300
  },
  {
    "timestamp": 5.85,
    "latitude": 37.7903642420630,
    "longitude": -122.398448677575,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 5.9,
    "latitude": 37.7903707762270,
    "longitude": -122.398460032555,
    "altitude": 10.1171531677240
  },
  {
    "timestamp": 5.95,
    "latitude": 37.7903773627769,
    "longitude": -122.398471386755,
    "altitude": 10.1170740127560
  },
  {
    "timestamp": 6.0,
    "latitude": 37.7903840017165,
    "longitude": -122.398482741908,
    "altitude": 10.1171169281000
  },
  {
    "timestamp": 6.05,
    "latitude": 37.7903906930487,
    "longitude": -122.398494097842,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 6.1,
    "latitude": 37.7903974367754,
    "longitude": -122.398505454381,
    "altitude": 10.1173210144040
  },
  {
    "timestamp": 6.15,
    "latitude": 37.7904042328987,
    "longitude": -122.398516811528,
    "altitude": 10.1174259185790
  },
  {
    "timestamp": 6.2,
    "latitude": 37.7904110814197,
    "longitude": -122.398528169107,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 6.25,
    "latitude": 37.7904179823390,
    "longitude": -122.398539527033,
    "altitude": 10.1175928115840
  },
  {
    "timestamp": 6.3,
    "latitude": 37.7904249356573,
    "longitude": -122.398550885306,
    "altitude": 10.1176500320430
  },
  {
    "timestamp": 6.35,
    "latitude": 37.7904319413739,
    "longitude": -122.398562243665,
    "altitude": 10.1176948547360
  },
  {
    "timestamp": 6.4,
    "latitude": 37.7904389994896,
    "longitude": -122.398573602371,
    "altitude": 10.1177272796630
  },
  {
    "timestamp": 6.45,
    "latitude": 37.7904461100037,
    "longitude": -122.398584961164,
    "altitude": 10.1177511215200
  },
  {
    "timestamp": 6.5,
    "latitude": 37.7904532729160,
    "longitude": -122.398596320130,
    "altitude": 10.1177663803100
  },
  {
    "timestamp": 6.55,
    "latitude": 37.7904604882192,
    "longitude": -122.398607677883,
    "altitude": 10.1176519393920
  },
  {
    "timestamp": 6.6,
    "latitude": 37.7904677559127,
    "longitude": -122.398619035723,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 6.65,
    "latitude": 37.7904750753096,
    "longitude": -122.398630393742,
    "altitude": 10.1176176071160
  },
  {
    "timestamp": 6.7,
    "latitude": 37.7904824464103,
    "longitude": -122.398641752020,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 6.75,
    "latitude": 37.7904898692140,
    "longitude": -122.398653110385,
    "altitude": 10.1176633834830
  },
  {
    "timestamp": 6.8,
    "latitude": 37.7904973437199,
    "longitude": -122.398664468751,
    "altitude": 10.1176910400390
  },
  {
    "timestamp": 6.85,
    "latitude": 37.7905048699274,
    "longitude": -122.398675827289,
    "altitude": 10.1177148818900
  },
  {
    "timestamp": 6.9,
    "latitude": 37.7905124478357,
    "longitude": -122.398687185828,
    "altitude": 10.1177368164060
  },
  {
    "timestamp": 6.95,
    "latitude": 37.7905200774373,
    "longitude": -122.398698543154,
    "altitude": 10.1176271438590
  },
  {
    "timestamp": 7.0,
    "latitude": 37.7905277587251,
    "longitude": -122.398709899266,
    "altitude": 10.1174707412700
  },
  {
    "timestamp": 7.05,
    "latitude": 37.7905354916931,
    "longitude": -122.398721254426,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 7.1,
    "latitude": 37.7905432763353,
    "longitude": -122.398732608632,
    "altitude": 10.1171607971190
  },
  {
    "timestamp": 7.15,
    "latitude": 37.7905511126414,
    "longitude": -122.398743961019,
    "altitude": 10.1169099807730
  },
  {
    "timestamp": 7.2,
    "latitude": 37.7905590006064,
    "longitude": -122.398755312626,
    "altitude": 10.1167659759520
  },
  {
    "timestamp": 7.25,
    "latitude": 37.7905669402349,
    "longitude": -122.398766665403,
    "altitude": 10.1168107986400
  },
  {
    "timestamp": 7.3,
    "latitude": 37.7905749315314,
    "longitude": -122.398778019220,
    "altitude": 10.1169395446770
  },
  {
    "timestamp": 7.35,
    "latitude": 37.7905829744989,
    "longitude": -122.398789373859,
    "altitude": 10.1170969009390
  },
  {
    "timestamp": 7.4,
    "latitude": 37.7905910691405,
    "longitude": -122.398800729322,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 7.45,
    "latitude": 37.7905992150465,
    "longitude": -122.398812085439,
    "altitude": 10.1173830032340
  },
  {
    "timestamp": 7.5,
    "latitude": 37.7906074119440,
    "longitude": -122.398823442120,
    "altitude": 10.1174917221060
  },
  {
    "timestamp": 7.55,
    "latitude": 37.7906156598279,
    "longitude": -122.398834797979,
    "altitude": 10.1174545288080
  },
  {
    "timestamp": 7.6,
    "latitude": 37.7906239586991,
    "longitude": -122.398846154271,
    "altitude": 10.1174764633170
  },
  {
    "timestamp": 7.65,
    "latitude": 37.7906323085531,
    "longitude": -122.398857509869,
    "altitude": 10.1173954010000
  },
  {
    "timestamp": 7.7,
    "latitude": 37.7906407093911,
    "longitude": -122.398868865945,
    "altitude": 10.1174020767210
  },
  {
    "timestamp": 7.75,
    "latitude": 37.7906491612148,
    "longitude": -122.398880222540,
    "altitude": 10.1174488067620
  },
  {
    "timestamp": 7.8,
    "latitude": 37.7906576640255,
    "longitude": -122.398891579612,
    "altitude": 10.1175098419180
  },
  {
    "timestamp": 7.85,
    "latitude": 37.7906662178243,
    "longitude": -122.398902937117,
    "altitude": 10.1175699234000
  },
  {
    "timestamp": 7.9,
    "latitude": 37.7906748226116,
    "longitude": -122.398914294925,
    "altitude": 10.1176242828360
  },
  {
    "timestamp": 7.95,
    "latitude": 37.7906834783813,
    "longitude": -122.398925651737,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 8.0,
    "latitude": 37.7906921851336,
    "longitude": -122.398937008809,
    "altitude": 10.1175346374510
  },
  {
    "timestamp": 8.05,
    "latitude": 37.7907009428628,
    "longitude": -122.398948364971,
    "altitude": 10.1174345016470
  },
  {
    "timestamp": 8.1,
    "latitude": 37.7907097515698,
    "longitude": -122.398959721523,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.15,
    "latitude": 37.7907186112557,
    "longitude": -122.398971078508,
    "altitude": 10.1174640655510
  },
  {
    "timestamp": 8.2,
    "latitude": 37.7907275219209,
    "longitude": -122.398982435797,
    "altitude": 10.1175184249870
  },
  {
    "timestamp": 8.25,
    "latitude": 37.7907364830171,
    "longitude": -122.398993793480,
    "altitude": 10.1175756454460
  },
  {
    "timestamp": 8.3,
    "latitude": 37.7907454944005,
    "longitude": -122.399005150081,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.35,
    "latitude": 37.7907545560716,
    "longitude": -122.399016507029,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.4,
    "latitude": 37.7907636680312,
    "longitude": -122.399027864323,
    "altitude": 10.1175327301020
  },
  {
    "timestamp": 8.45,
    "latitude": 37.7907728302797,
    "longitude": -122.399039221921,
    "altitude": 10.1175765991210
  },
  {
    "timestamp": 8.5,
    "latitude": 37.7907820428170,
    "longitude": -122.399050579735,
    "altitude": 10.1176214218100
  },
  {
    "timestamp": 8.55,
    "latitude": 37.7907913056367,
    "longitude": -122.399061936466,
    "altitude": 10.1175374984740
  },
  {
    "timestamp": 8.6,
    "latitude": 37.7908006187389,
    "longitude": -122.399073293457,
    "altitude": 10.1175270080560
  },
  {
    "timestamp": 8.65,
    "latitude": 37.7908099821174,
    "longitude": -122.399084649452,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.7,
    "latitude": 37.7908193957730,
    "longitude": -122.399096005794,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 8.75,
    "latitude": 37.7908288597004,
    "longitude": -122.399107361312,
    "altitude": 10.1173334121700
  },
  {
    "timestamp": 8.8,
    "latitude": 37.7908383739004,
    "longitude": -122.399118717220,
    "altitude": 10.1173448562620
  },
  {
    "timestamp": 8.85,
    "latitude": 37.7908479383745,
    "longitude": -122.399130073648,
    "altitude": 10.1174001693720
  },
  {
    "timestamp": 8.9,
    "latitude": 37.7908575531238,
    "longitude": -122.399141430466,
    "altitude": 10.1174697875970
  },
  {
    "timestamp": 8.95,
    "latitude": 37.7908672181426,
    "longitude": -122.399152786418,
    "altitude": 10.1174125671380
  },
  {
    "timestamp": 9.0,
    "latitude": 37.7908769334252,
    "longitude": -122.399164141460,
    "altitude": 10.1173057556150
  },
  {
    "timestamp": 9.05,
    "latitude": 37.7908866985547,
    "longitude": -122.399175495704,
    "altitude": 10.1171846389770
  },
  {
    "timestamp": 9.1,
    "latitude": 37.7908965132520,
    "longitude": -122.399186849321,
    "altitude": 10.1170701980590
  },
  {
    "timestamp": 9.15,
    "latitude": 37.7909063775135,
    "longitude": -122.399198202441,
    "altitude": 10.1169719696040
  },
  {
    "timestamp": 9.2,
    "latitude": 37.7909162913360,
    "longitude": -122.399209555128,
    "altitude": 10.1168909072870
  },
  {
    "timestamp": 9.25,
    "latitude": 37.7909262547167,
    "longitude": -122.399220907511,
    "altitude": 10.1168279647820
  },
  {
    "timestamp": 9.3,
    "latitude": 37.7909362676598,
    "longitude": -122.399232260890,
    "altitude": 10.1169061660760
  },
  {
    "timestamp": 9.35,
    "latitude": 37.7909463301693,
    "longitude": -122.399243615310,
    "altitude": 10.1170415878290
  },
  {
    "timestamp": 9.4,
    "latitude": 37.7909564422487,
    "longitude": -122.399254970596,
    "altitude": 10.1171903610220
  },
  {
    "timestamp": 9.45,
    "latitude": 37.7909666038942,
    "longitude": -122.399266325384,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 9.5,
    "latitude": 37.7909768151018,
    "longitude": -122.399277679587,
    "altitude": 10.1171512603700
  },
  {
    "timestamp": 9.55,
    "latitude": 37.7909870758744,
    "longitude": -122.399289034569,
    "altitude": 10.1171989440910
  },
  {
    "timestamp": 9.6,
    "latitude": 37.7909973862150,
    "longitude": -122.399300390375,
    "altitude": 10.1172876358030
  },
  {
    "timestamp": 9.65,
    "latitude": 37.7910077461262,
    "longitude": -122.399311746896,
    "altitude": 10.1173849105830
  },
  {
    "timestamp": 9.7,
    "latitude": 37.7910181556101,
    "longitude": -122.399323104023,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 9.75,
    "latitude": 37.7910286146679,
    "longitude": -122.399334461617,
    "altitude": 10.1175584793090
  },
  {
    "timestamp": 9.8,
    "latitude": 37.7910391233006,
    "longitude": -122.399345819621,
    "altitude": 10.1176233291620
  },
  {
    "timestamp": 9.85,
    "latitude": 37.7910496808222,
    "longitude": -122.399357177957,
    "altitude": 10.1176738739010
  },
  {
    "timestamp": 9.9,
    "latitude": 37.7910602872266,
    "longitude": -122.399368535295,
    "altitude": 10.1175851821890
  },
  {
    "timestamp": 9.95,
    "latitude": 37.7910709425141,
    "longitude": -122.399379892916,
    "altitude": 10.1175680160520
  },
  {
    "timestamp": 10.0,
    "latitude": 37.7910816466851,
    "longitude": -122.399391250861,
    "altitude": 10.1175842285150
  },
  {
    "timestamp": 10.05,
    "latitude": 37.7910923997403,
    "longitude": -122.399402609105,
    "altitude": 10.1176166534420
  }
]
```



```
f = open('gps.json', 'r')
gps = f.read()
f.close()
gpslines = gps.split('n')
pos = []
for line in gpslines:
  i0 = line.find('timestamp')
  if i0 >= 0:
    ti = line[i0+12:-1]
  i1 = line.find('latitude')
  if i1 >= 0:
    la = float(line[i1+11:-1])
  i2 = line.find('longitude')
  if i2 >= 0:
    lo = float(line[i2+12:-1])
  i3 = line.find('altitude')
  if i3 >= 0:
    al = float(line[i3+11:-1])
    pos.append( [la, lo, al, ti] )

rate = (0.0107700551979-0.000017) / 0.0107700551979
print rate
for i in range(len(pos) - 1):
  pos[1 + i][0] = rate*(pos[1+i][0] - pos[0][0]) + pos[i][0]

f = open('gps_new.json', 'w')
f.write('[n')
for i in range(len(pos)):
  f.write('  {n')
  f.write('    "timestamp": %s,n' % pos[i][3])
  f.write('    "latitude": %.13f,n' % pos[i][0])
  f.write('    "longitude": %.12f,n' % pos[i][1])
  f.write('    "altitude": %.13fn' % pos[i][2])
  if i == len(pos) - 1:
    f.write('  }n')
  else:
    f.write('  },n')
f.write(']')
f.close()
```



```
[
  {
    "timestamp": 0.0,
    "latitude": 37.7899753693032,
    "longitude": -122.397121279501,
    "altitude": 10.1277933120720
  },
  {
    "timestamp": 0.05,
    "latitude": 37.7899754265434,
    "longitude": -122.397132214792,
    "altitude": 10.1244440078730
  },
  {
    "timestamp": 0.1,
    "latitude": 37.7899755414654,
    "longitude": -122.397143236731,
    "altitude": 10.1220254898070
  },
  {
    "timestamp": 0.15,
    "latitude": 37.7899757143859,
    "longitude": -122.397154347742,
    "altitude": 10.1203002929680
  },
  {
    "timestamp": 0.2,
    "latitude": 37.7899759458176,
    "longitude": -122.397165532403,
    "altitude": 10.1192083358760
  },
  {
    "timestamp": 0.25,
    "latitude": 37.7899762360459,
    "longitude": -122.397176773210,
    "altitude": 10.1185302734370
  },
  {
    "timestamp": 0.3,
    "latitude": 37.7899765851408,
    "longitude": -122.397188054742,
    "altitude": 10.1180019378660
  },
  {
    "timestamp": 0.35,
    "latitude": 37.7899769933924,
    "longitude": -122.397199366426,
    "altitude": 10.1177244186400
  },
  {
    "timestamp": 0.4,
    "latitude": 37.7899774602113,
    "longitude": -122.397210697351,
    "altitude": 10.1174736022940
  },
  {
    "timestamp": 0.45,
    "latitude": 37.7899779856691,
    "longitude": -122.397222042486,
    "altitude": 10.1173887252800
  },
  {
    "timestamp": 0.5,
    "latitude": 37.7899785698098,
    "longitude": -122.397233396459,
    "altitude": 10.1173906326290
  },
  {
    "timestamp": 0.55,
    "latitude": 37.7899792122478,
    "longitude": -122.397244755808,
    "altitude": 10.1174354553220
  },
  {
    "timestamp": 0.6,
    "latitude": 37.7899799127243,
    "longitude": -122.397256118452,
    "altitude": 10.1174955368040
  },
  {
    "timestamp": 0.65,
    "latitude": 37.7899806712363,
    "longitude": -122.397267480749,
    "altitude": 10.1174316406200
  },
  {
    "timestamp": 0.7,
    "latitude": 37.7899814876491,
    "longitude": -122.397278843740,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 0.75,
    "latitude": 37.7899823615452,
    "longitude": -122.397290205868,
    "altitude": 10.1173601150510
  },
  {
    "timestamp": 0.8,
    "latitude": 37.7899832927887,
    "longitude": -122.397301568517,
    "altitude": 10.1173706054680
  },
  {
    "timestamp": 0.85,
    "latitude": 37.7899842815179,
    "longitude": -122.397312931512,
    "altitude": 10.1174211502070
  },
  {
    "timestamp": 0.9,
    "latitude": 37.7899853275968,
    "longitude": -122.397324295028,
    "altitude": 10.1174869537350
  },
  {
    "timestamp": 0.95,
    "latitude": 37.7899864310199,
    "longitude": -122.397335657677,
    "altitude": 10.1174249649040
  },
  {
    "timestamp": 1.0,
    "latitude": 37.7899875917800,
    "longitude": -122.397347019113,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 1.05,
    "latitude": 37.7899888098787,
    "longitude": -122.397358381069,
    "altitude": 10.1173133850090
  },
  {
    "timestamp": 1.1,
    "latitude": 37.7899900847674,
    "longitude": -122.397369743377,
    "altitude": 10.1173658370970
  },
  {
    "timestamp": 1.15,
    "latitude": 37.7899914163023,
    "longitude": -122.397381104645,
    "altitude": 10.1173114776610
  },
  {
    "timestamp": 1.2,
    "latitude": 37.7899928044823,
    "longitude": -122.397392465914,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 1.25,
    "latitude": 37.7899942493082,
    "longitude": -122.397403827529,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 1.3,
    "latitude": 37.7899957507807,
    "longitude": -122.397415189491,
    "altitude": 10.1174774169920
  },
  {
    "timestamp": 1.35,
    "latitude": 37.7899973088924,
    "longitude": -122.397426550240,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 1.4,
    "latitude": 37.7899989236441,
    "longitude": -122.397437911336,
    "altitude": 10.1174364089960
  },
  {
    "timestamp": 1.45,
    "latitude": 37.7900005950354,
    "longitude": -122.397449272604,
    "altitude": 10.1174831390380
  },
  {
    "timestamp": 1.5,
    "latitude": 37.7900023230663,
    "longitude": -122.397460634047,
    "altitude": 10.1175384521480
  },
  {
    "timestamp": 1.55,
    "latitude": 37.7900041077364,
    "longitude": -122.397471995662,
    "altitude": 10.1175937652580
  },
  {
    "timestamp": 1.6,
    "latitude": 37.7900059490447,
    "longitude": -122.397483357278,
    "altitude": 10.1176424026480
  },
  {
    "timestamp": 1.65,
    "latitude": 37.7900078469830,
    "longitude": -122.397494717507,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 1.7,
    "latitude": 37.7900098015504,
    "longitude": -122.397506077736,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 1.75,
    "latitude": 37.7900118127473,
    "longitude": -122.397517438312,
    "altitude": 10.1175651550290
  },
  {
    "timestamp": 1.8,
    "latitude": 37.7900138805727,
    "longitude": -122.397528798888,
    "altitude": 10.1175994873040
  },
  {
    "timestamp": 1.85,
    "latitude": 37.7900160043389,
    "longitude": -122.397540159470,
    "altitude": 10.1176385879510
  },
  {
    "timestamp": 1.9,
    "latitude": 37.7900181840450,
    "longitude": -122.397551520051,
    "altitude": 10.1176729202270
  },
  {
    "timestamp": 1.95,
    "latitude": 37.7900204196836,
    "longitude": -122.397562879420,
    "altitude": 10.1175775527950
  },
  {
    "timestamp": 2.0,
    "latitude": 37.7900227112465,
    "longitude": -122.397574237402,
    "altitude": 10.1174325942990
  },
  {
    "timestamp": 2.05,
    "latitude": 37.7900250587336,
    "longitude": -122.397585595557,
    "altitude": 10.1174049377440
  },
  {
    "timestamp": 2.1,
    "latitude": 37.7900274621393,
    "longitude": -122.397596952847,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 2.15,
    "latitude": 37.7900299214635,
    "longitude": -122.397608310309,
    "altitude": 10.1173181533810
  },
  {
    "timestamp": 2.2,
    "latitude": 37.7900324367004,
    "longitude": -122.397619666905,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 2.25,
    "latitude": 37.7900350078510,
    "longitude": -122.397631023848,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 2.3,
    "latitude": 37.7900376349166,
    "longitude": -122.397642381310,
    "altitude": 10.1173467636100
  },
  {
    "timestamp": 2.35,
    "latitude": 37.7900403178919,
    "longitude": -122.397653737906,
    "altitude": 10.1173048019400
  },
  {
    "timestamp": 2.4,
    "latitude": 37.7900430567774,
    "longitude": -122.397665094849,
    "altitude": 10.1173410415640
  },
  {
    "timestamp": 2.45,
    "latitude": 37.7900458515678,
    "longitude": -122.397676450925,
    "altitude": 10.1172819137570
  },
  {
    "timestamp": 2.5,
    "latitude": 37.7900487022645,
    "longitude": -122.397687807521,
    "altitude": 10.1173124313350
  },
  {
    "timestamp": 2.55,
    "latitude": 37.7900516088691,
    "longitude": -122.397699164638,
    "altitude": 10.1173801422110
  },
  {
    "timestamp": 2.6,
    "latitude": 37.7900545713823,
    "longitude": -122.397710522100,
    "altitude": 10.1174583435050
  },
  {
    "timestamp": 2.65,
    "latitude": 37.7900575895309,
    "longitude": -122.397721880085,
    "altitude": 10.1175317764280
  },
  {
    "timestamp": 2.7,
    "latitude": 37.7900606628968,
    "longitude": -122.397733237034,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 2.75,
    "latitude": 37.7900637914735,
    "longitude": -122.397744592943,
    "altitude": 10.1173553466790
  },
  {
    "timestamp": 2.8,
    "latitude": 37.7900669752625,
    "longitude": -122.397755949371,
    "altitude": 10.1173486709590
  },
  {
    "timestamp": 2.85,
    "latitude": 37.7900702142654,
    "longitude": -122.397767306320,
    "altitude": 10.1173944473260
  },
  {
    "timestamp": 2.9,
    "latitude": 37.7900735084767,
    "longitude": -122.397778662402,
    "altitude": 10.1173362731930
  },
  {
    "timestamp": 2.95,
    "latitude": 37.7900768578972,
    "longitude": -122.397790018831,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 3.0,
    "latitude": 37.7900802625282,
    "longitude": -122.397801375779,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 3.05,
    "latitude": 37.7900837223706,
    "longitude": -122.397812733075,
    "altitude": 10.1174898147580
  },
  {
    "timestamp": 3.1,
    "latitude": 37.7900872374250,
    "longitude": -122.397824090717,
    "altitude": 10.1175565719600
  },
  {
    "timestamp": 3.15,
    "latitude": 37.7900908076859,
    "longitude": -122.397835447492,
    "altitude": 10.1174907684320
  },
  {
    "timestamp": 3.2,
    "latitude": 37.7900944331540,
    "longitude": -122.397846804614,
    "altitude": 10.1174936294550
  },
  {
    "timestamp": 3.25,
    "latitude": 37.7900981138227,
    "longitude": -122.397858160697,
    "altitude": 10.1174030303950
  },
  {
    "timestamp": 3.3,
    "latitude": 37.7901018496929,
    "longitude": -122.397869517126,
    "altitude": 10.1174039840690
  },
  {
    "timestamp": 3.35,
    "latitude": 37.7901056407599,
    "longitude": -122.397880872861,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 3.4,
    "latitude": 37.7901094870182,
    "longitude": -122.397892227731,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 3.45,
    "latitude": 37.7901133881886,
    "longitude": -122.397903581909,
    "altitude": 10.1171007156370
  },
  {
    "timestamp": 3.5,
    "latitude": 37.7901173438544,
    "longitude": -122.397914935398,
    "altitude": 10.1169986724850
  },
  {
    "timestamp": 3.55,
    "latitude": 37.7901213540128,
    "longitude": -122.397926288540,
    "altitude": 10.1169157028190
  },
  {
    "timestamp": 3.6,
    "latitude": 37.7901254186603,
    "longitude": -122.397937641163,
    "altitude": 10.1168479919430
  },
  {
    "timestamp": 3.65,
    "latitude": 37.7901295377954,
    "longitude": -122.397948993785,
    "altitude": 10.1167964935300
  },
  {
    "timestamp": 3.7,
    "latitude": 37.7901337114227,
    "longitude": -122.397960347447,
    "altitude": 10.1168823242180
  },
  {
    "timestamp": 3.75,
    "latitude": 37.7901379395461,
    "longitude": -122.397971702149,
    "altitude": 10.1170234680170
  },
  {
    "timestamp": 3.8,
    "latitude": 37.7901422221700,
    "longitude": -122.397983057891,
    "altitude": 10.1171770095820
  },
  {
    "timestamp": 3.85,
    "latitude": 37.7901465592959,
    "longitude": -122.397994414152,
    "altitude": 10.1173191070550
  },
  {
    "timestamp": 3.9,
    "latitude": 37.7901509509200,
    "longitude": -122.398005769894,
    "altitude": 10.1173143386840
  },
  {
    "timestamp": 3.95,
    "latitude": 37.7901553970439,
    "longitude": -122.398017126156,
    "altitude": 10.1173677444450
  },
  {
    "timestamp": 4.0,
    "latitude": 37.7901598976691,
    "longitude": -122.398028482938,
    "altitude": 10.1174392700190
  },
  {
    "timestamp": 4.05,
    "latitude": 37.7901644527987,
    "longitude": -122.398039840499,
    "altitude": 10.1175127029410
  },
  {
    "timestamp": 4.1,
    "latitude": 37.7901690624332,
    "longitude": -122.398051198407,
    "altitude": 10.1175804138180
  },
  {
    "timestamp": 4.15,
    "latitude": 37.7901737265738,
    "longitude": -122.398062556748,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 4.2,
    "latitude": 37.7901784452210,
    "longitude": -122.398073915436,
    "altitude": 10.1176815032950
  },
  {
    "timestamp": 4.25,
    "latitude": 37.7901832178247,
    "longitude": -122.398085274129,
    "altitude": 10.1177158355710
  },
  {
    "timestamp": 4.3,
    "latitude": 37.7901880442420,
    "longitude": -122.398096631956,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 4.35,
    "latitude": 37.7901929244722,
    "longitude": -122.398107989870,
    "altitude": 10.1175899505610
  },
  {
    "timestamp": 4.4,
    "latitude": 37.7901978585161,
    "longitude": -122.398119348130,
    "altitude": 10.1175985336300
  },
  {
    "timestamp": 4.45,
    "latitude": 37.7902028463666,
    "longitude": -122.398130705264,
    "altitude": 10.1174993515010
  },
  {
    "timestamp": 4.5,
    "latitude": 37.7902078880181,
    "longitude": -122.398142061445,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.55,
    "latitude": 37.7902129834647,
    "longitude": -122.398153416760,
    "altitude": 10.1172180175780
  },
  {
    "timestamp": 4.6,
    "latitude": 37.7902181327083,
    "longitude": -122.398164772594,
    "altitude": 10.1172151565550
  },
  {
    "timestamp": 4.65,
    "latitude": 37.7902233357502,
    "longitude": -122.398176128949,
    "altitude": 10.1172771453850
  },
  {
    "timestamp": 4.7,
    "latitude": 37.7902285925861,
    "longitude": -122.398187484610,
    "altitude": 10.1172380447380
  },
  {
    "timestamp": 4.75,
    "latitude": 37.7902339032172,
    "longitude": -122.398198840791,
    "altitude": 10.1172828674310
  },
  {
    "timestamp": 4.8,
    "latitude": 37.7902392676462,
    "longitude": -122.398210197665,
    "altitude": 10.1173610687250
  },
  {
    "timestamp": 4.85,
    "latitude": 37.7902446858735,
    "longitude": -122.398221554886,
    "altitude": 10.1174459457390
  },
  {
    "timestamp": 4.9,
    "latitude": 37.7902501578997,
    "longitude": -122.398232912367,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 4.95,
    "latitude": 37.7902556837195,
    "longitude": -122.398244269068,
    "altitude": 10.1174678802400
  },
  {
    "timestamp": 5.0,
    "latitude": 37.7902612633335,
    "longitude": -122.398255626116,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 5.05,
    "latitude": 37.7902668961933,
    "longitude": -122.398266983515,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 5.1,
    "latitude": 37.7902725821561,
    "longitude": -122.398278340048,
    "altitude": 10.1174421310420
  },
  {
    "timestamp": 5.15,
    "latitude": 37.7902783212225,
    "longitude": -122.398289696929,
    "altitude": 10.1174468994140
  },
  {
    "timestamp": 5.2,
    "latitude": 37.7902841133799,
    "longitude": -122.398301051556,
    "altitude": 10.1172370910640
  },
  {
    "timestamp": 5.25,
    "latitude": 37.7902899586237,
    "longitude": -122.398312405490,
    "altitude": 10.1170768737790
  },
  {
    "timestamp": 5.3,
    "latitude": 37.7902958569563,
    "longitude": -122.398323760117,
    "altitude": 10.1170806884760
  },
  {
    "timestamp": 5.35,
    "latitude": 37.7903018083750,
    "longitude": -122.398335114398,
    "altitude": 10.1170358657830
  },
  {
    "timestamp": 5.4,
    "latitude": 37.7903078128825,
    "longitude": -122.398346469459,
    "altitude": 10.1170988082880
  },
  {
    "timestamp": 5.45,
    "latitude": 37.7903138704808,
    "longitude": -122.398357825126,
    "altitude": 10.1172056198100
  },
  {
    "timestamp": 5.5,
    "latitude": 37.7903199811726,
    "longitude": -122.398369181487,
    "altitude": 10.1173219680780
  },
  {
    "timestamp": 5.55,
    "latitude": 37.7903261449596,
    "longitude": -122.398380538454,
    "altitude": 10.1174306869500
  },
  {
    "timestamp": 5.6,
    "latitude": 37.7903323618431,
    "longitude": -122.398391895854,
    "altitude": 10.1175231933590
  },
  {
    "timestamp": 5.65,
    "latitude": 37.7903386318175,
    "longitude": -122.398403252388,
    "altitude": 10.1174716949460
  },
  {
    "timestamp": 5.7,
    "latitude": 37.7903449548840,
    "longitude": -122.398414609355,
    "altitude": 10.1174850463860
  },
  {
    "timestamp": 5.75,
    "latitude": 37.7903513310431,
    "longitude": -122.398425966669,
    "altitude": 10.1175251007000
  },
  {
    "timestamp": 5.8,
    "latitude": 37.7903577602899,
    "longitude": -122.398437323203,
    "altitude": 10.1174497604300
  },
  {
    "timestamp": 5.85,
    "latitude": 37.7903642420630,
    "longitude": -122.398448677575,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 5.9,
    "latitude": 37.7903707762270,
    "longitude": -122.398460032555,
    "altitude": 10.1171531677240
  },
  {
    "timestamp": 5.95,
    "latitude": 37.7903773627769,
    "longitude": -122.398471386755,
    "altitude": 10.1170740127560
  },
  {
    "timestamp": 6.0,
    "latitude": 37.7903840017165,
    "longitude": -122.398482741908,
    "altitude": 10.1171169281000
  },
  {
    "timestamp": 6.05,
    "latitude": 37.7903906930487,
    "longitude": -122.398494097842,
    "altitude": 10.1172113418570
  },
  {
    "timestamp": 6.1,
    "latitude": 37.7903974367754,
    "longitude": -122.398505454381,
    "altitude": 10.1173210144040
  },
  {
    "timestamp": 6.15,
    "latitude": 37.7904042328987,
    "longitude": -122.398516811528,
    "altitude": 10.1174259185790
  },
  {
    "timestamp": 6.2,
    "latitude": 37.7904110814197,
    "longitude": -122.398528169107,
    "altitude": 10.1175174713130
  },
  {
    "timestamp": 6.25,
    "latitude": 37.7904179823390,
    "longitude": -122.398539527033,
    "altitude": 10.1175928115840
  },
  {
    "timestamp": 6.3,
    "latitude": 37.7904249356573,
    "longitude": -122.398550885306,
    "altitude": 10.1176500320430
  },
  {
    "timestamp": 6.35,
    "latitude": 37.7904319413739,
    "longitude": -122.398562243665,
    "altitude": 10.1176948547360
  },
  {
    "timestamp": 6.4,
    "latitude": 37.7904389994896,
    "longitude": -122.398573602371,
    "altitude": 10.1177272796630
  },
  {
    "timestamp": 6.45,
    "latitude": 37.7904461100037,
    "longitude": -122.398584961164,
    "altitude": 10.1177511215200
  },
  {
    "timestamp": 6.5,
    "latitude": 37.7904532729160,
    "longitude": -122.398596320130,
    "altitude": 10.1177663803100
  },
  {
    "timestamp": 6.55,
    "latitude": 37.7904604882192,
    "longitude": -122.398607677883,
    "altitude": 10.1176519393920
  },
  {
    "timestamp": 6.6,
    "latitude": 37.7904677559127,
    "longitude": -122.398619035723,
    "altitude": 10.1176156997680
  },
  {
    "timestamp": 6.65,
    "latitude": 37.7904750753096,
    "longitude": -122.398630393742,
    "altitude": 10.1176176071160
  },
  {
    "timestamp": 6.7,
    "latitude": 37.7904824464103,
    "longitude": -122.398641752020,
    "altitude": 10.1176366806000
  },
  {
    "timestamp": 6.75,
    "latitude": 37.7904898692140,
    "longitude": -122.398653110385,
    "altitude": 10.1176633834830
  },
  {
    "timestamp": 6.8,
    "latitude": 37.7904973437199,
    "longitude": -122.398664468751,
    "altitude": 10.1176910400390
  },
  {
    "timestamp": 6.85,
    "latitude": 37.7905048699274,
    "longitude": -122.398675827289,
    "altitude": 10.1177148818900
  },
  {
    "timestamp": 6.9,
    "latitude": 37.7905124478357,
    "longitude": -122.398687185828,
    "altitude": 10.1177368164060
  },
  {
    "timestamp": 6.95,
    "latitude": 37.7905200774373,
    "longitude": -122.398698543154,
    "altitude": 10.1176271438590
  },
  {
    "timestamp": 7.0,
    "latitude": 37.7905277587251,
    "longitude": -122.398709899266,
    "altitude": 10.1174707412700
  },
  {
    "timestamp": 7.05,
    "latitude": 37.7905354916931,
    "longitude": -122.398721254426,
    "altitude": 10.1173086166380
  },
  {
    "timestamp": 7.1,
    "latitude": 37.7905432763353,
    "longitude": -122.398732608632,
    "altitude": 10.1171607971190
  },
  {
    "timestamp": 7.15,
    "latitude": 37.7905511126414,
    "longitude": -122.398743961019,
    "altitude": 10.1169099807730
  },
  {
    "timestamp": 7.2,
    "latitude": 37.7905590006064,
    "longitude": -122.398755312626,
    "altitude": 10.1167659759520
  },
  {
    "timestamp": 7.25,
    "latitude": 37.7905669402349,
    "longitude": -122.398766665403,
    "altitude": 10.1168107986400
  },
  {
    "timestamp": 7.3,
    "latitude": 37.7905749315314,
    "longitude": -122.398778019220,
    "altitude": 10.1169395446770
  },
  {
    "timestamp": 7.35,
    "latitude": 37.7905829744989,
    "longitude": -122.398789373859,
    "altitude": 10.1170969009390
  },
  {
    "timestamp": 7.4,
    "latitude": 37.7905910691405,
    "longitude": -122.398800729322,
    "altitude": 10.1172485351560
  },
  {
    "timestamp": 7.45,
    "latitude": 37.7905992150465,
    "longitude": -122.398812085439,
    "altitude": 10.1173830032340
  },
  {
    "timestamp": 7.5,
    "latitude": 37.7906074119440,
    "longitude": -122.398823442120,
    "altitude": 10.1174917221060
  },
  {
    "timestamp": 7.55,
    "latitude": 37.7906156598279,
    "longitude": -122.398834797979,
    "altitude": 10.1174545288080
  },
  {
    "timestamp": 7.6,
    "latitude": 37.7906239586991,
    "longitude": -122.398846154271,
    "altitude": 10.1174764633170
  },
  {
    "timestamp": 7.65,
    "latitude": 37.7906323085531,
    "longitude": -122.398857509869,
    "altitude": 10.1173954010000
  },
  {
    "timestamp": 7.7,
    "latitude": 37.7906407093911,
    "longitude": -122.398868865945,
    "altitude": 10.1174020767210
  },
  {
    "timestamp": 7.75,
    "latitude": 37.7906491612148,
    "longitude": -122.398880222540,
    "altitude": 10.1174488067620
  },
  {
    "timestamp": 7.8,
    "latitude": 37.7906576640255,
    "longitude": -122.398891579612,
    "altitude": 10.1175098419180
  },
  {
    "timestamp": 7.85,
    "latitude": 37.7906662178243,
    "longitude": -122.398902937117,
    "altitude": 10.1175699234000
  },
  {
    "timestamp": 7.9,
    "latitude": 37.7906748226116,
    "longitude": -122.398914294925,
    "altitude": 10.1176242828360
  },
  {
    "timestamp": 7.95,
    "latitude": 37.7906834783813,
    "longitude": -122.398925651737,
    "altitude": 10.1175432205000
  },
  {
    "timestamp": 8.0,
    "latitude": 37.7906921851336,
    "longitude": -122.398937008809,
    "altitude": 10.1175346374510
  },
  {
    "timestamp": 8.05,
    "latitude": 37.7907009428628,
    "longitude": -122.398948364971,
    "altitude": 10.1174345016470
  },
  {
    "timestamp": 8.1,
    "latitude": 37.7907097515698,
    "longitude": -122.398959721523,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.15,
    "latitude": 37.7907186112557,
    "longitude": -122.398971078508,
    "altitude": 10.1174640655510
  },
  {
    "timestamp": 8.2,
    "latitude": 37.7907275219209,
    "longitude": -122.398982435797,
    "altitude": 10.1175184249870
  },
  {
    "timestamp": 8.25,
    "latitude": 37.7907364830171,
    "longitude": -122.398993793480,
    "altitude": 10.1175756454460
  },
  {
    "timestamp": 8.3,
    "latitude": 37.7907454944005,
    "longitude": -122.399005150081,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.35,
    "latitude": 37.7907545560716,
    "longitude": -122.399016507029,
    "altitude": 10.1175012588500
  },
  {
    "timestamp": 8.4,
    "latitude": 37.7907636680312,
    "longitude": -122.399027864323,
    "altitude": 10.1175327301020
  },
  {
    "timestamp": 8.45,
    "latitude": 37.7907728302797,
    "longitude": -122.399039221921,
    "altitude": 10.1175765991210
  },
  {
    "timestamp": 8.5,
    "latitude": 37.7907820428170,
    "longitude": -122.399050579735,
    "altitude": 10.1176214218100
  },
  {
    "timestamp": 8.55,
    "latitude": 37.7907913056367,
    "longitude": -122.399061936466,
    "altitude": 10.1175374984740
  },
  {
    "timestamp": 8.6,
    "latitude": 37.7908006187389,
    "longitude": -122.399073293457,
    "altitude": 10.1175270080560
  },
  {
    "timestamp": 8.65,
    "latitude": 37.7908099821174,
    "longitude": -122.399084649452,
    "altitude": 10.1174268722530
  },
  {
    "timestamp": 8.7,
    "latitude": 37.7908193957730,
    "longitude": -122.399096005794,
    "altitude": 10.1174201965330
  },
  {
    "timestamp": 8.75,
    "latitude": 37.7908288597004,
    "longitude": -122.399107361312,
    "altitude": 10.1173334121700
  },
  {
    "timestamp": 8.8,
    "latitude": 37.7908383739004,
    "longitude": -122.399118717220,
    "altitude": 10.1173448562620
  },
  {
    "timestamp": 8.85,
    "latitude": 37.7908479383745,
    "longitude": -122.399130073648,
    "altitude": 10.1174001693720
  },
  {
    "timestamp": 8.9,
    "latitude": 37.7908575531238,
    "longitude": -122.399141430466,
    "altitude": 10.1174697875970
  },
  {
    "timestamp": 8.95,
    "latitude": 37.7908672181426,
    "longitude": -122.399152786418,
    "altitude": 10.1174125671380
  },
  {
    "timestamp": 9.0,
    "latitude": 37.7908769334252,
    "longitude": -122.399164141460,
    "altitude": 10.1173057556150
  },
  {
    "timestamp": 9.05,
    "latitude": 37.7908866985547,
    "longitude": -122.399175495704,
    "altitude": 10.1171846389770
  },
  {
    "timestamp": 9.1,
    "latitude": 37.7908965132520,
    "longitude": -122.399186849321,
    "altitude": 10.1170701980590
  },
  {
    "timestamp": 9.15,
    "latitude": 37.7909063775135,
    "longitude": -122.399198202441,
    "altitude": 10.1169719696040
  },
  {
    "timestamp": 9.2,
    "latitude": 37.7909162913360,
    "longitude": -122.399209555128,
    "altitude": 10.1168909072870
  },
  {
    "timestamp": 9.25,
    "latitude": 37.7909262547167,
    "longitude": -122.399220907511,
    "altitude": 10.1168279647820
  },
  {
    "timestamp": 9.3,
    "latitude": 37.7909362676598,
    "longitude": -122.399232260890,
    "altitude": 10.1169061660760
  },
  {
    "timestamp": 9.35,
    "latitude": 37.7909463301693,
    "longitude": -122.399243615310,
    "altitude": 10.1170415878290
  },
  {
    "timestamp": 9.4,
    "latitude": 37.7909564422487,
    "longitude": -122.399254970596,
    "altitude": 10.1171903610220
  },
  {
    "timestamp": 9.45,
    "latitude": 37.7909666038942,
    "longitude": -122.399266325384,
    "altitude": 10.1172027587890
  },
  {
    "timestamp": 9.5,
    "latitude": 37.7909768151018,
    "longitude": -122.399277679587,
    "altitude": 10.1171512603700
  },
  {
    "timestamp": 9.55,
    "latitude": 37.7909870758744,
    "longitude": -122.399289034569,
    "altitude": 10.1171989440910
  },
  {
    "timestamp": 9.6,
    "latitude": 37.7909973862150,
    "longitude": -122.399300390375,
    "altitude": 10.1172876358030
  },
  {
    "timestamp": 9.65,
    "latitude": 37.7910077461262,
    "longitude": -122.399311746896,
    "altitude": 10.1173849105830
  },
  {
    "timestamp": 9.7,
    "latitude": 37.7910181556101,
    "longitude": -122.399323104023,
    "altitude": 10.1174783706660
  },
  {
    "timestamp": 9.75,
    "latitude": 37.7910286146679,
    "longitude": -122.399334461617,
    "altitude": 10.1175584793090
  },
  {
    "timestamp": 9.8,
    "latitude": 37.7910391233006,
    "longitude": -122.399345819621,
    "altitude": 10.1176233291620
  },
  {
    "timestamp": 9.85,
    "latitude": 37.7910496808222,
    "longitude": -122.399357177957,
    "altitude": 10.1176738739010
  },
  {
    "timestamp": 9.9,
    "latitude": 37.7910602872266,
    "longitude": -122.399368535295,
    "altitude": 10.1175851821890
  },
  {
    "timestamp": 9.95,
    "latitude": 37.7910709425141,
    "longitude": -122.399379892916,
    "altitude": 10.1175680160520
  },
  {
    "timestamp": 10.0,
    "latitude": 37.7910816466851,
    "longitude": -122.399391250861,
    "altitude": 10.1175842285150
  },
  {
    "timestamp": 10.05,
    "latitude": 37.7910923997403,
    "longitude": -122.399402609105,
    "altitude": 10.1176166534420
  }
]
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634876281.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634876281.jpeg)