# FastAPI를 이용해 HTML 폼에서 사용자 입력을 받고, 서버에서 해당 데이터를 처리하는 예제
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/insert") # 클라이언트가 POST /insert/로 요청을 보낼 때 호출됨.
# Form()은 HTML form 데이터에서 값을 읽기 위한 FastAPI의 도우미 함수.
# Annotated[str, Form()]: 해당 파라미터가 form에서 오는 문자열임을 명시함.
async def login(username: Annotated[str, Form()], emailaddress: Annotated[str, Form()]):
  print(username, emailaddress)  # 터미널에 값이 출력됨 (개발용 로그)
  return {"username" : username, "emailaddress" : emailaddress} # 입력된 값을 JSON 형태로 응답함.

@app.get("/")
async def main(): # 루트 경로(/)에 접속하면 HTML 페이지를 반환하는 함수.
  content = """
      <!DOCTYPE html> 
      <html>
        <head>
        <meta charset="UTF-8">
        <title>HTML학습</title>
      </head>
      <body>
        <h1>개인 정보 작성</h1><hr>
        <form action="/insert/" method="post">
        <input name="username" type="text" placeholder="계정을 입력하세요"><br>
        <input name="emailaddress" type="email" placeholder="메일주소를 입력하세요"><br>
        <input type="submit" value="요청">
        </form>
      </body>
    """
  # <form> 태그로 사용자로부터 이름(username)과 이메일(emailaddress)을 입력받음.
  # 전송 방식은 POST, 전송 주소는 /insert/.
  return HTMLResponse(content=content) # HTML을 문자열로 반환하고, text/html로 렌더링되도록 HTMLResponse를 사용함.


# 전체 동작 흐름 요약
# 1. 사용자가 /로 접속하면 HTML 폼이 브라우저에 표시됨.
# 2. 사용자가 이름과 이메일을 입력하고 "요청" 버튼을 누르면 /insert/로 POST 요청이 전송됨.
# 3. 서버는 폼 데이터를 파싱해서 username과 emailaddress를 추출하고, JSON 형식으로 응답함.