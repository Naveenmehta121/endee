# DevAssist AI – Developer Knowledge Assistant

## 1. Project Title and Introduction

DevAssist AI is an AI-powered developer assistant that answers programming questions by retrieving relevant documentation using vector similarity search. This project is built as part of an **Endee.io internship assessment**.

It demonstrates how modern AI systems combine embeddings, vector databases, and retrieval pipelines to build intelligent applications. Vector databases are crucial in modern AI because they allow for semantic search—finding information based on meaning rather than just exact keyword matches—which is the foundation of Retrieval-Augmented Generation (RAG).

## 2. Demo / Features

* **Semantic Search**: Find relevant developer documentation based on the meaning of the query.
* **Embedding Generation**: Utilizes Sentence Transformers (`all-MiniLM-L6-v2`) to convert text into high-dimensional vector representations.
* **Vector Similarity Search Pipeline**: Efficiently retrieves the most relevant context using cosine similarity.
* **REST API Integration**: Demonstrates integration with the Endee vector database via standard REST endpoints.
* **Robust Fallback**: Includes a local NumPy-based fallback mechanism for seamless development and testing when the Endee Docker container is unavailable.
* **FastAPI Backend**: A high-performance, asynchronous REST API for executing search queries.
* **Streamlit Frontend**: A polished, modern, and interactive chat-like user interface.
* **Clean Modular Architecture**: Separation of concerns between ingestion, searching, API routing, and the user interface.

## 3. System Architecture

The AI pipeline follows a standard Retrieval-Augmented Generation (RAG) pattern (without the final LLM generation step for this scope):

```text
User Question 
      │
      ▼
Embedding Model (all-MiniLM-L6-v2)  ──────►  Converts text to Vector
      │
      ▼
Vector Database (Endee / NumPy fallback) ──►  Performs Similarity Search
      │
      ▼
Retrieved Context (Top K Documents)
      │
      ▼
Streamlit UI Display
```

## 4. Project Structure

```text
endee-dev-assistant/
│
├── backend/
│   ├── main.py        # FastAPI server endpoints
│   ├── ingest.py      # Embedding generation and Endee DB insertion
│   ├── search.py      # Vector similarity search logic
│   └── rag.py         # Search abstraction layer
│
├── frontend/
│   └── app.py         # Streamlit user interface
│
├── data/              # Knowledge base documents and saved embeddings
│
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## 5. How Endee Vector Database is Used

The system integrates with the Endee vector database using its REST API. During development, the vector search pipeline is implemented locally with a precise mock. In production, the embeddings are inserted and queried using Endee endpoints:

* **Ingestion:** Text chunks are embedded and sent to Endee for storage alongside their original text metadata.
  * `POST /api/v1/vectors/insert`
* **Retrieval:** User queries are embedded and sent to Endee to perform a similarity search, returning the closest matching documents.
  * `POST /api/v1/vectors/search`

## 6. Installation and Setup

### Prerequisites
* Python 3.8+
* Docker (Optional, for running the Endee server)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd endee-dev-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run embedding ingestion script**
   This script reads the knowledge base, generates embeddings, and inserts them into the vector database (or saves them locally for the fallback).
   ```bash
   cd backend
   python ingest.py
   ```

4. **Start FastAPI backend**
   Keep the backend running in a separate terminal.
   ```bash
   uvicorn main:app --port 8000
   ```

5. **Run Streamlit frontend**
   Open a new terminal, navigate to the frontend folder, and start the UI.
   ```bash
   cd ../frontend
   streamlit run app.py
   ```
   The application will automatically open in your browser at `http://localhost:8501`.

## 7. Example Queries

Try asking the assistant:
* *Explain binary search*
* *What are React hooks*
* *What is FastAPI*

## 8. Future Improvements

* **Full RAG pipeline with LLM**: Pass the retrieved context to an LLM (like GPT-4 or Claude) to generate conversational answers instead of just displaying the raw context.
* **Larger datasets**: Ingest thousands of documentation pages from frameworks like React, FastAPI, or Pandas.
* **Multi-language support**: Use multilingual embedding models to allow queries in different languages.
* **Production deployment**: Containerize the FastAPI and Streamlit apps using Docker and deploy to AWS, GCP, or a PaaS like Render.

## 9. Conclusion

This project successfully demonstrates the core infrastructure required to build modern, context-aware AI applications. By implementing a vector search pipeline that integrates with the Endee vector database, it showcases practical skills in embedding generation, similarity search, API development, and robust error handling—key components of any enterprise AI system.
