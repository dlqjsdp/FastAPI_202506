# FastAPI에서 정적 파일 서빙, 경로 파라미터, 쿼리 파라미터(선택/필수) 등을 종합적으로 활용한 예제
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
# /static 경로로 접속하면 로컬 디렉터리 static/ 안의 파일들을 제공함
# 예: static/hello.jpg 파일이 있을 경우 → http://localhost:8000/static/hello.jpg
# 정적 자원 제공용 (HTML, JS, CSS, 이미지) 웹 서버의 기본 기능을 FastAPI에서도 구현 가능

# /items/{item_id} – 선택적 쿼리 파라미터 포함
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
  # item_id: 경로 파라미터 (필수), q: 쿼리 파라미터 (Optional[str]), short: 불리언 타입, 기본값은 False
  item = {"item_id": item_id} # item_id는 항상 포함
  if q: # q가 있으면 추가
    item.update({"q": q})
  if not short: # short=False일 경우에만 설명(description)을 포함함
    item.update(
      {"description": "유용하고 잘 만들어진 상품"}
    )
  return item
# short=False는 생략하거나 false, 0, off, no
# short=True는 true, 1, on, yes


# /items2/{item_id} – 필수 쿼리 파라미터
@app.get("/items2/{item_id}")
async def read_user_item(item_id: str, needy: str):
  # item_id: 경로에서 받음, needy: 반드시 쿼리 문자열에 포함돼야 함 (?needy=...)
  item = {"item_id": item_id, "needy": needy}
  return item

# 정리
  # /static → 정적 파일 제공용 디렉토리 (static/ 내부 파일 브라우저에서 접근 가능)
  # /items/{item_id} → item_id와 선택적 쿼리(q, short)를 이용해 응답 구성
  # /items2/{item_id} → 반드시 needy 쿼리 파라미터를 포함해야 함, 없으면 422 에러 발생