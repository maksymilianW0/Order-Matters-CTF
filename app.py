from flask import Flask, request, render_template
import sqlite3

with open("dbscript", "r") as f:
    sql = f.read()

conn = sqlite3.connect("./database.sqlite3")
conn.executescript(sql)
conn.commit()
conn.close()

app = Flask("Web Server")

@app.route('/')
def root():
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
    return render_template("posts.html", rows=rows)

app.run(host="0.0.0.0", port=8080)