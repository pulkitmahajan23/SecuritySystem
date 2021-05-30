from flask import Flask, request, render_template, redirect, Response
import db_init
from sqlite3 import connect

app = Flask(__name__)
app.secret_key = "klhewvi"

@app.route('/')
def defaul():
    return render_template("index.html")

@app.route("/danger", methods=["POST"])
def danger():
    conn = connect("data.db")
    fet=conn.execute("SELECT * FROM STAT").fetchone()
    conn.close()
    if fet[0]=="t":
        return "1"
    else:
        return "0"

@app.route("/vfeed", methods=["GET"])
def vfeed():
    with open('Test_image.jpg', "rb") as f:
        b = f.read()
    return Response(b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + b + b'\r\n')
if __name__ == "__main__":
    app.run(debug=True)