from flask import Flask, redirect, render_template, request
from flask_scss import Scss
from conversation import converstaion_chat
from greet import greet_chat
from quiz_generator import quiz_generator_chat
from feedback import feedback_chat

app=Flask(__name__)
Scss(app)

db={
    "flag": False,
    "level":"expert"
}

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method=="POST":
        user_selected_topic=request.form['input-field']
        detail=greet_chat(user_selected_topic)
        db["topic"]=detail["topic"]
        db["flag"]=detail["flag"]
        db["conversation_prompt"]=detail["prompt"]
        # redirect to /chat so the chat route can prepare the first AI response
        return redirect('/level')
    else:
        return render_template("index.html")
    
@app.route('/chat', methods=["GET", "POST"])
def chat():
    if request.method=="POST":
        user_query=request.form['input-field']
        ai_response=converstaion_chat(db['topic'], db['level'], user_query, "idx_testing")
        return render_template('chat.html',ai_response=ai_response, user_response=user_query )
    else:
        ai_response=converstaion_chat(db['topic'], db['level'], db['conversation_prompt'], "idx_testing")
        return render_template('chat.html',ai_response=ai_response, user_response="user" )
        


@app.route('/level', methods=["POST", "GET"])
def level():
    return render_template("level.html")

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    pass

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    pass
    

if __name__ =="__main__":
    app.run(debug=True)