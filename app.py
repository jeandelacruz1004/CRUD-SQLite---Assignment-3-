from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3



app = Flask(__name__)

app.secret_key = 'many random bytes'

class students(object):
    def __init__(self, idno, firstname, midname,lastname, gender, course, yearlevel):
        self.idno = idno
        self.fName = firstname
        self.mName = midname
        self.lName = lastname
        self.gender = gender
        self.course = course
        self.yrLevel = yearlevel
class courses(object):
    def __init__(self, courseID, college):
        self.courseID = courseID
        self.college = college

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS students(idno TEXT PRIMARY KEY, fname TEXT, mName TEXT,LName TEXT, gender TEXT, course TEXT,yrLevel TEXT )")
c.execute("CREATE TABLE IF NOT EXISTS courses(courseID TEXT PRIMARY KEY, college TEXT)")
c.execute("CREATE VIEW IF NOT EXISTS studcourse AS SELECT courseID,idno,fName,mName,LName,gender,yrLevel FROM students CROSS JOIN courses WHERE courses.courseID = students.course")
conn.commit()
conn.close()



@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/students')
def Index():
    connection = sqlite3.connect("test.db")
    crsr = connection.cursor()  
    crsr.execute("SELECT  * FROM students")
    data = crsr.fetchall()
    crsr.close()
    return render_template('index2.html', students=data )


@app.route('/courses')
def Index2():
    connection = sqlite3.connect("test.db")
    crsr = connection.cursor()  
    crsr.execute("SELECT  * FROM courses")
    data = crsr.fetchall()
    crsr.close()
    return render_template('index.html', courses=data )

@app.route('/studentxcourse')
def Index3():
    connection = sqlite3.connect("test.db")
    crsr = connection.cursor()  
    crsr.execute("SELECT  * FROM studcourse")
    data = crsr.fetchall()
    crsr.close()
    return render_template('index3.html', joined=data )

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        idno = request.form['idno']
        fName = request.form['firstname']
        mName = request.form['midname']
        lName = request.form['lastname']
        gender = request.form['gender']     
        course = request.form['course']
        yrlevel = request.form['yearlevel']
        with sqlite3.connect('test.db') as connection:

            crsr = connection.cursor()
            crsr.execute("INSERT INTO students (idno, fName, mName, lName, gender, course, yrlevel ) VALUES (?, ?, ?, ?, ?, ?, ?)", (idno, fName,mName,lName,gender,course,yrlevel))
            connection.commit()

        return redirect(url_for('Index'))


@app.route('/insertcourse', methods = ['POST'])
def insertcourse():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        courseID = request.form['courseID']
        college = request.form['college']
        with sqlite3.connect('test.db') as connection:
            crsr = connection.cursor()
            crsr.execute("INSERT INTO courses (courseID, college) VALUES (?, ?)", (courseID, college))
            connection.commit()

        return redirect(url_for('Index2'))


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = sqlite3.connect('test.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM students WHERE idNo=?", (id_data,))
    connection.commit()
    return redirect(url_for('Index'))


@app.route('/deletecourse/<string:id_data>', methods = ['GET'])
def deletecourse(id_data):
    flash("Record Has Been Deleted Successfully")
    connection = sqlite3.connect('test.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM courses WHERE courseID=?", (id_data,))
    connection.commit()
    return redirect(url_for('Index2'))




@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == "POST":
        id_data = request.form['idno']
        fName = request.form['firstname']
        mName = request.form['middlename']
        lName = request.form['lastname']
        gender = request.form['gender']     
        course = request.form['course']
        yrlevel = request.form['yearlevel']

        with sqlite3.connect('test.db') as connection:

            crsr = connection.cursor()
            crsr.execute("SELECT * FROM students")
            for row in crsr.fetchall():
                crsr.execute("UPDATE students SET fName=?, mName=?, lName=?, gender=?, course=?, yrLevel=? where idno =?",(fName, mName, lName, gender, course,yrlevel,id_data,))
                connection.commit()

    
    flash("Data Updated Successfully")
    return redirect(url_for('Index'))
    connection.close()



@app.route('/updatecourse',methods=['POST','GET'])
def updatecourse():

    if request.method == "POST":
        courseID = request.form['courseID']
        college = request.form['college']


        with sqlite3.connect('test.db') as connection:

            crsr = connection.cursor()
            crsr.execute("SELECT * FROM courses")
            for row in crsr.fetchall():
                crsr.execute("UPDATE courses SET college=? where courseID =?",(college,courseID,))
                connection.commit()

    
    flash("Data Updated Successfully")
    return redirect(url_for('Index2'))
    connection.close()






if __name__ == "__main__":
    app.run(debug=True)




