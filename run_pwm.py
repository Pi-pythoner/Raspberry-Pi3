import RPi.GPIO as GPIO
import time
import mag3110,servo_mg996r
import sonic_distance

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(15, GPIO.OUT)   
GPIO.setup(11, GPIO.OUT)   
GPIO.setup(13, GPIO.OUT)   
GPIO.setup(16, GPIO.OUT)
GPIO.setup(40, GPIO.OUT,initial=False)

p1= GPIO.PWM(11, 100)      #right back 
p2= GPIO.PWM(13, 100)      #right front 
p3= GPIO.PWM(15, 100)      #left front
p4= GPIO.PWM(16, 100)      #left back

def front(d):
    #d=d*0.7
    p1.start(00)
    p2.start(d)
    p3.start(d)
    p4.start(00)   

def back(d):
    #d=d*0.7
    p1.start(d)
    p2.start(00)
    p3.start(00)
    p4.start(d)
        
def right(d):
    #d=d*0.7
    p1.start(00)
    p2.start(d)
    p3.start(00)
    p4.start(d)
    
def left(d):
    #d=d*0.7
    p1.start(d)
    p2.start(00)
    p3.start(d)
    p4.start(00)
    
def stop():
    p1.start(0)
    p2.start(0)
    p3.start(0)
    p4.start(0)

def servo_openmv_p1():
    servo_mg996r.servo_V(180)
    servo_mg996r.servo_T(132)
    time.sleep(1.2)
    servo_mg996r.servo_silent()
    print("Servo moved to openmv position1!")
    
def fix_front_dist(x):
    i=0
    bias_itg=0
    bias_div=0
    bias_d_last=0  
    while i<=50:
        a=sonic_distance.sonic_detect()
        if abs(x-a)>=3:
            bias_d=a-x
            bias_itg+=bias_d
            bias_div=bias_d_last-bias_d
            output=bias_d*1.5#+bias_itg*0.01+bias_div*0.01   (-75,75)
            if output>=0:
                if output>=75:
                    output=75
                back(25+output)
            else:
                if output<=-75:
                    output=-75
                front(25+(-output))
            time.sleep(0.04)
            bias_d_last=bias_d
        else:
            i+=2
            stop()
            time.sleep(0.04)
    print("Move to front distance:%dcm done" % x)
       
    
def move_mag(ang_target): #car will rotate mag3110 to  target angle     
    i=0
    bias_ang_itg=0
    bias_ang_div_last=0
    bias_ang_last=0
    while i<=50:
        ang_current=mag3110.mag3110_ang()
        bias_ang=ang_target-ang_current
        bias_ang_itg+=bias_ang
        bias_ang_div=bias_ang_last-bias_ang
        bias_ang_last=bias_ang
        if abs(bias_ang)>=2:
        #bace on L298N input voltage 8.2V,car start rotate pwm is 42
            output=bias_ang*0.4#+bias_ang_itg*0.1+bias_ang_div*0.3
            if abs(bias_ang)<=330:
                if output>=35:
                    output=35
                elif output<=-35:
                    output=-35    
                if output>0:
                    if bias_ang>=40:   #if angle biger than 40 full spd
                        right(90)
                    else:
                        right(35+output)
                elif output<0:
                    if bias_ang<=-40:   #if angle biger than 40 full spd
                        left(90)
                    else:
                        left(35+abs(output))
            elif abs(bias_ang)>330:
                bias_ang2=360-abs(bias_ang)
                output=bias_ang2*0.3
                #print(output,ang_current)
                if ang_target>=340:
                    left(35+output)
                elif ang_target<20:
                    right(35+abs(output))           
        else:
            i+=1
            stop()
        time.sleep(0.02)   #dont't refresh too fast,mag3110 cycle time
    print("Move to angle:%d" % ang_target)
        
def move_ang(angle): #base on current angle,and left/right side rotate
    ang_current=mag3110.mag3110_ang()
    ang_target=ang_current+angle
    if ang_target>360:
        ang_target=ang_target-360
    if ang_target<0:
        ang_target=360+ang_target
    move_mag(ang_target)

def openmv_camera_test():
    while 1:
        print("Close cam 2 S!")
        GPIO.output(40,0)
        time.sleep(2)
        print("Open cam 2 S!")
        GPIO.output(40,1)
        time.sleep(2)

   
    
if __name__=='__main__':
    #openmv_camera_test()
    stop()
    print("Car will move in 0.5 secs!!!")
    move_mag(180)
    fix_front_dist(20)
    time.sleep(2)
    fix_front_dist(40)
        
        
    


        
        
        
            
        




        
    

