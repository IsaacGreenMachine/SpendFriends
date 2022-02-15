const request = require('request');

request.post({
    headers: {'content-type' : 'application/json'},
    url:     'http://104.59.55.38:5000/api/users/',
    body:    JSON.stringify({'username': 'newUser1003', "password": "u1003", "settings":""})
  },
  function(error, response, body){
    console.log(body);
  }
  );
