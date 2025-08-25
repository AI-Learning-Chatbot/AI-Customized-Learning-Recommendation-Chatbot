from model import *

# Greeting structure


class UserLearningContext(BaseModel):
    topic: Optional[str] = Field(
        None, description="The main topic the user wants to learn, including subtopic/focus if mentioned")
    flag: bool = Field(
        False, description="Flag indicating when a topic has been provided by the user")
    reply: str = Field(
        "", description="Holds either the userprompt for the conversation LLM (once topic is given) or the assistant’s greeting/simple chat reply")


    # Greeting Chain
greeting_system = SystemMessagePromptTemplate.from_template("""You are a friendly learning assistant. Your goal is to converse with the user to understand what they want to learn.  

Rules:
1. Greet the user politely.  
2. Ask the user what topic they want to learn about.  
3. Once the user provides a topic, immediately set 'flag' to True.  
4. When the user provides a topic, set the `reply` field to contain only the detailed 'userprompt'. The 'userprompt' must instruct the conversation LLM to explain the topic clearly and thoroughly with step-by-step explanations, examples, and analogies.  
5. Always respond **only** as a valid JSON object matching the UserLearningContext schema.  
6. Never include text outside JSON. The `reply` field must contain only the greeting (before topic is given) or the userprompt (after topic is given).  
""")

greeting_prompt = ChatPromptTemplate.from_messages([
    greeting_system,
    HumanMessagePromptTemplate.from_template("{query}")
])

greeting_structured_llm = llm.with_structured_output(UserLearningContext)

greeting_chain = (greeting_prompt
                  | greeting_structured_llm)


def greet_chat(query):
    greet = greeting_chain.invoke(query)
    details = {
        'topic': greet.topic,
        'flag': greet.flag,
        'prompt': greet.reply
    }

    return details
