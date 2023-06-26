from fastapi import FastAPI, HTTPException
from uploads import loaders
from utils.url_checker import url_checker
from utils.get_context import get_context_from_milvus
import os

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOADED_DIR = os.path.join(BASE_DIR, "uploaded_files")


@app.post("/upload_zilliz")
async def upload_zilliz(path: str, collection_name: str="unnamedcollection"):
    
    if not url_checker(path):
        raise HTTPException(status_code=400, detail="Invalid url")
    
    result = await loaders.base_loader(path, collection_name)

    print(result)
    if result.get("status") == "error":
        raise HTTPException(400, detail=result)
    
    return result


@app.get("/get_context")
async def get_context(message: str):

    result = get_context_from_milvus(message)

    return result
