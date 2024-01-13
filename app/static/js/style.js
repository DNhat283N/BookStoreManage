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
function updateCartCounter(data) {
     let totalQuantity = data.total_quantity
    let cartCounters = document.getElementsByClassName('cart-counter');
        for (let counter of cartCounters) {
            counter.innerText = totalQuantity;
        }

}

// Hàm thêm sách vào giỏ hàng
function addToCart(bookId, bookName, price) {
    var quantity = 1;
    $.ajax({
        url: '/api/cart',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "Book_ID": bookId,
            "BookName": bookName,
            "Price": price,
            "quantity": quantity
        }),
        success: function (response) {
            if (response.success) {
                console.log(response.message);// Log thành công
                updateCartCounter(response.cart);
            } else {
                alert(response.error);  // Hiển thị thông báo lỗi
            }
        },
        error: function (xhr, status, error) {
            // Xử lý lỗi AJAX
            alert("Không đủ hàng cung cấp.");
        }
    });
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
function pay(){
    if (confirm("Bạn chắc chắc thanh toán?") ===true){
        fetch("/api/pay",{
            method:'post'
        }).then(res =>res.json()).then(data =>{
            console.log(data);
            if (data.status === 200)
                location.reload();
            else
                alert(data.err_msg)
        })
    }

}