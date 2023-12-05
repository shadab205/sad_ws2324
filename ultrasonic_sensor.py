class UltrasonicSensor:

    def __init__(self):

        self.us_sense_map_x=[]
        self.us_sense_map_y=[]
        self.us_sense_map_sen_dis=[]
        self.us_sense_map_y_dis=[]
        self.val_fac=0
        self.val_st=-1
        self.val_end=-1
        self.valid_flag=-1
        
        for k in range(100)
            self.us_sense_map_x.append(0)
            self.us_sense_map_y.append(0)
            self.us_sense_map_sen_dis.append(0)
            
    def add_us_data(self,xpoint,x_dis,ypoint,ydis):
        
        self.us_sense_map_x.pop(0)
        self.us_sense_map_y.pop(0)
        self.us_sense_map_sen_dis.pop(0)
        
        self.us_sense_map_x.append(xpoint)
        self.us_sense_map_y.append(ypoint)
        self.us_sense_map_sen_dis.append(x_dis)
        

    def check_us_data_validity(self):
"""        
a=[2, 2, 6, 6, 6, 6, 1, 1, 8, 9]
#a=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
x=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45 ]
y=[]
#for k in range(10):
#    a.append(k)	
print (a)

val_fac=0
val_st=-1
val_end=-1
valid_flag=-1

for i in range(9):
    if a[i]>5 and a[i+1]>5:
        val_fac=val_fac+1
        val_end=i+1
        if val_st == -1:
            val_st=i
    else:
        if val_st != -1:
            val_fac=0
            val_st=-1
            val_end=i
    if val_st != -1 and val_end != -1:
        if(x[val_end]-x[val_st] > 14):
            valid_flag=1
            break
        else:
            valid_flag=-1
    
print("valid_flag = "+str(valid_flag))        
print("val_fac    = "+str(val_fac))
print("val_start  = "+str(val_st))
print("val_end    = "+str(val_end))
"""