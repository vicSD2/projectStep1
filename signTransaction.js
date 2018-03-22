const EthereumTx = require('ethereumjs-tx')
const privateKey = Buffer.from('82f7a41925b65cd45338989c3aa16967cd08632934eeef39dc302ac0ed40c026', 'hex')
 
const txParams = {
  nonce: '0x00',
  gasPrice: '0x09184e72a000', 
  gasLimit: '0x2710',
  to: '0x0000000000000000000000000000000000000000', 
  value: '0x00', 
  data: '0x7f7465737432000000000000000000000000000000000000000000000000000000600057',
  // EIP 155 chainId - mainnet: 1, ropsten: 3
  chainId: 4
}
 
const tx = new EthereumTx(txParams)
tx.sign(privateKey)
const serializedTx = tx.serialize()

console.log(serializedTx)