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
2. Feedback should mention strengths and weaknesses briefly.
3. Provide 2-4 recommended resources (YouTube, blogs, tutorials) to improve.
4. Output ONLY a JSON object matching the QuizFeedback Pydantic model.
5. Do not add any extra text outside the JSON.""")

feedback_prompt=ChatPromptTemplate([
    feedback_system,
    HumanMessagePromptTemplate.from_template("Quiz Results:\nScore: {score}\nTopic: {topic}\nLevel: {level}\nProvide feedback")
])

feedback_chain=(feedback_prompt
                |feedback_structured_llm)

def feeback_chat(score, topic, level):
    return feedback_chain.invoke({
    "score": score,
    "topic": topic,
    "level": level
})
