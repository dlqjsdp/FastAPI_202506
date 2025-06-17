from typing import Union
from fastapi import FastAPI, Query
# Union은 여러 타입 중 하나를 허용하는 타입 힌트를 의미함.
# 예: Union[str, None]은 문자열이거나 None일 수 있다는 뜻 (즉, Optional)

# FastAPI: API 서버를 만들기 위한 메인 클래스.
# Query: 쿼리 파라미터에 대한 유효성 검사나 메타데이터를 설정할 수 있는 도우미.


app = FastAPI() # FastAPI 애플리케이션 인스턴스를 생성함. 이후 라우팅 함수들과 연결됨.

# /items1/ – 쿼리 문자열에 제한 없음
@app.get("/items1/")
async def read_items1(q: Union[str, None] = None): # q는 쿼리 파라미터. 문자열이거나 None일 수 있고, 기본값은 None이므로 생략 가능함.
  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]} # 초기 응답 데이터를 미리 정의. items라는 키에 리스트 형태로 두 개의 아이템이 있음.
  if q:
    results.update({"q": q}) # q가 존재하면, 결과에 q 값을 추가로 포함시킴.
  return results # 최종적으로 딕셔너리 형태의 JSON 응답을 반환함.

# /items2/ — 최소 5자, 최대 50자 문자열만 허용
@app.get("/items2/")
async def read_items2(q: Union[str, None] = Query(default=None, min_length=5, max_length=50)):
  # q는 쿼리 파라미터로 문자열이거나 None일 수 있음.
  # Query()는 FastAPI에서 유효성 검사 설정용 함수. 
    # default=None: 생략 가능하게 설정
    # min_length=5: 최소 5자 이상
    # max_length=50: 최대 50자 이하
  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
  if q:
    results.update({"q": q})
  return results
# items1과 로직은 동일하지만 q에 대한 유효성 검사가 추가됨.

# /items3/ — unico로 시작하고 3~10자여야 함
@app.get("/items3/")
async def read_items3(q: Union[str, None] = Query(default=None, min_length=3, max_length=10, pattern="^unico")):
  # q는 쿼리 파라미터로 None이거나 문자열일 수 있음.
  # Query()로 다음 조건들이 붙음:
    # 최소 3자, 최대 10자
    # pattern="^unico": 정규표현식. 문자열이 unico로 시작해야 함
  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
  if q:
    results.update({"q": q})
  return results
# items 리스트를 반환하고, q가 있으면 추가로 포함.


# items1은 아무 조건 없음
# items2는 길이 조건만 있음
# items3은 길이 조건 + "unico"로 시작하는지 검사함


# 각 함수는 공통적으로 q라는 쿼리 파라미터를 사용하지만, 
# items2와 items3은 유효성 검사가 들어가고, 
# items3은 패턴 검사까지 포함되어 있어 더 엄격한 필터를 적용하는 구조

