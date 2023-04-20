from flask import Blueprint, render_template, request, flash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", boolean=True)


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 4:
            flash("Your email must be longer than 3 characters", category="error")
        elif len(first_name) < 2:
            flash("Your first name must be greater than 1 character", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 7:
            flash("Password must be longer than 7 characters", category="error")
        else:
            flash("Account created!", category="success")
            # Add user to database

    elif request.method == "GET":
        pass

    return render_template("signup.html")
