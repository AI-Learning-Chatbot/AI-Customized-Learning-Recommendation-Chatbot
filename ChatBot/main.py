from flask import Flask, redirect, render_template, request
from flask_scss import Scss
from conversation import converstaion_chat
from greet import greet_chat
from quiz_generator import quiz_generator_chat
from feedback import feedback_chat

app=Flask(__name__)
Scss(app)

@app.route('/')
def index():
    return render_template("index.html")
    

if __name__ =="__main__":
    app.run(debug=True)