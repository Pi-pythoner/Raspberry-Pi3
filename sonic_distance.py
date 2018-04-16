import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.OUT)  #set PIN 29 as SR04 tirgger
GPIO.setup(31, GPIO.IN)   #set PIN 31 as SR04 echo


def sonic_detect():              
    
    GPIO.output(29,0)     
    GPIO.output(29,1)     # init I/O
    time.sleep(0.000015)  # sensor enable signal trigger 15uS
    GPIO.output(29,0)     # enable signal send end
    t0=time.time()
    while not GPIO.input(31):   
        t3=time.time()    # waitting echo signal time 't3'
        if (t3-t0)>=20:
            print("SR04 cable connection maybe NG,or U set sample frequecy too high!")
            time.sleep(0.5)
        else:
            pass              
    t1 = time.time()
    while GPIO.input(31):
        pass                
    t2 = time.time()
    sonf = int((t2 - t1) * 17000)
    #print(sonf)
    return sonf
        


if __name__=='__main__':
    print("Sonic wave distanse start!")
    while 1:
        a=sonic_detect()
        print(a,"cm")
        time.sleep(0.1)
        



        
    

