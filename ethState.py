import os,sys
import web3
import time

w = web3.Web3(web3.HTTPProvider('https://rinkeby.infura.io/12345678'))
w.eth.enable_unaudited_features()
# gas example
gas_limit = 250000
gas_price = 60
#eth_amount = 0.02
#to_addr = '0x2b84b4d2c6feb31232b5f6a0d39eb132fe67dcda'
from_addr = '0x577d0be430fca2b0331f5b1dcc2ee21962c4b0df' #Node A
key = '4415ad17a0445b70514322a25a05e9b31d458a0b6fa73c1d7ff3ea3286677d7b'
#Every node will have the rest of the addresses.
nodeBAddr = '0x8a0e3931463b71050033253af4e5e35a95b19b38'
nodeCAddr = '0x2b84b4d2c6feb31232b5f6a0d39eb132fe67dcda'
# Below is equivalent to ethTransaction() from nodeState.js
energyNeeded = True
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

# Below is equivalent to the getBalance from nodeState.js
def check_bal(from_addr):
    weibalance = w.eth.getBalance(w.toChecksumAddress(from_addr)) #Checks balance in Wei
    balance = w.fromWei(weibalance,'ether') #Converts Wei balance to ether
    print ("the balance is " + str(balance))
    return balance

def idle():
    print ("Checking Node Balance......")
    print ("Checking Battery Levels....")
   # energyNeeded = True #check_batt() goes here

    #If there is a positive change in balance then perform the transfer.
    if currentBalance < check_bal(from_addr):
        print ("Deposit detected, beginning transfer now.")
        amt_received = check_bal(from_addr) - currentBalance
        #triggerRelays(amt_received)
        print ("We received " + str(amt_received))
        print ('Enegery Transfer Comeplete.')
    elif energyNeeded:
        #socketProgram will find appropriate vendor
        #socketProgram will return appropriate price
        price = 0.1
        targetNodeAddr = 'C' #socketProgram will set this value. Currently test value.

        if targetNodeAddr == 'B':
            send_eth(from_addr,nodeBAddr,price,gas_limit,gas_price)
        else:
            send_eth(from_addr,nodeCAddr,price,gas_limit,gas_price)
    else:
        print ('No change detected, no energy needed.')

#def triggerPyScript(amt_received):

while True:
    currentBalance = check_bal(from_addr)
    idle()
    energyNeeded = False
    time.sleep(10)
