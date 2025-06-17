# astAPI를 이용해서 다양한 타입의 데이터를 반환하는 예제
# 각 엔드포인트(/test1, /test2, /test3, /test4)가 서로 다른 자료형을 반환

from fastapi import FastAPI

app = FastAPI()

# /test1
@app.get("/test1")
async def root1():
  return {"name": "둘리"} # dict 타입 → FastAPI가 자동으로 JSON 응답으로 변환

# /test2
@app.get("/test2")
async def root2():
  return ["둘리", "또치", "도우너"] # list 타입 → JSON 배열로 반환

# /test3
@app.get("/test3")
async def root3():
  return "<h1>안녕?</h1>"
# str을 그대로 반환 → Content-Type은 application/json이 아니라 text/plain이 됨
# <h1> 태그가 HTML로 해석되지 않고 문자열 그대로 표시됨
# 브라우저에서 보면 그냥 <h1>안녕?</h1> 텍스트가 출력됨

# /test4
@app.get("/test4")
async def root4():
  return 1000 # int 타입 → FastAPI가 숫자를 JSON 응답으로 변환


# /test1 → 딕셔너리 반환: {"name": "둘리"}
# /test2 → 리스트 반환: ["둘리", "또치", "도우너"]
# /test3 → 문자열 반환: "<h1>안녕?</h1>" (텍스트 그대로 출력됨)
# /test4 → 정수 반환: 1000 (숫자 그대로 응답됨)