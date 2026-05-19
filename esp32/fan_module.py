from yolobit import *

current_fan_speed = 0
speed_fan_value = pin10
def set_speed(speed_input): 
    global current_fan_speed
    try: 
        val = int(speed_input) 
        if val < 0: val = 0 
        if val > 100: val = 100
        
        current_fan_speed = val 
        
        duty_value = int(current_fan_speed * 10.23)
        
        speed_fan_value.write_analog(duty_value)
        
        print("Sent PWM :", duty_value)
    except Exception as e: 
        print("Error in control fan:", e)

def fan_callback(topic, msg): 
    print("Received command from Cloud:", msg) 
    set_speed(msg)
