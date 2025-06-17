# FastAPI를 이용해 단일 및 다중 파일 업로드를 구현
# 업로드된 파일을 서버의 static/files/ 디렉토리에 저장하는 예제
# lifespan, UploadFile, 파일 저장 등 실제 서버에서 사용할 수 있는 핵심 기능이 포함
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from typing import List
import os
from contextlib import asynccontextmanager
import signal

# lifespan – 서버 시작 시 디렉터리 생성
@asynccontextmanager
async def my_lifespan(app: FastAPI):
    print("서버 기동시 실행")
    if not os.path.isdir("static/files"): # 서버가 실행되면 static/files 디렉토리가 없을 경우 생성함.
      os.mkdir("static/files") # 파일 업로드 시 저장 위치가 없으면 오류가 발생할 수 있기 때문에 미리 준비함.
    yield

# app = FastAPI(lifespan=my_lifespan)에서 이 컨텍스트를 등록함.
app = FastAPI(lifespan=my_lifespan) 

# /singleuploadfile – 단일 파일 업로드
@app.post("/singleuploadfile")
async def create_upload_file(file: UploadFile): # UploadFile 객체를 통해 파일 메타데이터와 내용 접근 가능
  path = f"static/files/{file.filename}"
  content = await file.read() # await file.read()로 파일 내용을 읽음 (바이트로)
  with open(path, 'w+b') as fp: # 'w+b' 모드로 파일을 바이너리로 저장
    fp.write(content)

  return {
      'file': file.filename,
      'content': file.content_type, 
      'path': path,
  } # 저장 후 파일명, 타입, 경로를 JSON 응답으로 반환

# /multiuploadfiles – 여러 파일 업로드
@app.post("/multiuploadfiles")
async def create_upload_files(files: List[UploadFile]): # List[UploadFile] 타입으로 여러 파일을 한 번에 받음
  # 루프를 돌면서 각각의 파일을 읽고 저장
  # 결과는 각 파일에 대한 정보를 담은 리스트로 응답
  result = []
  for file in files:
    path = f"static/files/{file.filename}"
    content = await file.read()
    with open(path, 'w+b') as fp:
      fp.write(content) 

    result.append({
      'file': file.filename,
      'content': file.content_type,
      'path': path,
    })
  return result

# / – HTML 파일 업로드 폼 제공
@app.get("/")
async def main():
  content = """
      <body>
        <h2>파일 업로드하여 서버에 저장하기</h2>
        <hr>
        <form action="/singleuploadfile" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit" value="싱글파일 업로드">
        </form>
        <hr>
        <form action="/multiuploadfiles" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit" value="다중파일 업로드">
        </form>
      </body>
    """
  # <form action="/singleuploadfile" enctype="multipart/form-data" method="post">
    # 첫 번째 폼: /singleuploadfile로 단일 파일 전송
  # <form action="/multiuploadfiles" enctype="multipart/form-data" method="post">
    # 두 번째 폼: /multiuploadfiles로 다중 파일 전송 (multiple 속성)
  return HTMLResponse(content=content)


# 주요 기능 요약
  # lifespan : 서버 시작 시 디렉터리(static/files) 자동 생성
  # / : HTML 업로드 폼 제공 (싱글 & 멀티 업로드)
  # /singleuploadfile : 단일 파일 업로드 받아 저장
  # /multiuploadfiles : 다중 파일 업로드 받아 저장