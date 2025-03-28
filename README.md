
# Scalable, Low-Latency LLM QnA

## Overview
This project is a **Retrieval-Augmented Generation (RAG) QnA ** built to provide low-latency, scalable question-answering capabilities using various technologies, including **Redis**, **FAISS**, and **Gemini (Google’s LLM)**. It uses **FastAPI**, **Gunicorn**, and **Uvicorn** to handle asynchronous, multi-worker scalable requests and is deployed using **Docker** for easy orchestration.

The assistant intelligently routes queries to the most efficient backend system:
1. **Redis**: For <1ms cache hits on exact matches.
2. **FAISS**: For semantic search fallback when no exact matches are found.
3. **Gemini (Google's LLM)**: For final fallback when other systems cannot provide an answer.

## Technologies Used
- **Backend Framework**: FastAPI + Uvicorn + Gunicorn
- **Caching**: Redis (In-memory key-value store for fast retrieval)
- **Vector Search**: FAISS (Semantic search engine for finding similar content)
- **LLM API**: Gemini 1.5 Flash (Google's Large Language Model for generative responses)
- **Async Tasking**: asyncio for handling asynchronous tasks
- **Containerization**: Docker for deployment and scalability
- **Deployment**: Docker Compose for container orchestration

## Key Features
- **Low-Latency Performance**: Uses Redis and FAISS for ultra-fast query response times (<5ms for most queries).
- **Scalability**: Leveraging FastAPI, Gunicorn, and Uvicorn to handle high concurrency.
- **Graceful Fallback**: Uses Gemini (Google's LLM) only when Redis and FAISS cannot provide an answer.
- **Dockerized Deployment**: Easy setup and deployment through Docker containers.

## Architecture
1. **User Query** is received and routed to **Redis** for an exact match.
2. If no result is found in Redis, the query is forwarded to **FAISS** for semantic search.
3. If FAISS cannot find a matching answer, the query is sent to **Gemini** for generation.
4. **Redis** and **FAISS** are used for caching answers and ensuring that future queries are answered quickly.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Install Dependencies
It is recommended to use a virtual environment. You can use **conda** or **venv**:

```bash
conda create -p venv python==3.10
conda activate venv
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the project directory and add the following (replace `<your_api_key>` with your actual Gemini API key):

```bash
GEMINI_API_KEY=<your_api_key>
```

### 4. Running the Application
Use Docker to run the app. This ensures that all dependencies and services are correctly set up in a containerized environment:

```bash
docker-compose up --build
```

This will start the FastAPI application and Redis container.

### 5. Running the Frontend
Once the backend is running, the frontend (Streamlit) can be started with the following command:

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser to access the application.

## Query Handling Flow
- **Redis Cache**: Queries that have been previously asked are returned immediately from Redis.
- **FAISS**: If the query is semantically similar to a stored answer but does not exactly match, it will be answered using FAISS.
- **Gemini (Google's LLM)**: If neither Redis nor FAISS provides a satisfactory answer, Gemini is called to generate a response. The system caches and refines answers over time to improve future responses.

## Latency Breakdown
- **Redis**: ~1ms for cache hits
- **FAISS**: ~3ms for semantic search
- **Gemini**: ~400ms (only invoked when necessary)

## Future Enhancements
- **Multi-language support**: Extend the assistant to support multiple languages.
- **Streaming response optimization**: Implement real-time streaming for longer queries using Gemini's API.
- **Deployment**: Consider deploying to cloud platforms like AWS or Google Cloud to scale further.
- **Real-time analytics**: Implement a feedback loop to improve answers based on user input.


