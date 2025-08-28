from model import *

#loading nesscery enviroment variables
load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv("GOOGLE_API_KEY") or getpass("Enter your API key")

llm=ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")

class SummaryBufferHistory(BaseChatMessageHistory, BaseModel):
    messages:list[BaseMessage]=Field(default_factory=list)
    llm:ChatGoogleGenerativeAI=Field(default_factory=ChatGoogleGenerativeAI)
    k:int=Field(default_factory=int)

    def __init__(self, llm:ChatGoogleGenerativeAI, k:int):
        super().__init__(llm=llm, k=k)

    def add_messages(self, messages:list[BaseMessage])->None:

        old_summary:SystemMessage|None=None
        old_messages:list[BaseMessage]|None=None

        if len(self.messages)>0 and isinstance(self.messages[0], SystemMessage):
            old_summary=self.messages.pop(0)

        self.messages.extend(messages)

        threshold=self.k*2
        if len(self.messages)>threshold:
            old_messages=self.messages[:self.k]
            self.messages=self.messages[-self.k:]

            summary_system=SystemMessagePromptTemplate.from_template(""""You are tasked with maintaining a running summary of a conversation.  
                        You will be given:  
                        1. The existing summary of the conversation so far.  
                        2. A set of new messages exchanged in the conversation.  

                        Your job:  
                        - Merge the existing summary and the new messages into a new summary.  
                        - Keep the summary **short, concise, and focused on important details only**.  
                        - Do not lose any essential information.  
                        - Avoid repetition or unnecessary details.  
                        - The summary should be compact enough to be passed repeatedly to an LLM without overwhelming it.  """)
            
            summary_prompt=ChatPromptTemplate([
                summary_system,
                ("user", "Existing summary:{old_summary}\nNew messages:{new_messages}\nProvide the updated summary:")
            ])

            new_summary=self.llm.invoke(summary_prompt.format_messages(
                old_summary=old_summary,
                new_messages=old_messages
            ))

            self.messages=[SystemMessage(content=new_summary.content)]+self.messages

    def clear(self)->None:
            self.messages=[]
            
chat_history={}

def get_chat_history(session_id:str, llm:ChatGoogleGenerativeAI, k:int)->SummaryBufferHistory:
    if session_id not in chat_history:
        chat_history[session_id]=SummaryBufferHistory(llm=llm, k=k)

    return chat_history[session_id]


conversational_system=SystemMessagePromptTemplate.from_template("""You are a helpful tutor chatbot.

## Learner Context
- **Topic:** {topic}
- **Current Level:** {level}

## Your Job
- Explain concepts clearly at the learner’s level.
- Keep answers **short, simple, and easy to follow** (like a friendly chat message).
- Use **examples or analogies** when helpful.
- Focus on the **key idea only**, avoid overwhelming details.
- Format your output in **Markdown** (with headings, lists, code snippets if needed).
- Suggest a **related subtopic** the learner can explore next.
- Do **not** respond to sensitive, inappropriate, or offensive content.

## Teaching Flow
1. Start with the **most basic or foundational concept** of the topic.
2. Explain it concisely in a **chat-style message**.
3. Suggest the **next natural subtopic** the learner could ask about.
4. If the learner agrees, explain that next topic the same way.
5. Repeat step by step until the learner decides to stop.

""")

conversation_prompt=ChatPromptTemplate.from_messages([
    conversational_system,
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{query}")
])

conversation_chain=(conversation_prompt
                    |llm
                    |{"content":lambda x :x.content})

conversation_memory_chain=RunnableWithMessageHistory(
    conversation_chain,
    get_session_history=get_chat_history,
    input_messages_key="query",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="session_id",
            annotation=str,
            name="Session ID",
            description="The ID for a session",
            default="IDX"
        ),
        ConfigurableFieldSpec(
            id="llm",
            annotation=ChatGoogleGenerativeAI,
            name="LLM",
            description="Model used for answering",
            default=llm
        ),
        ConfigurableFieldSpec(
            id="k",
            annotation=int,
            name="k",
            description="Number of messages that the history keep intact",
            default=2
        )
    ]

)

def converstaion_chat(topic, level, query, session_id):
     response=conversation_memory_chain.invoke({"topic":topic, "level":level, "query":query},
                                 config={"configurable":{"session_id":session_id, "llm":llm, "k":3}})
     return response["content"]