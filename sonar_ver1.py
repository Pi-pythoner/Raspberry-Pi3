import RPi.GPIO as GPIO   #Servo type (SG90 and MG90S)
import time
#from sonic_distance import sonic_pst WARN:here global list refresh fail
import sonic_distance
import pygame,math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT, initial=False)
GPIO.setup(36, GPIO.OUT, initial=False)  
#p = GPIO.PWM(3,50) #50HZ  #SG90/MG90
#p.start(0)
p = GPIO.PWM(33,50)   #front ultra sonic servo
p2 = GPIO.PWM(36,50)
p.start(0)
p2.start(0)

def get_position(d,angle):
    Hight=round(math.sin(math.pi*angle/180)*d*3,3)
    Width=round(math.cos(math.pi*angle/180)*d*3,3)
    return [Width,Hight]

print(get_position(10,135))
    
def get_cordinates(front_distances,angle_resolution):
    start_angle=0
    j=0
    cordinates=[]
    for i in front_distances:
        angle=start_angle+j*angle_resolution
        cordinate=get_position(i,angle)
        j+=1
        cordinates.append([320-cordinate[0],480-cordinate[1]])
    return cordinates

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
        
def sonic_scan():
    scan=[]
    scan_b=[]
    for i in range(25,120,3):
        p.ChangeDutyCycle(i/10)
        time.sleep(0.08)
        p.ChangeDutyCycle(0)
        a=sonic_distance.sonic_detect()
        scan.append(a)
    for i in range(120,25,-3):
        p.ChangeDutyCycle(i/10)
        time.sleep(0.08)
        p.ChangeDutyCycle(0)
        a=sonic_distance.sonic_detect()
        scan_b.append(a)
    return [scan,scan_b]
    

def rada():
    scanner=[]
    for i in range(1,180,3):
        p.ChangeDutyCycle(i*0.05+3)
        time.sleep(1)
        a=sonic_distance.sonic_detect()
        scanner.append(a)
    print(scanner)
    scanner=[]


if __name__=='__main__':
    if 1:
        pygame.init()
        screen = pygame.display.set_mode([640, 480])
        screen.fill([0, 0, 0])
        running = True

        
        
        while 1:
            pygame.time.delay(30)
            a=sonic_scan()
            e=get_cordinates(a[0],6)
            pygame.display.init()
            screen.fill([0, 0, 0])
            for d in e:
                ##color_d=abs(((d[0]-320)**2+(d[1]-480)**2)**0.5)
                #print(color_d)
                pygame.draw.line(screen,[255, 255, 255],[320,480],d,2)
                pygame.display.flip()
           
            
            pygame.event.pump()
        pygame.display.init()
        screen.fill([0, 0, 0])
        pygame.display.flip()
        
        
        
            

        
    

