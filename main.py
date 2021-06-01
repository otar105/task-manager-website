import sqlite3

def users():
    sql = "select * from users;"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    users = cur.fetchall()
    con.close()
    return users

def signup(email, password,):
    sql = f"insert into users(email, password) values('{email}', '{password}')"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def posts(id):
    sql = f"select * from posts where user_id = {id};"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    posts = cur.fetchall()
    con.close()
    return posts

def add_posts(name, text,tags, user_id):
    sql = f"insert into posts(name, text, tags, user_id) values('{name}','{text}', '{tags}', {user_id});"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def update_user(id,email, password):
    sql = f"update users set email = '{email}', password = '{password}' where id = {id}"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def get_tags(id):
    sql = f"select * from tags where user_id = {id};"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    tags = cur.fetchall()
    con.close()
    return tags

def add_tag(name, user_id):
    sql = f"insert into tags(name,user_id) values('{name}', {user_id});"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def delete_tag(id):
    sql = f"delete from tags where id = {id}"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def edit_tag(id, name):
    sql = f"update tags set name = '{name}' where id = {id}"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def tag_info(id):
    sql = f"select * from tags where id = {id}"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    tag = cur.fetchone()
    con.close()
    return tag

def posts_filter(name):
    sql = f"select * from posts where tags = '{name}'"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    posts = cur.fetchall()
    con.close()
    return posts

def posts_finder(search):
    sql = f"select * from posts where name like '{search}'"
    con = sqlite3.connect("date.db")
    cur = con.cursor()
    cur.execute(sql)
    posts = cur.fetchall()
    con.close()
    return posts