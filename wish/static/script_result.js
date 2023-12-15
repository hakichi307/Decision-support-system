function goBack() {
      window.location.href = 'index';
    }
    // Hàm để thêm dòng vào bảng kết quả
    function addRowToTable(name, tuitionFit, locationFit, quotaFit, rating) {
      var table = document.getElementById('resultTable');
      var row = table.insertRow(-1);
    
      var cell1 = row.insertCell(0);
      var cell2 = row.insertCell(1);
      var cell3 = row.insertCell(2);
      var cell4 = row.insertCell(3);
      var cell5 = row.insertCell(4);
    
      cell1.innerHTML = name;
      cell2.innerHTML = tuitionFit;
      cell3.innerHTML = locationFit;
      cell4.innerHTML = quotaFit;
      cell5.innerHTML = rating;
    }
    
    // Xử lý thông tin đăng ký từ URL và thêm dòng vào bảng kết quả
    var urlParams = new URLSearchParams(window.location.search);
    var region = urlParams.get('region');
    var examScore = urlParams.get('examScore');
    var major = urlParams.get('major');
    var tuition = urlParams.get('tuition');
    
    // Bạn cần thay thế nó với dữ liệu thực tế từ cơ sở dữ liệu hoặc nguồn dữ liệu khác.
    addRowToTable('{{ data[0]["uni_name"]}}', '{{ data[0]["price"]}}', '{{ data[0]["locate"]}}', '{{ data[0]["clgt"]}}', '{{ data[0]["rating"]}}');
    addRowToTable('{{ data[1]["uni_name"]}}', '{{ data[1]["price"]}}', '{{ data[1]["locate"]}}', '{{ data[1]["clgt"]}}', '{{ data[1]["rating"]}}');
    addRowToTable('Trường B', 'Phù hợp', 'Không phù hợp', 'Phù hợp', 'Rất tốt');
    // console.log({{ data }}) 
