# FastAPI를 활용한 다중 파일 업로드 예제
# 클라이언트가 여러 개의 파일을 동시에 업로드할 수 있고, 
# 서버는 두 가지 방식(bytes, UploadFile)으로 이를 처리
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# /files – List[bytes] 방식
@app.post("/files")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}
# files는 바이트 리스트 (List[bytes])
# 모든 파일을 메모리에 한꺼번에 올림 → 작은 파일에 적합
# 각 파일의 크기를 len()으로 계산해서 응답함

# /uploadfiles – List[UploadFile] 방식
@app.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}
# files는 UploadFile 객체 리스트
# 메모리에 한 번에 올리지 않고 스트리밍 방식으로 처리 가능 → 대용량 파일에 적합
# 각 파일 이름을 추출해서 응답으로 반환

@app.get("/")
async def main():
	content = """
					<body>
					<h2>다중 파일 업로드</h2>
					<hr>
					<form action="/files" enctype="multipart/form-data" method="post">
					<input name="files" type="file" multiple>
					<input type="submit">
					</form>
					<hr>
					<form action="/uploadfiles" enctype="multipart/form-data" method="post">
					<input name="files" type="file" multiple>
					<input type="submit">
					</form>
					</body>
					"""
	return HTMLResponse(content=content)

# <form action="/files" enctype="multipart/form-data" method="post">
	# /files로 전송됨 → List[bytes]로 처리
# <form action="/uploadfiles" enctype="multipart/form-data" method="post">
	# /uploadfiles로 전송됨 → List[UploadFile]로 처리


# List[bytes] → 모든 파일을 한 번에 메모리에 올림 → 작은 파일에 적합
# List[UploadFile] → 스트리밍 방식 처리 → 대용량 파일에 적합, 효율적


# 전체 흐름 요약
# 1. / 경로에 접속하면 HTML 페이지가 반환됨.
# 2. 두 개의 <form>이 있고, 각각은 다중 파일을 업로드할 수 있음.
# 3. 사용자가 파일 여러 개를 업로드하면 /files 또는 /uploadfiles로 전송됨.
# 4. 서버에서는 리스트 형태로 파일을 받고, 각각의 방식에 따라 처리함.