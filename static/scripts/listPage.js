// starts jquery actions when DOM is ready

$(document).ready(function () {
    var currentFilter
    console.log(document.cookie)
    console.log(typeof document.cookie)
    cookieObj = {}
    cookielist = document.cookie.split('; ')
    cookielist.forEach(function (element) {
      cookieObj[element.split('=')[0]] = element.split('=')[1]
    });
    console.log(cookieObj)

    $('.transactionHeader > *').click(function () {
    $('.transactionHeader > *').css("background-color", "#d0bce3")
    $(this).css("background-color", "#a783c9")
    if ($(this).attr('class') != currentFilter) {
      $('.transaction').remove()
    }
    if ($(this).hasClass('incomeButton')) {
      currentFilter = $(this).attr('class')
      $.ajax({
        method: 'GET',
        url: 'http://104.59.55.38:5000/api/users/' + cookieObj.user_id + "/lists/d2ebfe2d-c04f-4b9f-976a-480c271575ac/incomes",
        contentType: 'application/json',
        success: function (data) {
        incomesList = JSON.parse(JSON.parse(data).incomes)
        console.log(incomesList)
        incomesList.forEach(function (element) {
          $('.transactions').append('<div class="transaction"><p>' + element[2] + ' : ' + element[1] + '<\p>' + element[3] + '</p><\div>')
        });
        }});
    }
    if ($(this).hasClass('expenseButton')) {
      currentFilter = $(this).attr('class')
      $.ajax({
        method: 'GET',
        url: 'http://104.59.55.38:5000/api/users/' + cookieObj.user_id + "/lists/d2ebfe2d-c04f-4b9f-976a-480c271575ac/expenses",
        contentType: 'application/json',
        success: function (data) {
        incomesList = JSON.parse(JSON.parse(data).expenses)
        console.log(incomesList)
        incomesList.forEach(function (element) {
          $('.transactions').append('<div class="transaction"><p>' + element[2] + ' : ' + element[1] + '<\p>' + element[3] + '</p><\div>')
        });
        }});
    }
    if ($(this).hasClass('allButton')) {
      currentFilter = $(this).attr('class')
      $.ajax({
        method: 'GET',
        url: 'http://104.59.55.38:5000/api/users/' + cookieObj.user_id + "/lists/d2ebfe2d-c04f-4b9f-976a-480c271575ac/incomes",
        contentType: 'application/json',
        success: function (data) {
        incomesList = JSON.parse(JSON.parse(data).incomes)
        console.log(incomesList)
        incomesList.forEach(function (element) {
          $('.transactions').append('<div class="transaction"><p>' + element[2] + ' : ' + element[1] + '<\p>' + element[3] + '</p><\div>')
        });
        }});
      $.ajax({
        method: 'GET',
        url: 'http://104.59.55.38:5000/api/users/' + cookieObj.user_id + "/lists/d2ebfe2d-c04f-4b9f-976a-480c271575ac/expenses",
        contentType: 'application/json',
        success: function (data) {
        incomesList = JSON.parse(JSON.parse(data).expenses)
        console.log(incomesList)
        incomesList.forEach(function (element) {
          $('.transactions').append('<div class="transaction"><p>' + element[2] + ' : ' + element[1] + '<\p>' + element[3] + '</p><\div>')
        });
        }});
    }
    });

    $('.addExpense').click(function () {
    $('.addExpensePopUp').css("visibility", "visible")
    $('.addIncomePopUp').css("visibility", "hidden")
  });

    $('.addIncome').click(function () {
      $('.addExpensePopUp').css("visibility", "hidden")
      $('.addIncomePopUp').css("visibility", "visible")
      });

    $('.x').click(function () {
    $('.addExpensePopUp').css("visibility", "hidden")
    $('.addIncomePopUp').css("visibility", "hidden")
    });

  });
