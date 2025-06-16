from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import urllib.request
from bs4 import BeautifulSoup

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
  "http://localhost:5500",
  "http://127.0.0.1:5500",
  "http://localhost:5501",
  "http://127.0.0.1:5501"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/weather")
async def main():
  res = urllib.request.urlopen("""http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey=%2BjzsSyNtwmcqxUsGnflvs3rW2oceFvhHR8AFkM3ao%2Fw50hwHXgGyPVutXw04uAXvrkoWgkoScvvhlH7jgD4%2FRQ%3D%3D&numOfRows=10&pageNo=1&base_date=20250614&base_time=0500&nx=55&ny=127""")
  bs = BeautifulSoup(res, "xml")
  target = bs.findAll("fcstValue")[6]
  print(target)
  wvalue = target.string
  print(wvalue)

  if wvalue == 1 :
    img = "rain.png"
  elif wvalue == 3:
    img = "snow.png"
  elif wvalue == 5:  
    img = "cloud.png"  
  else:
    img = "sun.png"

  return {"img": img}