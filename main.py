from flask import Flask,flash,send_file
from flask import render_template
from flask import request
from flask import redirect,url_for,session
import Backend as B
import mysql_data



app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def welcome():
    if request.method == 'POST':
        
        if request.form['val']=='admin':
            return redirect("login_admin")
        elif request.form['val']=='hod':
            return redirect("login_hod")
        elif request.form['val']=='student':
            return redirect("login_student")
   


    return render_template('selection.html')




@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    

    if request.method == 'POST':
        user1 = request.form.get('login')
        passwd1 = request.form.get('passwd')
        result = B.admin_check(username = user1,passwd=passwd1)
        
      
        if result == 0:

            return redirect(url_for('login_admin'))

        else:
            session['loginsuccess'] = True
            return redirect(url_for("admin_logged"))

    return render_template('adminlogin.html')


@app.route('/admin_page',methods=['POST','GET'])
def admin_logged():
    flag='Changed'
    if request.method == 'POST':
        print("in")
        value=request.form.get('check')
        if value=='Check Integrity':
            result=B.check_integrity()
            print(result)
            for i in range(0,len(result)):
                temp=result[i]
                place=i
                if flag in temp.values():
                    val1='Block has been compermised AT:'+str(place)
                    return render_template("check_admin.html",info=val1)
                    


            
            
            return render_template("check_admin.html",info='All blocks okay ')

            




    return render_template("check_admin.html")#######################



@app.route('/login_hod',methods=['POST','GET'])
def login_hod():
    

    if request.method == 'POST':
        user1 = request.form.get('login')
        passwd1 = request.form.get('passwd')
        result = B.hod_check(username = user1,passwd=passwd1)
        

        if result == 0:

            return redirect(url_for('login_hod'))

        else:
            session['loginsuccess'] = True
            return redirect(url_for("hod_logged"))#####

    return render_template('hodlogin.html')

@app.route('/hod_logged',methods=['POST','GET'])
def hod_logged():

    if request.method == 'POST':
        value=request.form.get('dept')
        if value=='ec':
            print("in")
            mysql_data.new_data("SELECT student_name,Student_usn,ide_selected FROM Blocks WHERE Student_usn LIKE '%EC%'")
            path_file="student_list12.xlsx"

            return send_file(path_file,as_attachment=True)
        elif value=='cs':
            ob=B.get_data('node0')
        else:
            ob=B.get_data('node0')

    return render_template("hodloginpage.html")





@app.route('/login_student',methods=['POST','GET'])
def login_student():
    global usn

    if request.method == 'POST':
        user1 = request.form.get('login')
        passwd1 = request.form.get('passwd')
        result = B.authentic(username = user1,passwd=passwd1)
        usn=user1.upper()

        if result == 0:

            return render_template('loginstudent.html',info='invalid username or password')

        else:
            session['loginsuccess'] = True
            return redirect(url_for("profile_details_and_selection"))

    return render_template('loginstudent.html')


@app.route('/new/profile_details_and_selection',methods=['POST','GET'])
def profile_details_and_selection():

    if session['loginsuccess'] == True:

        global student_name
        global student_usn
        global subjects
        
        student_name, student_usn, subjects = B.displaying_of_student_info(usn)

        if request.method == 'POST':
            print("in")
            global ide_selection
            ide_selection = request.form.get('Course')
            print(ide_selection)
            result,seats = B.selsection(ide_selection,student_usn)
            print(seats)

            if seats > 0:

                if result == 1:
                    
                    session["selection_successful"] = True
                    return redirect(url_for('block_creation'))
                elif result==-1:
                    print('in')
                    flash(u'sunject exist', 'error')
                    render_template('selectsub.html',student_name=student_name,student_usn=student_usn,subjects=subjects)
                else: 
                    flash("already selectedor exists in your history")
                    render_template('selectsub.html',student_name=student_name,student_usn=student_usn,subjects=subjects)
                    
                    
                
            else:
                #alert he could have already chossen the sub or not the seats are filleed
                flash(u'no seats buddy', 'error')
                render_template('selectsub.html',student_name=student_name,student_usn=student_usn,subjects=subjects)
                


    return render_template('selectsub.html',student_name=student_name,student_usn=student_usn,subjects=subjects)


               





@app.route('/block_creation')
def block_creation():
    print(student_name)
    print(student_usn)
    print(ide_selection)
    

    result=B.block(usn=student_usn,ide_short=ide_selection)
    print(result)####block condition check intergrity

    return render_template('success.html')






if __name__=='__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'



    app.run(debug=True)


