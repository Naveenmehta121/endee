from fastapi import FastAPI
from search import search

app = FastAPI(title="DevAssist AI API")

@app.get("/")
def home():
    return {"message": "DevAssist AI API"}

@app.get("/ask")
def ask(question: str):
    # Retrieve relevant documents purely from Vector Database semantic search
    results = search(question)
    
    return {
        "question": question,
        "results": results
    }
