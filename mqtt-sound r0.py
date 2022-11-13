import pygame
from mqtt_helper import Mqtt, STATE_MAP
import time
import json

global name, pan, tilt, rotate, delay
# pan = 0
# tilt =0
# rotate =0
# delay =0
name = "/home/pi/dobby/dobbysound/s1.ogg"

dobby = Mqtt()

pygame.init() 
#s1 = pygame.mixer.Sound("/home/pi/dobby/dobbysound/s1.ogg")
#s2 = pygame.mixer.Sound("/home/pi/dobby/dobbysound/s2.ogg")


def phrasepayload(msg):
    global name, pan, tilt, rotate, delay
    payload = json.loads(msg['payload'])
    name = payload['name']
    pygame.mixer.Sound(name).play()
    # pan = payload['pan']
    # tilt = payload['tilt']
    # rotate = payload['rotate']
    # delay = payload['delay']
    # print("file name :",name,"pan :", pan,"tilt :", tilt, "rotate :", rotate,"delay :" ,delay)

dobby.subscribe('/phrase', phrasepayload)


while 1:
    time.sleep(0.05)
    
