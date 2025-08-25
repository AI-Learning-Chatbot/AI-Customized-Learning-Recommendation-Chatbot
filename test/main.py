from flask import Flask, redirect, render_template, request, url_for
from flask_scss import Scss
from conversation import converstaion_chat
from greet import greet_chat
from quiz_generator import quiz_generator_chat
from feedback import feedback_chat
import markdown
from markupsafe import Markup

app = Flask(__name__)
Scss(app)

db = {}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        value = request.form.get("input-field")  # from the input box
        if value:
            detail = greet_chat(value)
            db["topic"] = detail["topic"]
            db["conversation_prompt"] = detail["prompt"]
            return redirect(url_for("level"))
    return render_template("index.html")


@app.route("/select_topic", methods=["POST"])
def select_topic():
    value = request.json.get("topic") if request.is_json else None
    if value:
        detail = greet_chat(value)
        db["topic"] = detail["topic"]
        db["conversation_prompt"] = detail["prompt"]
        return {"redirect": url_for("level")}, 200
    return {"error": "No topic provided"}, 400

@app.route("/level", methods=["GET", "POST"])
def level():
    return render_template("level.html")

@app.route("/set_level", methods=["POST"])
def set_level():
    level_value = request.json.get("level")
    target = request.json.get("target")   # "quiz" or "chat"
    if level_value and target:
        db["level"] = level_value
        if target == "quiz":
            return {"redirect": url_for("quiz")}
        elif target == "chat":
            return {"redirect": url_for("chat")}
    return {"error": "Invalid request"}, 400


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "messages" not in db:
        db["messages"] = []

    if request.method == "GET":
        # First AI message
        response = converstaion_chat(db["topic"], db["level"], db["conversation_prompt"], "idx")
        # Convert markdown → HTML safely
        html_response = Markup(markdown.markdown(response, extensions=["fenced_code", "tables"]))
        db["messages"].append({"role": "ai", "text": html_response})
        return render_template("chat.html", messages=db["messages"])

    if request.method == "POST":
        query = request.form.get("input-field")
        if query:
            db["messages"].append({"role": "user", "text": query})

            response = converstaion_chat(db["topic"], db["level"], query, "idx")
            html_response = Markup(markdown.markdown(response, extensions=["fenced_code", "tables"]))
            db["messages"].append({"role": "ai", "text": html_response})

        return render_template("chat.html", messages=db["messages"])

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "quiz_data" not in db:
        # Generate quiz only once
        db["quiz_data"] = quiz_generator_chat(db["topic"], db["level"])
        db["current_index"] = 0
        db["score"] = 0

    return render_template("quiz.html", quiz=db["quiz_data"], index=db["current_index"], score=db["score"])



@app.route("/feedback")
def feedback():
    score = request.args.get("score", 0, type=int)
    total = request.args.get("total", 0, type=int)

    db["score"] = score
    db["total"] = total

    feedback_data = feedback_chat(score, db["topic"], db["level"])

    # Convert markdown → HTML
    feedback_html = Markup(markdown.markdown(
        feedback_data["feedback"],
        extensions=["fenced_code", "tables"]
    ))

    return render_template(
        "feedback.html",
        score=score,
        total=total,
        feedback=feedback_html,
        resources=feedback_data.get("resources", [])
    )


if __name__ == "__main__":
    app.run(debug=True)
