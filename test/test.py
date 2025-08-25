from conversation import converstaion_chat
from greet import greet_chat
from quiz_generator import quiz_generator_chat
from feedback import feedback_chat

db={
    "level":"expert",
    "flag": False
}
flag=False
while not flag:
    query=str(input("enter:"))
    detail=greet_chat(query)
    db["topic"]=detail['topic']
    db["conversation_prompt"]=detail["prompt"]
    if not db['flag']:
        print(db["conversation_prompt"])
    flag=db['flag']
print("\n -------------------------------------------------------------------------------------")

print("What would you like to do Learn(1) or Take a quiz(2)")
option=int(input("enter your choice"))
if option==1:
    #learn
    response=converstaion_chat(db['topic'], db['level'], db["conversation_prompt"], 'idx')
    print(response)
    print("\n -------------------------------------------------------------------------------------")
else:
    #quiz
    quiz=quiz_generator_chat(db['topic'], db['level'])
    print(quiz[0]['question'])
    print(quiz[0]['options'])
    print(quiz[0]['answer'])
    print(quiz[0]['explanation'])
    print("\n -------------------------------------------------------------------------------------")

feedback=feedback_chat(2, db['topic'], db['level'])
print(feedback['feedback'])
print(feedback['resources'])