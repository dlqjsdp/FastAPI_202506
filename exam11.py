# FastAPI를 사용해 **상품 정보 등록(POST)**과 **수정(PUT)**을 처리하는 API를 제공
# Pydantic의 BaseModel을 통해 데이터 구조와 유효성 검사도 같이 처리
from fastapi import FastAPI
from pydantic import BaseModel

# Item 모델 정의
class Item(BaseModel):
    name: str # name: 상품명 (필수)
    description: str | None = None # description: 설명 (선택, 없을 수 있음)
    price: float # price: 가격 (필수, 실수형)
    tax: float | None = None # tax: 세금 (선택, 없을 수 있음)


app = FastAPI()

# POST /items – 새 상품 등록
@app.post("/items", status_code=201) # 응답 코드: 201 Created
# POST /items로 JSON 데이터를 전송하면 Item 모델로 변환됨
async def create_item(item: Item):
  item_dict = item.model_dump() # Pydantic의 model_dump()로 객체를 딕셔너리로 변환
  print(item_dict)
  if item.tax: # 세금이 존재하는 경우 price_with_tax 필드를 추가해서 최종 금액 계산
    price_with_tax = item.price + item.tax
    item_dict.update({"price_with_tax": price_with_tax})
  return item_dict # 모든 정보(필드 + 계산된 세금 포함)를 JSON으로 응답

# PUT /items/{item_id} – 기존 상품 수정
@app.put("/items/{item_id}") # 경로 파라미터로 item_id를 받아서 특정 아이템을 수정한다고 가정
async def update_item(item_id: int, item: Item): # 본문에는 수정할 데이터를 Item 모델 형태로 받음
  return {"item_id": item_id, **item.model_dump()} # 기존 item_id에 새 데이터 값을 덧붙여서 JSON으로 반환


# 요약
  # POST /items	: 새 아이템 등록, 세금 계산 포함
  # PUT /items/{item_id} : 아이템 ID에 해당하는 데이터 수정
  # model_dump() : Item 객체를 딕셔너리로 변환
  # price_with_tax : 세금이 포함된 총 가격 (선택적으로 추가됨)
