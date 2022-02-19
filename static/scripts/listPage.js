// starts jquery actions when DOM is ready

$(document).ready(function () {
    var currentFilter
    $('.transactionHeader > *').click(function () {
    $('.transactionHeader > *').css("background-color", "#d0bce3")
    $(this).css("background-color", "#a783c9")
    if ($(this).attr('class') != currentFilter) {
      $('.transaction').remove()
    }
    if ($(this).hasClass('incomeButton')) {
      $('.transactions').append('<div class="transaction"><p>test1</p><\div>')
      currentFilter = $(this).attr('class')



      $.ajax({
        method: 'GET',
        url: 'http://104.59.55.38:5000/api/users/',
        contentType: 'application/json',
        data: JSON.stringify(""),
        // adds Place objects and data to HTML using append method
        success: function (data) {
        console.log(JSON.parse(data))
        console.log( Cookies('session') );
        //console.log(data)
        }});



    }
    if ($(this).hasClass('expenseButton')) {
      $('.transactions').append('<div class="transaction"><p>test2</p><\div>')
      currentFilter = $(this).attr('class')
    }
    if ($(this).hasClass('allButton')) {
      $('.transactions').append('<div class="transaction"><p>test3</p><\div>')
      currentFilter = $(this).attr('class')
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
