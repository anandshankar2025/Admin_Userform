from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

users = {}
admins = {"admin": {"password": "admin123", "type": "admin"}} 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        account_type = request.form.get("account_type")
        return redirect(url_for("login_choice", account_type=account_type))
    return render_template("index.html")

@app.route("/login_choice/<account_type>", methods=["GET", "POST"])
def login_choice(account_type):
    if account_type == "user":
        return redirect(url_for("user_login"))
    elif account_type == "admin":
        return redirect(url_for("admin_login"))

@app.route("/login/user", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        user_id = request.form.get("userid")
        password = request.form.get("password")
        
        if user_id in users and users[user_id]["password"] == password:
            session["user_id"] = user_id
            session["user_type"] = "user"
            return redirect(url_for("user_dashboard"))
        
        flash("Invalid credentials. Please try again.", "danger")
    return render_template("user_login.html")

@app.route("/login/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user_id = request.form.get("userid")
        password = request.form.get("password")
        
        if user_id in admins and admins[user_id]["password"] == password:
            session["user_id"] = user_id
            session["user_type"] = "admin"
            return redirect(url_for("admin_dashboard"))
        
        flash("Invalid credentials. Please try again.", "danger")
    return render_template("admin_login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_id = request.form.get("userid")
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        account_type = request.form.get("account_type") 

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("signup"))

        if account_type == "admin":
            if user_id in admins:
                flash("Admin ID already exists!", "danger")
                return redirect(url_for("signup"))

            admins[user_id] = {
                "name": name,
                "email": email,
                "phone": phone,
                "message": message,
                "password": password,
                "type": "admin"
            }
            flash("Admin account created successfully! Please log in.", "success")
            return redirect(url_for("index"))

        elif account_type == "user":
            if user_id in users or user_id in admins:
                flash("User ID already exists!", "danger")
                return redirect(url_for("signup"))

            users[user_id] = {
                "name": name,
                "email": email,
                "phone": phone,
                "message": message,
                "password": password,
                "type": "user"
            }
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("index"))

    return render_template("signup.html")

@app.route("/user_dashboard", methods=["GET", "POST"])
def user_dashboard():
    if "user_id" not in session or session["user_type"] != "user":
        return redirect(url_for("index"))
    
    user_id = session["user_id"]
    user_data = users[user_id]

    if request.method == "POST":
        users[user_id]["name"] = request.form.get("name")
        users[user_id]["email"] = request.form.get("email")
        users[user_id]["phone"] = request.form.get("phone")
        users[user_id]["message"] = request.form.get("message")
        flash("Information updated successfully!", "success")

    return render_template("user_dashboard.html", user=user_data)

@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if "user_id" not in session or session["user_type"] != "admin":
        return redirect(url_for("index"))

    if request.method == "POST":
        user_id = request.form.get("userid")
        if user_id in users:
            users[user_id]["name"] = request.form.get("name")
            users[user_id]["email"] = request.form.get("email")
            users[user_id]["phone"] = request.form.get("phone")
            users[user_id]["message"] = request.form.get("message")
            flash(f"Updated details for User ID: {user_id}", "success")
        else:
            flash("User ID not found!", "danger")

    return render_template("admin_dashboard.html", users=users)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
