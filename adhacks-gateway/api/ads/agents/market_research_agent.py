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
from langchain.chains.summarize import load_summarize_chain

from llama_index import download_loader


class ResearchAgent:
    
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.environ.get('OPENAI_API_KEY'))
        self.embeddings = OpenAIEmbeddings()
    
    # talking to the uploading resources
    def check_similar_marketing_strategies(self, company_index_name, company_description):
        competitor_context = self.indexing(f"{company_index_name}-competitors", "Marketing strategies of the competitors")
        
        selling_template = """
        Use the competitor's marketing strategies as context to write 
        a short blog post to of how the company can emulate the marketing strategies:
        
        Context: {context}
        Company: {company_description}
        
        Topic: {topic}
        
        Blog post:"""

        marketing_prompt = PromptTemplate(
            template=selling_template, input_variables=["context", "topic", "company"]
        )
        marketing_prompt.format(context=competitor_context, company=company_description, topic=f"Check the competitors marketing strategies and figure out how it can be adopted for the company")
        marketing_chain = LLMChain(llm=self.llm, prompt=marketing_prompt)
        return marketing_chain
    
    def create_unique_selling_points(self, company_index_name, company_selling_points):
        
        competitor_context = self.indexing(f"{company_index_name}-competitors", "Unique selling points of competitors")
        
        selling_template = """
        Use the competitor's unique selling points as context to write 
        a short blog post to compare the context and company selling points:
        
        Context: {context}
        Company: {company}
        
        Topic: {topic}
        
        Blog post:"""

        selling_prompt = PromptTemplate(
            template=selling_template, input_variables=["context", "topic", "company"]
        )
        selling_prompt.format(context=competitor_context, company=company_selling_points, topic=f"Compare the the competitors unique selling point against the {company_index_name} unique selling points and mention how the company can stand out")
        selling_chain = LLMChain(llm=self.llm, prompt=selling_prompt)
        return selling_chain
    
    def scrape_competitor_data(self, result, company_index_name):
        summary_chain = load_summarize_chain(self.llm, chain_type="stuff")
        search_term = summary_chain.run(input_documents=result, question="""
                                    Write a short google search term the business the company is in and the targeted location ad in less than 10 words
                                    Example: Milk tea franchise store in Kuching
                                    """)
    
        competitor_link = self.get_search_results_link(search_term)
        competitor_marketing_link = self.get_search_results_link(f"how to promote {search_term} and its marketing / advertising strategies")
        
        self.scrape_websites([competitor_link, competitor_marketing_link], f"{company_index_name}-competitors")
    
    def get_search_results_link(self, search_term: str):
        link = ""
        wrapper = GoogleSerperAPIWrapper()
        metadata = wrapper.results(search_term)
        data = json.loads(metadata)
        if "organic" in data:
            if len(data["organic"]) > 0:
                link = data["organic"][0]["link"]
        return link
    
    def scrape_websites(self, links, name):
        BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
        loader = BeautifulSoupWebReader()
        web_data = loader.load_data(urls=links)
        Chroma.from_documents(web_data, self.embeddings, collection_name=name, persist_directory=".chromadb/")
     
    def indexing(self, name, query):
        index = Chroma(collection_name=name, persist_directory=".chromadb/", embedding_function=self.embeddings)
        result = index.similarity_search(query)
        return result
        