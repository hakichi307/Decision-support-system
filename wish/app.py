# Import class 'Flask' và hàm 'render_template' từ module 'flask'
from flask import Flask, render_template
import json
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    data = [{
        "uni_name": "Truong A",
        "price": "Phu hop",
        "locate": "Phu8 hop",
        "clgt": "phu hop",
        "rating": "tot" 
    }, {
        "uni_name": "Truong A",
        "price": "Phu hop",
        "locate": "Phu8 hop",
        "clgt": "phu hop",
        "rating": "tot" 
    }]
    return render_template("result.html", data=json.dumps(data))

@app.route('/about')
def about():
    return 'Flask Design by team member 5'
# Kiểm tra nếu đây là file chính được chạy
if __name__ == "__main__":
    # Chạy ứng dụng Flask với chế độ debug được bật
    app.run(debug=True)

#python .\wish\app.py runserver