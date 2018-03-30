/*
A script that will sign and broadcast an ethereum transaction to the network, then shows the result in the console.
argv[0]: node, argv[1]: command, argv[2]: recipient address, argv[3]: desired amount
WARNING!
If executed this script will send ether, be sure the info is correct before you run this!
Alternatively you should use a test net with test ether first before running this on the main net.

For an explanation of this code, navigate to the wiki https://github.com/ThatOtherZach/Web3-by-Example/wiki/Send-Ether-Transaction
*/

// Add the web3 node module
var Web3 = require('web3');

// Show web3 where it needs to look for the Ethereum node.
web3 = new Web3(new Web3.providers.HttpProvider('https://rinkeby.infura.io/sPHjtjaDwLBgYyXQL6Ps'));
//web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));

// An extra module is required for this, use npm to install before running
var Tx = require('ethereumjs-tx');

var pubKey = "0x8a0e3931463b71050033253af4e5e35a95b19b38" //Replace with appropriate node addess
// Used to sign the transaction. Obviously you SHOULD better secure this than just plain text
var privateKey = new Buffer('82f7a41925b65cd45338989c3aa16967cd08632934eeef39dc302ac0ed40c026', 'hex'); //Replace with appropriate node private key
var publicKey = new Buffer(pubKey, 'hex');

if (!process.argv[2]) {
    console.log("Missing Address");
}

if (!process.argv[3]) {
    console.log("Amount");
}

var txValue = web3.utils.numberToHex(web3.utils.toWei(process.argv[3], 'ether'));
var receivingAddr = (process.argv[2]); // '0xb2d180dc3c55e57783c0351fd0279d779aa63286'

web3.eth.getTransactionCount(pubKey).then((nonce) => {
  var tx = new Tx({
    nonce: nonce,
    from: pubKey, 
    to: receivingAddr, 
    value: txValue, 
    gasLimit: 22000,
    chainId: 4,
    gasPrice:50000
  });
  tx.sign(privateKey);
  web3.eth.sendSignedTransaction('0x'+tx.serialize().toString('hex')).then((response) => {
     console.log(response);
  });
});

/*
var number = web3.eth.getTransactionCount(pubKey);

number.then(function(numb) {
	numb +=1;
    // The reciviing address of the transaction
    var receivingAddr = (process.argv[2]); // '0xb2d180dc3c55e57783c0351fd0279d779aa63286'

    // Value to be sent, converted to wei and then into a hex value
    var txValue = web3.utils.numberToHex(web3.utils.toWei(process.argv[3], 'ether'));

    // Data to be sent in transaction, converted into a hex value. Normal tx's do not need this and use '0x' as default, but who wants to be normal?
    var txData = web3.utils.asciiToHex(process.argv[3]+' Ether sent for Energy');

    var rawTx = {
        nonce: "0x"+numb, // Nonce is the times the address has transacted, should always be higher than the last nonce 0x0#
        gasPrice: '0x14f46b0400', // Normal is '0x14f46b0400' or 90 GWei
        gasLimit: '0x55f0', // Limit to be used by the transaction, default is '0x55f0' or 22000 GWei
        to: receivingAddr, // The receiving address of this transaction
        value: txValue, // The value we are sending '0x16345785d8a0000' which is 0.1 Ether
        data: txData // The data to be sent with transaction, '0x6f6820686169206d61726b' or 'oh hai mark'
    }

    //console.log(rawTx); // This is used for testing to see if the rawTx was formmated created properly, comment out the code below to use.


    var tx = new Tx(rawTx);
    tx.sign(privateKey); // Here we sign the transaction with the private key

    var serializedTx = tx.serialize(); // Clean things up a bit

    console.log(serializedTx.toString('hex')); // Log the resulting raw transaction hex for debugging if it fails to send
    //console.log("https://rinkeby.etherscan.io/tx/" + '0x' + serializedTx.toString('hex'))
    web3.eth.sendSignedTransaction('0x' + serializedTx.toString('hex')) // Broadcast the transaction to the network
        .on('receipt', console.log); // When a receipt is issued, log it to the console
});
