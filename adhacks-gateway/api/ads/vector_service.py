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
from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter


class VectorService:
    
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings()
    
    def create_company_profile(self, index_name, company_name, company_description, company_website, company_industry_type):
        
        content = f"""
         Company Name: 
         {company_name}
         
         Company Description: 
         {company_description}
         
         Company Website: 
         {company_website}
         
         Company Industry: 
         {company_industry_type}
        
        """
        
        docs = [
            Document(
                page_content=content,
                metadata={"year":2023, "industry_type": company_industry_type}
            ),
        ]
        
        Chroma.from_documents(docs, self.embeddings, collection_name=index_name, persist_directory=".chromadb/")
        
    def upload_doc(self, filename, index_name):
        destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs')
        doc_path = os.path.join(destination_folder, filename)
        loader = PyPDFLoader(doc_path)
        texts = loader.load_and_split(text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0))
        Chroma.from_documents(texts, self.embeddings, collection_name=index_name, persist_directory=".chromadb/")
        
    def indexing(self, name, query):
        index = Chroma(collection_name=name, persist_directory=".chromadb/", embedding_function=self.embeddings)
        result = index.similarity_search(query)
        return result
    
    def upsert_new_index(self, name, content, type):
        docs = [
            Document(
                page_content=content,
                metadata={"year":2023, "type":type}
            ),
        ]
        Chroma.from_documents(docs, self.embeddings, collection_name=name, persist_directory=".chromadb/")