#!/usr/bin/python
# first of all import the socket library
import socket    
import thread           
def new_client(c_socket,addr):
   print 'Got connection from', addr
   while b!= 'end':
   # send a thank you message to the client. 
     b=c.recv(1024)
     print(b)     
     a = raw_input('Enter your input:')
     c.send(a)
   c_socket.close()
# next create a socket object
s = socket.socket()         
print "Socket successfully created"
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('', port))        
print "socket binded to %s" %(port)
 
# put the socket into listening mode
s.listen(5)     
print "socket is listening"           
b= None
# a forever loop until we interrupt it or 
# an error occurs

while True:
 
   # Establish connection with client.
   c, addr = s.accept()   
   thread.start_new_thread(new_client,(c,addr))
s.close()