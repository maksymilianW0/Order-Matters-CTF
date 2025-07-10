from flask import Flask, request, render_template, session, redirect
import sqlite3

with open("dbscript", "r") as f:
    sql = f.read()

conn = sqlite3.connect("./database.sqlite3")
conn.executescript(sql)
conn.commit()
conn.close()

app = Flask("Web Server")

app.secret_key = "abcd"

@app.route("/")
def root():
    if not session.get("logged_in"):
        return redirect("/login")
    else:
        return redirect("/posts")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET": # Zwróć formularz
        if not session.get("logged_in"):
            return render_template("login.html")
    # Klikną "login". sprawdź dane.
    user = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("./database.sqlite3")
    cursor = conn.cursor()

    sql = f"SELECT * FROM users WHERE user='{user}' AND password='{password}' LIMIT 1"
    print(sql)
    response = cursor.execute(sql).fetchall()

    cursor.close()
    conn.close()

    if len(response) == 1:
        session["user"] = user
        session["role"] = response[0][3]
        session["logged_in"] = True
        return redirect("/posts")
    else:
        return redirect("/login")

@app.route('/posts')
def posts():
    if not session.get("logged_in"):
        return redirect("/")
    
    sort = request.args.get("sort", "id")  # default to ID
    for forbidden in ['union', '--', ';', "#", "insert", "update", "delete"]:
        if forbidden in sort.lower():
            return "Naughty hacker!"
    query = f"SELECT * FROM posts ORDER BY {sort} LIMIT 7"
    conn = sqlite3.connect("./database.sqlite3")
    cursor = conn.cursor()
    try:
        rows = cursor.execute(query).fetchall()
    except sqlite3.Error as e:
        return f"SQL error: {e}"
    cursor.close()
    conn.close()
    return render_template("posts.html", rows=rows, username=session.get("user"), role=session.get("role"))

app.run(host="0.0.0.0", port=8080)