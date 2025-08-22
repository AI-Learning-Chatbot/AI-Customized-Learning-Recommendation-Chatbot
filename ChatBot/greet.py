from model import *

#Greeting structure
class UserLearningContext(BaseModel):
    topic: Optional[str] = Field(None, description="The main topic the user wants to learn, including subtopic/focus if mentioned")
    level: Optional[str] = Field(None, description="User understanding level: beginner, intermediate, expert")
    ready_to_learn: bool = Field(False, description="Flag indicating when topic and level are selected and conversation can continue")
    reply: str = Field("", description="Assistant’s follow-up reply asking for missing info or confirming readiness")



    # Greeting Chain
greeting_system=SystemMessagePromptTemplate.from_template("""You are a friendly learning assistant. Your goal is to converse with the user to understand what they want to learn and assess their level.

Rules:
1. Greet the user politely.
2. Ask the user what topic they want to learn about.
3. Ask the user how much they understand about the topic: 'beginner', 'intermediate', or 'expert'.
6. Once both topic and level are known, set 'ready_to_learn' flag to True.
7.Always respond **only** as a valid JSON object matching the UserLearningContext schema. 
Never include text outside JSON. 
All greetings, follow-up questions, or confirmations must go inside the `reply` field.
""")

greeting_prompt=ChatPromptTemplate.from_messages([
    greeting_system,
    HumanMessagePromptTemplate.from_template("{query}")
])

greeting_structured_llm=llm.with_structured_output(UserLearningContext)

greeting_chain=(greeting_prompt
                |greeting_structured_llm)
