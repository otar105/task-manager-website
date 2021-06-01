from flask import Flask, render_template, request, session, flash, redirect
from main import edit_tag, users, signup, posts, add_posts, update_user, get_tags, add_tag, delete_tag, tag_info, posts_filter, posts_finder
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
        return render_template("index.html", posts = posts(), len_posts = len(posts()), tags = get_tags())
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
    if s > 0 and password == repeat_password:
        signup(email, password)
        return redirect("/login")
    elif s == 0:
        flash("email is already used! log in http://localhost:5000/login")
    elif password != repeat_password:
        flash("Passwords dose not match!")
    return redirect("/signup")

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
        return render_template("create.html", tags = get_tags())
    return redirect("/login")

@app.route("/createsave", methods=["post"])
def createsave_page():
    name = request.form["name"]
    text = request.form["body"]
    #tags = request.form.getlist("checkbox") not working
    tags = request.form.get("checkbox")
    add_posts(name,text, tags)
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
        return render_template("tags.html", tags_count = len(get_tags()), tags = get_tags())
    return redirect("/login")

@app.route("/tagsave", methods=["post"])
def tagssave_page():
    tags = request.form["tag"]
    add_tag(tags)
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
    edit_tag(editid, tag)
    return redirect("/tags")

@app.route("/tags/<name>")
def filtered_tags_page(name):
    posts = posts_filter(name)
    try:
        return render_template("filtered.html", posts = posts, tags = get_tags())
    except:
        return render_template("filtered.html", msg = "The notes you added will appear here", tags = get_tags())

@app.route("/search", methods=["get"])
def search_page():
    search = request.args.get("search")
    searched = posts_finder(search)
    print(len(searched))
    return render_template("searched.html", posts = searched, len_posts = len(searched), tags = get_tags())

if __name__ == "__main__":
    app.run()