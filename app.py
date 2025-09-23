from flask import Flask, render_template
from flask import request, jsonify, abort
from dotenv import load_dotenv
import os

from langchain_community.llms import Cohere
from langchain_core.prompts import PromptTemplate
from langchain.chains import SequentialChain, RetrievalQA
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_chroma import Chroma


import os

app = Flask(__name__)

load_dotenv()

def load_db():
    try:
        embeddings = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"], model="embed-english-v3.0")
        vectordb = Chroma(persist_directory='db', embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(
            llm=Cohere(),
            chain_type="refine",
            retriever=vectordb.as_retriever(),
            return_source_documents=True
        )
        return qa
    except Exception as e:
        print("Error:", e)

qa = load_db()

def answer_from_knowledgebase(message):
    try:
        res = qa.invoke({"query": message})
        if not res or (isinstance(res, dict) and not res.get('result')):
            return "No relevant information found in the knowledgebase."
        return res['result'] if isinstance(res, dict) and 'result' in res else str(res)
    except IndexError:
        return "No relevant information found in the knowledgebase."
    except Exception as e:
        return f"Error searching knowledgebase: {e}"

def search_knowledgebase(message):
    # TODO: Write your code here
    sources = ""
    return sources

def answer_as_chatbot(message):

    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        return "Cohere API key not found. Please set COHERE_API_KEY in your .env file."
    chat = ChatCohere(cohere_api_key=api_key)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in Quantum Computing. Answer the user's question as helpfully as possible."),
        ("human", "{question}")
    ])
    chain = prompt | chat
    try:
        res = chain.invoke({"question": message})
    except Exception as e:
        return f"Error communicating with Cohere Chat API: {e}"
    return res.content if hasattr(res, "content") else str(res)


@app.route('/kbanswer', methods=['POST'])
def kbanswer():
    message = request.json['message']
    
    # Generate a response
    response_message = answer_from_knowledgebase(message)
    
    # Return the response as JSON
    return jsonify({'message': response_message}), 200


@app.route('/search', methods=['POST'])
def search():    
    # Search the knowledgebase and generate a response
    # (call search_knowledgebase())
    
    # Return the response as JSON
    return

@app.route('/answer', methods=['POST'])
def answer():
    message = request.json['message']
    
    # Generate a response
    response_message = answer_as_chatbot(message)
    
    # Return the response as JSON
    return jsonify({'message': response_message}), 200

@app.route("/")
def index():
    return render_template("index.html", title="")

if __name__ == "__main__":
    app.run()