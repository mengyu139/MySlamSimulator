#coding=utf-8

import numpy as np
import os
import cv2
import math

import matplotlib.pyplot as plt


def closest_point(point,point_list):

    f=[]

    for item in point_list:

        f.append( math.sqrt( (item[0]-point[0])**2 +(item[1]-point[1])**2 ) )

    f = np.array(f)

    index = np.argmin(f)

    return index , point_list[index]


# p1 p2 -> ax + by +c = 0
def points_form_line(p1,p2):

    a=0
    b=0
    c = 0
    # x1==x2
    if p1[0] == p2[0]:
        a=1
        b=0
        c=-p1[0]

    elif p1[1]==p2[1]:
        a=0
        b=1
        c=-p1[1]

    else:
        a=1
        b=-( p2[0] - p1[0] )/1.0/( p2[1] - p1[1] )
        c = ( p2[0] - p1[0] )/1.0/( p2[1] - p1[1] ) * p1[1] - p1[0]

    return (a,b,c)



def point_to_line_distance(point,line):

    a,b,c=line

    distance = a*point[0] + b*point[1] +c

    distance = distance / math.sqrt( a**2+b**2 )

    return distance


def two_line_cross_point(para1,para2):

    a1,b1,c1=para1
    a2,b2,c2=para2


    if a1==0 and b2==0:
        y = -c1/b1
        x=-c2/a2
        return [x,y]

    if b1==0 and a2==0:
        x=-c1/a1
        y=-c2/b2
        return [x,y]

    if b2*a1==b1*a2:
        print 'two parallel line no cross'
        return None


    if a1 == 0:
        y=-c1/b1
        x=(c1*b2-c2*b1)/(b1*a2)
        return [x,y]

    if b1 == 0:
        x=-c1/a1
        y=(c1*a2-c2*a1)/(a1*b2)
        return [x,y]

    if a2==0:
        y=-c2/b2
        x=(c2*b1-c1*b2)/(b2*a1)
        return [x,y]

    if b2 == 0:
        x=-c2/a2
        y=(a1*c2-a2*c1)/(a2*b1)
        return [x,y]


    x = -(b1*a2*(c1-c2)/(b2*a1-b1*a2)+c1)/a1
    y = (c1-c2)*a2/(b2*a1-b1*a2)
    return [x,y]



def angle_from_two_points(pt1,pt2):

    if pt1[0]==pt2[0]:
        if pt2[1]>pt1[1]:
            return 0.5*math.pi
        else:
            return -0.5*math.pi
    else:
        return math.atan2( pt2[1]-pt1[1],pt2[0]-pt1[0] )


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

    a1 =  angle_from_two_points(end,start)
    a2 =  angle_from_two_points(end,test)
    angle1 = abs( a1-a2 )

    a1 =  angle_from_two_points(start,end)
    a2 =  angle_from_two_points(start,test)
    angle2 = abs( a1-a2 )

    if angle1 < math.pi/2. and angle2 < math.pi/2.:
        return True
    else:
        return False



def sim_liadr_beam(pt1,pt2,points):

    # print 'pt2 is: ', pt2

    f = []

    a,b,c = points_form_line(pt1,pt2)

    multi = 1

    for item in points:
        # print item
        f.append( a*item[0]+b*item[1]+c )


    f = np.array(f)
    #
    f1 = f[f>=0]
    f2 = f[f<=0]

    find_index = -1
    findex_point=None

    if f1.size == f.size or f2.size == f.size:

        # print 'no colision, endpoint is : ',pt2

        return [pt2 , False]

    else:
        # print ' maybe colision'

        pos_points=[]
        neg_points=[]
        candinate_line=[]

        for item in points:

            if a*item[0]+b*item[1]+c >= 0:
                pos_points.append( item )
            else:
                neg_points.append( item )


        # print 'pos_points is: ',pos_points
        # print 'neg_points is: ', neg_points

        candinate_line.append( closest_point( pt1, pos_points)[1] )
        candinate_line.append( closest_point( pt1, neg_points)[1] )

        # print  'candinate_line is : ' ,candinate_line

        a,b,c = points_form_line( candinate_line[0],candinate_line[1] )

        distance1 = point_to_line_distance( pt1,[a,b,c] )
        distance2 = point_to_line_distance( pt2,[a,b,c] )

        if distance1*distance2 < 0:

            a2,b2,c2=points_form_line( pt1,pt2 )

            crosspoint = two_line_cross_point([a,b,c],[a2,b2,c2])

            # print 'we confirmed pt1->pt2 collide with candinate line at : ',crosspoint
            return [crosspoint,True]

        else:
            # print 'no collision'
            return [pt2,False]



if __name__=="__main__":



    # a1,b1,c1=points_form_line( [0,0],[1,1] )
    # a2,b2,c2=points_form_line( [1,0],[0,1] )
    #
    # print two_line_cross_point( [a1,b1,c1],[a2,b2,c2] )


    a,b,c = points_form_line( (0,0),(1,1) )

    y=[]

    for i in range(10):

        y.append( (-a*i-c)/1./b )


    print sim_liadr_beam((0,0),(-2,-4),[(-1,0),(-2,0),(-1,1),(-2,1)])
