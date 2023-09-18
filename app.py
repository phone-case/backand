from flask import Flask, request, render_template, redirect, url_for
import pymysql


app = Flask(__name__)

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

@app.route('/insert/')
def insert():
    inserts = '''
        <form action="/create/" method="POST">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><input type="password" name="password" placeholder="password"></p>
            <p><input type="confirm_password" name="confirm_password" placeholder="confirm_password"></p>
            <p><input type="text" name="name" placeholder="name"></p>
            <p><input type="text" name="role" placeholder="role"></p>
            <p><input type="submit" value="create"></p>
        </form>
    '''
    return inserts

@app.route('/create/', methods=['POST'])
def create():
    # 폼 데이터 가져오기
    title = request.form.get('title')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    role = request.form.get('role')
    print(title, password, name, role)

    if password != confirm_password:
        return "비밀번호가 일치하지 않습니다."
    else :

        # MySQL 쿼리 실행
        # cursor = db.cursor()  # 이 부분을 주석 처리 또는 제거
        sql = "INSERT INTO test (id, password, name, role) VALUES (%s, %s, %s, %s)"
        val = (title, password, name, role)
        cursor.execute(sql, val)
        db.commit()
        # cursor.close()  # 이 부분을 주석 처리 또는 제거

        return '<a href="/select/">보러가기</a>'

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