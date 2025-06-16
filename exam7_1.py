from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/html3")
async def test3(request: Request):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y년 %m월 %d일")
    formatted_time = now.strftime("%p %I시 %M분 %S초")
    return templates.TemplateResponse("exam7_3.html",context={"request":request,
                            "fd" : formatted_date, "ft" : formatted_time});
@app.get("/html4/{shownum}") 
async def test4(request: Request, shownum : int):
    imgname = "images/hf1.png" if shownum % 2 else "images/hf2.png"
    return templates.TemplateResponse("exam7_4.html",{"request":request, "imgname": imgname})

@app.get("/html5")
async def test5(request: Request):    
    return templates.TemplateResponse(request=request, name="exam7_5.html",
                        context={"description" : "둘리와친구들", "imgname" : "doolys.png"});