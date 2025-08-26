from model import *
from typing import Optional

# Feedback structure with optional roadmap
class QuizFeedback(BaseModel):
    feedback: str = Field(..., description="Short, concise feedback for the user based on their score, topic, and level along with the roadmap")
    resources: List[str] = Field(..., description="List of recommended links (YouTube, blogs, tutorials) for further improvement")
    roadmap: Optional[List[str]] = Field(None, description="Optional sequential roadmap of learning steps/milestones for the topic")

# Structured LLM output
feedback_structured_llm = llm.with_structured_output(QuizFeedback)

# System prompt with updated instructions for roadmap
feedback_system = SystemMessagePromptTemplate.from_template("""
You are an AI tutor. Your task is to provide short, concise feedback for a quiz attempt.

Rules:
1. Use the user's quiz score, topic, and level of understanding to generate feedback.
2. If the score is low, provide encouraging feedback that motivates the user not to give up and to keep studying to improve. Add positive and supportive emojis (e.g., 😊📘✨).
3. If the score is high, provide feedback on how the user can expand their knowledge further by suggesting a next milestone or advanced concept to explore. Add achievement/next-level emojis (e.g., 🎯🚀📈).
4. Provide recommended resources with **only popular, widely recognized, publicly accessible URLs** (e.g., official documentation, top YouTube channels, widely used blogs/tutorials). Do NOT invent URLs. Only include links that are highly likely to be working.
5. The `resources` field should contain **only URLs**, no descriptive text.
6. Always provide a learning roadmap for the topic as a **list of sequential steps or milestones**, even if there is no official roadmap. Each step should be short and concise. You can format roadmap items in markdown style if you want.
7. Output ONLY a JSON object matching the QuizFeedback Pydantic model, including `feedback`, `resources`, and `roadmap`.
8. Do not add any extra text outside the JSON.
""")

feedback_prompt = ChatPromptTemplate([
    feedback_system,
    HumanMessagePromptTemplate.from_template(
        "Quiz Results:\nScore: {score}/5\nTopic: {topic}\nLevel: {level}\nProvide feedback"
    )
])

feedback_chain = (feedback_prompt | feedback_structured_llm)

# Feedback function returning dict with roadmap
def feedback_chat(score, topic, level):
    feeds = feedback_chain.invoke({
        "score": score,
        "topic": topic,
        "level": level
    })
    feedback_dict = {
        'feedback': feeds.feedback,
        'resources': feeds.resources,
        'roadmap': feeds.roadmap  # Optional list of roadmap steps
    }
    return feedback_dict
