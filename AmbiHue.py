#! /usr/bin/python
import simplejson as json
import urllib2 as url
from time import sleep
from phue import Bridge
import colorsys

#ip adress op ambilight TV
ambilight_tv_ip = "192.168.1.103"

#ip adress HUE bridge
hue_ip = "192.168.1.198"

#HUE bidge API key
hue_api_key = "ec2c80890ecba9c42d65d44d3be6d7564dca63c8"

#grid to attach lights to one of 9 zones of the tv
#the HUE light nr's can be found in the official HUE app
#              top
#         0     1     2
#        _______________
#     2 |               | 0
#       |               |
#left 1 |               | 1 right
#       |               |
#     0 |_______________| 2
#
#         2     1     0
#             bottom

left   = [6, 0, 17] #left  [0, 1, 2]
top    = [0, 0, 0]  #top   [0, 1, 2]
right  = [0, 1, 2]  #right [0, 1, 2]
bottom = [0, 0, 0]  #bottom[0, 1, 2]

#================================================================
#
# DO NOT CHANGE ANYTHING BELOW THIS LINE
#
#================================================================

ambilight_api = "http://" + ambilight_tv_ip + ":1925/1/ambilight/processed"
delay         = 0.5
trans_time    = 10
color_offset  = 0.1

current_light_state = {}

#send xyz to lights
def send_hsb_to_light(bridge, light, h, s, b): 
   global current_light_state

   current_hsb = current_light_state[light]

   diff_h = abs(h - current_hsb[0])
   diff_s = abs(s - current_hsb[1])
   diff_b = abs(b - current_hsb[2])
#   print("diff hue: " + str(diff_h))
   if diff_h > (color_offset * 65535) or diff_s > (color_offset * 255): # or diff_b > (color_offset * 255):
      command = {"transitiontime" : trans_time, "on" : True, "hue": h, "sat": s, "bri" : b}
      print("Sending Hue:" + str(h) + ", Sat:" + str(s) + " and Bri: " + str(b) + " to light " + str(light))
      bridge.set_light(light, command)

   current_hsb[0] = h
   current_hsb[1] = s
   current_hsb[2] = b

   current_light_state[light] = current_hsb

def rgb_to_hsb(r, g, b):
   h, s, b = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
   h = int(h * 65535)
   s = int(s * 255)
   b = int(b * 255)
   return h, s, b

def init_side(lights, side_lights, side):
   global current_light_state
   i = 0   
   for light in side_lights:
      if light != 0:
         lights[light] = [side, str(i)]
         current_light_state[light] = [0, 0, 0]
      i += 1
   return lights

def init_lights(l, t, r, b):
   lights = {}
   
   lights = init_side(lights, l, "left")
   lights = init_side(lights, t, "top")
   lights = init_side(lights, r, "right")
   lights = init_side(lights, b, "bottom")
  
   return lights      
  
#main loop
bridge = Bridge(hue_ip)
bridge.connect()

lights = init_lights(left, top, right, bottom)
print(lights)

while True:
   f = url.urlopen(ambilight_api)
   data = f.read()
   
   json_data = json.loads(data)
   ambilight_data = json_data['layer1']
   
   for light in lights:
      side = lights[light][0]
      zone = lights[light][1]

      color = ambilight_data[side][zone]

      hue, sat, bri = rgb_to_hsb(color["r"], color["g"], color["b"])     
      send_hsb_to_light(bridge, light, hue, sat, bri)
      
   sleep(delay)
