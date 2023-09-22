from flask import *
from flask_cors import CORS
import pymysql


app = Flask(__name__)
CORS(app, resources={r"/create/*": {"origins": "http://127.0.0.1:3000"}})
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

@app.route('/select/')
def select():
    # SQL query 작성
    sql = "SELECT * FROM test"

    # SQL query 실행
    cursor.execute(sql)

    name = cursor.fetchall()

    # Database 닫기 (주석 처리 또는 제거)
    # db.close()

    return render_template('select.html', name=name)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # MySQL에서 데이터를 가져오는 쿼리 실행
        sql = "SELECT * FROM test"
        cursor.execute(sql)
        results = cursor.fetchall()

        # 데이터를 JSON 형식으로 변환
        data = []
        for row in results:
            item = {
                'id': row[0],
                'password': row[1],
                'name': row[2],
                'role': row[3]
            }
            data.append(item)

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/get_name', methods=['GET'])
def get_name():
    try:
        # 아이디와 비밀번호를 GET 요청에서 가져옴
        id = request.args.get('id')
        password = request.args.get('password')

        # 사용자를 찾는 쿼리 실행 (예시)
        sql = "SELECT name FROM test WHERE id = %s AND password = %s"
        cursor.execute(sql, (id, password))
        result = cursor.fetchone()

        if result:
            name = result[0]
        else:
            name = None

        return jsonify({'name': name})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/create/', methods=['POST'])
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

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        # 폼 데이터 가져오기
        title = request.form.get('title')
        password = request.form.get('password')
        name = request.form.get('name')
        role = request.form.get('role')
        print(title, password, name, role)

        # MySQL 쿼리 실행 (id를 기준으로 업데이트)
        sql = "UPDATE test SET password=%s, name=%s, role=%s WHERE id=%s"
        val = (password, name, role, title)
        cursor.execute(sql, val)
        db.commit()

        return redirect(url_for('select'))  # 업데이트 후 다시 목록 페이지로 리다이렉트



    sql = "SELECT * FROM test WHERE id = %s"
    cursor.execute(sql, (id,))
    data = cursor.fetchone()

    return render_template('update.html', data=data)

@app.route('/delete/', methods=['POST'])
def delete():
    # POST 요청에서 title 값을 가져옵니다.
    title = request.form.get('title')

    # 삭제를 수행하는 SQL 쿼리
    sql = "DELETE FROM test WHERE id = %s"  # 예를 들어, id 대신 title을 사용
    cursor.execute(sql, (title,))
    db.commit()

    return redirect(url_for('select'))  # 삭제 후 다시 목록 페이지로 리다이렉트




@app.route('/myHobby/')
def myHobby():
    return render_template('myHobby.html')



if __name__ == '__main__':
    app.run(debug=True)