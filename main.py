from flask import Flask, request, render_template, redirect, Response
import db_init
from sqlite3 import connect
import cv2

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
    elif fet[0]=="f":
        return "0"
    else:
        return "2"

@app.route("/vfeed")
def vfeed():
    img=cv2.imread("Test_image.jpg")
    _,buffer=cv2.imencode(".jpeg",img)
    return Response(b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=80)