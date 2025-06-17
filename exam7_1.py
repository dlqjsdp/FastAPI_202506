# FastAPI에서 Jinja2 템플릿을 활용한 HTML 렌더링 + 동적 데이터 전달 예제
# 시간, 조건 분기, 경로 파라미터, 템플릿 변수 전달
from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# /html3 – 현재 날짜/시간 출력
@app.get("/html3")
async def test3(request: Request):
    now = datetime.datetime.now() # datetime.datetime.now()로 현재 시각을 가져옴
    formatted_date = now.strftime("%Y년 %m월 %d일") # strftime()으로 한국어 형식의 날짜/시간 문자열 생성
    formatted_time = now.strftime("%p %I시 %M분 %S초")
    return templates.TemplateResponse("exam7_3.html",context={"request":request,
                            "fd" : formatted_date, "ft" : formatted_time}); # 템플릿(exam7_3.html)에 fd, ft라는 이름으로 전달됨

# /html4/{shownum} – 홀짝에 따라 이미지 바꾸기
@app.get("/html4/{shownum}") 
async def test4(request: Request, shownum : int): # URL 경로 파라미터 shownum을 정수로 받음
    imgname = "images/hf1.png" if shownum % 2 else "images/hf2.png"
    # shownum이 홀수면 "images/hf1.png", 짝수면 "images/hf2.png"로 결정
    return templates.TemplateResponse("exam7_4.html",{"request":request, "imgname": imgname})
# 템플릿에 imgname으로 이미지 경로 전달

# /html5 – 설명 + 이미지명 전달
@app.get("/html5")
async def test5(request: Request):    
    return templates.TemplateResponse(request=request, name="exam7_5.html",
                        context={"description" : "둘리와친구들", "imgname" : "doolys.png"});
# 템플릿에 설명 문자열(description)과 이미지 파일명(imgname) 전달
# exam7_5.html에서 아래와 같이 활용 가능

# 요약
  # /html3 → 현재 날짜와 시간 출력
  # /html4/{shownum} → 홀/짝에 따라 이미지 선택
  # /html5 → 설명과 이미지 파일명을 템플릿에 전달해 출력