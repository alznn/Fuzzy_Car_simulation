import cmath

class TrackInfo():
    def __init__(self):
        self.start_point = [-6, -3]
        self.nodes_x = [] # x list
        self.nodes_y = [] # y list
        self.ends_x = [] #list
        self.ends_y = [] #list
    def insert_end(self,x,y):
        self.ends_x.append(x)
        self.ends_y.append(y)
        # end_x =  [18, 30]
        # end_y =  [37, 40]
        return self.ends_x,self.ends_y
    def insert_node(self, x, y):
        self.nodes_x.append(x)
        self.nodes_y.append(y)
        # node_X = [-6,-6,18,18,30,30,6,6,-6]
        # node_y = [-3,22,22,50,50,10,10,-3,-3]
        return self.nodes_x,self.nodes_y
class CarInfo():
    def __init__(self):
        self.theta = 0.0 #方向盤
        self.x = 0.0
        self.y = 0.0
        self.fai = 0.0 #車子與水平面夾角
        self.r = 3 #直徑為6
class Guassion_Function():
    def __init__(self):
        self.f_small_mean = 3
        self.f_small_dev = 10
        self.f_medium_mean = 6
        self.f_medium_dev = 5
        self.f_large_mean = 18
        self.f_large_dev = 5

        self.lr_small_mean = -3
        self.lr_small_dev = 2
        self.lr_medium_mean = 0
        self.lr_medium_dev = 3
        self.lr_large_mean = 15
        self.lr_large_dev = 2

        self.tha_small_mean = -15
        self.tha_small_dev = 20
        self.tha_medium_mean = 0
        self.tha_medium_dev = 25
        self.tha_large_mean = 15
        self.tha_large_dev = 20

class Premise_Set():
    def __init__(self):
        self.f_large=0.0
        self.f_medium=0.0
        self.f_small=0.0
        self.lr = 0.0
        self.lr_l=0.0
        self.lr_m=0.0
        self.lr_s=0.0
class car_state():
    def __init__(self):
        self.x=[]
        self.y=[]

        self.fia=[]       #車子角度
        self.theta=[]       #方向盤

        self.forward=[]     #前方牆壁距離座標
        self.left=[]        #左方牆壁距離座標
        self.right=[]       #左方牆壁距離座標

        self.f_dist = []  # 前方牆壁距離變化紀錄
        self.l_dist = []  # 左方牆壁距離變化紀錄
        self.r_dist = []  # 左方牆壁距離變化紀律
    def insert_carlog(self,x,y,fia,):
        self.x.append(x)
        self.y.append(y)
        self.fia.append(fia)
    def insert_sensorlog(self,forward,left,right,f_dist,left_dist,right_dist):
        self.forward.append(forward)    #
        self.left.append(left)
        self.right.append(right)
        self.f_dist.append(f_dist)
        self.l_dist.append(left_dist)
        self.r_dist.append(right_dist)
    def insert_newtheta(self,theta):
        self.theta.append(theta)