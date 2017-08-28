#coding=utf-8

import numpy as np
import cv2
import math


from MySlam.Geometry import geometry

# def AngleFromTwoPoint( x1 ,  y1 ,  x2 ,  y2):
#
#     belta = 0
#     if  x2 - x1 == 0 :
#         if y2 >  y1 :
#             belta = 0.5*math.pi
#         elif y2 <  y1 :
#             belta = -0.5*math.pi
#         else:
#             belta = 0
#     else:
#         belta = math.atan2( (y2-y1) , (x2-x1) )
#
#     return belta
#
#
# angle = AngleFromTwoPoint( 1,1,0,0 )
# print angle/math.pi * 180.0
#


print geometry.angle_from_two_points( [0,0],[-1,1] ) / math.pi * 180.


def estimate_interior(point,shape):

    angle = []

    for item in shape:

        angle.append( geometry.angle_from_two_points(point,item) )

    print angle
    return sum(angle)


def is_point_in(x, y, points):
    count = 0
    x1, y1 = points[0]
    x1_part = (y1 > y) or ((x1 - x > 0) and (y1 == y)) # x1在哪一部分中
    x2, y2 = '', ''  # points[1]
    points.append((x1, y1))
    for point in points[1:]:
        x2, y2 = point
        x2_part = (y2 > y) or ((x2 > x) and (y2 == y)) # x2在哪一部分中
        if x2_part == x1_part:
            x1, y1 = x2, y2
            continue
        mul = (x1 - x)*(y2 - y) - (x2 - x)*(y1 - y)
        if mul > 0:  # 叉积大于0 逆时针
            count += 1
        elif mul < 0:
            count -= 1
        x1, y1 = x2, y2
        x1_part = x2_part
    if count == 2 or count == -2:
        return True
    else:
        return False




def is_acute_angle(start,end,test):

    a1 =  geometry.angle_from_two_points(end,start)
    a2 =  geometry.angle_from_two_points(end,test)
    angle1 = abs( a1-a2 )

    a1 =  geometry.angle_from_two_points(start,end)
    a2 =  geometry.angle_from_two_points(start,test)
    angle2 = abs( a1-a2 )

    if angle1 < math.pi/2. and angle2 < math.pi/2.:
        return True
    else:
        return False

    # return [ angle1/math.pi*180. , angle2/math.pi*180. ]



x = is_acute_angle( [0,0],[1,0],[2,1] )

print x

# a = estimate_interior( [-100,0],[ [-1,1],[1,1],[1,-1],[-1,-1] ] )
#
# print a/math.pi*180
#
# print is_point_in( 0,0,[ [-1,1],[1,1],[1,-1],[-1,-1] ] )