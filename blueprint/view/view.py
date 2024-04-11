from flask import Flask,request,session,render_template,redirect,Blueprint,url_for,g
import db_manager as db
from settings import Settings
import os

#if os.path.isfile(path) to remove file = os.remove(file)
var = Settings()
var.variables()
View = Blueprint("view",__name__, template_folder="templates")

@View.route("/homepage")
def homepage():
    pass

#all profile
@View.route("/profile", methods="GET")
def profile():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        page = var.profiles[role]

        if role == "Student" or role == "Parent":
            with db.connect() as conn:
                profile = db.Students_info(conn,"id",userID,False)
            return render_template(page,data=profile)
        elif role == "Teacher":
            with db.connect() as conn:
                profile = db.Techears_info(conn,"User",userID,False)
            return render_template(page,data=profile)
        else:
            return redirect(url_for("unauthorized"))
    else:
        redirect(url_for("login.user_login"))
#student pages
@View.route("/student_course_info")
def student_info():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        if role == "Student" or role == "Parent":
            with db.connect() as conn:
                studentInfo = db.Students_info(conn,"id",userID,False)
                sectionID = studentInfo[0][2]
                GradeID = db.Section_info(conn,sectionID,"Section")[0][1]
                courses = []
                coursesID = var.COURS_TAKE
                for key,item in coursesID.items():
                    if GradeID in item:
                        courses.append(key)
                Course_info = []
                for ID in courses:
                    _courses = db.Course_info(conn,ID,"Course")
                    for course in _courses:
                        teacher = db.Techears_info(conn,"Course",course[0],False)[0][3:5]
                        Course_info.append([course[0],teacher])
            StudentData = [studentInfo,Course_info]
            return render_template("student_course_info.html",data=StudentData)
        else:
            return redirect(url_for("unauthorized"))
    else:
        redirect(url_for("login.user_login"))

@View.route("/student_attendance_info")
def student_attendance():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        if role == "Student" or role == "Parent":
            with db.connect() as conn:
                atend = {}
                attendance_info = db.Attendace_info(conn,userID,"Student",False)
                for x,value in enumerate(attendance_info):
                    info = []
                    for value2 in attendance_info:
                        if value[-1] == value2[-1]:
                            m = m + 1
                            info.append(value2)
                    if m >= 2:
                        atend[x] = value2
            return render_template("student_attendace_info.html",data=atend)
        else:
            redirect(url_for("login.user_login"))


@View.route("/Student_Assessment")
def student_assessment():
    if "userID" in session:
        userID = session["userID"]
        role =  session["role"]
        if role != "Student":
            return redirect(url_for("unauthorized"))
        else:
            with db.connect() as conn:
                Student_assessment = db.Assessements_ifo(conn,userID,False,"Student")
            return render_template("student_assessment.html",data=Student_assessment)

#teacher

# unauthorized
@View.route("/403")
def unauthorized():
    return render_template("403.html")