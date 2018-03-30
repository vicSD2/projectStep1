//argv[0]: node, argv[1]: command, argv[2]: destination
var selfAddr = '0x8a0e3931463b71050033253af4e5e35a95b19b38'; //Pls change if this node is not node A!

function ethTransaction(recipientAddr,energyAmount){
  var Web3 = require('web3');
  var ethAmount = energyAmount;
  // Show web3 where it needs to look for the Ethereum node.
  web3 = new Web3(new Web3.providers.HttpProvider('https://rinkeby.infura.io/YOUR-API-TOKEN-HERE'));

  // An extra module is required for this, use npm to install before running
  var Tx = require('ethereumjs-tx');

  var pubKey = selfAddr;
  // Used to sign the transaction. Obviously you SHOULD better secure this than just plain text
  var privateKey = new Buffer('82f7a41925b65cd45338989c3aa16967cd08632934eeef39dc302ac0ed40c026', 'hex'); //Replace with appropriate node private key
  var publicKey = new Buffer(pubKey, 'hex');

  var number = web3.eth.getTransactionCount(pubKey);

  number.then(function(numb) {
  	numb +=1;
      // The reciviing address of the transaction
      var receivingAddr = recipientAddr; // '0xb2d180dc3c55e57783c0351fd0279d779aa63286'
      // Value to be sent, converted to wei and then into a hex value
      var txValue = web3.utils.numberToHex(web3.utils.toWei(ethAmount, 'ether'));
      // Data to be sent in transaction, converted into a hex value. Normal tx's do not need this and use '0x' as default, but who wants to be normal?
      var txData = web3.utils.asciiToHex(ethAmount+' Ether sent for Energy');
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

      web3.eth.sendSignedTransaction('0x' + serializedTx.toString('hex')) // Broadcast the transaction to the network
          .on('receipt', console.log); // When a receipt is issued, log it to the console

  });
}

function getBalance(){
  // Require the web3 node module.
  var Web3 = require('web3');

  // Show Web3 where it needs to look for a connection to Ethereum.
  web3 = new Web3(new Web3.providers.HttpProvider('https://rinkeby.infura.io/YOUR-API-TOKEN-HERE'));

  // Show the address in the console.
  console.log('Node Address:', selfAddr);
  var etherAmount = 0;
  // Use Wb3 to get the balance of the address, convert it and then show it in the console.
  web3.eth.getBalance(selfAddr, function(error, result) {
  if (!error){
      etherAmount = web3.utils.fromWei(result, 'ether');
      console.log('Node Balance: ', etherAmount); // Show the ether balance after converting it from Wei, be sure to change it to our respective unit of token.
  }
  else
      console.log('Houston we have a problem: ', error); // Should dump errors here
  });
  return etherAmount;
}

var currentBalance = getBalance();
var energyNeeded = true;
var nodeBAddr = '0xf880cbfecc4cf48682e45392d4ecc5f38004f276';
var nodeCAddr = '0x2b84b4d2c6feb31232b5f6a0d39eb132fe67dcda';

function idle(){
  console.log('Checking node balance.....');

  if(currentBalance < getBalance()){
    console.log('Deposit detected, beginning transfer now.');
    var amountReceived = getBalance() - currentBalance;
    //triggerPyScript(amountReceived);
    console.log('We received: ', amountReceived);
    console.log('Energy Transfer Supposedly Complete.');
    //Python script output here.
    //Run python script to trigger arduino relays.
  }
  else if(energyNeeded){
    //Future functions will provide a neighbor source  address
    //Future functions will provide an amount of price for transfer
    var price = '0.2'; //As an example
    var targetNode = 'nodeC'; //As an example
    if(targetNode == 'nodeC'){
      ethTransaction(nodeCAddr, price);
    }
    else {
      ethTransaction(nodeCAddr, price);
    }
    energyNeeded = false;
  }
  else{
    console.log('No Change Detected, no energy needed.');
  }
  currentBalance = getBalance();
  setTimeout(idle, 10000);
}

function triggerPyScript(receivedAmt){ //Currently in progress, pending implementation.
  var spawn = require("child_process").spawn;
  var filePath = "/home/vic/Documents/projectStep1/arduinoComms.py"
  var pythonProcess = spawn('python',[filePath,receivedAmt]); //Pls change depending on file location.
  pythonProcess.stdout.on('data', function (data){
    if(data == 1){
      console.log('Transaction Completed, Energy Delivered.');
    }
    else{
      console.log('Transaction Incomplete.');
    }
  });
}
idle();
