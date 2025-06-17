# FastAPI를 사용해서 단일 파일 업로드를 처리하는 예제
# HTML 폼을 통해 파일을 업로드하고, 서버에서는 두 가지 방식으로 처리
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# /singlefile – 파일을 바이트로 받기
@app.post("/singlefile")
async def create_file(file: bytes = File()):
  return {"file_size": len(file)}
# 업로드된 파일 전체를 메모리에 로딩해서 bytes 타입으로 받음
# 주로 작은 파일에 적합 (이미지, 텍스트 등)

# /singleuploadfile – 파일 객체로 받기
@app.post("/singleuploadfile")
async def create_upload_file(file: UploadFile):
  return {"filename": file.filename}
# UploadFile은 FastAPI가 제공하는 고성능 파일 처리 방식
# file.file 속성을 통해 직접 파일 읽기 가능 (file.file.read() 등)
# 메모리 효율이 좋고, filename, content_type 등의 메타데이터를 활용 가능


# / – HTML 파일 업로드 폼 반환
@app.get("/")
async def main():
  content = """
      <body>
      <body>
      <h2>단일 파일 업로드</h2>
      <hr>
      <form action="/singlefile" enctype="multipart/form-data" method="post">
      <input name="file" type="file">
      <input type="submit">
      </form>
      <hr>
      <form action="/singleuploadfile" enctype="multipart/form-data" method="post">
      <input name="file" type="file">
      <input type="submit">
      </form>
      </body>
    """
  return HTMLResponse(content=content)

# <form action="/singlefile" enctype="multipart/form-data" method="post">
  # 이 폼은 /singlefile로 POST 요청을 보냄
  # 업로드된 파일은 **바이트(bytes)**로 서버에 전달됨

# <form action="/singleuploadfile" enctype="multipart/form-data" method="post">
  # 이 폼은 /singleuploadfile로 POST 요청을 보냄
  # 업로드된 파일은 UploadFile 객체로 전달됨
  # enctype="multipart/form-data"는 파일 업로드에 필수임


# File() → bytes로 전체 파일을 메모리에 올림 → 작은 파일에 적합, 메모리 부담 큼
# UploadFile → 스트리밍 방식 처리 → 대용량 파일에 적합, 메모리 효율 좋음


# 전체 흐름 요약
# 1. 사용자가 /에 접속하면 HTML 폼이 나타남.
# 2. 두 개의 파일 업로드 폼이 제공됨:
  # /singlefile로 전송하는 폼
  # /singleuploadfile로 전송하는 폼
# 3. 서버는 각각 다르게 파일을 처리함:
  # File(): 전체 파일을 메모리에 올려서 **바이트(bytes)**로 받음
  # UploadFile: 파일 객체로 받으며, 효율적이고 메모리 부담이 적음