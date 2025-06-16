from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pgvector.psycopg import register_vector
import psycopg
import numpy as np
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from transformers import pipeline

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the AI model
    ml_model["embedding_model"] = SentenceTransformer("upskyy/bge-m3-korean", device="cpu")
    ml_model["lm_model"] = pipeline("text-generation", model="google/gemma-3-1b-it")
    print("AI 모델 로드 완료")
    yield
    ml_model.clear()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5501",
    "http://127.0.0.1:5501"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/rag")
async def rag(query : str):
    conn = psycopg.connect(dbname='edudb', user='edu', password='1234', autocommit=True)
    conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
    register_vector(conn)

    input = 'search_query: '+query
    embedding =  ml_model["embedding_model"].encode(input)

    result = conn.execute(
        'SELECT content FROM hotel ORDER BY embedding <=> %s LIMIT 1', (np.array(embedding),)).fetchall()

    context = '\n\n'.join([row[0] for row in result])
    context = context[2:]

    prompt = f'Answer this question: {query}\n\n{context}'

    response = ml_model["lm_model"](prompt)
    print(response)
    return {"message": response}




