'use strict';

const lanIP = `${window.location.hostname}:5500`;
console.log(lanIP);
const socket = io(`http://192.168.168.169:5000`);

const showTemp = function (jsonObject) {
  console.log(jsonObject.data.waarde)
  document.querySelector('.js-temp').innerHTML = jsonObject.data.waarde
}

const showSound = function (jsonObject) {
  console.log(jsonObject.data_sound.waarde)
  document.querySelector('.js-decibel').innerHTML = jsonObject.data.waarde
}

const showTempSocket = function (jsonObject) {
  document.querySelector('.js-temp').innerHTML = jsonObject.data
}

const showSoundSocket = function (jsonObject) {
  document.querySelector('.js-decibel').innerHTML = jsonObject.data_sound
}

const getTemp = function(){
  const url = `http://192.168.168.169:5000/api/v1/temp`
  handleData(url, showTemp)
}

const getSound = function(){
  const url = `http://192.168.168.169:5000/api/v1/sound`
  handleData(url, showSound)
}

const listenToUI = function () {
};

const init = function () {
  listenToUI();
  listenToSocket();
  getTemp();
  getSound();
}

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });
  socket.on("B2F_refresh", function(jsonObject) {
    console.log(jsonObject)
    showTempSocket(jsonObject)
    showSoundSocket(jsonObject)
  })
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  init();
});




