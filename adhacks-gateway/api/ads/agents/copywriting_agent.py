import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import json

import langchain
from langchain import PromptTemplate
from langchain.chains import APIChain, LLMMathChain, RetrievalQA, SQLDatabaseChain, LLMChain, SequentialChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents import AgentType
from langchain.memory import SimpleMemory

from langchain.cache import SQLiteCache
langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

load_dotenv()

class CopywritingAgent:
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.environ.get('OPENAI_API_KEY'))
    
    ### 1. Access company data
    ### 2. Access market research data
    ### 3. llm chain to correlate company and advertising objectives to know what you are selling and use previous market research data to your advantage
    ### 4. Come up with a general advertising copywriting with a certain tone
    
    def create_general_copywriting_chain(self, company_index_name, objectives, target, tone):
        business = self.question_answering_chain(company_index_name, "What is the company's business amd what are they selling?")
        strategy = self.question_answering_chain(f"{company_index_name}-market-research", "What is the company's unique selling point and marketing strategies?")
        
        template = """You are a advertising executive for an ad agency. Given the company descrption, marketing strategy, objectives of the advert, tone of the advert, target market,
        it is your job to write an general for that copywriting with SEOs that mateches the objectives.
        
        Company business:
        {business}
        
        Marketing strategy:
        {strategy}
        
        Target market:
        {target}
        
        Objectives of the advert:
        {objective}

        Tone of the advert:
        {tone}
        
        General copywriting:
        """
        prompt_template = PromptTemplate(input_variables=["business", "strategy", "target", "objective", "tone"], template=template)
        copywriting_chain = LLMChain(llm=self.llm, prompt=prompt_template)

        data = copywriting_chain.run(business = business, strategy = strategy, target = target, objective = objectives, tone = tone)
    
        return data
        
    def generate_instagram_content(self, general_ad_copywriting):
        characters = self.question_answering_chain("instagram-kb-index", "What is the preferred number of charcters for a instagram post?")
        day = self.question_answering_chain("instagram-kb-index", "What is the day to post to instagram? Return only the day")
        time = self.question_answering_chain("instagram-kb-index", "What is the best time to post to instagram? Return only the time")
        
        template = """You are a social media manager for an instagram account.  Given the general copywriting, 
        the best number of charcters for the post, the day of the instagram post, the time of the post, it is your job to write an instagram post for that copywriting.
        Here is some context about the day, time and characters of the posting
        
        Day: {day}
        Time: {time}
        
        Number of characters:
        {characters}
        
        Intagram copywriting:
        {copywriting}
        
        Instagram Post:
        """
        prompt_template = PromptTemplate(input_variables=["day", "time", "characters", "copywriting"], template=template)
        social_chain = LLMChain(llm=self.llm, prompt=prompt_template)

        post = social_chain.run({"day": day, "time": time, "characters": characters, "copywriting": general_ad_copywriting})
        return {"post": post, "day": day, "time": time}
    
    def question_answering_chain(self, name, query):
        search = Chroma(collection_name=name, persist_directory=".chromadb/", embedding_function=OpenAIEmbeddings())
        qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=search.as_retriever())
        return qa.run(query)

        