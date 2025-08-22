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
            existing_summary=self.messages.pop(0)

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
                ("user", "Existing summary:{existing_summary}\nNew messages:{new_messages}\nProvide the updated summary:")
            ])

            new_summary=self.llm.invoke(summary_prompt.format_messages(
                existing_summary=old_summary,
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


conversational_system=SystemMessagePromptTemplate.from_template("""You are a helpful tutor.

The learner is studying the topic: {topic}  
Their current level of understanding is: {level}  

Your job:
- Always explain concepts clearly at the learner’s level of understanding.  
- Keep answers short, sweet, and easy to follow.  
- If the learner asks about a subtopic, explain it in the same simple and concise way.  
- Use examples or analogies when helpful.  
- Avoid overwhelming details, but make sure the key idea is covered.  
- If the learner shows interest, suggest one or two natural follow-up subtopics.  

Stay concise, friendly, and supportive.
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

def converstaion_chat(topic, level, query, session_id, k):
     return conversation_memory_chain.invoke({"topic":topic, "level":level, "query":query},
                                 config={"configurable":{"session_id":session_id, "llm":llm, "k":k}})