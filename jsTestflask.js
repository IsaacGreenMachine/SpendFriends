const request = require('request');

request.post({
    headers: {'content-type' : 'application/json'},
    url:     'http://104.59.55.38:5000/api/users/a224a042-cedc-4c29-ae07-17897cb1cdf3/lists/5453e73c-7b7d-497f-bfbc-887e53fa9ff7/incomes',
    body:    JSON.stringify({"income_amount": 20.35, "income_name": "inc2", "income_description":"second one"})
  },
  function(error, response, body){
    console.log(body);
  }
  );
