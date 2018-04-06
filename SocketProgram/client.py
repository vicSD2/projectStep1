#!/usr/bin/python
# Import socket module
import socket 
import sys              
 
# Create a socket object
s = socket.socket()         
 
# Define the port on which you want to connect
port = 12345               
 
# connect to the server on local computer

try:
  s.connect(('127.0.0.1', port))
except socket.error:
  print('connection refused')
  sys.exit()
  
b = None
# receive data from the server
while b!= 'end':
 
   # send a thank you message to the client. 
   a = raw_input('Enter your input:')
   s.send(a)
   b=s.recv(1024)
   print(b)
# close the connection
s.close()       