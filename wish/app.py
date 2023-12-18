from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("./Book1_Quan.csv")

def process_input(B1, B2, B3):
    dia_diem_dict = {'Miền bắc': 1, 'Miền trung': 2, 'Miền nam': 3}
    C_list = []

    for i in range(len(df)):
        A1 = df['Học phí'][i]
        A2 = df['Đánh giá'][i]
        A3 = dia_diem_dict[df['Địa điểm'][i]]
        A4 = df['Điểm dự kiến'][i]
        A5 = df['Điểm chuẩn năm trước'][i]
        A6 = df['Chỉ tiêu'][i]

        C1 = 1 if B1 >= 2 * A1 else (0 if B1 <= A1 else (B1 - A1) / (2 * A1))
        C2 = A2
        C3 = 1 if abs(A3 - B3) <= 2 else 0
        C4 = max(0, min(1, (B2 - (A4 - abs(A5 - A4))) / (2 * abs(A5 - A4))))
        C5 = A6 / np.sqrt(np.sum(A6 ** 2))

        C = np.array([C1, C2, C3, C4, C5])
        C_list.append(C)

    C_matrix = np.array(C_list)
    C_matrix = C_matrix / np.sqrt(np.sum(C_matrix ** 2, axis=0))

    W = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
    C_matrix = C_matrix * W

    A_opt = np.max(C_matrix, axis=0)
    D = np.sqrt(np.sum((C_matrix - A_opt) ** 2, axis=1))

    min_index = np.argmin(D)
    return int(min_index + 1)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input_route():
    if request.method == 'POST':
        B1 = float(request.form['tuition'])
        B2 = float(request.form['examScore'])
        B3 = int(request.form['region'])

        result = process_input(B1, B2, B3)

        # Pass the required variables to the result route
        return redirect(url_for('result', result=result, B1=B1, B2=B2, B3=B3))


@app.route('/result/<result>')
def result(result):
    B1 = float(request.args.get('B1'))
    B2 = float(request.args.get('B2'))
    B3 = int(request.args.get('B3'))

    return render_template("result.html", result=result, B1=B1, B2=B2, B3=B3)

if __name__ == "__main__":
    app.run(debug=True)
