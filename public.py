from flask import *
from database import *


public=Blueprint('public',__name__)

@public.route('/',methods=['get','post'])
def home():
    return render_template('home.html')


@public.route('/login',methods=['post','get'])
def login():

    if 'btn' in request.form:
        uname=request.form['uname']
        pasw =request.form['pasw']

        q="select * from login where username='%s' and password='%s'"%(uname,pasw)
        res=select(q)


        if res:
            session['loginid']=res[0]["login_id"]
            utype=res[0]["usertype"]
            if utype == "admin":
                flash("Login Success")
                return redirect(url_for("admin.adminhome"))
            elif utype == "agent":
                q="select * from agent where login_id='%s'"%(session['loginid'])
                val=select(q)
                if val:
                    session['aid']=val[0]['agent_id']
                    flash("Login Success")
                    return redirect(url_for("agent.agenthome"))

               
            
            else:
                flash("failed try again")
                return redirect(url_for("public.login"))
        else:
            flash("Invalid Username or Password!")
            return redirect(url_for("public.login"))


    return render_template("login.html")



@public.route('/reg',methods=['get','post'])
def reg():

    if 'btn' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        gender=request.form['gender']
        place=request.form['place']
        pin=request.form['pin']
        phone=request.form['phone']
        email=request.form['email'] 
        uname=request.form['uname'] 
        passw=request.form['passw'] 

        q="select * from login where username='%s'"%(uname)
        res=select(q)
        if res:
            flash("Username Already Exist!")
        else:
            q="insert into `login` values(NULL,'%s','%s','agent')"%(uname,passw)
            res=insert(q)

            w="insert into agent value(NULL,'%s','%s','%s','%s','%s','%s','%s','%s')"%(res,fname,lname,gender,place,pin,email,phone)
            insert(w)
            flash("Registration Successfull")
            return redirect(url_for("public.login"))

    return render_template("reg.html")
