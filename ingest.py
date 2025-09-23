import os
from dotenv import load_dotenv
load_dotenv()
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma

def ingest_documents():
    # Example documents to add
    documents = [
        "Quantum computing is a type of computation that harnesses the collective properties of quantum states.",
        "Qubits are the basic unit of quantum information.",
        "Entanglement is a key resource in quantum computing."
    ]
    metadatas = [
        {"source": "wiki"},
        {"source": "wiki"},
        {"source": "wiki"}
    ]
    embeddings = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"], model="embed-english-v3.0")
    vectordb = Chroma(persist_directory='db', embedding_function=embeddings)
    vectordb.add_texts(documents, metadatas=metadatas)
    print("Ingested documents into Chroma DB.")

if __name__ == "__main__":
    ingest_documents()
