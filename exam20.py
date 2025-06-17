# FastAPI를 이용하여 기상청 공공데이터 API로 
  # 날씨 예보를 가져오고, 그 값을 기반으로 날씨에 맞는 이미지 파일명을 반환하는 API
# 클라이언트에서 이 이미지를 표시할 수 있도록 CORS 설정과 정적 파일 설정도 포함
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import urllib.request
from bs4 import BeautifulSoup

app = FastAPI()

# /static 정적 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")
# static 폴더 안의 이미지 파일을 /static/파일명 형식으로 접근 가능 → 예: sun.png는 /static/sun.png

# CORS 설정
  # CORS 오류는 다른 출처(origin)에서 API 요청할 때 브라우저가 보안 때문에 차단하는 것이고, 
  # FastAPI에서 CORSMiddleware로 허용해줄 수 있음
origins = [
  "http://localhost:5500",
  "http://127.0.0.1:5500",
  "http://localhost:5501",
  "http://127.0.0.1:5501"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins, # 허용할 프론트 주소
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
# JavaScript 코드가 HTML에서 API 요청을 보낼 수 있도록 허용
# fetch()나 XMLHttpRequest() 사용 시 CORS 오류 방지
# 보안 상 필요한 origin만 열어놓음


# /weather API 설명
@app.get("/weather")
async def main(): # 호출 시 기상청 날씨 API에서 XML 데이터를 가져와서 날씨 상태를 판별
  res = urllib.request.urlopen("""http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey=%2BjzsSyNtwmcqxUsGnflvs3rW2oceFvhHR8AFkM3ao%2Fw50hwHXgGyPVutXw04uAXvrkoWgkoScvvhlH7jgD4%2FRQ%3D%3D&numOfRows=10&pageNo=1&base_date=20250616&base_time=0500&nx=55&ny=127""")
  bs = BeautifulSoup(res, "xml")
  target = bs.findAll("fcstValue")[6] # 응답 XML에서 fcstValue 중 7번째(index 6) 데이터를 가져옴
  print(target)
  wvalue = target.string # 해당 값(wvalue)을 숫자로 비교해서 날씨 상태 판단
  print(wvalue)

  if wvalue == 1 :
    img = "rain.png"
  elif wvalue == 3:
    img = "snow.png"
  elif wvalue == 5:  
    img = "cloud.png"  
  else:
    img = "sun.png"
  # wvalue는 string 타입이므로 int(wvalue)로 변환해주는 게 안전함

  return {"img": img} # 이미지 파일명을 JSON 형태로 반환

# 주요 기능 요약
  # /weather : 기상청 API로 날씨 정보를 받아 이미지 파일명(sun.png, rain.png 등) 반환
  # CORS 설정 : 로컬에서 다른 포트(5500, 5501)로 접근 가능한 JS 클라이언트를 허용
  # /static : 이미지 파일이 저장된 디렉토리 (static/) 경로를 서빙