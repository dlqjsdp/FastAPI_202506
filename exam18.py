from fastapi import FastAPI
from contextlib import asynccontextmanager
import random

app = FastAPI()

friends = []
@asynccontextmanager
async def startup(app: FastAPI):
  print("UVICORN에 의해 서버가 기동될 때 실행됩니다요~~~")
  friends.extend(["둘리", "또치", "도우너", "희동이", "마이콜"])
  yield
  print("UVICORN이 종료될 때 실행됩니다요~~~")

app = FastAPI(lifespan=startup)

@app.get("/myfriend")
async def main():
  return {"myfriend" : random.choice(friends)}


