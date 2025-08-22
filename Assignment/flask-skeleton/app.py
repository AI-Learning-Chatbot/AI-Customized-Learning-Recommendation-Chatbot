from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock quiz data 
QUIZZES = {
    "beginner": [
        {
            "question": "What does `len('hello')` return?",
            "options": ["5", "hello", "Error"],
            "answer": 0
        }
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_quiz', methods=['POST'])
def get_quiz():
    level = request.json.get('level', 'beginner')
    return jsonify(QUIZZES.get(level, []))

@app.route('/submit', methods=['POST'])
def submit():
    user_answer = request.json.get('answer')
    question_idx = request.json.get('question_idx', 0)
    level = request.json.get('level', 'beginner')
    
    is_correct = user_answer == QUIZZES[level][question_idx]["answer"]
    return jsonify({
        "correct": is_correct,
        "feedback": "Correct! `len()` returns string length." if is_correct 
                   else "Try again! Hint: Count the letters."
    })

if __name__ == '__main__':
    app.run(debug=True)