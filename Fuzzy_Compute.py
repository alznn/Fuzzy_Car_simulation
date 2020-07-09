import math
from DataPoint import *
import shapely.geometry as sp
import pickle

def readFile(File):
    car_init = CarInfo()
    track = TrackInfo()
    f = open(File,'r')
    lines = []

    for line in f.readlines():
        line = line.replace('\n','')
        lines.append(line)
    for index in range(len(lines)):
        if index == 0:
            car_init.x,car_init.y,car_init.fai\
                = [int(i) for i in lines[index].split(',')]
        else:
            x, y = [int(i) for i in lines[index].split(',')]
            if index==1 or index==2:
                track.insert_end(x,y)
            else:
                track.insert_node(x, y)
    print(car_init.x)
    print(car_init.y)
    print(car_init.theta)
    print(car_init.fai)
    print(track.nodes_x)
    print(track.nodes_y)
    print(track.ends_x)
    print(track.ends_y)
    return car_init,track

def writeFile(car_log):
    #train4D.txt格式:前方距離、右方距離、左方距離、方向盤得出角度(右轉為正)
    f = open('train4D.txt','w',encoding='utf-8')
    for index in range(len(car_log.f_dist)):
        f.write(str(car_log.f_dist[index])+" ")
        f.write(str(car_log.r_dist[index])+" ")
        f.write(str(car_log.l_dist[index])+" ")
        f.write(str(car_log.theta[index])+"\n")
        # f.write('\n')
    f.close()

    f = open('train6D.txt', 'w', encoding='utf-8')
    for index in range(len(car_log.f_dist)):
        f.write(str(car_log.x[index]) + " ")
        f.write(str(car_log.y[index]) + " ")
        f.write(str(car_log.f_dist[index]) + " ")
        f.write(str(car_log.r_dist[index]) + " ")
        f.write(str(car_log.l_dist[index]) + " ")
        f.write(str(car_log.theta[index]) + "\n")
        # f.write('\n')
    f.close()
    #train6D.txt格式: X座標、Y座標、前方距離、右方距離、左方距離、方向盤得出角度(右轉為正)
def update(x,y,fai,theta,b):
    '''
    -90 < fai < 270
    -40 < theta <40
    '''
    print("X:",x)
    new_x = x + math.cos(math.radians(fai +theta))+math.sin(math.radians(fai))*math.sin(math.radians(theta))
    print("new_X:",new_x)
    new_y = y + math.sin(math.radians(fai +theta))-math.sin(math.radians(theta))*math.cos(math.radians(fai))
    print("new_y:",new_y)

    new_fai =fai-math.degrees(math.asin((math.sin(math.radians(theta))*2)/b))
    print("new_fai: ",new_fai)

    return new_x,new_y,new_fai
'''
front_small = self.g_decreasing_funct(dir_dist, self.fuzzy_variable[0], self.fuzzy_variable[1])
front_medium = self.gfun(dir_dist, self.fuzzy_variable[2], self.fuzzy_variable[3])
front_large = self.gufun(dir_dist, self.fuzzy_variable[4], self.fuzzy_variable[5])
'''
def Gaussian (x,mean,deviation):
    return math.exp(-(x - mean) ** 2 / deviation ** 2)

def large_fuzzi(x,mean,deviation):
    if x > mean:
        return 1
    else: return Gaussian(x,mean,deviation)

def small_fuzzi(x,mean,deviation):
    if x < mean:
        return 1
    else:
        return  Gaussian (x,mean,deviation)

def lr_large_fuzzi(x,mean,deviation):
    if x < mean:
        return 1
    else: return Gaussian(x,mean,deviation)

def lr_small_fuzzi(x,mean,deviation):
    if x > mean:
        return 1
    else:
        return  Gaussian (x,mean,deviation)


# 輸入變數模糊化，即把確定的輸入轉化成為由隸屬度描述的模糊集。
def fuzzifier(car,premise,para):
    # fuzzifier(car,car_current, trackObj, mv_range)
    '''
       一、將明確的數值型式資料 x0 視為一個模糊單點型式的模糊集合 A：
           Mx = 1 if x =x x0,else Mx = 0
       二、 當 x= x0 時，其歸屬函數值為 1；當 x 越來越遠離 x0 時，其歸屬函數值則遞減，表示如下：
           Mx = exp(-(x-x0)^2/Sigma^2) , Sigma 為歸屬函數遞減的速率
           ex: (1)高斯函數作為歸屬函數
    '''
    deviation = 5 #隨便設的
    large_mean = 6 #車車長度

    ### Forward
    #3,10
    print("para",type(para.f_large_mean))
    # input()
    f_small = small_fuzzi(car.f_dist[-1], para.f_small_mean, para.f_small_dev)
    #12 5
    f_medium = Gaussian(car.f_dist[-1], para.f_medium_mean, para.f_medium_dev)
    #20 5
    f_large = large_fuzzi(car.f_dist[-1], para.f_large_mean ,para.f_large_dev)
    # Right-Left
    lr = car.r_dist[-1]-car.l_dist[-1] #越小表示車越靠左
    # lr = car.l_dist[-1]-car.r_dist[-1] #越小表示車越靠左
    lr_s = lr_small_fuzzi(lr,para.lr_small_mean, para.lr_small_dev)
    # lr_s = small_fuzzi(lr,-6, 5)
    #左 - 右 = 0 表示靠中間
    lr_m = Gaussian(lr,para.lr_medium_mean, para.lr_medium_dev)
    lr_l = lr_large_fuzzi(lr,  para.lr_large_mean ,para.lr_large_dev)
    # lr_l = large_fuzzi(lr, 6, 3)
    # print("---------------------模糊化機構----------------------------")
    # print("與前方距離: ", car.f_dist[-1])
    # print("歸屬度:")
    # print("front_large: ", f_large)
    # print("front_small: ", f_small)
    # print("front_medium: ", f_medium)
    # print("左右距離:", car.r_dist[-1])
    # print("歸屬度: ")
    # print("lr:", lr)
    # print("lr_s:", lr_s)
    # print("lr_m:", lr_m)
    # print("lr_l:", lr_l)
    # print("---------------------模糊化機構----------------------------")
    # input()
    premise.f_large=f_large
    premise.f_medium=f_medium
    premise.f_small=f_small
    premise.lr=lr
    premise.lr_l=lr_l
    premise.lr_m=lr_m
    premise.lr_s=lr_s
    #回傳前鑑部的歸屬度
    return premise
    # pass

def fuzzy_rule(para):
    rules = []
    rules.append({'rule_description': 'f_s&&lr_s', 'result': 'theta_l'})
    rules.append({'rule_description': 'f_s&&lr_m', 'result': 'theta_l'})
    rules.append({'rule_description': 'f_s&&lr_l', 'result': 'theta_s'})
    rules.append({'rule_description': 'f_m&&lr_s', 'result': 'theta_l'})
    rules.append({'rule_description': 'f_m&&lr_m', 'result': 'theta_m'})
    rules.append({'rule_description': 'f_m&&lr_l', 'result': 'theta_s'})
    rules.append({'rule_description': 'f_l&&lr_s', 'result': 'theta_l'})
    rules.append({'rule_description': 'f_l&&lr_m', 'result': 'theta_m'})
    rules.append({'rule_description': 'f_l&&lr_l', 'result': 'theta_s'})

    # print(rules)
    # input()
    #f_large, lr_l
    #[f_large,f_medium,f_small,lr_l,lr_m,lr_s]
    degree_list = []
    # for i in range(len(rules)):
    #     degree_list.append([])
    for index in range(len(rules)):
        tmp = []
        for degree in range(-40, 41, 1):
            theta_l = large_fuzzi(degree, para.tha_large_mean, para.tha_large_dev)
            theta_m = Gaussian(degree, para.tha_medium_mean, para.tha_medium_dev)
            theta_s = small_fuzzi(degree, para.tha_small_mean, para.tha_small_dev)
            if rules[index]['result'] == 'theta_s':
                tmp.append(theta_s)
            if rules[index]['result'] == 'theta_m':
                tmp.append(theta_m)
            if rules[index]['result'] == 'theta_l':
                tmp.append(theta_l)
        degree_list.append(tmp)
        # print(tmp)
        # print(degree_list[degree+40])
        # input()
    # print([len(degree_list[i]) for i in range(len(degree_list))])
    # print("---------------------檢查Rule----------------------------")
    # print("r_s: ", theta_s)
    # print("r_m ", theta_m)
    # print("r_l: ", theta_l)
    # print(rules[0])
    # print(degree_list[0])
    # input()
    # print([degree_list[i] for i in range(len(degree_list))])
    return rules,degree_list



                  #(car,car_current, trackObj, premise)
def Fuzzy_Inferenc(car,car_current,para, premise):
    # print("RULE:+========================================")
    rules,degree_list = fuzzy_rule(para)
    # input()
    #模糊規則庫中的模糊“if-then”規則轉換成某種對映
    '''
    MA = 為 A 在 A 的歸屬函數中的值
    兩個東西的啟動強度 alpha = min(Ma,Ma->b)
    啟動強度 alpha = min(Ma,Ma->b))
    最大-最小合成 Mub = max(min(Ma,Ma->b))
    最大乘積合成  max(Ma dot Mb)
    最大邊界積合成
    最大激烈積合成
    '''
    alpha = [  min(premise.f_small,premise.lr_s),
               min(premise.f_small, premise.lr_m),
               min(premise.f_small, premise.lr_l),
               min(premise.f_medium, premise.lr_s),
               min(premise.f_medium, premise.lr_m),
               min(premise.f_medium, premise.lr_l),
               min(premise.f_large,premise.lr_s),
               min(premise.f_large,premise.lr_m),#九條規則的啟動強度為 (Ma,Mb,Mab->c)
               min(premise.f_large,premise.lr_l),#九條規則的啟動強度為 (Ma,Mb,Mab->c)
               ]
    inference_result = []
    #Mc = (min(Ma,Mb),Mab->c) ?????????????  ch9 p6/23
    #啟動強度 & 歸屬度值是否一樣??????????????
    for degree in range(-40, 41, 1):
        # print("min ++++++++++++++++++++++++++++++++++++++++++")
        # print(premise.f_small,premise.lr_s,degree_list[0][degree+40],min(alpha[0],degree_list[0][degree+40]))
        # print(premise.f_small,premise.lr_m,degree_list[0][degree+40],min(alpha[1],degree_list[1][degree+40]))
        # print(premise.f_small,premise.lr_l,degree_list[0][degree+40],min(alpha[2],degree_list[2][degree+40]))
        # print(premise.f_medium,premise.lr_s,degree_list[0][degree+40],min(alpha[3],degree_list[3][degree+40]))
        # print(premise.f_medium,premise.lr_m,degree_list[0][degree+40],min(alpha[4],degree_list[4][degree+40]))
        # print(premise.f_medium,premise.lr_l,degree_list[0][degree+40],min(alpha[5],degree_list[5][degree+40]))
        # print(premise.f_large,premise.lr_s,degree_list[0][degree+40],min(alpha[6],degree_list[6][degree+40]))
        # print(premise.f_large,premise.lr_m,degree_list[0][degree+40],min(alpha[7],degree_list[7][degree+40]))
        # print(premise.f_large,premise.lr_l,degree_list[0][degree+40],min(alpha[8],degree_list[8][degree+40]))
        # print("Inference: ",max(
        #     min(alpha[0],degree_list[0][degree+40]),
        #     min(alpha[1],degree_list[1][degree+40]),
        #     min(alpha[2],degree_list[2][degree+40]),
        #     min(alpha[3],degree_list[3][degree+40]),
        #     min(alpha[4],degree_list[4][degree+40]),
        #     min(alpha[5],degree_list[5][degree+40]),
        #     min(alpha[6],degree_list[6][degree+40]),
        #     min(alpha[7],degree_list[7][degree+40]),
        #     min(alpha[8],degree_list[8][degree+40])
        # ))
        # print("min ++++++++++++++++++++++++++++++++++++++++++")
        # input()
        # print(len(degree_list[0]))
        # print(degree)
        # print("degree_list[0][degree]",degree_list[0][degree+40])
        # input()
        # print('alpha[0],degree_list[0][degree]:', premise.f_small,premise.lr_s, degree_list[0][degree+40])
        inference = max(
            min(alpha[0],degree_list[0][degree+40]),
            min(alpha[1],degree_list[1][degree+40]),
            min(alpha[2],degree_list[2][degree+40]),
            min(alpha[3],degree_list[3][degree+40]),
            min(alpha[4],degree_list[4][degree+40]),
            min(alpha[5],degree_list[5][degree+40]),
            min(alpha[6],degree_list[6][degree+40]),
            min(alpha[7],degree_list[7][degree+40]),
            min(alpha[8],degree_list[8][degree+40])
        )
        # print("inference: ",inference)
        inference_result.append(inference)
    # print("+++++++++++++++++++++++++++++++++++++++++++++++")
    # print("檢查規則: ")
    # print(min((premise.f_small, premise.lr_s, degree_list[0][0])))
    # print(min((premise.f_small, premise.lr_s, degree_list[0][40])))
    # print(inference_result[0])
    # print(inference_result[-1])
    # print("+++++++++++++++++++++++++++++++++++++++++++++++")
    # print(rules[0])
    # print(degree_list[0])
    # print(rules[2])
    # print(degree_list[2])
    # print(rules[-1])
    # print(degree_list[-1])
    return alpha,inference_result

def defuzzification(car,car_current, premise,alpha, inference_result,way=1):
    #輸出的模糊量轉化為實際用於控制的清晰量
    '''
    一、推論後得到的是模糊集合：
    1. 重心法
        論域為連散或離散不同演算法
        離散：sum(Mc(y)*y)/sum(Mc(y)   ch9 p7
    2. 最大平均法 y* = sum(y)/N
    3. 修正型最大平均法 y* = (max(y) + min(y) )/2
    4. 中心平均法
    5. 修正型重心法

    二、推論後得到"明確"的輸出值：
        權重式平均法  y* = sum(alpha*y) / sum(alpha) ch9 p7
        ex:(3)加權式平均法來去模糊化
    '''

    # bb.index(max(bb))
    if way==0:
        max_idx = inference_result.index(max(inference_result))
        max_value = [i for i,v in enumerate(inference_result) if v==inference_result[max_idx]]

        total = 0.0
        for data in max_value:
            total+=(data-40)

        print(total/len(max_value))

        if (total/len(max_value)) > 40.0:
            return 40
        elif (total/len(max_value)) < -40.0:
            return -40
        else:
            return (total/len(max_value))
    else:
        son = 0.0
        mom = 0.0
        # for degree in range(-40, 40, 1):
        #     son = degree * alpha[degree + 40]
        #     mom += alpha[degree + 40]


        # for i in inference_result:
        #     print(i)
        for degree in range(-40,40,1):
            son += degree*inference_result[degree+40]
            mom += inference_result[degree+40]
        # print("son:",son)
        # print("mom:",mom)
        # print(son/mom)

        if (son/mom) > 40.0:
            return 40
        elif (son/mom) < -40.0:
            return -40
        else:
            return (son/mom)


def main_run(para,File='case01.txt',way = 1):
    paras = Guassion_Function()
    paras = para
    count = 0
    mv_range = 1
    flag = True
         #CarInfo(x,y,theta,fai)

    premise = Premise_Set()
    car_current,track = readFile(File)
    #draw car circle
    carObj=sp.Point(car_current.x,car_current.y).buffer(car_current.r)
    # print(carObj)

    # draw track
    trackObj = sp.LineString([[track.nodes_x[i],track.nodes_y[i]] for i in range(len(track.nodes_y))])
    # print(trackObj)

    #draw endline 長方形
    endPolyObj = sp.Polygon([(track.ends_x[0],track.ends_y[0]),
                             (track.ends_x[1], track.ends_y[0]),
                             (track.ends_x[1], track.ends_y[1]),
                             (track.ends_x[0], track.ends_y[1])
                           ])
    print(endPolyObj)
    # input()
    ###初始化
    car = car_state()
                # (x, y, forward, left, right, theta, fai)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!running Start!!!!!!!!!!!!!!!!!!!!!!!!!
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!running Start!!!!!!!!!!!!!!!!!!!!!!!!!')
    while True:
        print('****************************************************************************************************************8')
        if(endPolyObj.contains(sp.Point(car_current.x, car_current.y))):
            print("get END")
            with open("data_point.pkl",'wb') as f:
                pickle.dump(car,f)
            writeFile(car)
            return 1
            # break
        '''
        car =car_state()
        #(self,x,y,forward,left,right,theta,fia,f_dist,left_dist,right_dist):
        car.inser(0,0,10,5,5,40,90,22,22,22)
        print(car.x)
        print(car.y)
        print(car.forward)
        
        car.inser(10,car.y[-1],20,10,10,40,45,31,2,2)
        print(car.x)
        print(car.y)
        print(car.forward)
        '''
        if flag:
            # print("get in flag")
            #(x, y, theta, fia):
            car.insert_carlog(car_current.x, car_current.y, car_current.fai)  # 車子狀態
            car.insert_newtheta(car_current.theta)  # 方向盤狀態
            max_x = max(track.nodes_x)
            max_y = max(track.nodes_y)
            min_x = min(track.nodes_x)
            min_y = min(track.nodes_y)
            # print("Max and Min: ", (max_x, max_y), (min_x, min_y))
            mv_range =math.sqrt(((max_x-min_x)**2)+((max_y-min_y)**2))
            # print("moving_range: ",mv_range)
            flag = False
        # elif (carObj.intersection(trackObj)) and flag == False:
        #     print("碰！  \ ( ‵ A ′ )/  ")
        #     break
        else:
            print("-----------------------------------",count,"------------------------------------------------")
            print("++++++++++++++++++++++++++++++++update++++++++++++++++++++++++++++++++++++++++++++")
            print("car_current.x: ",car_current.x)
            print("car_current.y: ",car_current.y)
            print("car_current.fai: ",car_current.fai)
            new_x,new_y,new_fai = update(car_current.x, car_current.y, car_current.fai, car_current.theta, car_current.r*2)
            car_current.x = new_x
            car_current.y = new_y
            car_current.fai =new_fai
            car.insert_carlog(new_x,new_y,new_fai)
            car.insert_newtheta(car_current.theta)  # 方向盤狀態
            print("car_current.x: ", car_current.x)
            print("car_current.y: ", car_current.y)
            print("car_current.fai: ", car_current.fai)
            print("car_current.theata: ", car_current.theta)


            carObj = sp.Point(car_current.x, car_current.y).buffer(car_current.r)
            print(car_current.x, car_current.y)
            if (carObj.intersection(trackObj)) and flag == False:
                with open("data_point.pkl", 'wb') as f:
                    pickle.dump(car, f)
                print("碰！  \ ( ‵ A ′ )/  ")
                return 0
                # break
            # print(carObj)
            # input()

        # car sensor compute
        setSensor(car,car_current, trackObj, mv_range)
        #模糊化
        premise = fuzzifier(car,premise,paras)
        alpha, inference_result = Fuzzy_Inferenc(car,car_current,paras,premise)
        # print("---------------------檢查模糊推論引擎----------------------------")
        # print("alpha: ", alpha)
        # print("inference_result: ",inference_result)
        # print("---------------------檢查模糊推論引擎----------------------------")

        new_theta = defuzzification(car,car_current,premise,alpha, inference_result,way)
        print("-------------------------count:",count,"------------------------------------")
        print("---------------------檢查模糊化機構----------------------------")
        print("與前方距離: ", car.f_dist[-1])
        print("歸屬度:")
        print("front_large: ", premise.f_large)
        print("front_small: ", premise.f_small)
        print("front_medium: ", premise.f_medium)
        print("左右距離:", car.r_dist[-1])
        print("歸屬度: ")
        print("lr:", premise.lr)
        print("lr_s:", premise.lr_s)
        print("lr_m:", premise.lr_m)
        print("lr_l:", premise.lr_l)
        print("---------------------檢查模糊化機構----------------------------")
        print("f_large: ",premise.f_large)
        print("f_medium: ",premise.f_medium)
        print("f_small: ",premise.f_small)

        print("---------------------檢查去模糊化機構----------------------------")
        print("new_theta: ", new_theta)
        car_current.theta = new_theta
        car.insert_newtheta(new_theta)
        print("當前車子狀態 x: ",car_current.x)
        print("當前車子狀態 y: ",car_current.y)
        print("當前車子狀態 theta: ",car_current.theta)
        print("當前車子狀態 fai: ",car_current.fai)
        print("---------------------檢查去模糊化機構----------------------------")
        print("dist",len(car.f_dist))
        print(car.f_dist)
        print("r dist",len(car.r_dist))
        print(car.r_dist)
        print("l dist",len(car.l_dist))
        print(car.l_dist)
        print("f point",len(car.forward))
        print(car.forward)
        print("right point: ",len(car.right))
        print(car.right)
        print("left point: ",len(car.left))
        print(car.left)
        count+=1
        # input()

def setSensor(car_log,car_current,track,mv_range):
    # 車體中心設有感測器，可偵測正前方與左右各45度之距離
    # 前方與牆的距離
    forward_pt = [[car_current.x, car_current.y],
                  [car_current.x + mv_range * math.cos(math.radians(car_current.fai)),
                   car_current.y + mv_range * math.sin(math.radians(car_current.fai))]]
    f_wall = sp.LineString(forward_pt).intersection(track)
    f_point, f_dist = getDistance(f_wall, car_current)
    # print("f_dist: ", f_dist)
    # input()

    # 左右牆距離，右為正(0-90)，固往右打的角度應該為減
    right_pt = [[car_current.x, car_current.y],
                [car_current.x + mv_range * math.cos(math.radians(car_current.fai - 45)),
                 car_current.y + mv_range * math.sin(math.radians(car_current.fai - 45))]]
    r_wall = sp.LineString(right_pt).intersection(track)
    r_point, r_dist = getDistance(r_wall, car_current)
    # print("r_dist: ", r_dist)
    # print("r_point: ", r_point)
    # input()

    left_pt = [[car_current.x, car_current.y],
               [car_current.x + mv_range * math.cos(math.radians(car_current.fai + 45)),
                car_current.y + mv_range * math.sin(math.radians(car_current.fai + 45))]]
    l_wall = sp.LineString(left_pt).intersection(track)
    l_point, l_dist = getDistance(l_wall, car_current)
    # print("l_dist: ", l_dist)
    # print("l_point: ", l_point)
    # input()
    #insert_sensorlog(self,forward,left,right,f_dist,left_dist,right_dist)
    car_log.insert_sensorlog(f_point,l_point,r_point,f_dist,l_dist,r_dist)

def getDistance(wall,car):
    dist_list = []
    min_dist = 9999999
    min_point = []
    # print("Car center: ", (car.x,car.y))
    if isinstance(wall, sp.Point):
        # print("x:",wall.x)
        # print("y:",wall.y)
        # print((wall.x - car.x) ** 2 )
        # print((wall.y - car.y) ** 2 )
        dist = math.sqrt(((wall.x - car.x) ** 2 + (wall.y - car.y) ** 2))
        # print(dist)
        if dist<min_dist:
            min_dist = dist
            min_point = [wall.x,wall.y]
        dist_list.append(dist_list)
    elif isinstance(wall, sp.MultiPoint):
        for data in range(0,len(wall)):
            dist = math.sqrt(((wall[data].x - car.x) ** 2 + (wall[data].y - car.y) ** 2))
            if (dist < min_dist):
                min_dist = dist
                min_point = [wall[data].x, wall[data].y]
                # print("原始的 dist:", dist)
                # print("new dist:", min_dist)
    return min_point,min_dist

# main_run()