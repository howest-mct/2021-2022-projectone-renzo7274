'use strict';

// kijkt naar url website en is nodig om data te tonen zonder ethernet kabel
const lanIP = `${window.location.hostname}:5000`;
console.log(lanIP);
const socket = io(`http://${lanIP}`);

// const showTemp = function (jsonObject) {
//   console.log(jsonObject.data.waarde)
//   document.querySelector('.js-temp').innerHTML = jsonObject.data.waarde
// }

// const showSound = function (jsonObject) {
//   console.log(jsonObject.data_sound.waarde)
//   document.querySelector('.js-decibel').innerHTML = jsonObject.data.waarde
// }

const showTempSocket = function (jsonObject) {
  document.querySelector('.js-temp').innerHTML = jsonObject.dataCelcius
  document.querySelector('.js-decibel').innerHTML = jsonObject.dataDecibel
}

// const showSoundSocket = function (jsonObject) {
//   document.querySelector('.js-decibel').innerHTML = jsonObject
// }

// const getTemp = function(){
//   const url = `http://192.168.168.169:5000/api/v1/temp`
//   handleData(url, showTemp)
// }

// const getSound = function(){
//   const url = `http://192.168.168.169:5000/api/v1/sound`
//   handleData(url, showSound)
// }

const listenToUI = function () {
  console.log("listening to UI");
  const knop = document.getElementById("auto_control");
    knop.addEventListener("click", function () {
      console.log("clicked", this.checked);
      // const id = this.dataset.idlamp;
      // let nieuweStatus;
      // if (this.dataset.statuslamp == 0) {
      //   nieuweStatus = 1;
      // } else {
      //   nieuweStatus = 0;
      // }
      // //const statusOmgekeerd = !status;
      // clearClassList(document.querySelector(`.js-room[data-idlamp="${id}"]`));
      // document.querySelector(`.js-room[data-idlamp="${id}"]`).classList.add("c-room--wait");
      socket.emit("F2B_switch_fanmode",  this.checked );
    });
    const slider = document.getElementById("scrollbar");
    slider.addEventListener("change", function () {
      console.log("changed", this.value);
      // const id = this.dataset.idlamp;
      // let nieuweStatus;
      // if (this.dataset.statuslamp == 0) {
      //   nieuweStatus = 1;
      // } else {
      //   nieuweStatus = 0;
      // }
      // //const statusOmgekeerd = !status;
      // clearClassList(document.querySelector(`.js-room[data-idlamp="${id}"]`));
      // document.querySelector(`.js-room[data-idlamp="${id}"]`).classList.add("c-room--wait");
      socket.emit("F2B_switch_fanspeed",  this.value );
    });
};

const init = function () {
  listenToUI();
  listenToSocket();
  // getTemp();
  // getSound();
}

const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket webserver");
    socket.emit("B2F_refresh")
  });
//wordt maar 1 keer uitgevoerd
  socket.on("B2F_refresh", function(jsonObject) {
    console.log("test");
    console.log("incoming data", jsonObject);
    // var data = JSON.parse(jsonObject);
    // console.log(data)
    showTempSocket(jsonObject);
    setTimeout(function(){
    socket.emit("B2F_refresh")
    }, 5000)
    // showSoundSocket(jsonObject)
  })
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  init();
});




