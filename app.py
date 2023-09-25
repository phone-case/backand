from flask import *
from flask_cors import CORS
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
        sql = "SELECT name FROM test WHERE id = %s AND password = %s"
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
    title = request.form.get('title')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    print(title, password, name)

    if password != confirm_password:
        return "<a href='http://localhost:3000'>비밀번호가 일치하지 않습니다</a>"
    else :

        # MySQL 쿼리 실행
        # cursor = db.cursor()  # 이 부분을 주석 처리 또는 제거
        sql = "INSERT INTO test (id, password, name) VALUES (%s, %s, %s)"
        val = (title, password, name)
        cursor.execute(sql, val)
        db.commit()
        # cursor.close()  # 이 부분을 주석 처리 또는 제거

        return redirect("http://localhost:3000")

if __name__ == '__main__':
    app.run(debug=True)