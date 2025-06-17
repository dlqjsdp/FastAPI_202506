# FastAPI를 활용해서 쿼리 파라미터와 경로 파라미터를 동시에 사용하는 예제
# 리스트 데이터를 부분적으로 조회할 수 있는 페이징 처리 구조도 포함
from fastapi import FastAPI

app = FastAPI()

# /items – 페이징 처리
fake_items_db = [{"item_name": "Dooly"}, {"item_name": "Ddochi"}, {"item_name": "Dauner"}, {"item_name": "Olaf"}]

# /items – 페이징 처리
@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10): 
  # skip: 몇 개를 건너뛸지 (start index), limit: 최대 몇 개를 가져올지 (count)
  print(skip, " : ", limit)
  return fake_items_db[skip : skip + limit] # fake_items_db[skip : skip + limit] → 슬라이싱 사용

# /items/{item_id} – 경로 + 선택 쿼리 파라미터
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
  # item_id: URL 경로에서 직접 받음 (필수), q: 쿼리 파라미터, 선택사항 (str | None)
  if q:
    return {"item_id": item_id, "q": q}
  return {"item_id": item_id}

# 정리
  # /items → skip과 limit 쿼리 파라미터로 리스트 일부만 조회 가능 (페이징)
  # /items/{item_id} → 특정 항목 조회하며, q라는 선택적 쿼리 파라미터도 사용 가능