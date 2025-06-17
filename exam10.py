# FastAPI와 Jinja2 템플릿을 활용하여, 곱셈 계산기 웹 앱을 구현한 예
from fastapi import Request

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

# 템플릿 설정
templates = Jinja2Templates(directory="templates")
# templates 폴더 안에 HTML 파일들을 넣고 사용함 → 예: templates/exam9_v.html

app = FastAPI()

# /calc 경로
@app.get("/calc")
async def calc(num1:int, num2:int):
    return {"result" : num1 * num2}
# 사용자가 입력한 숫자 2개를 받아 곱한 값을 JSON 형식으로 반환함
# 예: /calc?num1=3&num2=4 요청 시 → {"result": 12} 응답

# 루트 경로 /
@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("exam9_v.html",{"request":request})
# 사용자가 접속하면 exam9_v.html 파일이 렌더링됨
# 이 HTML 파일에는 num1, num2를 입력받는 <form>이 있어야 함
# form 액션은 /calc로 전송될 것으로 예상됨


# 동작 흐름 예시
    # 1. / 접속 시 exam9_v.html이 렌더링됨
    # 2. 사용자 입력 → "계산하기" 클릭
    # 3. /calc?num1=3&num2=4로 요청됨
    # 4. 응답으로 { "result": 12 }가 JSON 형태로 표시됨