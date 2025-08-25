from model import *

#Feedback structure
class QuizFeedback(BaseModel):
    feedback: str = Field(..., description="Short, concise feedback for the user based on their score, topic, and level")
    resources: List[str] = Field(..., description="List of recommended links (YouTube, blogs, tutorials) for further improvement")

# feeback

feedback_structured_llm=llm.with_structured_output(QuizFeedback)


feedback_system=SystemMessagePromptTemplate.from_template("""You are an AI tutor. Your task is to provide a short, concise feedback for a quiz attempt.

Rules:
1. Use the user's quiz score, topic, and level of understanding to generate feedback.
2. If the score is low, provide encouraging feedback that motivates the user not to give up and to keep studying to improve. Add positive and supportive emojis (e.g., 😊📘✨).
3. If the score is high, provide feedback on how the user can expand their knowledge further by suggesting a next milestone or advanced concept to explore. Add achievement/next-level emojis (e.g., 🎯🚀📈).
4. Provide 2-4 recommended resources with actual links (YouTube ▶️, blogs 📖, tutorials 💻) to improve or go deeper into the topic.
5. Output ONLY a JSON object matching the QuizFeedback Pydantic model.
6. Do not add any extra text outside the JSON.
""")

feedback_prompt=ChatPromptTemplate([
    feedback_system,
    HumanMessagePromptTemplate.from_template("Quiz Results:\nScore: {score}/5\nTopic: {topic}\nLevel: {level}\nProvide feedback")
])

feedback_chain=(feedback_prompt
                |feedback_structured_llm)

def feedback_chat(score, topic, level):
    feeds= feedback_chain.invoke({
    "score": score,
    "topic": topic,
    "level": level
    })
    feedback_dict={
        'feedback':feeds.feedback,
        'resources':feeds.resources
    }
    return feedback_dict
