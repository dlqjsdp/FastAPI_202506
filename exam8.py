# FastAPI 코드는 동적으로 HTML 페이지를 렌더링하면서 이미지와 ID 값을 전달하는 예제
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse) # GET /items/5처럼 숫자 ID를 경로로 받음, 반환 형식은 HTML 응답
async def read_item(request: Request, id: int): 
  # FastAPI의 템플릿 렌더링을 위해 request 객체 필요, id는 URL에서 받는 정수

  return templates.TemplateResponse(name="exam8_v.html",  # exam8_v.html 템플릿을 렌더링
                    context={"request":request,
                              "id": id, "nextid" : 1 if id == 10 else id+1, "img_name" : f"images/{id}.jpg"})
  # 전달되는 값:
    # id: 현재 ID 값
    # nextid: 다음 ID (10이면 1로 순환, 아니면 +1)
    # img_name: images/5.jpg 같은 이미지 경로 (이미지는 /static/images/ 폴더에 있어야 함)

# 핵심 기능
# /items/{id} 경로에 숫자 ID를 넣으면
# templates/exam8_v.html 파일을 렌더링하고
# 다음 ID 값과 해당 ID에 대응하는 이미지 경로를 전달함


# 요약
  # ID에 따라 다른 이미지를 보여주는 HTML 페이지를 반환함
  # ID가 10이면 다시 1로 순환
  # 템플릿에서 이미지와 다음 링크까지 보여줄 수 있음