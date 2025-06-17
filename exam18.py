# FastAPI의 새로운 lifespan 기능과 @asynccontextmanager를 활용해서, 
# 서버의 시작과 종료 시점에 특정 작업을 수행하는 구조
from fastapi import FastAPI
from contextlib import asynccontextmanager
import random

app = FastAPI()

friends = []

# @asynccontextmanager로 lifespan 정의
@asynccontextmanager
async def startup(app: FastAPI): # 서버 시작 전:
  print("UVICORN에 의해 서버가 기동될 때 실행됩니다요~~~") # 콘솔에 메시지 출력
  friends.extend(["둘리", "또치", "도우너", "희동이", "마이콜"]) # friends 리스트에 캐릭터들 추가
  yield # 서버 종료 시:
  print("UVICORN이 종료될 때 실행됩니다요~~~") # yield 이후의 코드 실행 → 종료 메시지 출력

# app = FastAPI(lifespan=startup)
app = FastAPI(lifespan=startup)
# lifespan 파라미터로 startup() 컨텍스트를 전달
# → 이로 인해 FastAPI는 서버 시작과 종료 시 startup()을 자동 호출함

# /myfriend 엔드포인트
@app.get("/myfriend")
async def main():
  return {"myfriend" : random.choice(friends)}
# /myfriend로 요청하면 friends 리스트에서 랜덤으로 하나를 반환


# 주요 개념 요약
  # lifespan: 서버가 시작될 때와 종료될 때 실행되는 코드를 정의하는 기능 (FastAPI 0.95+에서 공식 도입됨)
  # @asynccontextmanager: async with 구조에서 사용할 수 있는 비동기 컨텍스트 관리자
  # friends: 전역 리스트로, 서버가 시작할 때 초기값이 채워짐


# 실행 흐름 요약
# 1. uvicorn 실행 시:
  # "서버가 기동될 때 실행됩니다요~~~" 출력
  # friends 리스트에 값 추가
# 2. 사용자가 /myfriend 호출 시:
  # 리스트에서 랜덤으로 친구 하나를 선택하여 JSON으로 응답
# 3. 서버 종료 시:
  # "UVICORN이 종료될 때 실행됩니다요~~~" 출력


# 참고사항
  # lifespan은 기존의 @app.on_event("startup"), @app.on_event("shutdown")보다 더 명확한 구조를 제공함
  # friends 리스트는 전역 변수이므로 여러 요청 간에 공유됨 (주의 필요)


