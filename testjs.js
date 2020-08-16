var data = JSON.stringify({"did":"NJHYTFQAT0000029","gpsEndTime":"20170602120646","filterIfMissing":true,"pageSize":10,"pageType":0,"reversed":false,"startRowKey":"a","gpsStartTime":"20170602120649","token":"92d4e3fef54e432a01127200365d039f","vin":""});
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var xhr = new XMLHttpRequest();
xhr.withCredentials = true;

xhr.addEventListener("readystatechange", function() {
  if(this.readyState === 4) {
    console.log(this.responseText);
  }
});

xhr.open("POST", "http://openapi.uml-tech.com/farm/getHistoryCanInfo");
xhr.setRequestHeader("Content-Type", "application/json");

xhr.send(data);