import mysql.connector, secrets
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# 連接 MariaDB 資料庫
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mydatabase'
    )
    return conn

@app.route('/')
def index0():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search_id', methods=['POST'])
def search_id():
    student = session['student']
    cid = request.form.get('search_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM course WHERE Cid = %s", (cid,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return render_template('search_id.html', course=result, student=student, cid=cid)
    return render_template('search_id.html', course='', student=student, cid=cid)

@app.route('/search_name', methods=['POST'])
def search_name():
    student = session['student']
    name = request.form.get('search_name')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    name = f'%{name}%'
    cursor.execute("SELECT * FROM course WHERE Name LIKE %s", (name,))
    name = request.form.get('search_name')
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return render_template('search_name.html', course=result, student=student, name=name)
    return render_template('search_name.html', course=result, student=student, name=name)
    
@app.route('/add_course' , methods=['POST'])
def add_course():
    student = session['student']
    cid = request.form.get('cid')

    # connect the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # check cid is availble or not
    cursor.execute("SELECT * FROM course WHERE Cid=%s" %(cid))
    course = cursor.fetchone()
    if(not course) : # invalid cid
        cursor.close()
        conn.close()
        return render_template('result.html' , result='加選失敗，請輸入正確的課程代碼' , student=student, timetable=session['timetable'])
    
    # check this course is already select or not
    cursor.execute("SELECT * FROM enrollment WHERE Sid=\'%s\' AND Cid=%s" %(session['student']['Sid'] , cid))
    result = cursor.fetchone()
    if(result) : # already have this course in time table
        cursor.close()
        conn.close()
        return render_template('result.html' , result='加選失敗，您已經加選此課程' , student=student, timetable=session['timetable'])
    
    # check studen't credit is full or not
    cursor.execute('SELECT * FROM student WHERE Sid=\'%s\'' %(session['student']['Sid']))
    student_detail = cursor.fetchone()
    if(int(student_detail['Credit']) >= 25) : 
        cursor.close()
        conn.close()
        return render_template('result.html' , result='加選失敗，您已達到學分上限' , student=student, timetable=session['timetable'])

    # check course's capacity is full or not
    if(int(course['Capacity']) == int(course['Members'])) : 
        cursor.close()
        conn.close()
        return render_template('result.html' , result='加選失敗，這門課人數已滿' , student=student, timetable=session['timetable'])
    
    # 判斷衝堂
    if(session['student']['Credit'] != 0):
        cursor.execute("SELECT * FROM enrollment WHERE Sid=\'%s\'" %(session['student']['Sid']))
        all_class = cursor.fetchall()
        print(all_class)

        for i in all_class : 
            print(i['Cid'])
            cursor.execute("SELECT * FROM course WHERE Cid=\'%s\'" %(i['Cid']))
            class_from_table = cursor.fetchone()

            table_class_time = class_from_table['Time_id'].split('-')
            course_time = course['Time_id'].split('-')
            
            # (course start time is in the range of table_class_time) or (course end time is in the range of table_class_time) or (table_class_time in in the range of course time)
            if( ( int(course_time[0])>=int(table_class_time[0]) and int(course_time[0])<=int(table_class_time[1]) ) or ( int(course_time[1])>=int(table_class_time[0]) and int(course_time[1])<=int(table_class_time[1]) ) or ( int(table_class_time[0])>=int(course_time[0]) and int(table_class_time[0])<=int(course_time[1]) ) or ( int(table_class_time[1])>=int(course_time[0]) and int(table_class_time[1])<=int(course_time[1]) )) : # not done here
                cursor.close()
                conn.close()
                return render_template('result.html' , result='加選失敗，課程衝堂' , student=student, timetable=session['timetable'])
    # end of checking


    cursor = conn.cursor(dictionary=True)
    # add to time table
    cursor.execute("INSERT INTO enrollment VALUES (\'%s\' , %s)" %(session['student']['Sid'] , cid))

    # update student's credit
    new_credit = int(student_detail['Credit']) + int(course['Credit'])
    cursor.execute("UPDATE student SET Credit=%d WHERE Sid=\'%s\'" %(new_credit , session['student']['Sid']))
    session['student']['Credit'] = new_credit

    # update course members
    new_members = int(course['Members']) + 1
    cursor.execute("UPDATE course SET Members = %s WHERE Cid = %s", (new_members, cid))

    conn.commit()

    cursor.close()
    conn.close()
    return render_template('result.html', result='加選成功' , student=student, timetable=session['timetable'])

@app.route('/drop_course', methods=['POST'])
def drop_course():
    student = session['student']
    cid = request.form.get('cid')

    # connect the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # check cid is availble or not
    cursor.execute("SELECT * FROM course WHERE Cid=%s" %(cid))
    course = cursor.fetchone()
    if(not course) : # invalid cid
        cursor.close()
        conn.close()
        return render_template('result.html' , result='退選失敗，請輸入正確的課程代碼' , student=student, timetable=session['timetable'])

    # check if student has the class
    cursor.execute("SELECT * FROM enrollment WHERE Sid = %s AND Cid = %s", (student['Sid'], cid))
    result = cursor.fetchall()
    if not result:
        cursor.close()
        conn.close()
        return render_template('result.html', result="退選失敗，您沒有這堂課", student=student, timetable=session['timetable'])

    # worning message
    warnings = []

    # check studen't credit is < 12
    cursor.execute('SELECT * FROM student WHERE Sid=\'%s\'' %(session['student']['Sid']))
    student_detail = cursor.fetchone()
    if int(student_detail['Credit']) <= 12:
        warnings.append("警告，您的學分低於12學分")
    
    if course['Is_required'] == 1:
        warnings.append('警告，您退掉必修課')

    # drop the class from time table
    cursor.execute("DELETE FROM enrollment WHERE Sid = %s AND Cid = %s", (student['Sid'], cid))

    # update student's credit
    reduce_credit = int(student_detail['Credit']) - int(course['Credit'])
    cursor.execute('UPDATE student SET Credit=%d' %(reduce_credit))
    session['student']['Credit'] = reduce_credit

    # update course members
    reduce_members = int(course['Members']) - 1
    cursor.execute("UPDATE course SET Members = %s WHERE Cid = %s", (reduce_members, cid))

    conn.commit()

    cursor.close()
    conn.close()

    result_message = "退選成功"
    if warnings:
        result_message += "<br>" + "<br>".join(warnings)

    return render_template('result.html', result=result_message, student=student, timetable=session['timetable'])

@app.route('/login', methods=['POST'])
def login():
    sid = request.form.get('sid')
    password = request.form.get('passwd')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student WHERE Sid = %s AND Password = %s", (sid, password))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if(student and sid == student['Sid'] and password == student['Password']):
        session['student'] = student
        return redirect(url_for('home'))
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('student', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM course")
    course = cursor.fetchall()
    cursor.execute("SELECT * FROM student WHERE Sid = %s AND Password = %s", (session['student']['Sid'], session['student']['Password']))
    student = cursor.fetchone()
    cursor.execute("SELECT Cid FROM enrollment WHERE Sid = %s ", (session['student']['Sid'], ))
    cids = cursor.fetchall()
    timetable = []
    for x in cids:
        cursor.execute("SELECT * FROM course WHERE Cid = %s", (x['Cid'], ))
        result = cursor.fetchone()
        time = str(result['Time_id']).split('-')
        time_start = int(time[0])
        time_end = int(time[1])
        for y in range(time_start, time_end+1):
            course_data = {
                "Cid": result['Cid'],
                "Name": result['Name'],
                "Time_id": y
            }
            timetable.append(course_data)
    session['timetable'] = timetable
    cursor.close()
    conn.close()
    return render_template('home.html', student=student, course=course, timetable=timetable)

if __name__ == '__main__':
    app.run(debug=True)