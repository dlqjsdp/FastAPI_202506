# FastAPI에서 Enum과 경로 파라미터 타입 지정, path 타입 경로 매핑 기능을 보여주는 예제
from enum import Enum
from fastapi import FastAPI

# Enum을 사용하는 /models/{model_name}
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
# Enum 클래스를 이용해 허용 가능한 모델 이름 3가지를 정의
# 이 값을 str 기반으로 사용하면 URL 파라미터를 제한할 수 있음

app = FastAPI()

@app.get("/models/{model_name}") 
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
# model_name은 ModelName Enum의 멤버 중 하나여야 함
# 유효하지 않은 값으로 요청하면 FastAPI가 자동으로 422 오류를 반환

# 경로 전체를 받는 /files/{file_path:path}
@app.get("/files/{file_path:path}") 
async def read_file(file_path: str):
    return {"file_path": file_path}
# :path 타입 지정자는 슬래시(/)가 포함된 경로 전체를 문자열로 받아줌
# 예를 들어, files/images/dooly.png처럼 하위 경로까지 받는 데 유용함

# 요약 정리
    # /models/{model_name} → Enum 타입으로 모델 이름 제한 (alexnet, resnet, lenet만 허용)
    # /files/{file_path:path} → 경로 전체를 문자열로 받아 반환 (/ 포함 가능)
    # FastAPI가 자동으로 Enum 유효성 검사와 경로 파싱을 해줘서 구현이 간단해짐