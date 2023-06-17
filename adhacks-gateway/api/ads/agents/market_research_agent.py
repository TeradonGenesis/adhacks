import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import json

from bs4 import BeautifulSoup
import langchain
from langchain import PromptTemplate, SQLDatabase
from langchain.chains import APIChain, LLMMathChain, RetrievalQA, SQLDatabaseChain
from langchain.experimental.plan_and_execute import  load_agent_executor, load_chat_planner
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
import requests
from llama_index import download_loader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.schema import Document

from langchain.cache import SQLiteCache
langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

load_dotenv()

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
        Company: {company}
        
        Topic: {topic}
        
        Blog post:"""

        marketing_prompt = PromptTemplate(
            template=selling_template, input_variables=["context", "company", "topic"]
        )
        marketing_chain = LLMChain(llm=self.llm, prompt=marketing_prompt)
        message = marketing_chain.run(context=competitor_context, company=company_description, topic=f"Check the competitors marketing strategies and figure out how it can be adopted for the company")
        return message
        
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
        selling_chain = LLMChain(llm=self.llm, prompt=selling_prompt)
        message = selling_chain.run(context=competitor_context, company=company_selling_points, topic=f"Compare the the competitors unique selling point against the {company_index_name} unique selling points and mention how the company can stand out")
        return message
    
    def scrape_competitor_data(self, company_index_name):

        docsearch = Chroma(collection_name=company_index_name, persist_directory=".chromadb/", embedding_function=self.embeddings)
        qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=docsearch.as_retriever())
        search_term = qa.run("What type of business is the company operating in and what are they selling? Limit the number of words to only 5")
        
        print(search_term)
        print(company_index_name)
        competitor_link = self.get_search_results_link(search_term)
        competitor_marketing_link = self.get_search_results_link("how to promote "+ search_term + " and its marketing / advertising strategies")
        competitor_index_name = company_index_name + "-competitors"
        print(competitor_index_name)
        self.scrape_websites(competitor_link, competitor_index_name)
        self.scrape_websites(competitor_marketing_link, competitor_index_name)
    
    def get_search_results_link(self, search_term: str):
        link = ""
        wrapper = GoogleSerperAPIWrapper(serper_api_key=os.environ.get('SERPER_API_KEY'))
        metadata = wrapper.results(search_term)
        if "organic" in metadata:
            if len(metadata["organic"]) > 0:
                link = metadata["organic"][0]["link"]
        return link
    
    def scrape_websites(self, link, name):
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' }
        response = requests.get(link, headers=headers)
        docs = [
            Document(
                page_content=response.text,
                metadata={"year":2023}
            ),
        ]
        Chroma.from_documents(docs, self.embeddings, collection_name=name, persist_directory=".chromadb/")
     
    def indexing(self, name, query):
        index = Chroma(collection_name=name, persist_directory=".chromadb/", embedding_function=self.embeddings)
        result = index.similarity_search(query)
        return result
        