from flask import Flask, redirect, render_template, request
from flask_scss import Scss
from conversation import converstaion_chat
from greet import greet_chat
from quiz_generator import quiz_generator_chat
from feedback import feedback_chat

app=Flask(__name__)
Scss(app)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method=="POST":
        user_response=request.form['input-field']
        ai_response=converstaion_chat(topic="python Function", level="expert", query=user_response, session_id="idx", k=2)
        return render_template("chat.html", user_response=user_response, ai_response=ai_response)
    
    else:
        return render_template("chat.html")
    

if __name__ =="__main__":
    app.run(debug=True)