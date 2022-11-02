// const rpcURL = "https://public-node-api.klaytnapi.com/v1/cypress";
// const networkID = "8217";
// const rpcURL = "https://api.baobab.klaytn.net:8651/";
// const networkID = "1001";
const abi = require("./abi.js");
const rpcURL = "https://ropsten.infura.io/v3/YOURAPI";
const networkID = "4";

const Caver = require("caver-js");
const caver = new Caver(rpcURL);

const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider(`https://rinkeby.infura.io/v3/YOURAPI`));

//const CONTRACT_ABI = require("./abi/MyGame.json");
//const CONTRACT_ABI = require("./abi/mycontract.json");
//const contract_addr = CONTRACT_ABI.networks[networkID].address;
const contract_addr = "YOURETHCONTRACTADD";
//const contract = new caver.klay.Contract(CONTRACT_ABI.abi, contract_addr);
const contract = new web3.eth.Contract(abi, contract_addr);

console.log("contract_addr", contract_addr);


let ret;
let busy = false;
let call_count = 0;
let last_block_id = 11196532;
let depth = 5;

async function read_event() {
  if (busy) {
    console.log("read_event busy");
    return;
  }

  busy = true;
  call_count++;

  try {
    //const bn = await caver.klay.getBlockNumber();
    const bn = await web3.eth.getBlockNumber();

    const fromBlock = last_block_id + 1;
    const toBlock = last_block_id + depth;
    if (toBlock > bn) {
      console.log("bn not yet", toBlock - bn);
      busy = false;
      return;
    }
//ret = await contract.methods.balanceOf(wallet_addr).call().then(data => {
    //ret = await contract.getPastEvents("play_log", {
    ret = await contract.getPastEvents("Transfer", {  
      filter: {},
      fromBlock,
      toBlock,
    });

    console.log("nft_log ret", fromBlock, ret.length);
    for (let i = 0; i < ret.length; i++) {
      let e = ret[i];
      console.log(i, e.blockNumber, e.returnValues);
    }

    last_block_id = toBlock;
  } catch (e) {
    console.log("read_event fail", e);
  }

  busy = false;
}

setInterval(read_event, 1000 * 5);
