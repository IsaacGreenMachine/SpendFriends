$(document).ready(function () {
    // creating a list of useful cookie info {password, user_id, user_name}
    cookieObj = {}
    cookielist = document.cookie.split('; ')
    cookielist.forEach(function (element) {
      cookieObj[element.split('=')[0]] = element.split('=')[1]
    console.log(cookieObj)
    });

    // display lists
    $.ajax({
        method: 'GET',
        url: 'http://104.59.55.38:5000/api/users/' + cookieObj.user_id + '/lists/',
        contentType: 'application/json',
        success: function (data) {
        console.log(JSON.parse(JSON.parse(data)[0].lists))
        lists = JSON.parse(JSON.parse(data)[0].lists)
        lists.forEach(function (element) {
          $('.listsContainer').append('<div class="listItem"><p>' + element + '</p><\div>')
        });
        }});

    $('.addList').click(function () {
        if ($('.newListInput').css("visibility") == "hidden") {
            $('.newListInput').css("visibility", "visible")
        }
        else {
            $('.newListInput').css("visibility", "hidden")
        }
    });
});
