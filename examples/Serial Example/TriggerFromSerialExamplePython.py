# for raspberry pi pico or pico W, language: MicroPython
from machine import Pin,UART
import time

#initialize serial comms with a boudrate of 9600, and define rx and tx pins
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=2)

#define output pin, and set as output
output = Pin(6, Pin.out)

while True:
    #check for any serial comms. if present, collect comms
    if uart.any():
        data = uart.read()
        
        #if comms is equal to "T", trigger output
        if data == b'T':
            output.toggle()
            time.sleep(1)
            output.toggle()