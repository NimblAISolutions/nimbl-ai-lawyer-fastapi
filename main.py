from fastapi import FastAPI, HTTPException
from uploads import upload_pdf
from utils.url_checker import url_checker

app = FastAPI()


@app.post("/upload_zilliz")
async def upload_zilliz(path: str, collection_name: str="UnNamedCollectionName"):
    
    if not url_checker(path):
        raise HTTPException(status_code=400, detail="Invalid url")
    
    result = upload_pdf.upload_pdf_from_url(path, collection_name)
    return result



