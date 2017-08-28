import numpy as np
import os
import cv2
import math
from MySlam.Geometry import geometry

from MySlam.World import world



class robot(object):

    def __init__(self,World,x=0.,y=0.,theta=0.,lidar_bling=21,angle_range=180./180*math.pi  ,lidar_length = 100):

        self.x = x
        self.y = y
        self.theta = theta

        self.size = World.grid/2

        self.key_dict={}

        self.key_dict['up'] = 82
        self.key_dict['down'] = 84
        self.key_dict['left'] = 81
        self.key_dict['right'] = 83

        self.lidar_angles=[]
        self.lidar_bling = lidar_bling
        self.angle_range = angle_range
        self.angle_step = angle_range/1./(lidar_bling-1)
        self.lidar_length = lidar_length
        self.lidar_point=[[0,0]]*self.lidar_bling
        self.lidar_interest_area=[[0,0],[0,0],[0,0],[0,0]]

        self.scan_map = np.ones( [World.grid_h,World.grid_w],dtype=np.uint8 )  # 0: 0cc 1: no know  2: free

        self.prob_map = np.ones( [World.height,World.width],dtype=np.uint8 )*125

        self.move_signal = 0


        for i in range( lidar_bling ):
            self.lidar_angles.append( -self.angle_range/2 + ( self.angle_step * i ) )


    def dispalay_robot(self,World):

        #body
        cv2.circle( World.canvas,center=(self.x,self.y),radius=self.size,color=(255,0,0),thickness=-1 )

        #dirction
        k  = World.grid
        cv2.line( World.canvas,pt1=( self.x,self.y ),pt2=( int(self.x+k*math.cos(self.theta)),int(self.y+k*math.sin(self.theta)) ),color=(0,255,100),thickness=4 )

        # lidar visual
        for i in range( self.lidar_bling ):
            # cv2.line( World.canvas,pt1=( self.x , self.y),pt2=( self.lidar_point[i][0] , self.lidar_point[i][1] ),color=(0,0,255),thickness=2 )

            cv2.circle(World.canvas,center=(self.lidar_point[i][0] , self.lidar_point[i][1]),radius=3,color=(0,0,255),thickness=-1)


    def display_scan_map(self,World):

        scan_map = np.ones([ World.height,World.width ],np.uint8)*125

        for i in range( World.grid_h ):
            for j in range( World.grid_w ):

                if self.scan_map[i,j] == 2:

                    scan_map[i*World.grid:(i+1)*World.grid ,j*World.grid:(j+1)*World.grid] = 255
                elif self.scan_map[i,j] == 0:
                    scan_map[i*World.grid:(i+1)*World.grid ,j*World.grid:(j+1)*World.grid] = 0

        cv2.imshow('scan_map',scan_map)


    def display_prob_map(self,World):
        if self.move_signal == 1:
            self.move_signal=0

            for i in range( World.grid_h ):
                for j in range( World.grid_w ):

                    if self.scan_map[i,j] == 2:
                        v = self.prob_map[i*World.grid ,j*World.grid]
                        v += 10
                        if v>255:
                            v=255
                        self.prob_map[i*World.grid:(i+1)*World.grid ,j*World.grid:(j+1)*World.grid] = v


                    elif self.scan_map[i,j] == 0:

                        v = self.prob_map[i*World.grid ,j*World.grid]

                        if v < 150:
                            v -= 3
                            if v<0:
                                v=0
                            self.prob_map[i*World.grid:(i+1)*World.grid ,j*World.grid:(j+1)*World.grid] = v

        cv2.imshow('prob_map',self.prob_map)


    def move(self,key,World):


        if key == self.key_dict['right']:
            self.theta += 0.05
            self.move_signal=1

        elif  key == self.key_dict['left']:
            self.theta -= 0.05
            self.move_signal=1

        elif  key == self.key_dict['up']:
            self.x += 5 * math.cos(self.theta )
            self.y += 5 * math.sin(self.theta )

            self.x = int(self.x)
            self.y = int(self.y)
            self.move_signal=1

        elif  key == self.key_dict['down']:
            self.x -= 5 * math.cos(self.theta )
            self.y -= 5 * math.sin(self.theta )

            self.x = int(self.x)
            self.y = int(self.y)

            self.move_signal=1


        while self.theta > 2*math.pi:
            self.theta -= 2*math.pi

        while self.theta < -2*math.pi:
            self.theta += 2*math.pi



        # update lidar info
        for i in range(self.lidar_bling):

            a = int(self.x + self.lidar_length * math.cos(self.theta +   self.lidar_angles[i]) )
            b = int(self.y + self.lidar_length * math.sin(self.theta +   self.lidar_angles[i]) )

            # for every beam , detect if there is any collision with obstacles
            endpoint = [a,b]

            for obs in World.obstacles:

                endpoint,COLLISION = geometry.sim_liadr_beam( [self.x,self.y],endpoint, obs)

                # self.lidar_point[i][0] = int(endpoint[0])
                # self.lidar_point[i][1] = int(endpoint[1])

                if not COLLISION:
                    self.lidar_point[i]=[a,b]

                if COLLISION:
                    self.lidar_point[i][0] = int(endpoint[0])
                    self.lidar_point[i][1] = int(endpoint[1])
                    break




        position_grid = [ int(self.x / World.grid) ,int(self.y / World.grid) ]
        cv2.circle(World.canvas,center=( position_grid[0]*World.grid+World.grid/2 , position_grid[1]*World.grid+World.grid/2  ),\
                   radius=7,color=(0,0,255),thickness=3)


        self.scan_map[...]=1
        for i in range(self.lidar_bling):

            line = geometry.points_form_line( [self.x,self.y],self.lidar_point[i] )

            if( self.lidar_point[i][0] < self.x ):
                e_x = int( math.floor( self.lidar_point[i][0]/1./World.grid ) )
                x_interval = -1
            else:
                e_x = int( math.floor( self.lidar_point[i][0]/1./World.grid ) )
                x_interval = 1

            if( self.lidar_point[i][1] < self.y ):
                e_y = int( math.floor( self.lidar_point[i][1]/1./World.grid ) )
                y_interval = -1
            else:
                e_y = int( math.floor( self.lidar_point[i][1]/1./World.grid ) )
                y_interval = 1

            if e_y > World.grid_h-1:
                    e_y = World.grid_h-1

            if e_x > World.grid_h-1:
                e_x = World.grid_w-1

            end_grid = [e_x, e_y ]

            cv2.circle(World.canvas,center=( end_grid[0]*World.grid+World.grid/2 , end_grid[1]*World.grid+World.grid/2  ),\
                   radius=4,color=(255,0,255),thickness=3)

            # x_step = end_grid[0] - position_grid[0]
            # y_step = end_grid[1] - position_grid[1]

            for x_grid in range(position_grid[0],end_grid[0]+x_interval,x_interval):
                for y_grid in  range(position_grid[1],end_grid[1]+y_interval,y_interval):

                    if y_grid > World.grid_h-1:
                        y_grid = World.grid_h-1

                    if x_grid > World.grid_h-1:
                        x_grid = World.grid_w-1


                    if self.scan_map[y_grid,x_grid] != 2:
                        cord_x = x_grid * World.grid + World.grid /2
                        cord_y = y_grid * World.grid + World.grid /2
                        distance = abs(geometry.point_to_line_distance( [ cord_x,cord_y ] , line ))

                        if distance < World.grid /2:

                            self.scan_map[y_grid,x_grid] = 2

                            cv2.circle(World.canvas,center=( cord_x , cord_y   ),radius=8,color=(0,100,100),thickness=2)
            #Finally , detect obstacle grid
            self.scan_map[end_grid[1],end_grid[0]] = 0




        # estimate interior
        # self.interior_grid=[]
        # for i in range( World.grid_h ):
        #     for j in range( World.grid_w):
        #         grid_x = World.grid * i + World.grid/2
        #         grid_y = World.grid * j + World.grid/2
        #
        #         if geometry.is_point_in( grid_x,grid_y,self.lidar_point):
        #             self.interior_grid.append([i,j])
        #
        # print len(self.interior_grid)




key = 0
if __name__ == "__main__":


    World = world.world()

    Robot = robot(World , 100,100)

    while True:

        World.flush()
        World.display_grid()
        World.display_obstacle()


        Robot.move(key,World)

        Robot.dispalay_robot(World)
        Robot.display_scan_map(World)

        Robot.display_prob_map(World)


        World.show()

        key = cv2.waitKey(40) & 0xff

