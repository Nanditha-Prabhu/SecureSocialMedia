from flask import Flask, render_template, request,redirect,url_for,session
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "jef123"

def isloggedin():
    return "username" in session

@app.route('/signup',methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        number = request.form.get("number")
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        con = sql.connect("user.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("insert into instagram (number,name,username,password) values(?,?,?,?)",
                    (number,name,username,password))
        con.commit()
        return redirect(url_for('login'))
    return render_template ("signup.html")

@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        name1 = request.form.get("username1")
        pass1 = request.form.get("password1")
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("select * from instagram where username=? and password=?", (name1,pass1))
        fet = cur.fetchall()
        for i in fet:
            if name1 in i and pass1 == i[3]:
                session["username"] = name1
                return redirect (url_for('main'))
            else:
                return "Incorrect Username or Password"
    return render_template ("login.html")
    
# story section starts here




@app.route('/search', methods = ["GET","POST"])
def search():
    if request.method == "POST":
        search = request.form.get("search")
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("select name from search")
        fet = cur.fetchone()
        for i in fet:
            if search in i:
                return redirect (url_for('ronaldo'))
            else:
                return "No user found"
    return render_template ("search.html")

@app.route('/instagram')
def main():
        conn = sql.connect("user.db")
        conn.row_factory=sql.Row
        cursor = conn.cursor()
        cursor.execute("select * from post")
        rows = cursor.fetchall()
        conn.close()
        if isloggedin():
            con = sql.connect("user.db")
            cur = con.cursor()
            cur.execute("select * from student")
            fet = cur.fetchone()
            count = fet[0]
            count1 = fet[1]
            count2 = fet[2]
            count3 = fet[3]
            return render_template ("main.html",count = count ,count1 = count1, count2 = count2, count3 = count3,fetch = rows)
        else:
            return "Not Able To Access"

@app.route('/operate/<counter>', methods = ["GET","POST"])
def operate(counter):
    if request.method == "POST":
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("select * from student")
        fet = cur.fetchone()
        count = fet[0]
        count1 = fet[1]
        count2 = fet[2]
        count3 = fet[3]

        if counter == '0':
            count += 1
        elif counter == '1':
            count1 += 1
        elif counter == '2':
            count2 += 1
        elif counter == '3':
            count3 += 1
        
        cur.execute("update student set  count=?,count1=?,count2=?,count3=?",(count,count1,count2,count3))
        con.commit()
    return redirect (url_for('main'))
    # return render_template ("main.html")

@app.route("/post",methods=['GET','POST'])
def upload():                
        if request.method=="GET":
            return render_template('post.html')
        if request.method=="POST":
            fileobj = request.files['file']
            caption = request.form.get("caption")
            file_extensions =  ["jpg","jpeg","png","gif"]
            uploaded_file_extension = fileobj.filename.split(".")[1]
            if uploaded_file_extension in file_extensions:
                destination_path= f"static/uploads/{fileobj.filename}"
                fileobj.save(destination_path)
                try:
                    conn = sql.connect("user.db")
                    cursor = conn.cursor()
                    cursor.execute("""insert into post values(:userid,:username,
                                :imagelink,:caption)""",{'userid':1,'username':'__d_rex__','imagelink':destination_path,'caption':caption})
                    conn.commit()
                    conn.close()
                except:
                    return render_template('post.html')
            else:
                return render_template('post.html') 
        return redirect(url_for("main"))

# @app.route("/view")
# def view():
#         conn = sql.connect("user.db")
#         conn.row_factory=sql.Row
#         cursor = conn.cursor()
#         cursor.execute("select * from post")
#         rows = cursor.fetchall()
#         conn.close()
#         return render_template('main.html',fetch = rows)


@app.route('/virat_story')
def virat():
    return render_template ("virat.html")

@app.route('/abde_story')
def abde():
    return render_template ("abde.html")

@app.route('/ronaldo')
def ronaldo():
    return render_template ("user.html")

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect (url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)