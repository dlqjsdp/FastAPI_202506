# FastAPI의 가장 기본적인 예제
# 웹 서버를 실행하고 루트 경로(/)에 접속했을 때 간단한 JSON 응답을 반환하는 기능을 제공

# FastAPI 프레임워크를 불러옴.
from fastapi import FastAPI

# FastAPI 앱 인스턴스를 생성. 이 객체가 전체 API의 진입점이 됨.
app = FastAPI()

@app.get("/")
async def root(): # GET / 요청이 들어오면 root() 함수가 실행됨.
    return {"message": "안녕? FastAPI!! ^^"} # 반환 값은 JSON 형태이며, "message" 키에 한국어 인사말이 담겨 있음.
