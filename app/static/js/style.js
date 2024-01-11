document.addEventListener('DOMContentLoaded', function () {
    var body = document.body;
    var darkModeButton = document.querySelector('.dark-mode-button');

    function toggleDarkMode(event) {
        event.preventDefault();
        body.classList.toggle('dark-mode');
        var isDarkMode = body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode);


        var tableRows = document.querySelectorAll('.table tr');
        tableRows.forEach(function (row) {
            row.classList.toggle('dark-mode');
        });


        var cartTableRows = document.querySelectorAll('.cart-table tr');
        cartTableRows.forEach(function (row) {
            row.classList.toggle('dark-mode');
        });
    }

    darkModeButton.addEventListener('click', toggleDarkMode);

    var isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        body.classList.add('dark-mode');
    }

    window.addEventListener('pageshow', function (event) {
        var isDarkMode = localStorage.getItem('darkMode') === 'true';
        if (isDarkMode) {
            body.classList.add('dark-mode');
        } else {
            body.classList.remove('dark-mode');
        }
    });
});

function handleViewDetailClick(name, image, info, overlayId) {
    var detailOverlay = document.getElementById(overlayId);
    detailOverlay.style.display = 'block';

    console.log(name, image, info);

    detailOverlay.querySelector('.detailName').textContent = name;
    detailOverlay.querySelector('.detailImage').src = image;
    detailOverlay.querySelector('.detailInfo').textContent = info;
}
function closeDetailOverlay(button) {
    var overlay = button.closest('.overlay');

    if (overlay) {
        overlay.style.display = 'none';
    }
}


function addToCart(id, name, price){
    fetch("/api/cart",{
        method: "post",
        body: JSON.stringify({
            "Book_ID": id,
            "BookName": name,
            "Price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;

    })
}
function addToCart1(id, name, price){
    fetch("/api/cart",{
        method: "post",
        body: JSON.stringify({
            "Book_ID": id,
            "BookName": name,
            "Price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;

        window.location.href = '/cart';
    })
}

function uppDateCart(Book_ID, obj) {
    obj.disable = true;
    fetch(`/api/cart/${Book_ID}`,{
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        obj.disable = false;
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName('cart-amount');
        for (let c of amounts)
            c.innerText = data.total_amount.toLocaleString("en");
    })
}
function deleteCart(Book_ID, obj){
    if (confirm("Bạn chắc chắn xóa?") === true){
        obj.disable = true;
        fetch(`/api/cart/${Book_ID}`,{
            method: "delete",
            body: JSON.stringify({
                "quantity": obj.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            obj.disable = false;
            let carts = document.getElementsByClassName('cart-counter');
            for (let c of carts)
                c.innerText = data.total_quantity;

            let amounts = document.getElementsByClassName('cart-amount');
            for (let c of amounts)
                c.innerText = data.total_amount.toLocaleString("en");

            let t = document.getElementById(`product${Book_ID}`);
            t.style.display = "none";

            })
    }
}

