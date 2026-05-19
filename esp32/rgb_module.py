from machine import Pin 
import neopixel 
from yolobit import * 

pixels = neopixel.NeoPixel(Pin(pin0.pin), 4)

def hex_to_rgb(hex_str): 
    hex_str = hex_str.lstrip('#')
    
    if len(hex_str) != 6:
        return (0, 0, 0)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def led_callback(topic, msg):
    try: 
        print("RGB command received: ", msg) 
        
        if msg == "0" or msg == "#000000":
            color = (0, 0, 0)
        elif msg.startswith('#'):
            color = hex_to_rgb(msg)
        else:
            print("Invalid RGB format, skipping...")
            return

        for i in range(4): 
            pixels[i] = color 
        
        pixels.write() 
        print("Changed color to : ", color) 
        
    except Exception as e: 
        print("Error in RGB: ", e)
