from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

# 설정: 업로드된 파일 저장 폴더
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['pyname']
    phone = request.form['pyphone']
    birthday = request.form['pybirthday']
    photo = request.files['pyphoto']

    # 사진 저장 처리
    if photo:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(photo_path)

    # Save to addbook.txt in CSV format
    with open('addbook.txt', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, phone, birthday, photo.filename])  # 사진 파일명도 저장

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)