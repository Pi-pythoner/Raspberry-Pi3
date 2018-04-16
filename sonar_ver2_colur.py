import RPi.GPIO as GPIO   
import time
import sonic_distance
import pygame,math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#ultra sonic servo Pin assign 33
GPIO.setup(33, GPIO.OUT, initial=False)
#Servo type (SG90 and MG90S) set PWM 50
p = GPIO.PWM(33,50)                     
p.start(0)


#get single coordinate (distance,angle)
def get_position(d,angle):              
    Hight=round(math.sin(math.pi*angle/180)*d*3,3)
    Width=round(math.cos(math.pi*angle/180)*d*3,3)
    return [Width,Hight]

#get multy coordinates iteration from the SR04 distances list(rotate to left)
def get_cordinates(front_distances,angle_resolution):
    start_angle=0
    iter_angle=0
    cordinates=[]
    for i in front_distances:
        angle=start_angle+iter_angle*angle_resolution
        cordinate=get_position(i,angle)
        iter_angle+=1
        cordinates.append([320-cordinate[0],480-cordinate[1]])
    return cordinates

#get multy coordinates iteration from the SR04 distances list,(rotate to right)
def get_cordinates_r(front_distances,angle_resolution):
    start_angle=0
    j=0
    cordinates=[]
    for i in front_distances:
        angle=start_angle+j*angle_resolution
        cordinate=get_position(i,angle)
        j+=1
        cordinates.append([320+cordinate[0],480-cordinate[1]])
    return cordinates

#SR04 left scan and store the distances into list scan_l       
def sonic_scan_l():
    scan_l=[]
    #range(25,120,3) means PWM duty cycle*10
    #PWM duty cycle 2.5 to 12 is servo angle start from 0 end in about 180 degree
    for i in range(25,120,3):
        p.ChangeDutyCycle(i/10)
        time.sleep(0.08)
        p.ChangeDutyCycle(0)
        a=sonic_distance.sonic_detect()
        scan_l.append(a)
    return scan_l

#SR04 right scan and store the distances into list scan_r     
def sonic_scan_r():
    scan_r=[]
    #
    for i in range(120,25,-3):
        p.ChangeDutyCycle(i/10)
        time.sleep(0.08)
        p.ChangeDutyCycle(0)
        a=sonic_distance.sonic_detect()
        scan_r.append(a)
    return scan_r


if __name__=='__main__':
    if 1:  
        pygame.init()
        #set screen size 640X480
        screen = pygame.display.set_mode([640, 480])
        
        screen.fill([0, 0, 0])
        Red=[255,0,0]
        Green=[0,255,0]
        Yellow=[200,140,0]
        while 1:        
            distance_list=sonic_scan_l()
            coord=get_cordinates(distance_list,7)
            pygame.display.init()
            screen.fill([0, 0, 0])
            i=0
            for d in coord:
                if distance_list[i]<=30: 
                    pygame.draw.line(screen,Red,[320,480],d,2)
                    pygame.display.flip()
                elif distance_list[i]>=60: 
                    pygame.draw.line(screen,Green,[320,480],d,2)
                    pygame.display.flip()
                else : 
                    pygame.draw.line(screen,Yellow,[320,480],d,2)
                    pygame.display.flip()
                i+=1
            distance_list=sonic_scan_r()
            coord=get_cordinates_r(distance_list,6.3)
            pygame.display.init()
            screen.fill([0, 0, 0])
            i=0
            for d in coord:
                if distance_list[i]<=30: 
                    pygame.draw.line(screen,Red,[320,480],d,2)
                    pygame.display.flip()
                elif distance_list[i]>=60: 
                    pygame.draw.line(screen,Green,[320,480],d,2)
                    pygame.display.flip()
                else : 
                    pygame.draw.line(screen,Yellow,[320,480],d,2)
                    pygame.display.flip()
                i+=1          
            pygame.event.pump()

        
        
        
            

        
    

