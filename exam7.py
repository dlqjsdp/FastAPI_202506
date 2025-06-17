# FastAPI에서 Jinja2 템플릿 엔진을 활용한 HTML 렌더링 예제
# 정적 파일도 함께 서빙할 수 있게 설정되어 있고,
# /html1, /html2로 각각 다른 HTML 템플릿을 반환하게 되어 있음
from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")
# templates 폴더 내의 HTML 파일을 렌더링할 수 있게 설정

app = FastAPI()

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")
# /static/경로로 접근 시 static/ 폴더 내부의 파일 제공
# 예: static/css/style.css → /static/css/style.css

# /html1 → exam7_1.html 렌더링
@app.get("/html1")
async def test1(request: Request):
    return templates.TemplateResponse("exam7_1.html",{"request":request})
    # 템플릿에서 {{ request }} 객체를 사용할 수 있도록 request를 context에 포함해야 함 (필수)
    # 템플릿 파일은 templates/exam7_1.html이어야 함

# /html2 → exam7_2.html 렌더링
@app.get("/html2") 
async def test2(request: Request):
    return templates.TemplateResponse("exam7_2.html",{"request":request})
    # 위와 동일하게 동작하지만 다른 템플릿(exam7_2.html)을 반환

# 결과 예시
    # http://localhost:8000/html1 → exam7_1.html 페이지 보여짐
    # http://localhost:8000/html2 → exam7_2.html 페이지 보여짐
    # 템플릿 안에서 정적 리소스는 이렇게 사용 가능: <link rel="stylesheet" href="/static/css/style.css">