from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, BaseMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
from getpass import getpass
import os

#loading nesscery enviroment variables
load_dotenv()
os.environ['GOOGLE_API_KEY']=os.getenv("GOOGLE_API_KEY") or getpass("Enter your API key")

llm=ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")

