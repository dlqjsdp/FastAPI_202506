# FastAPI를 이용해 웹에서 두 숫자를 곱한 결과를 보여주는 간단한 곱셈 웹 애플리케이션을 구현한 예
from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# 곱셈 연산 처리
@app.get("/calc")
async def login(num1:int, num2:int): # 쿼리 스트링으로 전달된 num1, num2를 int로 받음
    return {"result" : num1 * num2} # 예: /calc?num1=3&num2=4 → 결과는 { "result": 12 }

# HTML 폼 제공
@app.get("/") # 브라우저에서 /로 접속하면 입력 폼을 반환, HTML 폼은 GET /calc/ 경로로 데이터를 전송함
async def main():
    content = """
        <!DOCTYPE html> 
        <html>
        <head>
            <meta charset="UTF-8">
            <title>HTML학습</title>
        </head>
        <body>
            <h1 style="color:red">곱셈 연산</h1><hr>
            <form action="/calc/" method="get">
                <input name="num1" type="number" placeholder="숫자1을 입력하세요" required><br>
                <input name="num2" type="number" placeholder="숫자2를 입력하세요" required><br>
                <input type="submit" value="곱셈요청">
            </form>
        </body>
    """
    # 사용자가 입력한 숫자들이 num1, num2 이름으로 /calc로 전송됨
    return HTMLResponse(content=content)

# 기능 요약
    # / 경로 : HTML 폼을 보여줌 (숫자 2개 입력 후 곱셈 요청)
    # /calc 경로 : 두 숫자를 받아 곱셈 결과를 JSON 형태로 응답

# 예시 실행 흐름
    # 1. 사용자가 / 접속
    # 2. 입력창에 3, 4를 입력하고 "곱셈요청" 클릭
    # 3. 브라우저가 /calc?num1=3&num2=4로 요청
    # 4. FastAPI가 계산하여 결과 반환: