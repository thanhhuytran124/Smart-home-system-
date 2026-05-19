import network
import time
import ntptime
from config import WIFI_SSID, WIFI_PASS

def connect_wifi(lcd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Dang ket noi WiFi...")
        lcd.move_to(0, 0)
        lcd.putstr("Connecting WiFi ")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
            
    print("\nWiFi connected! IP:", wlan.ifconfig()[0])
    lcd.clear()
    lcd.putstr("WiFi OK!")
    time.sleep(1)

def sync_time(lcd):
    try:
        ntptime.settime()
        print("Da dong bo gio Internet")
        lcd.clear()     
        lcd.putstr("Time set up")
        time.sleep(1)
        lcd.clear()
        lcd.putstr("Successfully!")
        time.sleep(1)
    except:
        print("Loi dong bo gio")
        lcd.clear()
        lcd.putstr("Time setup error")
        time.sleep(1)
