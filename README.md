# Fuzzy_Car_simulation
### DataPoint.py
此份程式碼設計來定義本次作業需要用到的 data 的 data structurer 使用。
1.	TrackInfo():紀錄讀取的軌道資訊，draw.py 與 Fuzzy_Compute.py 使用
Start_point 紀錄軌道起點
nodes_x、nodes_y 分別紀錄每個軌道點的 X 座標、Y 座標，
ends_x、ends_y 分別紀錄終點線的 X 座標、Y 座標，
設定 insert_end() 與 insert_node() 來讀取不同檔案的座標點，並插入到座標點的 list 之中。

2.	CarInfo()
紀錄車車的資訊，包含座標、方向盤角度與車子本身角度，因題目設定直徑為 6 ，故 class 中直接將半徑座標設定為 3

3.	Guassion_Function()
因提供使用者設定所有條件的規屬函數的參數的功能，包含前方距離、左右距離與方向盤變化大小，且每個距離條件分別有 small、medium、large 三個等級，本次作業為求方便，統一選定用高斯函數，高斯函數中需要設定變異數與 mean，故總共有會有 18 個可調參數，為了化簡程式的繁瑣程度，將所有可調式參數設定在 class 中。若使用者特別設定參數，則使用預設值。

選定這些值作為預設值的原因如下：
前方距離(front)的 mean 我以車的半徑為基準點，故分別設為 3、6、18 三個等級。
左右距離(lr)的設計概念相同，但是因為距離可能有負，故在 small 與 medium 的 mean 參數，我統一減六當作預設參數（此時剛好會發現 medium 預設值變為 0 ，代表車子保持在中間）。但在 large 的時候，考量一般來說軌道都比較窄，且車子一定是保持前行，故若參數設定 18 會太大，不太可能過彎，因此在 lr 的部分先將 large 參數設定為 3。
方向盤的部分(Theta)，因總共可轉角度為 45度，故將 small 、large、medium 三個等級直接用 90度除以3，因此 mean 分別設定為，每個區間為 30度，45-30 = 15、15-30 = -15 ，指定給 small 與 large 的參數，最後挑中間值 0度設定為 medium。
Variance 則因感覺上是決定規屬函數的寬度，本次作業都隨便設。

4.	Premise_Set()
作為前鑑部相關資料紀錄使用，記錄每個座標點距離進行模糊化後的結果，會在 Fuzzy_Compute.py 用到，所以值的預設值都為 0。

5.	car_State()
紀錄車車所有的狀態變化，並以 list 儲存。因在我所設計的模糊系統上，sensor 計算與更新時間、車車座標更新時間、方向盤角度更新狀態，是連帶關係執行，不會同時被更新到本身，故另外設定三個 insert function 進行分開處理。

### Fuzzy_Compute.py
將模糊系統主要計算函式，將講義上的 function 逐一實作

1.	模糊化機構：主要功用是將輸入的變數模糊化，因此輸入參數為
a.	車車的 log 檔 car，並取最新的資料計算(即 index = -1)，其中 car = car_state()
b.	記錄前鑑部結果的 data structure premise ，其中 premise = Premise_Set()
c.	使用者輸入的參數資料 para，其中 para = Guassion_Function()

在 function 中，所有規屬函數統一用高斯函數，將現階段車車的距離的歸屬度算出來後，記錄到 premise並回傳。

2.	模糊推論引擎與規則庫：推論引擎 Fuzzy_Inferenc 會先呼叫規則庫 fuzzy_rule，規則庫中紀錄我所定義規則的映射規系，規則以 dictionary 儲存。並設定 degree_list，紀錄每個規則下，每個角度的歸屬程

推論引擎輸入為前鑑部中的結果與使用者輸入的參數，來進行推論，程式中定義 alpha，紀錄每個規則的啟動強度，啟動強度為前鑑不「前方距離」、「左右距離」的最小值，並使用最大最小合成的方法，將每個規則的啟動強度跟每個角度模糊化後的歸屬度的值進行找最小值，最後找所有規則的最大值，作為推論結果（詳細公式可參考黃色部份的註解），並回傳啟動強度與推論結果。 
	
3.	去模糊化機構：將輸出的模糊向量轉化為實際的值，輸入參數為使用者選擇的去模糊化機構方法 way 作為判斷。方法上原本想使用權種平均法，但邏輯上反而與本此作業相反，和老師討論後發現不適合，故改使用離散重心法或式最大平均法，inference_result 則為上一層之之模糊推論結果。。

### 其他重要函式：
main_run()：主要流程管控，本次作業主要根據 GIS 系統常用的套件shapley 實作，套件可設跟據點座標作圖，並計算做出來的圖的距離、是否發生交集(即碰撞)、或是蘊含(即抵達終點)。
進入主程式後，先初始化所有物件，並進入無窮迴圈，若初始化的 flag 設為1時，程式初始化，開始設定 sensor，並進行第一次模糊推論更新，若 flag 為否，update 車子的 log， update 完後重新畫圖，並檢查是否發生碰撞，若無則往下繼續更新車車的 Sensor 與模糊推論，直到車車抵達終點或是發生碰撞，則結束。

### GUI.py 與 draw.py
最後在 GUI 與 draw 兩個介面中設計界面與畫圖，其中 draw.py 包含 draw_map() 與 draw_moving_car() 兩個 function，第一個繪畫出軌道與車的位置，傳送到 GUI 介面中，第二個則是在模糊推論結束後，根據 log 檔案畫出車子移動狀態。
(3)	模糊規則設計
規則如下，基本上就是都小的時候可以大轉，都大的時候要小轉，偏小或中間的時候也可以大轉，但偏大的時候就要小轉
Forward Dist	Small	Small	Small	Medium	Medium	Medium	Large	Large	Large
RL Dist	Small	Medium	Large	Small	Medium	Large	Small	Medium	Large
方向盤轉動大小	Large	Large	Small	Large	Medium	Small	Large	Medium	Small

### 分析
本實驗中模糊規則為固定九條，實作上可以比較簡單，要討論的內容較少，因此在本次實驗主要是比較模糊化機構與去模糊化機構對模糊系統的影響。
在模糊系統中，我發現模糊化機構的影響比去模糊化的影響大一點，同樣的歸屬函數參數中，不管選哪一個去模糊化機構基本上車車都可以走到終點，反之只要調不對的參數，不管哪一個去模糊化機構也都無法走到終點。

參數設計上，我個人覺得以車車的半徑為主要歸屬函數的邊界蠻合理的，即便是很奇怪的 case03.txt 都可以順利走出來，故我認為相較於去模糊化，模糊化機構影響比較大。

最後我發現很有趣的一點，用最大平均法車子容易走得比較搖搖擺擺，擺動幅度蠻大的，詳細原因為推測是因為最大平均法式直接角度和除以最大角度數，故值部會像離散重心法那麼細 (小數點後的位數比較少) 的緣故。
