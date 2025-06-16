from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
@app.get("/calc")
async def login(num1:int, num2:int):
    return {"result" : num1 * num2}

@app.get("/")
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
    return HTMLResponse(content=content)
