function submitForm() {
    // Lấy giá trị từ combobox "Địa Chỉ"
    var region = document.getElementById('region').value;
  
    // Lấy giá trị từ các trường khác
    var examScore = document.getElementById('examScore').value;
    var major = document.getElementById('major').value;
    var tuition = document.getElementById('tuition').value;
  
    // Chuyển hướng sang trang mới và truyền các thông tin đăng ký
    window.location.href = 'result' + '?region=' + region + '&examScore=' + examScore + '&major=' + major + '&tuition=' + tuition;
  }
  