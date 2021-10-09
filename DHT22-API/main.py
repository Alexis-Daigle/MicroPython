from machine import Pin, I2C
from time import sleep
import dht
import network
import ssd1306
import json
import urequests
dht22 = dht.DHT22(Pin(2))
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

while True:
  try:
    sleep(20)
    dht22.measure()
    temp = dht22.temperature()
    hum = dht22.humidity()
    str_temp = str('Temp: %3.2f C' %temp)
    str_shum = str('Hum: %3.2f %%' %hum)
    oled.fill(0)
    oled.text(str_temp, 0, 10)
    oled.text(str_shum, 0, 20)
    oled.show()
    #print('Temp: %3.2f C' %temp)
    #print('Hum: %3.2f %%' %hum)
    data = {"api_key":"KEyKEyKEy","sensor_name":"DHT22","temperature":temp,"humidity":hum}
    api = urequests.post("https://NodeRedIP:1880/update-sensor", json=data)
    if api.status_code in [200, 201]:
      print('success')
    else:
      print(api.text)
      raise Exception(api.text)
    api.close()
  except OSError as e:
    print('Failed to read data from the DHT22 sensor.')
