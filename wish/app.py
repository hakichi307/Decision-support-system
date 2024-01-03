import numpy as np
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def process_input(B1, B2, B3, B4):
    df = pd.read_csv("./Data_NguyenVong.csv")
    df = df.loc[df["Chuyên ngành"] == B4]

    # Scale chỉ tiêu
    from sklearn import preprocessing

    Chitieu = df["Chỉ tiêu"].values.reshape(-1, 1)  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    df.loc[:, "Chỉ tiêu scaler"] = min_max_scaler.fit_transform(Chitieu)

    dia_diem_dict = {"Miền bắc": 1, "Miền trung": 2, "Miền nam": 3}
    C_list = []
    C2D = [[] for i in range(5)]  # Thêm dataframe mảng 2 chiều
    for i in range(len(df)):
        A1 = df["Học phí"].iloc[i]
        A2 = df["Đánh giá"].iloc[i]
        A3 = dia_diem_dict[df["Địa điểm"].iloc[i]]
        A4 = df["Điểm dự kiến"].iloc[i]
        A5 = df["Điểm chuẩn năm trước"].iloc[i]
        A6 = df["Chỉ tiêu scaler"].iloc[i]

        # Sự phù hợp về học phí
        if B1 >= 2 * A1:
            C1 = 1
        elif B1 <= A1:
            C1 = 0
        else:
            C1 = 1 - (B1 - A1) / A1
        # Đánh giá trường
        C2 = A2  # A2 = 0 :  đánh giá trường trung bình
        # A2 = 0.5 : đánh giá trường tốt
        # A2 = 1 :  đánh giá trường rất tốt
        # Sự phù hợp về địa điểm
        if abs(A3 - B3) == 0:
            C3 = 1
        elif abs(A3 - B3) == 1:
            C3 = 0.5
        else:
            C3 = 0
        # Sự phù hợp về điểm thi
        if B2 >= (A4 - abs(A5 - A4)):
            C4 = 1
        elif B2 <= (A4 - abs(A5 - A4)):
            C4 = 0
        else:
            C4 = (B2 - (A4 - abs(A5 - A4))) / (2 * abs(A5 - A4))
            C4 = max(0, min(1, C4))  # Giới hạn C4 trong khoảng [0, 1]
        # Sự phù hợp về chỉ tiêu
        C5 = A6
        # Tạo một mảng để lưu trữ các giá trị của bảng quyết định
        C = np.array([C1, C2, C3, C4, C5])
        # Tao dataframe
        C2D[0].append(C1)
        C2D[1].append(C2)
        C2D[2].append(C3)
        C2D[3].append(C4)
        C2D[4].append(C5)
        # Thêm mảng vào danh sách
        C_list.append(C)

    df["C1"] = C2D[0]
    df["C2"] = C2D[1]
    df["C3"] = C2D[2]
    df["C4"] = C2D[3]
    df["C5"] = C2D[4]

    # Chuyển đổi danh sách thành một ma trận
    C_matrix = np.array(C_list)
    # Chuẩn hóa ma trận theo cột
    C_matrix = C_matrix / np.sqrt(np.sum(C_matrix**2, axis=0))

    W = np.array([0.2, 0.2, 0.2, 0.2, 0.2])  # Trọng số
    # Nhân ma trận với trọng số
    C_matrix = C_matrix * W

    A_opt = np.max(C_matrix, axis=0)  # Phương án tối ưu
    A_worst = np.min(C_matrix, axis=0)  # Phương án tồi tệ
    # Tính khoảng cách từ mỗi phương án đến phương án tối ưu
    D_opt = np.sqrt(np.sum((C_matrix - A_opt) ** 2, axis=1))
    D_worst = np.sqrt(np.sum((C_matrix - A_worst) ** 2, axis=1))
    # Tính độ tương tự với phương án tối ưu
    S = D_worst / (D_opt + D_worst)  # Độ tương tự
    # best_index = np.argmax(S)
    top_5_indices = np.argsort(S)[::-1][:5]
    # Tạo DataFrame cho top 5 phương án tốt nhất
    top_5_df = df.iloc[top_5_indices]
    return top_5_df.to_json(orient="records")  # type: ignore


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/index")
def index():
    df = pd.read_csv("./Data_NguyenVong.csv")
    cn = df["Chuyên ngành"].unique()
    return render_template("index.html", cn=cn)


@app.route("/process_input", methods=["POST"])  # type: ignore
def process_input_route():
    if request.method == "POST":
        B1 = float(request.form["tuition"])
        B2 = float(request.form["examScore"])
        B3 = int(request.form["region"])
        B4 = request.form["academicMajor"]
        result = process_input(B1, B2, B3, B4)

        # Pass the required variables to the result route
        return redirect(url_for("result", result=result, B1=B1, B2=B2, B3=B3))


@app.route("/result/<result>")
def result(result):
    B1 = float(request.args.get("B1"))  # type: ignore
    B2 = float(request.args.get("B2"))  # type: ignore
    B3 = int(request.args.get("B3"))  # type: ignore
    import json

    result = json.loads(result)
    print("result", result)
    return render_template("result.html", result=result, B1=B1, B2=B2, B3=B3)


if __name__ == "__main__":
    app.run(debug=True)

# Console chạy chương trình
# python .\wish\app.py runserver
