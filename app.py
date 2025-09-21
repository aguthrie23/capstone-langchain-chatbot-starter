from flask import Flask, render_template
from flask import request, jsonify, abort

from langchain_community.llms import Cohere
from langchain_core.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain_cohere import ChatCohere
from langchain.prompts import ChatPromptTemplate


import os

app = Flask(__name__)

def answer_from_knowledgebase(message):
    # TODO: Write your code here
    return ""

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
    # TODO: Write your code here
    
    # call answer_from_knowledebase(message)
        
    # Return the response as JSON
    return 

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