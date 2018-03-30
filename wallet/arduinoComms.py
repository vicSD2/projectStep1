import os,sys
import serial
import RPi.GPIO as GPIO
import time

seri = serial.Serial("/dev/ttyACM0",9600) #Pls change after checking it through ls /dev/tty/ACM*
seri.baudrate=9600

def switch(argv[1]){
    if(argv[1] == 'nodeA')

}
