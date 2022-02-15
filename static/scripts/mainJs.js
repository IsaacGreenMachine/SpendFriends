// starts jquery actions when DOM is ready
$(document).ready(function () {
    // when search button is clicked
    $('.transactionHeader > *').click(function () {
    $('.transactionHeader > *').css("background-color", "#d0bce3")
    $(this).css("background-color", "#a783c9")
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
