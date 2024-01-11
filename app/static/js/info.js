function confirmAndSubmit() {
    // Lấy giá trị từ các trường nhập liệu
    var customerID = document.getElementById('Customer_ID').value;
    var fullName = document.getElementById('FullName').value;
    var phoneNumber = document.getElementById('Phone_Number').value;
    var birthDay = document.getElementById('BirthDay').value;
    var address = document.getElementById('Address').value;

    // Kiểm tra đầy đủ 5 thuộc tính
    if (customerID === '' || fullName === '' || phoneNumber === '' || birthDay === '' || address === '') {
      alert('Vui lòng điền đầy đủ thông tin.');
      return;
    }

    // Hiển thị thông báo cho người dùng
    alert('Dữ liệu đã được gửi. Cảm ơn bạn!');

    // Gửi yêu cầu đến server (có thể sử dụng AJAX nếu cần)
    document.getElementById('myForm').submit();
  }