# FastAPI에서 경로 파라미터(Path Parameter)*와 예외 처리, 유효성 검사를 사용하는 예제
from fastapi import FastAPI, Path, HTTPException
from typing import Annotated


app = FastAPI()

items = {"dooly": "귀여운 아기 공룡"} # 여기서 "dooly"라는 키만 등록되어 있음.
# items는 간단한 딕셔너리. 키는 아이템 ID, 값은 설명.

# /items/{item_id} – 존재 여부 검사 + 예외 처리
@app.get("/items/{item_id}") # item_id는 URL 경로에서 직접 받음 (예: /items/dooly)
async def read_item(item_id: str): # 문자열로 받으며, items 딕셔너리에 키가 있는지 확인함.
    if item_id not in items: # items에 해당 ID가 없으면 HTTPException을 발생시켜 404 오류 반환.
      raise HTTPException(status_code=404, detail=f"{item_id} 명의 아이템은 존재하지 않습니다.")
    return {"item": items[item_id]} # 존재할 경우 해당 설명을 포함한 JSON 반환.

# /items2/{item_id} – 숫자만 허용 + 쿼리 문자열
@app.get("/items2/{item_id}") 
async def read_item2(item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
                    q: str = 'unico'): 
    # item_id: 경로 파라미터이며, int형으로 받고 1 이상의 값만 허용됨 (ge=1)
    # title: Swagger 문서에 보일 설명, q: 쿼리 파라미터. 기본값 'unico'
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results # item_id와 q를 JSON으로 반환함.


# /items/{item_id}는 문자열 기반이고, 없는 항목이면 404 오류 반환.
# /items2/{item_id}는 정수만 허용하고, 1 이상이어야 하며 쿼리 파라미터도 함께 받을 수 있음.

