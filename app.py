from flask import *
from flask_cors import CORS
#from make_image import makeimage
from image_module import *
from base64 import b64encode
import pymysql



app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
db = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='hyotaedb', charset='utf8')
# 데이터에 접근
cursor = db.cursor()

def data():
    # SQL query 작성
    sql = "select * from test"

    # SQL query 실행
    cursor.execute(sql)

    # db 데이터 가져오기
    print(cursor.fetchall()) #모든 행 가져오기
    #cursor.fetchone() # 하나의 행만 가져오기
    #cursor.fetchmany(n) # n개의 데이터 가져오기 

    # 수정 사항 db에 저장
    db.commit()
    
    # Database 닫기
    db.close()

    return

#대현 이미지 반환
@app.route('/api/getImage/<title>', methods=['GET'])
def get__image(title):
    try:
        cursor.execute("SELECT data FROM images WHERE title = %s", (title,))
        image_data = cursor.fetchone()

        if image_data:
            image_binary = image_data[0]
            return send_file(io.BytesIO(image_binary), mimetype='image/png')  # 이미지 타입에 따라 변경
        else:
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 내부 서버 오류 (500)을 반환합니다

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/api/get_name', methods=['POST'])
def get_name():
    try:
        # 클라이언트에서 JSON 형식으로 전송한 데이터를 추출
        data = request.get_json()
        id = data.get('email')
        password = data.get('password')

        # 사용자를 찾는 쿼리 실행
        sql = "SELECT name from login WHERE id = %s AND password = %s"
        cursor.execute(sql, (id, password))
        result = cursor.fetchone()

        if result:
            name = result[0]
            print(name)
        else:
            name = None

        return jsonify({'name': name})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/create/', methods=['POST'])
def create():
    # 폼 데이터 가져오기
    id = request.form.get('id')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    print(id, password, name)

    if password != confirm_password:
        return "<a href='http://localhost:3000'>비밀번호가 일치하지 않습니다</a>"
    else :

        # MySQL 쿼리 실행
        # cursor = db.cursor()  # 이 부분을 주석 처리 또는 제거
        sql = "INSERT INTO login (id, password, name) VALUES (%s, %s, %s)"
        val = (id, password, name)
        cursor.execute(sql, val)
        db.commit()
        # cursor.close()  # 이 부분을 주석 처리 또는 제거

        return redirect("http://localhost:3000/login")

@app.route('/api/check_username/<username>', methods=['GET'])
def check_username(username):
    # 데이터베이스에서 입력받은 아이디가 이미 사용 중인지 확인
    sql = "SELECT id FROM login WHERE id = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    # 결과를 JSON 형태로 반환
    is_taken = result is not None
    return jsonify({'isTaken': is_taken})

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']  # 이미지 파일
        image_name = request.form.get('imageName')  # 이미지 이름
        imgae_text = request.form.get('imageText') 

        # 이미지 데이터를 MySQL에 저장하거나 다른 작업 수행
        if image and image_name:
            try:
                cursor.execute("INSERT INTO images (title, text, data) VALUES (%s, %s, %s)", (image_name, imgae_text, image.read()))
                db.commit()
                
                return 'Image uploaded successfully'
            except Exception as e:
                db.rollback()
                return 'Error uploading image'

    return 'No image provided for upload'

@app.route('/api/submit_text', methods=['POST'])
def submit_text():
    if request.method == 'POST':
        try:
            content = request.json.get('content')

            # 여기서 content 변수에 클라이언트로부터 받은 텍스트 데이터가 들어 있습니다.
            # 원하는 대로 이 데이터를 처리하고 응답을 생성합니다.
            print(content)
            eng_text = to_eng(content)
            print(eng_text)
            return jsonify(searchimage(eng_text))

        except Exception as e:
            return jsonify({'error': '텍스트 데이터 처리 중 오류가 발생했습니다.'})

@app.route('/api/create_text', methods=['POST'])
def create_text():
    if request.method == 'POST':
        try:
            content = request.json.get('content')

            # 여기서 content 변수에 클라이언트로부터 받은 텍스트 데이터가 들어 있습니다.
            # 원하는 대로 이 데이터를 처리하고 응답을 생성합니다.
            print(content)
            eng_text = to_eng(content)
            print(eng_text)
            return jsonify(create_image(eng_text))

        except Exception as e:
            return jsonify({'error': '텍스트 데이터 처리 중 오류가 발생했습니다.'})


@app.route('/api/check_imagename/<imagename>', methods=['GET'])
def check_imagename(imagename):
    # 데이터베이스에서 입력받은 이미지 이름이 이미 사용 중인지 확인
    sql = "SELECT title FROM images WHERE title = %s"
    cursor.execute(sql, (imagename,))
    result = cursor.fetchone()

    # 결과를 JSON 형태로 반환
    is_taken = result is not None
    return jsonify({'isTaken': is_taken})

@app.route('/api/get_image', methods=['POST'])
def get_image():
    try:
        # 클라이언트로부터 텍스트를 받습니다.
        data = request.get_json()
        text = data.get('imageName')

        # 텍스트를 기반으로 이미지 데이터를 데이터베이스에서 가져옵니다.
        cursor = db.cursor()
        
        cursor.execute("SELECT data, text FROM images WHERE title = %s", (text,))
        result = cursor.fetchone()

        if result:
            image_data = result[0]
            text_data = result[1]

            # Encode image_data to Base64
            encoded_image = b64encode(image_data).decode()

            # 이미지 데이터와 텍스트 데이터를 클라이언트로 전송
            response_data = {
                'image_data': encoded_image,
                'text_data': text_data
            }

            return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)})

    except Exception as e:
        print('Error:', str(e))

    return 'Image not found', 404

if __name__ == '__main__':
    app.run(debug=True)