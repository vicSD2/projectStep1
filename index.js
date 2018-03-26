
require('dotenv').config()

var Web3 = require('web3'); 			//git config --global url.https://github.com/.insteadOf git://github.com/ command needed to circumvent firewall
var util = require('ethereumjs-util'); 		//npm install ethereumjs-util --save
var tx = require('ethereumjs-tx'); 		//npm install ethereumjs-tx --save
var lightwallet = require('eth-lightwallet'); 	//npm install eth-lightwallet
var txutils = lightwallet.txutils;
var web3 = new Web3(
    new Web3.providers.HttpProvider('https://rinkeby.infura.io/')
);

//Change for every node, each will have different wallets
var address = process.env.PUB_KEY;//'0x8a0e3931463b71050033253af4e5e35a95b19b38'; //public
var key = process.env.PRIV_KEY;//'82f7a41925b65cd45338989c3aa16967cd08632934eeef39dc302ac0ed40c026'; // private

checkBal(address);

function sendRaw(rawTx) {
    var privateKey = new Buffer(key, 'hex');
    var transaction = new tx(rawTx);
    transaction.sign(privateKey);
    var serializedTx = transaction.serialize().toString('hex');
    web3.eth.sendRawTransaction(
    '0x' + serializedTx, function(err, result) {
        if(err) {
            console.log(err);
        } else {
            console.log(result);
        }
    });
}

// Create transaction to send ethereum
// var rawTx = {
//     nonce: web3.toHex(web3.eth.getTransactionCount(address)),
//     gasLimit: web3.toHex(21000),
//     gasPrice: web3.toHex(20000000000),
//     to: '0x31B98D14007bDEe637298086988A0bBd31184523',
//     value: web3.toHex(web3.toBigNumber(web3.eth.getBalance(address))
//           .minus(web3.toBigNumber(21000).times(20000000000)))
// };
// sendRaw(rawTx);

// Create monitoring function
// checks every 15s for money in account and who sent it
function checkBal(addr1) {
	var addr = addr1;
	var localBalance = web3.eth.getBalance(addr1); //Current balance at that moment.
	
	setTimeout(function () {monitorAddress(addr,localBalance)}, 1000); //Keep it runing every second
	//monitorAddress(addr,localBalance);
	localBalance = web3.eth.getBalance(addr); //Update balance after it checks it in case it changed.
		
}

function monitorAddress(addr,localBal) {
	var addy = addr;
	var localBalance= localBal;
	if(localBalance!= web3.eth.getBalance(addy)){ //Checks the balance passed by the method with the current balance of that moment.
		console.log('Transaction Occurred'); 
		//Will always output this because for some reason the balance is read as a junk value??
		//Send signal through GPIO to enable the relays
	}
	else {
	console.log('No Transaction Occurred');
		}
}
// check web3 api for how to check balances



