import os

import streamlit as st
from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

#load gemini API
load_dotenv()

#create settings
Settings.llm = GoogleGenAI(model="gemini-2.5-flash")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

#add title
st.title("Babson Handbook Chatbot")

#build the query/index student handbook
@st.cache_resource
def build_query_engine():
    st.write("🔄 Loading...")
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


query_engine = build_query_engine()

#ask user for a question
question = st.text_input("Ask a question about the Babson student handbook:")

#when user submits question, put question through query created and output response
if st.button("Submit") and question:
    response = query_engine.query(question)
    st.write("Response:")
    st.write(str(response))



