# FastAPI의 경로 매개변수(Path Parameters)*를 사용하는 예제
# 두 개의 엔드포인트가 정의되어 있고, 각각 URL 경로 안의 값을 변수처럼 받아서 처리
from fastapi import FastAPI

app = FastAPI()

# /items/{item_id}
@app.get("/items/{item_id}")
def read_item(item_id): # item_id는 자료형 미지정이므로 기본적으로 문자열(str)로 처리됨
  return {"item_id": item_id}
# 자료형을 명시하고 싶다면 item_id: int 또는 item_id: str처럼 쓰는 것이 권장

# /friend/{name}/{age}
@app.get("/friend/{name}/{age}")
async def read_item(name : str, age : int): # name: 문자열, age: 정수
  return {"이름": name, "나이" : age}
# FastAPI가 자동으로 age를 정수로 파싱하고 유효성 검사도 해줌
# /friend/둘리/hello처럼 숫자가 아닌 값을 age에 넣으면 422 오류가 발생


# 전체 구조 요약
  # /items/{item_id} → 경로에서 item_id 값을 받아 JSON으로 반환
  # /friend/{name}/{age} → 이름과 나이를 경로로 받아 JSON으로 반환
