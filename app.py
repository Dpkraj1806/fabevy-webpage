from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as sql

app=Flask(__name__)


@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        user=request.form['username']
        user_pass=request.form['password']
        print(user,user_pass)
        con=sql.connect("fabevy.db")
        cur=con.cursor()
        cur.execute("select * from userslogincredentials where username=?",(user,))
        data=cur.fetchone()
        if data:
            if data[1]==user:
                            if data[2]==user_pass:
                                if data[3]=="developer":
                                    return "developer"
                                elif data[3]=="admin":
                                  return redirect(url_for("admindashboard"))
                                else:
                                    return "Student"
            else:
                return render_template("login.html",error="Password Mismatch")
        else:
            return render_template("login.html",error="Username Not found")
    return render_template("login.html")

@app.route("/user_dashboard")
def userdashboard():
    return render_template("user_dashboard.html")

@app.route("/admin",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        fabevy_user=request.form['username']
        user_password=request.form['password']
        print(fabevy_user,user_password)        
        return render_template("signup.html")
    return render_template("signup.html")

@app.route("/admin_dashboard")
def admindashboard():
    con=sql.connect("fabevy.db")    
    con.row_factory=sql.Row
    cur=con.cursor()   
    cur.execute("select * from students")
    data=cur.fetchall()
    # print(data)
    return render_template("admin_dashboard.html",datas=data)   

@app.route("/student_details/<string:id>")
def student_details(id):
    con=sql.connect("fabevy.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute(" select * from  students where ID=?",(id,))
    data=cur.fetchall()
    # print(data[0]["number"])
    return render_template("student_details.html",datas=data)


@app.route("/add_students",methods=["GET","POST"])
def add_students():
    if request.method=="POST":
        add_stud=request.form["username"]
        con=sql.connect("fabevy.db")
        cur=con.cursor()
        # print(add_stud)
        cur.execute(" insert into students (USERNAME) values(?)",(add_stud,)) 
        con.commit()       
        return redirect(url_for('admindashboard'))
    return render_template("add_students.html")  

@app.route("/edit_students/<string:id>",methods=["GET","POST"])
def edit_students(id):
    if request.method=="POST":
        username=request.form["username"]
        name=request.form["name"]
        number=request.form["number"]
        degree=request.form["degree"]
        con=sql.connect("fabevy.db")
        cur=con.cursor()
        cur.execute("update students set USERNAME=?,NAME=?,NUMBER=?,DEGREE=?  where ID=?",(username,name,number,degree,id))
        con.commit()
        return redirect(url_for('admindashboard'))    
    con=sql.connect("fabevy.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from students where ID=?",(id,))
    data=cur.fetchone()
    # print(data)
    print(data['name'])
    return render_template("edit_students.html",datas=data)     



@app.route("/delete_students/<string:id>",methods=["GET","POST"])
def delete_students(id):
    con=sql.connect("fabevy.db")
    cur=con.cursor()
    cur.execute("delete from students where ID=?",(id,))
    con.commit()
    return render_template("admin_dashboard.html")     

@app.route("/batches/<string:name>",)
def batches(name):
        con=sql.connect("fabevy.db")
        cur=con.cursor()
        cur.execute("select * from "+name)
        data=cur.fetchall()
        return render_template("batches.html",datas=data)

@app.route("/createbatch",methods=["GET","POST"])
def create_batch():
    if request.method=="POST":
        b_name=request.form["batchname"]
        b_date=request.form["startdate"]
        conn=sql.connect("fabevy.db")
        cur=conn.cursor()
        value="create table "+b_name+"(name char(20)  ,date char(20))"
        cur.execute(value)
        cur.execute("insert into "+b_name+" (name,date) values(?,?)",(b_name,b_date))
        return render_template("admin_dashboard.html")
    return render_template("createbatch.html")


if __name__=="__main__":
    app.run(debug=True)