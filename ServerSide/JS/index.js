const express = require("express");
const bodyParser = require("body-parser");
const { port } = require("./config.js");

const abi = require("./abi.js");

const Web3 = require('web3');
//const { PartialWebhookMixin } = require("discord.js");
const { fstat } = require("fs");
const fs = require("fs");

const web3 = new Web3(new Web3.providers.HttpProvider(`http://192.168.1.2:8545`));

//const rpcURL = "https://public-node-api.klaytnapi.com/v1/cypress";
const rpcURL = "http://192.168.1.2:8545";
const networkID = "5777";
//const caver = new Caver(rpcURL);

const CONTRACT_ADDR = "YourETHEREUMContract";
let contract = null;


async function initContract() {
  //contract = await caver.kct.kip17.create(CONTRACT_ADDR);
  contract = new web3.eth.Contract(abi, CONTRACT_ADDR);
  console.log("initContract ok");

}
initContract();


console.log(
  "nft auth test",
  "not ready homepage"
);

const app = express();

app.use(bodyParser.json());

app.get("/", (request, response) => {
  return response.sendFile("index.html", { root: "." });
});


app.post("/api_wallet", async (request, response) => {
  console.log("api_wallet", request.body);
  const addr = request.body.addr;
  let ret;
  let ccount;

  let an = '';

  ret = await contract.methods.balanceOf(addr).call().then(data => {
    ccount = data;

    fs.readFile("./adaptName.txt", "utf8", (err, data) => {
      if (err) {
        console.error(err);
      } else {
        an = data;
        console.log(an);

      }
    });
  });

  const count = Number(ccount);
  console.log("count", count);

  //getSSID, PW
  let tssid;
  let ssid;
  let tpw;
  let pwpw;

  tssid = await contract.methods.getSSID().call().then(data => {
    ssid = data;
  })

  //atob
  const atob = (base64) => {
    return Buffer.from(base64, 'base64').toString('binary');
  };

  ssid = atob(ssid); // V

  tpw = await contract.methods.getPW().call().then(data => {
    pwpw = data;
  })

  pwpw = atob(pwpw); // V

  // python in JS section 프로파일 만드는부분

  console.log(ssid);
  console.log(pwpw);



  let mp;

  const spawn = require('child_process').spawn;


  // Auth Writing
  if (count > 0) {
    let trimmac;

    const trim = spawn('python', ['trimMAC.py']);

    trim.stdout.on('data', function (data) {
      console.log(data.toString());
      console.log('config trim done');
    });

    trim.stderr.on('data', function (data) {
      console.log(data.toString());
    });
    console.log('config trim done2');


    let sm;
    //call mac and enroll
    let stamac = '';
    fs.readFile("./STAmac.txt", "utf8", (err, data) => {
      if (err) {
        console.error(err);
      } else {
        stamac = data;
        console.log(stamac);

        const enroll = spawn('python', ['enrollMAC.py', stamac, ssid]);

        enroll.stdout.on('data', function (data) {
          console.log(data.toString());
          console.log('enroll done');
        });

        enroll.stderr.on('data', function (data) {
          console.log(data.toString());
        });
        console.log('enroll done2');

      }

    });

    const result = spawn('python', ['makeProfile.py', ssid, pwpw, an]);

    result.stdout.on('data', function (data) {
      console.log(data.toString());
      console.log('makeprofile')
    });

    result.stderr.on('data', function (data) {
      console.log(data.toString());
    });







    console.log('File Writing...');

    // const file = "isAuth.txt";
    // const data = '1';
    // fs.writeFile(file, data, (err) => console.log(err));
    fs.writeFile('./isAuth.txt', '1', encoding = "utf-8", function (err) {
      if (err) throw err;
      console.log("Written");
    });

  }


  return response.json({
    code: 200,
    message: "ok",
    count,
  });
});

app.listen(port, () =>
  console.log(`App listening at http://localhost:${port}`)
);
