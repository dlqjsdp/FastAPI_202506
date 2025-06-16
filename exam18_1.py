from fastapi import FastAPI
from contextlib import asynccontextmanager
import random
from fastapi.responses import HTMLResponse

app = FastAPI()

friends = []
@asynccontextmanager
async def startup(app: FastAPI):
  print("UVICORN 에 의해 서버가 기동될 때 실행됩니다요~~~")
  friends.extend(["둘리", "또치", "도우너", "희동이", "마이콜"])
  yield

app = FastAPI(lifespan=startup)

@app.get("/myfriend")
async def main():
  return {"myfriend" : random.choice(friends)}

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
  return HTMLResponse(content=content)



