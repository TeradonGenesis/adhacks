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
from langchain.vectorstores import Pinecone
from pexels_api import API


from langchain.cache import SQLiteCache
langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

load_dotenv()
import pinecone
class CopywritingAgent:
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.environ.get('OPENAI_API_KEY'))
    
    ### 1. Access company data
    ### 2. Access market research data
    ### 3. llm chain to correlate company and advertising objectives to know what you are selling and use previous market research data to your advantage
    ### 4. Come up with a general advertising copywriting with a certain tone
    
    def create_general_copywriting_chain(self, company_index_name, objectives, target, tone):
        business = self.company_question_answering_chain(company_index_name, "What is the company's business and what are they selling?")
        strategy = self.company_question_answering_chain(f"{company_index_name}-market-research", "What is the company's unique selling point and marketing strategies?")
        
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
        characters = self.domain_question_answering_chain("instagram-kb-index", "What is the preferred number of charcters for a instagram post?")
        day = self.domain_question_answering_chain("instagram-kb-index", "What is the best day to post to instagram? Return only the day")
        time = self.domain_question_answering_chain("instagram-kb-index", "What is the best time to post to instagram? Return only the time")
        
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
    
    def create_hashtags(self, general_ad_copywriting):
        hashtags_template = """Based on the copywriting below, generate relevant hashtags to use:
                        Copywriting: {copywright}
                        Hashtags:"""

        hashtags_prompt = PromptTemplate(
            template=hashtags_template, input_variables=["copywright"]
        )
        hashtags_chain = LLMChain(llm=self.llm, prompt=hashtags_prompt, output_key="hashtags")
        hashtags = hashtags_chain.run({"copywright": general_ad_copywriting})
        return hashtags
    
    def company_question_answering_chain(self, name, query):
        search = Chroma(collection_name=name, persist_directory=".chromadb/", embedding_function=OpenAIEmbeddings())
        qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=search.as_retriever())
        return qa.run(query)
    
    def domain_question_answering_chain(self, name, query):
        pinecone.init(
            api_key=os.environ.get('PINECONE_API_KEY'),
            environment=os.environ.get('PINECONE_API_ENV')
        )
        docsearch = Pinecone.from_existing_index(name, OpenAIEmbeddings())
        qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=docsearch.as_retriever())
        return qa.run(query)
    
    def find_photos(self, ad_copywriting):
        pic_template = """Based on the copywriting below, suggest the best picture to be used to accompany the copywriting for an instagram post. 
        The picture description should not be more than 5 words:
                        Copywriting: {copywright}
                        Picture description:"""

        pic_prompt = PromptTemplate(
            template=pic_template, input_variables=["copywright"]
        )
        pic_chain = LLMChain(llm=self.llm, prompt=pic_prompt)
        pic_desc = pic_chain.run({"copywright": ad_copywriting})
        print(pic_desc)
        api = API(os.environ.get('PEXELS_API_KEY'))
        
        api.search(pic_desc, page=1, results_per_page=5)
        # Get photo entries
        photos = api.get_entries()
        # Loop the five photos
        photo = photos[0]
        print('Photographer: ', photo.photographer)
        # Print url
        print('Photo url: ', photo.url)
        # Print original size url
        print('Photo original size: ', photo.original)
        return photo.url
    
    def find_videos(self, ad_copywriting):
        pic_template = """Based on the copywriting below, suggest the best video scenario to be used to accompany the copywriting for an instagram reels post. 
        The picture description should not be more than 10 words:
                        Copywriting: {copywright}
                        Video description:"""

        pic_prompt = PromptTemplate(
            template=pic_template, input_variables=["copywright"]
        )
        pic_chain = LLMChain(llm=self.llm, prompt=pic_prompt)
        pic_desc = pic_chain.run({"copywright": ad_copywriting})
        print(pic_desc)
        api = API(os.environ.get('PEXELS_API_KEY'))
        
        videos = api.search_videos(pic_desc, page=1, results_per_page=5)
        # Get photo entries
        
        # Loop the five photos
        video = videos['videos'][0]['video_files'][0]
        
        return video["link"]
        