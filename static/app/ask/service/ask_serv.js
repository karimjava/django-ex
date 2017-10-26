require('angular')

angular
  .module('askApp.serv', [])
  .factory('askServ', ['$http', '$q', '$timeout', askServ]);

function askServ($http, $q, $timeout) {
    // debugger
  var serv = {};
  return serv;
}
