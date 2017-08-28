import numpy as np
import os
import cv2


class world(object):

    def __init__(self):

        self.height = 400

        self.width = 400

        self.grid = 25

        self.grid_h = self.height / self.grid
        self.grid_w = self.width / self.grid

        self.canvas = np.ones( [ self.height , self.width , 3 ],dtype=np.uint8 ) * 255
        self.name = 'world'

        self.map = np.zeros( [ self.height , self.width , 3 ],dtype=np.uint8 )

        self.obstacles=[]

        obstacle=[ [5,5],[8,5],[8,8],[5,8] ]
        for i in range(len(obstacle)):
            obstacle[i][0] = obstacle[i][0] * self.grid
            obstacle[i][1] = obstacle[i][1] * self.grid
        self.obstacles.append( obstacle )

        # fence 1
        obstacle=[ [0,0],[16,0],[16,1],[0,1] ]
        for i in range(len(obstacle)):
            obstacle[i][0] = obstacle[i][0] * self.grid
            obstacle[i][1] = obstacle[i][1] * self.grid
        self.obstacles.append( obstacle )

        # fence 2
        obstacle=[ [0,0],[0,16],[1,16],[1,0] ]
        for i in range(len(obstacle)):
            obstacle[i][0] = obstacle[i][0] * self.grid
            obstacle[i][1] = obstacle[i][1] * self.grid
        self.obstacles.append( obstacle )

        # fence 3
        obstacle=[ [15,0],[16,0],[16,16],[15,16] ]
        for i in range(len(obstacle)):
            obstacle[i][0] = obstacle[i][0] * self.grid
            obstacle[i][1] = obstacle[i][1] * self.grid
        self.obstacles.append( obstacle )

        # fence 4
        obstacle=[ [0,15],[16,15],[16,16],[0,16] ]
        for i in range(len(obstacle)):
            obstacle[i][0] = obstacle[i][0] * self.grid
            obstacle[i][1] = obstacle[i][1] * self.grid
        self.obstacles.append( obstacle )


        # ob2
        obstacle=[ [10,10],[10,13],[11,13],[11,10] ]
        for i in range(len(obstacle)):
            obstacle[i][0] = obstacle[i][0] * self.grid
            obstacle[i][1] = obstacle[i][1] * self.grid
        self.obstacles.append( obstacle )



    def display_grid(self):

        for i in range( self.grid_h ):
            cv2.line( self.canvas,pt1 = (0,self.grid *i) ,pt2=(self.width ,self.grid *i),color=(0,0,0),thickness=1)

        for j in range( self.grid_w ):
            cv2.line( self.canvas,pt1 = (self.grid *j,0) ,pt2=( self.grid *j,self.height),color=(0,0,0),thickness=1)


    def display_obstacle(self):

        for obs in self.obstacles:
        # obs = self.obstacles[0]
        #     print obs
            obs = np.array(obs)
            obs=obs.reshape(-1,1,2)

            cv2.polylines(self.canvas,[obs],True,(0,0,0),1)
            cv2.fillPoly(self.canvas,[obs],(0,0,0))



    def flush(self):

        self.canvas = np.ones( [ self.height , self.width , 3 ],dtype=np.uint8 ) * 255

    def show(self):

        cv2.imshow( self.name,  self.canvas)



if __name__ == "__main__":

    World = world()


    World.display_grid()
    World.display_obstacle()


    World.show()

    cv2.waitKey(0)