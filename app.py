from flask import Flask, render_template, request, session, flash, redirect
from main import edit_tag, users, signup, posts, add_posts, update_user, get_tags, add_tag, delete_tag, tag_info, posts_filter, posts_finder, delete_post, get_posts, edit_post, vefify_email, vefify_codes, delete_code
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


msg = MIMEMultipart('alternative')

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("otoelbakidze2020@gmail.com", "iyazfbrcmtoiebqo")

app = Flask(__name__)
app.secret_key = "web"

@app.route("/")
def setup_page():
    if "user" in session:
        return redirect("/index")
    return render_template("setup.html")

@app.route("/index")
def index_page():
    if "user" in session:
        id = session["user"]
        return render_template("index.html", posts = posts(id), len_posts = len(posts(id)), tags = get_tags(id))
    return redirect("/signup")

@app.route("/login")
def login_page():
    if "user" in session:
        return redirect("/index")
    return render_template("login.html")

@app.route("/loginsave", methods=["post"])
def loginsave_page():
    s = 0
    email = request.form["email"]
    password = request.form["password"]
    emails = users()
    for info in emails:
        if email == info[1] and password == info[2]:
            session["user"] = info[0]
            flash("Scuccessfully Loged in!")
            return redirect("/index")
    flash("Could not log in!")
    return redirect("/login")

@app.route("/signup")
def signup_page():
    if "user" in session:
        return redirect("/index")
    return render_template("signup.html")

@app.route("/signupsave", methods=["post"])
def signupsave_page():
    s = 0
    email = request.form["email"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]
    emails = users()
    for i in emails:
        if i ==email:
            s += 1
    if s < 1 and password == repeat_password:
        x = "ABCDEFJHIJKLMNOPQRSTUVWXYZ"
        code = ""
        for i in range(0,10):
            code += random.choice(x)
        print(code)
        html = f"Confirmation email code: {code}"
        msg['Subject'] = "No Reply"
        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        server.sendmail("otoelbakidze2020@gmail.com", f"{email}", msg.as_string())
        flash("Verify your email to verify!")
        vefify_email(email,password,code)
        return redirect("/verify")
    elif s == 0:
        flash("email is already used! log in http://localhost:5000/login")
    elif password != repeat_password:
        flash("Passwords dose not match!")
    return redirect("/signup")

@app.route("/verify")
def verify_page():
    return render_template("verify.html")

@app.route("/verifysave", methods=["post"])
def verifysave_page():
    code = request.form["code"]
    print(code)
    codes = vefify_codes()
    print(codes)
    for i in codes:
        if code == i[3]:
            signup(i[1],i[2])
            delete_code(i[3])
            return redirect("/index")
    return redirect("/")

@app.route("/logout")
def logoutuser_page():
    if "user" in session:
        session.pop("user",None)
        flash("Successfully Loged out!")
        return redirect("/login")
    return redirect("/")

@app.route("/create")
def create_page():
    if "user" in session:
        id = session["user"]
        return render_template("create.html", tags = get_tags(id))
    return redirect("/login")

@app.route("/createsave", methods=["post"])
def createsave_page():
    name = request.form["name"]
    text = request.form["body"]
    #tags = request.form.getlist("checkbox") not working
    tags = request.form.get("checkbox")
    user_id = session["user"]
    add_posts(name,text, tags, user_id)
    flash("Successfully created!")
    return redirect("/index")

@app.route("/user")
def user_page():
    if "user" in session:
        return render_template("user.html")
    return redirect("/login")

@app.route("/usersave", methods=["post"])
def usersave_page():
    email = request.form["email"]
    password = request.form["password"]
    repeat_password = request.form["repeat_password"]
    if password == repeat_password:
        id = session["user"]
        update_user(id, email, password)
        flash("Successfully updated!")
        return redirect("/user")
    flash("Passwords dose not match!")
    return redirect("/user")

@app.route("/tags")
def tags_page():
    if "user" in session:
        id = session["user"]
        return render_template("tags.html", tags_count = len(get_tags(id)), tags = get_tags(id))
    return redirect("/login")

@app.route("/tagsave", methods=["post"])
def tagssave_page():
    tags = request.form["tag"]
    user_id = session["user"]
    add_tag(tags, user_id)
    return redirect("/tags")

@app.route("/delete/<id>")
def deletetag_page(id):
    if "user" in session:
        delete_tag(id)
        return redirect("/tags")
    return redirect("/login")

@app.route("/edit/<id>")
def edittag_page(id):
    if "user" in session:
        global editid
        editid = id
        tag = tag_info(id)
        return render_template("edit.html", tag = tag)
    return redirect("/login")

@app.route("/editsave", methods=["post"])
def editsave_page():
    tag = request.form["tag"]
    user_id = session["user"]
    edit_tag(editid, tag, user_id)
    return redirect("/tags")

@app.route("/tags/<name>")
def filtered_tags_page(name):
    posts = posts_filter(name)
    id = session["user"]
    try:
        return render_template("filtered.html", posts = posts(id), tags = get_tags(id))
    except:
        return render_template("filtered.html", msg = "The notes you added will appear here", tags = get_tags(id))

@app.route("/search", methods=["get"])
def search_page():
    search = request.args.get("search")
    searched = posts_finder(search)
    print(len(searched))
    id = session["user"]
    return render_template("searched.html", posts = searched, len_posts = len(searched), tags = get_tags(id))

@app.route("/delete/<id>")
def post_page(id):
    return render_template("info.html")

@app.route("/delete/post/<id>")
def deletepage_page(id):
    delete_post(id)
    return redirect("/index")

@app.route("/edit/post/<id>")
def editpost_page(id):
    global editpostid
    editpostid = id
    user_id = session["user"]
    return render_template("editpost.html",  tags = get_tags(user_id), posts = get_posts(user_id, id))
  
@app.route("/editpostsave", methods=["post"])
def editpostsave_page():
    name = request.form["name"]
    text = request.form["body"]
    edit_post(name,text, editpostid)
    return redirect("/index")

if __name__ == "__main__":
    app.run()