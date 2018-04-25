import os,sys
import web3
import time
import socket
import threading
from pyfirmata import Arduino, util

relayBoard = Arduino('/dev/ttyACM0') #Remember to upload the StandardFirmata program in the arduino and change the port
it = util.Iterator(relayBoard) #Declare iterator 
it.start() #Start the iterator to read

w = web3.Web3(web3.HTTPProvider('https://rinkeby.infura.io/12345678'))
w.eth.enable_unaudited_features() #Enable web3 features

gas_limit = 250000 #Adjust when necessary
gas_price = 60 #Ditto

from_addr = '0x577d0be430fca2b0331f5b1dcc2ee21962c4b0df' #Node A recipient address
key = '4415ad17a0445b70514322a25a05e9b31d458a0b6fa73c1d7ff3ea3286677d7b' #private key

#Every node will have the rest of the addresses.
nodeBAddr = '0x8a0e3931463b71050033253af4e5e35a95b19b38'
nodeCAddr = '0x2b84b4d2c6feb31232b5f6a0d39eb132fe67dcda'
targetNode  = ''
minThreshold = 11.4 #minimum battery voltage to compare to before deciding to charge
energyNeeded = True #If value is hardcoded to True, it is for testing purposes.

relay1Pin = relayBoard.get_pin('d:2:o') #Declares the digital output pin 2 of the Arduino for relay. Remember to change according to designated pin
relay1Pin.write(0) #Default state must be switched off

#Sends ether from one account to another, takes recipient and sender address, ether amount, gas limit and price.
def send_eth(from_addr, to_addr, eth_amount, gas_limit, gas_price):
    nonce = w.eth.getTransactionCount(w.toChecksumAddress(from_addr))
    transaction = {
        'to':to_addr,
        'from':from_addr,
        'value':int(eth_amount*(10**18)),
        'gas':gas_limit,
        'gasPrice':int(gas_price*(10**9)),
        'chainId':4,
        'nonce':nonce
    }
    signed_transaction = w.eth.account.signTransaction(transaction, key)
    transaction_id = w.eth.sendRawTransaction(signed_transaction.rawTransaction)
    print ('\nhttps://rinkeby.etherscan.io/tx/{0}'.format(transaction_id.hex()))

# Checks account balance to look out for transactions.
def check_bal(from_addr):
    weibalance = w.eth.getBalance(w.toChecksumAddress(from_addr)) #Checks balance in Wei
    balance = w.fromWei(weibalance,'ether') #Converts Wei balance to ether
    print ("The current balance is " + str(balance))
    return balance

def idle():
    print ("Checking Node Balance......")
    print ("Checking Battery Levels....")
    #energyNeeded = energyCheck()

    #If there is a positive change in balance then perform the transfer.
    if  True: #currentBalance < check_bal(from_addr):
        print ("Deposit detected, beginning transfer now.")
        amt_received = 0.1 #check_bal(from_addr) - currentBalance
        triggerRelays(amt_received)
        print ("We received " + str(amt_received))
      
    elif energyNeeded:
        clientScript()#socketProgram will find appropriate vendor & price
        #targetNodeAddr = 'C' socketProgram will set this value. Currently test value.

        if targetNodeAddr == 'B':
            #send_eth(from_addr,nodeBAddr,price,gas_limit,gas_price)
            print('Transaction Made')
        else:
            #send_eth(from_addr,nodeCAddr,price,gas_limit,gas_price)
            print('Transaction Made')
    else:
        print ('No change detected, no energy needed.')

def energyCheck():
	num_samples = 10
	sampleCount = 0
	voltSum = 0
	digitalVolt = 0
	analogVolt = relayBoard.get_pin('a:0:i') #Change according to the designated pin
	analogVolt.enable_reporting()
	while sampleCount < num_samples:
		voltSum += analogVolt.read()
		sampleCount += 1
		time.sleep(10)
	digitalVolt = ((float(voltSum)/(float(num_samples)*5.015))/1024.0)*11.132
	if digitalVolt > minThreshold:
		return False
	else:
		return True
	
def clientScript():
	
def triggerRelays(amt_received):
    currency = amt_received
    transferTime = currency*60
    #Since charge time was tested at approximately 17W per second,currency rate is set at 1 Eth per kW
    relay1Pin.write(1)
    time.sleep(transferTime)
    relay1Pin.write(0)
    print ('Energy Transfer Complete.')

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

while True:
	currentBalance = check_bal(from_addr)
	idle()
	energyNeeded = False
	time.sleep(10)
