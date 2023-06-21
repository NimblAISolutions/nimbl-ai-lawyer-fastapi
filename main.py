from fastapi import FastAPI, HTTPException
from uploads import loaders
from utils.url_checker import url_checker
from all_types import Formats

app = FastAPI()

@app.post("/upload_zilliz")
async def upload_zilliz(path: str, format: Formats, collection_name: str="unnamedcollection"):
    
    if not url_checker(path):
        raise HTTPException(status_code=400, detail="Invalid url")
    
    result = await loaders.base_loader(path, collection_name, format)
    if result.get("status") == "error":
        raise HTTPException(400, detail=result)
    
    return result



