'use strict';

const lanIP = `${window.location.hostname}:5000`;
console.log(lanIP);
const socket = io(`http://${lanIP}`);

const showTemp = function (jsonObject) {
  console.log(jsonObject.data.waarde)
  document.querySelector('.js-temp').innerHTML = jsonObject.data.waarde
}

const showTempSocket = function (jsonObject) {
  document.querySelector('.js-temp').innerHTML = jsonObject.data
}

const getTemp = function(){
  const url = `http://192.168.168.169:5000/api/v1/temp`
  handleData(url, showTemp)
}

const listenToUI = function () {
};

const init = function () {
  console.log('hehe');
  listenToUI();
  listenToSocket();
  getTemp();
}

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });
  socket.on("B2F_refresh", function(jsonObject) {
    console.log(jsonObject)
    showTempSocket(jsonObject)
  })
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  init();
});




