import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import json

from langchain import PromptTemplate, SQLDatabase
from langchain.chains import APIChain, LLMMathChain, RetrievalQA, SQLDatabaseChain, LLMChain, SimpleSequentialChain, SequentialChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents import AgentType
from langchain.memory import SimpleMemory


class CopywritingAgent:
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.environ.get('OPENAI_API_KEY'))
        self.embeddings = OpenAIEmbeddings()
    
    ### 1. Access company data
    ### 2. Access market research data
    ### 3. llm chain to correlate company and advertising objectives to know what you are selling and use previous market research data to your advantage
    ### 4. Come up with a general advertising copywriting with a certain tone
    
    def create_general_copywriting_chain(self, company_index_name, objectives, tone):
        business = self.question_answering_chain(company_index_name, "What does the company do?")
        strategy = self.question_answering_chain(f"{company_index_name}-market-research", "What is the company's unique selling point and marketing strategies?")
        
        template = """You are a advertising executive for an ad agency. Given the company descrption, marketing strategy, objectives of the advert and tone of the advert
        it is your job to write an general for that copywriting with SEOs that mateches the objectives.
        
        Company business:
        {business}
        
        Marketing strategy:
        {strategy}
        
        Objectives of the advert:
        {objective}

        Tone of the advert:
        {tone}
        
        General copywriting:
        """
        prompt_template = PromptTemplate(input_variables=["business", "strategy", "objective", "tone"], template=template)
        prompt_template.format(business = business, strategy = strategy, objective = objectives, tone = tone)
        copywriting_chain = LLMChain(llm=self.llm, prompt=prompt_template)

        data = copywriting_chain.run("Create a general copywriting for the advertising effort")
    
        return data
    
    
    def question_answering_chain(self, name, query):
        search = Chroma(collection_name=name, persist_directory=".chromadb/", embedding_function=self.embeddings)
        qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=search.as_retriever())
        return qa.run(query)
        
        
    def generate_instagram_content(self, general_ad_copywriting, tone):
        charcters = self.question_answering_chain("instagram-kb-index", "What is the prefeered number of charcters for a instagram post?")
        day = self.question_answering_chain("instagram-kb-index", "What is the day to post to instagram? Return only the day")
        time = self.question_answering_chain("instagram-kb-index", "What is the best time to post to instagram? Return only the time")
        
        copywriting_template = """Rewrite the copywriting below into a more instagram compliant copywriting:
                        General copywriting: {copywriting}
                        Intagram copywriting:"""

        copywriting_prompt = PromptTemplate(
            template=copywriting_template, input_variables=["copywriting"]
        )
        
        copywriting_chain = LLMChain(llm=self.llm, prompt=copywriting_prompt)
        
        hashtags_template = """Based on the copywriting below, generate relevant hashtags to use:
                        Copywriting: {instagram_copywriting}
                        Hashtags:"""

        hashtags_prompt = PromptTemplate(
            template=hashtags_template, input_variables=["instagram_copywriting"]
        )
        hashtags_chain = LLMChain(llm=self.llm, prompt=hashtags_prompt)
        
        
        template = """You are a social media manager for an instagram account.  Given the general copywriting, 
        the best number of charcters for the post, the day of the instagram post, the time of the post, it is your job to write an instagram post for that copywriting.
        Here is some context about the day, time and characters of the posting
        Day: {day}
        Time: {time}
        
        Number of characters:
        {characters}

        Intagram copywriting:
        {copywriting}
        
        Intagram hashtags:
        {hashtags}
        
        Instagram Post:
        """
        prompt_template = PromptTemplate(input_variables=["day", "time", "characters", "copywriting"], template=template)
        social_chain = LLMChain(llm=self.llm, prompt=prompt_template, output_key="social_post_text")

        overall_chain = SequentialChain(
            memory=SimpleMemory(memories={"day": day, "time": time, "charcters": charcters, "copywriting": general_ad_copywriting}),
            chains=[copywriting_chain, hashtags_chain, social_chain],
            input_variables=["copywriting"],
            # Here we return multiple variables
            output_variables=["social_post_text"],
            verbose=True)

        json_data = overall_chain({"copywriting":general_ad_copywriting})
        return json_data

        