'use strict';

// kijkt naar url website en is nodig om data te tonen zonder ethernet kabel
const lanIP = `${window.location.hostname}:5000`;
console.log(lanIP);
const socket = io(`http://${lanIP}`);


const showDataSocket = function (jsonObject) {
  document.querySelector('.js-temp').innerHTML = jsonObject.dataCelcius
  document.querySelector('.js-decibel').innerHTML = jsonObject.dataDecibel
}

const listenToUI = function () {
  console.log("listening to UI");
  const knop = document.getElementById("auto_control");
    knop.addEventListener("click", function () {
      console.log("clicked", this.checked);
      socket.emit("F2B_switch_fanmode",  this.checked );
    });
    const slider = document.getElementById("scrollbar");
    slider.addEventListener("change", function () {
      console.log("changed", this.value);
      socket.emit("F2B_switch_fanspeed",  this.value );
    });
};

const init = function () {
  listenToUI();
  listenToSocket();
}

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    socket.emit("B2F_refresh")
  });
  socket.on("B2F_refresh", function(jsonObject) {
    console.log("incoming data", jsonObject);
    showDataSocket(jsonObject);
    setTimeout(function(){
    socket.emit("B2F_refresh")
    }, 5000)
  })
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  init();
});




