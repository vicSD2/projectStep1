
//console.log(process.argv[2])

if (!process.argv[2]) {
    console.log("Missing Address");
} else {
    // Require the web3 node module.
    var Web3 = require('web3');

    // Show Web3 where it needs to look for a connection to Ethereum.
    web3 = new Web3(new Web3.providers.HttpProvider('https://rinkeby.infura.io/YOUR-API-TOKEN-HERE'));

    // Write to the console the script will run shortly.
    console.log('Getting Ethereum address info.....');
    // Define the address to search witin.
    var addr = (process.argv[2]); //'0x8a0e3931463b71050033253af4e5e35a95b19b38'

    // Show the address in the console.
    console.log('Address:', addr);

    // Use Wb3 to get the balance of the address, convert it and then show it in the console.
    web3.eth.getBalance(addr, function(error, result) {
        if (!error)
            console.log('Ether:', web3.utils.fromWei(result, 'ether')); // Show the ether balance after converting it from Wei
        else
            console.log('Huston we have a promblem: ', error); // Should dump errors here
    });
}