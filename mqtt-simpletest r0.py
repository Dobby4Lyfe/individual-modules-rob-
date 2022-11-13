# simple test to simulate mqtt topics from dashboard


import time
from mqtt_helper import Mqtt
import json

mqtt = Mqtt()

# modes: auto, man (x/y pixels), 
#        inc (x/y small counts), 
#        home (goto home pos), 
#        servo (goto position x/y counts)


mode_dic = { 
            "mode" : 'home',
            "pan" : 500,
            "tilt" : 0,
            "rotate" : 0,
       }


mqtt_dic1 = {
           "name" :  '/home/pi/dobby/dobbysound/s1.ogg',
           "descr" : 'Dobby is mad',
           "type" : 'blah',
           "pan" : 200,
           "tilt" : -20, 
           "rotate" : 20, 
           "delay" : 5,
                  
        }

mqtt_dic2 = {
           "name" :  '/home/pi/dobby/dobbysound/s2.ogg',
           "descr" : 'Dobby is mad',
           "type" : 'blah',
           "pan" : -250,
           "tilt" : 50, 
           "rotate" :20, 
           "delay" : 10,
                  
        }


while 1:
#Test for servo mode -send pixel x/y to servo for conversion to servo counts
    mode_dic["mode"] = "home"
    mqtt.publish('/mode', json.dumps(mode_dic))
    time.sleep(4)
    mode_dic["mode"] = "servo"
    mode_dic["pan"] = 650
    mode_dic["tilt"] = 400
    mode_dic["rotate"] = 500
    mqtt.publish('/mode', json.dumps(mode_dic))
    time.sleep(60)
    
# Test for phrase topic,  sends two gestures with two different sound file names
# needs both servo code and voice code running

    # mqtt.publish('/phrase', json.dumps(mqtt_dic1))
    # time.sleep(5) 
    # mqtt.publish('/phrase', json.dumps(mqtt_dic2)) 

    
#Test for increments
    # mode_dic["mode"] = "home"
    # mqtt.publish('/mode', json.dumps(mode_dic))
    # time.sleep(4)
    # mode_dic["mode"] = "inc"
    # mode_dic["pan"] = 150
    # mode_dic["tilt"] = 0
    # mode_dic["rotate"] = 0
    # mqtt.publish('/mode', json.dumps(mode_dic))
    # time.sleep(5)
    # mode_dic["pan"] = -100
    # mqtt.publish('/mode', json.dumps(mode_dic))
    # time.sleep(5)
    
#test for home functions -dobby looks straight ahead.  only needs mode to be home ignors other items

    # mode_dic["mode"] = "home"
    # mqtt.publish('/mode', json.dumps(mode_dic))

