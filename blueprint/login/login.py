from flask import Flask,request,session,render_template,redirect,Blueprint,url_for,g
import db_manager as db
from settings import Settings


LOGIN = Blueprint("login",__name__,template_folder="template")

@LOGIN.route("/login",methods=["GET","POST"])
def user_login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        uid = request.form["password"]
        Role = request.form["role"]
        ToDo = "login"
        with db.connect() as conn:
            valid = db.user(conn,username,uid,ToDo)
            ToDo = "search"
            userID = db.user(conn,username,uid,ToDo)[0][0]
            if valid == "[LOGIN] Successful":
                session["userID"] = userid
                session["role"] = Role
                session["user"] = username
        return redirect(url_for("view.profile"))

@LOGIN.route("/admin")
def admin_login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        uid = request.form["UID"]
        Role = "admin"
        ToDo = "login"
        with db.connect() as conn:
            valid = db.user(conn,username,uid,ToDo)
            ToDo = "search"
            userID = db.user(conn,username,uid,ToDo)[0]
            if valid == "[LOGIN] Successful":
                session["userID"] = userid
                session["role"] = Role
                session["user"] = username
        return redirect(url_for("view.admin"))
