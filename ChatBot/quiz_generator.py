from model import *

#Quiz structure
class QuizOutput(BaseModel):
    question: List[str] = Field(
        ..., 
        title="Questions", 
        description="List of quiz questions", 
        example=["What is the capital of France?", "Which language is primarily spoken in Brazil?"]
    )
    options: List[List[str]] = Field(
        ..., 
        title="Options", 
        description="List of options for each question", 
        example=[["Paris", "London", "Berlin", "Rome"], ["Spanish", "Portuguese", "English", "French"]]
    )
    answer: List[str] = Field(
        ..., 
        title="Answers", 
        description="List of correct answers corresponding to each question", 
        example=['a', 'b']
    )
    explanation: List[str] = Field(
        ..., 
        title="Explanations", 
        description="List of explanations for each answer", 
        example=[
            "Paris is the capital city of France.",
            "Portuguese is the official language of Brazil."
        ]
    )

    #Quizz

quiz_system=SystemMessagePromptTemplate.from_template("""You are a quiz generator assistant. 
Your task is to automatically create quizzes in a structured JSON format that matches the Pydantic model with fields: 
- question (list of strings) 
- options (list of list of strings) 
- answer (list of strings) 
- explanation (list of strings)

Rules:
1. Generate exactly the number of questions requested.
2. All questions must strictly stay within the requested topic; do not include anything outside the topic.
3. Provide options, the correct answer as its corresponding letter label ('a', 'b', 'c', 'd'), and an explanation for why the answer is correct.
4. Output only in JSON format that can be directly parsed into the Pydantic model.
""" )


quiz_prompt=ChatPromptTemplate.from_messages([
    quiz_system,
    HumanMessagePromptTemplate.from_template("""Create {number_of_questions} questions on the topic "{topic}" at "{level}" level.
""")
])

quiz_structured_llm=llm.with_structured_output(QuizOutput)

quiz_chain=(quiz_prompt
            |quiz_structured_llm)


def quiz_generator_chat(topic, level):
    quiz= quiz_chain.invoke({
    "number_of_questions": 5,
    "topic": topic,
    "level": level
    })

    structured_quiz=[]

    for i in range(5):
        sets={}
        sets['question']=quiz.question[i]
        sets['options']=quiz.options[i]
        sets['answer']=quiz.answer[i]
        sets['explanation']=quiz.explanation[i]
        structured_quiz.append(sets)

    return structured_quiz

