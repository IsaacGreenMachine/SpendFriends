const request = require('request');

request.post({
    headers: {'content-type' : 'application/json'},
    url:     'http://104.59.55.38:5000/api/users/b43abd9f-22e1-48bc-aacb-b3117457458d/lists/d2ebfe2d-c04f-4b9f-976a-480c271575ac/expenses',
    body:    JSON.stringify({"expense_amount": 31.21, "expense_name":"defexpensive", "expense_description":"expensive expense"})
  },
  function(error, response, body){
    console.log(body);
  }
  );
