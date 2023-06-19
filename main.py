from fastapi import FastAPI
from upload_data_zilliz import upload_pdf_from_url

app = FastAPI()


@app.post("/upload_zilliz")
async def upload_zilliz(path: str, collection_name: str="UnNamedCollectionName"):
    
    upload_pdf_from_url(path, collection_name)
    return {"info": "uploaded", "name": collection_name}