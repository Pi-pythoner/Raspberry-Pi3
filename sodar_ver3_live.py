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

#set home position in screen middle bottom
def get_cordinate(d,angle):
    Hight=round(math.sin(math.pi*angle/180)*d*3,3)
    Width=round(math.cos(math.pi*angle/180)*d*3,3)
    Hight=480-Hight
    Width=320-Width
    return [Width,Hight]


if __name__=='__main__':
    if 1:  
        pygame.init()
        #set screen size 640X480
        screen = pygame.display.set_mode([640, 480])
        
        screen.fill([0, 0, 0])
        Red=[255,0,0]
        Green=[0,255,0]
        Yellow=[200,140,0]
        pygame.display.init()     
        while 1:
            screen.fill([0, 0, 0])
            pygame.display.flip()
            start_angle=0
            iter_angle=0
            for i in range(25,120,3):
                angle=start_angle+iter_angle*6.2
                p.ChangeDutyCycle(i/10)
                time.sleep(0.08)
                p.ChangeDutyCycle(0)
                dis=sonic_distance.sonic_detect()              
                coordinate=get_cordinate(dis,angle)
                                
                if dis<=30: 
                    pygame.draw.line(screen,Red,[320,480],coordinate,2)
                    pygame.display.flip()
                elif dis>=60: 
                    pygame.draw.line(screen,Green,[320,480],coordinate,2)
                    pygame.display.flip()
                else : 
                    pygame.draw.line(screen,Yellow,[320,480],coordinate,2)
                    pygame.display.flip()
                iter_angle+=1
            iter_angle=0
            screen.fill([0, 0, 0])
            pygame.display.flip()
            start_angle=180
            iter_angle=0
            for i in range(120,25,-3):
                angle=start_angle-iter_angle*6.2
                p.ChangeDutyCycle(i/10)
                time.sleep(0.08)
                p.ChangeDutyCycle(0)
                dis=sonic_distance.sonic_detect()              
                coordinate=get_cordinate(dis,angle)
                                
                if dis<=30: 
                    pygame.draw.line(screen,Red,[320,480],coordinate,2)
                    pygame.display.flip()
                elif dis>=60: 
                    pygame.draw.line(screen,Green,[320,480],coordinate,2)
                    pygame.display.flip()
                else : 
                    pygame.draw.line(screen,Yellow,[320,480],coordinate,2)
                    pygame.display.flip()
                iter_angle+=1
            iter_angle=0   
            pygame.event.pump()

        
        
        
            

        
    

