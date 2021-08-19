from flask import *
import sqlite3
import os
from Funtions import *
import json
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "Ranuga2008"
app.debug = True
app.permanent_session_lifetime = timedelta(days=365,minutes=60,seconds=60,microseconds=100)

@app.route("/")
def home():
    flash(" ! Welcome to the Home Page ! ", "success")
    return render_template("home.html")

@app.route("/Institue/Log Out")
def log_out():
    session.pop("User Name",None)
    session.pop("Password",None)
    flash("Loged out successdully ! ","success")
    return redirect("/")

@app.route("/Institue/<string:institue_Name>/")
def institue(institue_Name):
    # TODO
    if "User Name" in session or "Passowrd" in session or "Info" in session:
        return render_template("institue_creator/institute_base.html")
    else:
        return f"WELCOME TO " + institue_Name


@app.route("/New Account", methods=["POST", "GET"])
def new_account():
    # New Account #
    """ New Account """
    if "User Name" in session or "Password" in session or "Info" in session:
        flash("Log out to create a new account.", "warning")
        return redirect("/Institue/" + session["Info"][0][0] + "/")
    else:
        if request.method == "POST":
            # User Name
            user_name = request.form["User Name"]
            # Password
            passowrd = request.form["Password"]
            # Institue Name
            institue_name = request.form["Institute Name"]
            # File
            file_ = request.files["File"]
            # Email
            email = request.form["Email"]
            # If anything is not blank
            if (
                user_name == ""
                or passowrd == ""
                or institue_name == ""
                or file_ is None
                or email == ""
            ):
                flash(
                    "User Name or Password or Institue Name or File or Email is empty ! ",
                    "warning",
                )
                return redirect("/New Account")
            else:
                file_name, file_extention = os.path.splitext(file_.filename)
                print(file_extention)
                print(file_name)
                # If the file is json
                if file_extention != ".json":
                    flash("The file is not json ! ", "danger")
                    return redirect("/New Account")
                else:
                    # Checks if the json file has the requirments
                    f_name = file_.filename
                    file_.save(os.path.join("/home/indika/PycharmProjects/IS",file_.filename))
                    with open(f_name,"r") as l:
                        d = json.load(l)
                    if d is None or d == None:
                        os.remove(f_name)
                    else:
                        os.remove(f_name)
                        conn = sqlite3.connect("ISU.db")
                        c = conn.cursor()
                        c.execute(
                            "SELECT * FROM ISU WHERE User_Name=? AND Password=?",
                            (user_name, passowrd),
                        )
                        d = c.fetchall()
                        if d == [] or d is None:
                            pass
                        else:
                            flash(
                                "User name and Password has been already taken.", "danger"
                            )
                            return redirect("/New Account")
                        # If there is a Institue Name as the one that they are requesting for
                        c.execute(
                            "SELECT * FROM ISU WHERE Institue_Name=?", (institue_name,)
                        )
                        a = c.fetchall()
                        if a != []:
                            flash("The Institue Name is not available.", "info")
                            return redirect("/New Account")
                        else:
                            # Creates a dir as the name of the institue name
                            os.mkdir(
                                "/home/indika/PycharmProjects/IS/ISU_Files/" + institue_name
                            )
                            # Add the file to the institue dir
                            file_.save(
                                os.path.join(
                                    "/home/indika/PycharmProjects/IS/ISU_Files/"
                                    + institue_name,
                                    file_.filename,
                                )
                            )
                            # Add the Parents SQLITE DB TABLE
                            conn_parents = sqlite3.connect(
                                "/home/indika/PycharmProjects/IS/ISU_Files/"
                                + institue_name
                                + "/"
                                + "Parents.db"
                            )
                            c_parents = conn_parents.cursor()
                            conn_parents.commit()
                            # Add the Teachers SQLITE DB TABLE
                            conn_teachers = sqlite3.connect(
                                "/home/indika/PycharmProjects/IS/ISU_Files/"
                                + institue_name
                                + "/"
                                + "Teachers.db"
                            )
                            c_teachers = conn_parents.cursor()
                            conn_teachers.commit()
                            # Add the Students SQLITE DB TABLE
                            conn_parents = sqlite3.connect(
                                "/home/indika/PycharmProjects/IS/ISU_Files/"
                                + institue_name
                                + "/"
                                + "Students.db"
                            )
                            c_parents = conn_parents.cursor()
                            conn_parents.commit()
                            # Add the user to the DB
                            c.execute(
                                "INSERT INTO ISU (Institue_Name,User_Name,Password,File,Email) VALUES (?,?,?,?)",
                                (institue_name, user_name, passowrd, file_.filename,email]),
                            )
                            conn.commit()
                            # Add the user to session data
                            session["New Account User Name"] = user_name
                            session["New Account Password"] = passowrd
                            # Send a Email (User Name and Password and some instructions and some other stuff)
                            send_email(email,"IS",f"Your User Name is {user_name} \n Your Password is {passowrd}")
                            # REdirect them to the
                            return redirect("/Login")
        else:
            flash(" ! WELCOME TO NEW ACCOUNT PAGE ! ", "success")
            return render_template("new_account.html")


@app.route("/Login", methods=["POST", "GET"])
def login():
    if "User Name" in session or "Password" in session:
        flash("You are already Loged IN ! ", "danger")
        return redirect("/Institue/" + session["Info"][0][0] + "/")
    elif "New Account User Name" in session or "New Account Password" in session:
        conn = sqlite3.connect("ISU.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM ISU WHERE User_Name=? AND Password=?",
            (session["New Account User Name"], session["New Account Password"]),
        )
        info = c.fetchall()
        if info == [] or info is None:
            flash(
                "No Insitute has a User name or a Password like wht you enterd ! ",
                "warning",
            )
            return redirect("/")
        else:
            session["User Name"] = session["New Account User Name"]
            session["Password"] = session["New Account Password"]
            session["Info"] = info
            try:
                session.pop("New Account User Name", None)
                session.pop("New Account Password", None)
            except:
                pass
            return redirect("/Institue/" + info[0][0] + "/")
    else:
        if request.method == "POST":
            user_name = request.form["User Name"]
            password = request.form["Password"]
            if user_name == "" or password == "":
                flash("User Name or Password is empty ! ","danger")
                return redirect("/")
            else:
                conn = sqlite3.connect("ISU.db")
                c = conn.cursor()
                c.execute(
                    "SELECT * FROM ISU WHERE User_Name=? AND Password=?",
                    (user_name, password),
                )
                info = c.fetchall()
                if info == [] or info is None:
                    flash(
                        "No Insitute has a User name or a Password like wht you enterd ! ",
                        "warning",
                    )
                    return redirect("/")
                else:
                    session["User Name"] = user_name
                    session["Password"] = password
                    session["Info"] = info
                    try:
                        session.pop("New Account User Name", None)
                        session.pop("New Account Password", None)
                    except:
                        pass
                    send_email(session["Info"][0][4],f"Loged into {session['Info'][0][0]}.",f"You have successfuly loged into with the access to the information of {for i in session["Info"]}")
                    return redirect("/Institue/" + info[0][0] + "/")
        else:
            flash(" ! WELCOME TO LOGIN PAGE ! ", "success")
            return render_template("login.html")


if __name__ == "__main__":
    app.run(host="")

