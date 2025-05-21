# WebAppWebCam  


이 프로그램은 기존의 https://github.com/dlalsdyd01/WebApp를 확장하여 만든 프로그램이다.  

![image](https://github.com/user-attachments/assets/272e4988-de82-401d-8fee-3a8993cdf13a)  
웹브라우저에서 파일을 선택해서 서버로 전송후 이미지 파일을 uploads 폴더에 저장, addbook.txt 파일에 이미지 파일 이름을 저장하게 한다.  

  
# 주요확장 내용  
index.html
```
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Address Book</title>
    <!-- CSS 파일 연결 -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Address Book</h1>
    <form action="/add" method="post" enctype="multipart/form-data">
        <label for="name" class="label-name">Name:</label>
        <input type="text" id="name" name="pyname" required>
        <br><br>
        <label for="phone">Phone:</label>
        <input type="text" id="phone" name="pyphone" required>
        <br><br>
        <label for="birthday">Birthday:</label>
        <input type="date" id="birthday" name="pybirthday" required>
        <br><br>
        <label for="photo">Photo:</label>
        <input type="file" id="photo" name="pyphoto" accept="image/*" onchange="previewPhoto(event)">
        <br><br>
        <img id="photoPreview" src="#" alt="Photo Preview" style="display:none; max-width:200px;"/>
        <br><br>
        <button type="submit">Add Contact</button>        
    </form>
        <script>
        function previewPhoto(event) {
            const input = event.target;
            const preview = document.getElementById('photoPreview');
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(input.files[0]);
            } else {
                preview.src = '#';
                preview.style.display = 'none';
            }
        }
    </script>
</body>
</html>
```
# 수정내용
이 코드는 HTML 폼(form) 태그의 속성을 설정하는 부분입니다.
action="/add"
폼을 제출(submit)하면 데이터를 /add 경로(Flask의 /add 라우트)로 보냅니다.
method="post"
데이터를 서버로 보낼 때 HTTP POST 방식(숨겨진 방식, URL에 데이터가 노출되지 않음)으로 전송합니다.

enctype="multipart/form-data"
폼에 파일 업로드(input type="file")가 있을 때 반드시 필요한 속성입니다.
이 속성이 있어야 파일 데이터가 서버로 전송됩니다.
(없으면 request.files에서 파일을 받을 수 없습니다.)

폼 내부에 생일 입력 받는 곳과 파일 선택하는 곳이 추가 됨.


```
  @app.route('/add', methods=['POST'])
def add_contact():
 name = request.form['pyname']
 phone = request.form['pyphone']
 birthday = request.form['pybirthday']
 photo = request.files.get('pyphoto')

 photo_name_to_save = ''
 if photo and getattr(photo, 'filename', ''):
     photo_filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
     photo.save(photo_filename)
     photo_name_to_save = photo.filename

 # Save to addbook.txt in CSV format (사진 파일명도 저장)
 with open('addbook.txt', 'a', newline='', encoding='utf-8') as file:
     writer = csv.writer(file)
     writer.writerow([name, phone, birthday, photo_name_to_save])

 return redirect('/')
```

실행 화면  
![image](https://github.com/user-attachments/assets/bf14da67-5c7c-4ce7-8de4-45d15e3f288b)  

스크린샷이 upload 파일에 저장됌.
![image](https://github.com/user-attachments/assets/0d2466ee-81cc-4572-a34a-1d505191add7)

