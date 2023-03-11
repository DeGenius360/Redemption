

// initialize the socket variable
var socket = io();

//Add event listeners for category_list and category_count
socket.on('category_list', function(data) {
    // Update the HTML page with the received data
    var category_list = document.getElementById('category_list');
    console.log(category_list)
    category_list.innerHTML = '';

    data.forEach(function(category) {
        var category_item = document.createElement('li');
        category_item.textContent = category;
        category_list.appendChild(category_item);
    });
});
socket.on('category_count', function(data) {
    // Update the HTML page with the received data
    var category_count = document.getElementById('category_count');
    category_count.textContent = data;
});