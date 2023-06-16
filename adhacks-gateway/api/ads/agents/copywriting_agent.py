import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import json

from langchain import PromptTemplate, SQLDatabase
from langchain.chains import APIChain, LLMMathChain, RetrievalQA, SQLDatabaseChain
from langchain.experimental.plan_and_execute import  load_agent_executor, load_chat_planner
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents import AgentType
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.chains import LLMChain

from llama_index import download_loader


class CopywritingAgent:
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.environ.get('OPENAI_API_KEY'))
        self.embeddings = OpenAIEmbeddings()
    
    def copywriting_agent(self, doc_context, input_topic):
        copywriting_template = """Use the context below to write a 400 word blog post about the topic below:
                        Context: {context}
                        Topic: {topic}
                        Blog post:"""

        copywriting_prompt = PromptTemplate(
            template=copywriting_template, input_variables=["context", "topic"]
        )
        copywriting_prompt.format(context=doc_context, topic=input_topic)
        copywriting_chain = LLMChain(llm=self.llm, prompt=copywriting_prompt)
        
        tools = [
            Tool(
                name="Copywriting tool",
                func=copywriting_chain.run,
                description="This tool is useful to answer queries regarding the website content",
            ),
        ]
        
        agent = initialize_agent(llm=self.llm, tools=tools, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, max_iterations=10, max_execution_time=10, early_stopping_method="generate", verbose=True)
        return agent
    
    def create_general_copywriting_tool(self, doc_context, input_topic):
        copywriting_template = """Use the context below to write a 400 word blog post about the topic below:
                        Context: {context}
                        Topic: {topic}
                        Blog post:"""

        copywriting_prompt = PromptTemplate(
            template=copywriting_template, input_variables=["context", "topic"]
        )
        copywriting_prompt.format(context=doc_context, topic=input_topic)
        copywriting_chain = LLMChain(llm=self.llm, prompt=copywriting_prompt)
        
        
        tool = Tool(
            name="Copywriting tool",
            func=copywriting_chain.run,
            description="This tool is useful to answer queries regarding the website content",
        ),
        return tool
    
    def create_twitter_copywriting_tool(self, doc_context, input_topic):
        copywriting_template = """Use the context below to write a 400 word blog post about the topic below:
                        Context: {context}
                        Topic: {topic}
                        Blog post:"""

        copywriting_prompt = PromptTemplate(
            template=copywriting_template, input_variables=["context", "topic"]
        )
        copywriting_prompt.format(context=doc_context, topic=input_topic)
        copywriting_chain = LLMChain(llm=self.llm, prompt=copywriting_prompt)
        
        
        tool = Tool(
            name="Copywriting tool",
            func=copywriting_chain.run,
            description="This tool is useful to answer queries regarding the website content",
        ),
        return tool
    
    def create_facebook_copywriting_tool(self, doc_context, input_topic):
        copywriting_template = """Use the context below to write a 400 word blog post about the topic below:
                        Context: {context}
                        Topic: {topic}
                        Blog post:"""

        copywriting_prompt = PromptTemplate(
            template=copywriting_template, input_variables=["context", "topic"]
        )
        copywriting_prompt.format(context=doc_context, topic=input_topic)
        copywriting_chain = LLMChain(llm=self.llm, prompt=copywriting_prompt)
        
        
        tool = Tool(
            name="Copywriting tool",
            func=copywriting_chain.run,
            description="This tool is useful to answer queries regarding the website content",
        ),
        return tool
    
    def create_instagram_copywriting_tool(self, input_topic, input_tone):
        copywriting_template = """Rewrite the copywriting below into a more instagram based copywriting in a {tone} tone:
                        General copywriting: {copywriting}
                        Intagram copywriting:"""

        copywriting_prompt = PromptTemplate(
            template=copywriting_template, input_variables=["copywriting", "tone"]
        )
        
        copywriting_prompt.format(topic=input_topic, tone=input_tone)
        copywriting_chain = LLMChain(llm=self.llm, prompt=copywriting_prompt)
        
        
        tool = Tool(
            name="Copywriting tool",
            func=copywriting_chain.run,
            description="This tool is useful to answer queries regarding the website content",
        ),
        return tool
        
    
    def hashtags_generation_agent(self, doc_context, input_topic):
        copywriting_template = """Based on the copywriting below, generate relevant hashtags to use:
                        Copywriting: {topic}
                        Hashtags:"""

        copywriting_prompt = PromptTemplate(
            template=copywriting_template, input_variables=["context", "topic"]
        )
        copywriting_prompt.format(context=doc_context, topic=input_topic)
        copywriting_chain = LLMChain(llm=self.llm, prompt=copywriting_prompt)
        
        tools = [
            Tool(
                name="Hashtag generation tool",
                func=copywriting_chain.run,
                description="This tool is useful to answer queries regarding the website content",
            ),
        ]
        
        agent = initialize_agent(llm=self.llm, tools=tools, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, max_iterations=10, max_execution_time=10, early_stopping_method="generate", verbose=True)
        return agent
        