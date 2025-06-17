# FastAPI 코드는 다양한 타입의 데이터를 요청받거나 응답하는 POST/GET API 예제를 포함
from typing import Any, List, Union

from fastapi import FastAPI
from pydantic import BaseModel

# List, Union: 복합 타입 선언에 사용됨.
# BaseModel: 요청/응답 데이터의 구조를 정의하는 데 사용.
# FastAPI: API 서버 생성을 위한 핵심 클래스.

app = FastAPI()

class Item(BaseModel):
  name: str # name: 필수 문자열
  description: Union[str, None] = None
  price: Union[float, None] = None
  tax: Union[float, None] = None
  # description, price, tax: 생략 가능
  tags: List[str] = [] # tags: 문자열 리스트, 기본값은 빈 리스트

# /items1 – POST 요청으로 객체 받기
@app.post("/items1", response_model=Item) # response_model=Item → 반환 결과도 Item 형태로 제한됨.
# 클라이언트가 JSON 객체를 POST하면, Item 모델로 파싱하고 그대로 반환함.
async def proc1(item: Item) -> Any: 
# JSON 요청을 받아서 Item 객체로 처리하고 응답을 반환. 반환 타입은 Any이지만 실제로는 Item을 반환함.
  return item

# /items2 – 여러 개의 Item 객체 반환 (List)
@app.get("/items2", response_model=List[Item])
async def proc2() -> List[Item]:
# 아무 요청 파라미터 없이 Item 리스트를 반환함. 응답은 항상 List[Item] 형태로 고정됨.
  return [
    {"name": "둘리", "price": 42.0},
    {"name": "또치", "price": 32.0},
    {"name": "도우너", "price": 32.0},
  ]
# 리스트 형태의 Item 객체들을 반환
# 일부 필드는 생략 가능 (예: description, tags)


my_items = [ 
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

# /items3 – 외부 리스트에서 반환
@app.get("/items3", response_model=List[Item])
async def proc3():
    return my_items
# my_items는 전역 리스트이며, 해당 내용을 List[Item] 형태로 반환


# /items4 – 문자열 키, 실수 값 딕셔너리 반환
@app.get("/items4", response_model=dict[str, float])
async def proc4():
  return {"foo": 2.3, "bar": 3.4}
# 키는 문자열, 값은 float인 딕셔너리를 반환함
# Pydantic이 타입을 강제함 (int를 넣어도 float으로 변환)


# /items1	Item 객체를 POST로 받고 그대로 반환	( 응답 타입 : 단일 객체 (Item) )
# /items2	Item 여러 개를 리스트로 반환	( 응답 타입 : 	리스트 (List[Item]) )
# /items3	전역 변수에서 리스트 반환	( 응답 타입 :  리스트 (List[Item]) )
# /items4	문자열 키, float 값 딕셔너리 반환	( 응답 타입 : 딕셔너리 (dict[str, float]) )