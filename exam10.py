from fastapi import Request

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()
@app.get("/calc")
async def calc(num1:int, num2:int):
    return {"result" : num1 * num2}

@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("exam9_v.html",{"request":request})