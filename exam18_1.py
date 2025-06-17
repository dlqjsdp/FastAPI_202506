# FastAPI로 구성된 AJAX 기반 주기적 데이터 요청 예제
from fastapi import FastAPI
from contextlib import asynccontextmanager
import random
from fastapi.responses import HTMLResponse

app = FastAPI()

friends = []

# lifespan 함수 – 서버 시작 시 친구 리스트 초기화
@asynccontextmanager # @asynccontextmanager를 통해 FastAPI(lifespan=...) 구조에서 사용 가능
async def startup(app: FastAPI):
  print("UVICORN 에 의해 서버가 기동될 때 실행됩니다요~~~")
  friends.extend(["둘리", "또치", "도우너", "희동이", "마이콜"]) # 서버가 실행되면 friends 리스트에 캐릭터 이름들을 한 번만 추가함
  yield # 서버 종료 시 따로 동작은 없음 (원하면 yield 이후 코드 추가 가능)

app = FastAPI(lifespan=startup)

# /myfriend – 랜덤 친구 반환 API
@app.get("/myfriend")
async def main():
  return {"myfriend" : random.choice(friends)} # 친구 목록에서 무작위로 한 명 선택해서 JSON으로 반환

# / – 클라이언트에 HTML 페이지 반환
@app.get("/")
async def main():
  content = """
      <!DOCTYPE html> 
      <html>
        <head>
        <meta charset="UTF-8">
        <title>주기적 요청</title>  
        <style>
          h3 {
            color : #000066;            
            text-shadow : 2px 2px 2px #3399ff;
          }
        </style>      
      </head>
      <body>
        <h1>주기적 요청하는 AJAX</h1>
        <hr>
        <h3>잠시 기다리숑~~</h3>
        <script>
          const h3Dom = document.querySelector("h3");
          function commAjax() {
            const xhr = new XMLHttpRequest();
            xhr.addEventListener("load", function() {        
              h3Dom.textContent = `${JSON.parse(xhr.responseText).myfriend}`;
            });
            xhr.open("GET", `/myfriend`, true);
            xhr.send();
          }          
          window.setInterval(commAjax, 2000);
        </script>
      </body>
      </html>
    """
  # 이 HTML 페이지의 핵심 기능:
  # 처음에는 h3 요소에 "잠시 기다리숑~~"이 보임
  # function commAjax() : AJAX 요청 (2초마다 실행)
    # commAjax()는 /myfriend API를 호출하고
    # 받은 친구 이름을 <h3> 텍스트로 갱신함
    # setInterval(commAjax, 2000) → 2초마다 반복 실행
  # 최종 결과
    # 브라우저에서 http://localhost:8000/ 접속
    # 2초마다 <h3>에 무작위 친구 이름이 계속 바뀜 : 둘리 → 도우너 → 희동이 → 마이콜 ...
  return HTMLResponse(content=content)


# 전체 기능 요약
  # 서버가 시작될 때 friends 리스트를 초기화함 (lifespan 사용)
  # 클라이언트는 /에 접속하면 HTML 페이지를 받고, 그 안에서 JavaScript AJAX 요청을 2초마다 자동 실행
  # AJAX는 /myfriend API를 호출하고, 무작위 친구 이름을 받아 <h3> 요소에 표시함

# 주요 포인트 요약
  # lifespan : 서버 시작 시 친구 리스트 초기화
  # /myfriend : 랜덤 친구를 반환하는 API
  # / : HTML + AJAX 페이지 반환
  # setInterval : 2초마다 API를 호출하여 <h3> 업데이트

