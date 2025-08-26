from flask import Flask, redirect, render_template, request, url_for, session
from flask_scss import Scss
from conversation import converstaion_chat
from greet import greet_chat
from quiz_generator import quiz_generator_chat
from feedback import feedback_chat
import markdown
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = "supersecretkey"  # REQUIRED for Flask sessions
Scss(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        value = request.form.get("input-field")  # from the input box
        if value:
            detail = greet_chat(value)
            session["topic"] = detail["topic"]
            session["conversation_prompt"] = detail["prompt"]
            return redirect(url_for("level"))
    return render_template("index.html")


@app.route("/select_topic", methods=["POST"])
def select_topic():
    value = request.json.get("topic") if request.is_json else None
    if value:
        detail = greet_chat(value)
        session["topic"] = detail["topic"]
        session["conversation_prompt"] = detail["prompt"]
        return {"redirect": url_for("level")}, 200
    return {"error": "No topic provided"}, 400


@app.route("/level", methods=["GET", "POST"])
def level():
    topic = session.get("topic", "this topic")  # fallback if session['topic'] not set
    return render_template("level.html", topic=topic)



@app.route("/set_level", methods=["POST"])
def set_level():
    level_value = request.json.get("level")
    target = request.json.get("target")   # "quiz" or "chat"
    if level_value and target:
        session["level"] = level_value
        if target == "quiz":
            return {"redirect": url_for("quiz")}
        elif target == "chat":
            return {"redirect": url_for("chat")}
    return {"error": "Invalid request"}, 400


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = []

    topic = session.get("topic", "General")  # ensure topic is available

    if request.method == "GET":
        response = converstaion_chat(topic, session.get("level"), session.get("conversation_prompt", ""), "idx")
        html_response = Markup(markdown.markdown(response, extensions=["fenced_code", "tables"]))
        session["messages"].append({"role": "ai", "text": html_response})
        session.modified = True
        return render_template("chat.html", messages=session["messages"])

    if request.method == "POST":
        query = request.form.get("input-field")
        if query:
            session["messages"].append({"role": "user", "text": query})
            response = converstaion_chat(topic, session.get("level"), query, "idx")
            html_response = Markup(markdown.markdown(response, extensions=["fenced_code", "tables"]))
            session["messages"].append({"role": "ai", "text": html_response})
            session.modified = True

        return render_template("chat.html", messages=session["messages"])


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "quiz_data" not in session:
        # Generate quiz only once per user
        raw_quiz = quiz_generator_chat(session["topic"], session["level"])

        # Convert all fields to HTML with Markdown support
        quiz_data = []
        for q in raw_quiz:
            quiz_data.append({
                "question": Markup(markdown.markdown(q["question"])),
                "options": [Markup(markdown.markdown(opt)) for opt in q["options"]],
                "answer": q["answer"],  # keep raw answer to compare
                "explanation": Markup(markdown.markdown(q["explanation"]))
            })

        session["quiz_data"] = quiz_data
        session["current_index"] = 0
        session["score"] = 0
        session.modified = True

    return render_template(
        "quiz.html",
        quiz=session["quiz_data"],
        index=session["current_index"],
        score=session["score"]
    )

@app.route("/feedback")
def feedback():
    score = request.args.get("score", 0, type=int)
    total = request.args.get("total", 0, type=int)

    session["score"] = score
    session["total"] = total

    feedback_data = feedback_chat(score, session["topic"], session["level"])

    feedback_html = Markup(markdown.markdown(
        feedback_data["feedback"],
        extensions=["fenced_code", "tables"]
    ))

    # Convert roadmap (list) to markdown for display
    roadmap_list = feedback_data.get("roadmap", [])
    roadmap_html = ""
    if roadmap_list:
        roadmap_text = "\n".join(f"- {step}" for step in roadmap_list)
        roadmap_html = Markup(markdown.markdown(
            f"\n{roadmap_text}",
            extensions=["fenced_code", "tables"]
        ))

    # Clear quiz-related session data so a retry starts fresh
    session.pop("score", None)
    session.pop("total", None)
    session.pop("quiz_data", None)
    session.pop("current_index", None)

    return render_template(
        "feedback.html",
        score=score,
        total=total,
        feedback=feedback_html,
        roadmap=roadmap_html,
        resources=feedback_data.get("resources", [])
    )

@app.route("/reset")
def reset():
    session.clear()   # clear everything from this user's session
    return redirect(url_for("index"))



if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host="127.0.0.1", port=5001, debug=True)


