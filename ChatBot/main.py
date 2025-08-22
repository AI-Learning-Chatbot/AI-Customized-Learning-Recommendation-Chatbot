from flask import Flask, redirect, render_template, request
from flask_scss import Scss

app=Flask(__name__)
Scss(app)

@app.route('/')
def index():
    return render_template("index.html")


if __name__ =="__main__":
    app.run(debug=True)