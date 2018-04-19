#!/usr/bin/python3
# first of all import the socket library
import socket    
import threading   
available = 5 
def new_client(c_socket,addr):
   b= None   
   print ('Got connection from', addr)
   while b!= 'end':
   # send a thank you message to the client. 
     b=c.recv(1024).decode()
     print(b)     
     a = input('Enter your input:')
     c.sendall(a.encode('utf-8'))
     if(a == 'end'):
      break
   c_socket.close()
# next create a socket object
s = socket.socket()         
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12348              
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)     
print ("socket is listening")           

# a forever loop until we interrupt it or 
# an error occurs
count = 0
while True:
 
   # Establish connection with client.
   if(count == 2):
    break	
   if(threading.active_count ()== 1):
    c, addr = s.accept() 	
    t = threading.Thread(target = new_client, args=(c,addr, ))
    t.start()
   count +=1
s.close()
