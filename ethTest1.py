import web3
import time
import socket
import threading
from pyfirmata import Arduino, util

relayBoard = Arduino('/dev/ttyACM0')
it = util.Iterator(relayBoard)
# Declare iterator
it.start()
# Start the iterator to read
analogVolt = relayBoard.get_pin('a:3:i')
# Change according to the designated pin
analogVolt.enable_reporting()

w = web3.Web3(web3.HTTPProvider('https://rinkeby.infura.io/12345678'))
w.eth.enable_unaudited_features()
# Enable web3 features

gas_limit = 250000
# Adjust when necessary
gas_price = 60
# Ditto

from_addr = '0x577d0be430fca2b0331f5b1dcc2ee21962c4b0df'
# Node A recipient address
key = '4415ad17a0445b70514322a25a05e9b31d458a0b6fa73c1d7ff3ea3286677d7b'
# private key
# Every node will have the rest of the addresses.
nodeAIP = '192.168.137.119'
nodeBIP = '192.168.137.191'
nodeCIP = '192.168.137.153'
nodeBAddr = '0x8a0e3931463b71050033253af4e5e35a95b19b38'
nodeCAddr = '0x2b84b4d2c6feb31232b5f6a0d39eb132fe67dcda'
targetNode = ''
selfNode = 'B'
# Change depending on node!
volts_requested = None
openTime = 0
minThreshold = 11
# 12.5
# minimum battery voltage to compare to before deciding to buy
sellThreshold = 12
# 13.5
# minimum battery voltage to compare to before deciding to sell
energyNeeded = None
# If value is hardcoded to True, it is for testing purposes.

relay10Pin = relayBoard.get_pin('d:10:o')
relay2Pin = relayBoard.get_pin('d:2:o')
relay5Pin = relayBoard.get_pin('d:5:o')
# Declares the digital output pin 2 of the Arduino for relay.
relay10Pin.write(0)
relay2Pin.write(0)
relay5Pin.write(0)
# Default state must be switched off


# Sends ether from one account to another, takes recipient and sender address,
# ether amount, gas limit and price.
def send_eth(from_addr, to_addr, eth_amount, gas_limit, gas_price):
    nonce = w.eth.getTransactionCount(w.toChecksumAddress(from_addr))
    transaction = {
        'to': to_addr,
        'from': from_addr,
        'value': int(eth_amount*(10**18)),
        'gas': gas_limit,
        'gasPrice': int(gas_price*(10**9)),
        'chainId': 4,
        'nonce': nonce
    }
    signed_transaction = w.eth.account.signTransaction(transaction, key)
    transaction_id = w.eth.sendRawTransaction(
        signed_transaction.rawTransaction)
    print ('\nhttps://rinkeby.etherscan.io/tx/{0}'.format(
        transaction_id.hex()))


# Checks account balance to look out for transactions.
def check_bal(from_addr):
    weibalance = w.eth.getBalance(w.toChecksumAddress(from_addr))
    # Checks balance in Wei
    balance = w.fromWei(weibalance, 'ether')
    # Converts Wei balance to ether
    return balance


def idle():
    global targetNode
    global openTime
    print ("Checking Node Balance......")
    print ("Checking Battery Levels....")

    currentVoltage = energyCheck()
    if currentVoltage > minThreshold:
        energyNeeded = False
    else:
        energyNeeded = True

    # If there is a positive change in balance then perform the transfer.
    if currentVoltage > sellThreshold:
        # currentBalance < check_bal(from_addr):
        print ("Excess energy detected. Searching for available buyers...")
        sellScript()
        # targetNode established by this and volts requested
        triggerRelaysSND(volts_requested, targetNode)
        print ("We transmitted " + str(volts_requested) + " volts.")
        targetNode = ''

    elif energyNeeded and check_bal(from_addr) > 0.1:
        volts = 13.5 - currentVoltage
        openTime = clientScript(volts, selfNode)
        # socketProgram will find appropriate vendor & price
        relay2Pin.write(1)
        relay5Pin.write(0)
        if(selfNode == 'A'):
            if(targetNode == 'B'):
                relay10Pin.write(1)
            else:
                # target node is C
                relay10Pin.write(0)
        elif(selfNode == 'B'):
            if(targetNode == 'A'):
                relay10Pin.write(0)
            else:
                # Target node is C
                relay10Pin.write(1)
        elif(selfNode == 'C'):
            if(targetNode == 'B'):
                relay10Pin.write(0)
            else:
                # target node A
                relay10Pin.write(1)

        time.sleep(openTime)
        relay5Pin.write(0)
        relay2Pin.write(0)

        if targetNode == 'A':
            # remember to change
            # send_eth(from_addr,nodeBAddr,price,gas_limit,gas_price)
            print('Transaction Made')
            targetNode = ''
        elif targetNode == 'B':
            # send_eth(from_addr,nodeCAddr,price,gas_limit,gas_price)
            print('Transaction Made')
            targetNode = ''
        else:
            # send_eth(from_addr,nodeCAddr,price,gas_limit,gas_price)
            print('Transaction Made')
            targetNode = ''
    elif check_bal(from_addr) < 0.5:
        print ("Low ether balance detected.")
    else:
        print ('No energy needed. ')


def energyCheck():
    num_samples = 10
    sampleCount = 0
    voltSum = 0
    digitalVolt = 0
    time.sleep(1)
    while sampleCount < num_samples:
        sample = analogVolt.read()*48.4
        print(sample)
        voltSum += sample
        sampleCount += 1
        time.sleep(10)
    digitalVolt = (float(voltSum))/(float(num_samples))
    return digitalVolt


# Under close scrutiny
def clientScript(volts_needed, selfN):
    global targetNode
    global openTime
    # Create a socket object
    s = socket.socket()
    # Define the port on which you want to connect
    port = 12345
    # connect to the server on local computer
    a = None
    openTime = 0
    status = False
    while (not status):
        status = True
        try:
            s.connect((nodeAIP, port))
            # Change IP addresses
        except socket.error:
            print('connection refused, reattempting in 10s')
            time.sleep(10)
            try:
                s.connect((nodeBIP, port))
                # Change IP addresses
            except socket.error:
                print('connection refused, reattempting in 10s')
                time.sleep(10)
                status = False
    b = None
    b = s.recv(1024).decode()
    time.sleep(1)
    # receive data from the server
    while b != 'end':
        # send a thank you message to the client.
        print(b)
        if(b == 'Amount Requested: '):
            a = input(volts_needed)
            s.sendall(a.encode('utf-8'))
        elif(b == 'Name the energy destination node: '):
            a = input(selfN)
            s.sendall(a.encode('utf-8'))
        elif(b == 'Confirmed. Terminate Session?'):
            a = input('end')
            s.sendall(a.encode('utf-8'))
        elif(b == 'Connection Established'):
            a = input('Connection Confirmed')
            s.sendall(a.encode('utf-8'))
        elif(b == 'B'):
            targetNode = 'B'
            a = input('Received')
            s.sendall(a.encode('utf-8'))
        elif(b == 'A'):
            targetNode = 'A'
            a = input('Received')
            s.sendall(a.encode('utf-8'))
        elif(b == 'C'):
            targetNode = 'C'
            a = input('Received')
            s.sendall(a.encode('utf-8'))
        elif(b == 'Confirmed. Standby for payment destination:'):
            a = input('OK')
            s.sendall(a.encode('utf-8'))
        else:
            targetNode = ''
        b = s.recv(1024).decode()
    # close the connection
    openTime = int(volts_needed/0.000558333)
    s.close()


def triggerRelaysSND(v_requested, destNode):
    transferTime = int(v_requested/0.000558333)
    global targetNode
    # Since charge time was tested at approximately 17W per second,currency
    # rate is set at 1 Eth per kW
    relay2Pin.write(1)
    relay5Pin.write(1)
    # Change 5 to 0 only when receiving
    if(selfNode == 'A'):
        if(targetNode == 'B'):
            relay10Pin.write(1)
        else:
            # target node is C
            relay10Pin.write(0)
    elif(selfNode == 'B'):
        if(targetNode == 'A'):
            relay10Pin.write(0)
        else:
            # Target node is C
            relay10Pin.write(1)
    elif(selfNode == 'C'):
        if(targetNode == 'B'):
            relay10Pin.write(0)
        else:
            # target node A
            relay10Pin.write(1)

    time.sleep(transferTime)
    relay5Pin.write(0)
    relay2Pin.write(0)
    # Check with pin2 soon pls
    print ('Energy Transfer Complete.')


def sellScript():
    def new_client(c_socket, addr):
        global targetNode
        global volts_requested
        global offerFound
        b = ''
        incoming = None
        volts_requested = 0
        print ('Got connection from', addr)
        a = input('Connection Established')
        c_socket.sendall(a.encode('utf-8'))
        b = c_socket.recv(1024).decode()
        while b != 'end':
            # send a thank you message to the client.
            
            print(b)
            incoming = int(b)
            if (incoming > 2.5):
                a = input('The amount too high, select a smaller amount: ')
                c_socket.sendall(a.encode('utf-8'))
                # prints the message above
            elif (incoming < 2.5 and incoming > 0):
                volts_requested = incoming
                a = input('Name the energy destination node: ')
                # call to select target node, etc
                c_socket.sendall(a.encode('utf-8'))
                # prints the message above
                time.sleep(2)
                incomingNode = c_socket.recv(1024).decode()
                if(incomingNode == 'A'):
                    targetNode = 'A'
                    a = input('Confirmed. Standby for payment destination:')
                    c_socket.sendall(a.encode('utf-8'))
                    time.sleep(2)
                    confirmation = c_socket.recv(1024).decode()
                    if(confirmation == 'OK'):
                        a = input(selfNode)
                        c_socket.sendall(a.encode('utf-8'))
                        time.sleep(2)
                        confirmation = c_socket.recv(1024).decode()
                        if(confirmation == 'Received'):
                            a = input('Confirmed. Terminate Session?')
                            c_socket.sendall(a.encode('utf-8'))
                            # prints the message above
                            time.sleep(2)
                            confirmation = c_socket.recv(1024).decode()
                            offerFound = True
                            if(confirmation == 'end'):
                                a = 'end'
                                b = 'end'
                                c_socket.sendall(a.encode('utf-8'))
                elif(incomingNode == 'B'):
                    targetNode = 'B'
                    a = input('Confirmed. Standby for payment destination:')
                    c_socket.sendall(a.encode('utf-8'))
                    time.sleep(2)
                    confirmation = c_socket.recv(1024).decode()
                    if(confirmation == 'OK'):
                        a = input(selfNode)
                        c_socket.sendall(a.encode('utf-8'))
                        time.sleep(2)
                        confirmation = c_socket.recv(1024).decode()
                        if(confirmation == 'Received'):
                            a = input('Confirmed. Terminate Session?')
                            c_socket.sendall(a.encode('utf-8'))
                            # prints the message above
                            time.sleep(2)
                            confirmation = c_socket.recv(1024).decode()
                            offerFound = True
                            if(confirmation == 'end'):
                                a = 'end'
                                b = 'end'
                                c_socket.sendall(a.encode('utf-8'))
                elif(incomingNode == 'C'):
                    targetNode = 'C'
                    a = input('Confirmed. Standby for payment destination:')
                    c_socket.sendall(a.encode('utf-8'))
                    time.sleep(2)
                    confirmation = c_socket.recv(1024).decode()
                    if(confirmation == 'OK'):
                        a = input(selfNode)
                        c_socket.sendall(a.encode('utf-8'))
                        time.sleep(2)
                        confirmation = c_socket.recv(1024).decode()
                        if(confirmation == 'Received'):
                            a = input('Confirmed. Terminate Session?')
                            c_socket.sendall(a.encode('utf-8'))
                            # prints the message above
                            time.sleep(2)
                            confirmation = c_socket.recv(1024).decode()
                            offerFound = True
                            if(confirmation == 'end'):
                                a = 'end'
                                b = 'end'
                                c_socket.sendall(a.encode('utf-8'))
            elif(b == 'Connection Confirmed'):
                a = input('Amount Requested: ')
                c_socket.sendall(a.encode('utf-8'))
            if(b == 'end'):
                print('Connection Closed')
                c_socket.close()
                break
            b = c_socket.recv(1024).decode()
        c_socket.close()
    s = socket.socket()
    print ("Socket successfully created")
    port = 12345
    s.bind(('', port))
    print ("Socket bound to %s" % (port))
    s.listen(5)
    print("Socket is listening...")
    count = 0
    offerFound = False
    while not offerFound:
        if(threading.active_count() == 2):
            c, addr = s.accept()
            t = threading.Thread(target=new_client, args=(c, addr, ))
            t.start()
    print ("Available buyer found, closing socket.")
    s.close()


while True:
    currentBalance = check_bal(from_addr)
    idle()
    targetNode = ''
    time.sleep(10)
