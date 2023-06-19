from fastapi import FastAPI
import upload_data_zilliz

app = FastAPI()


@app.post("/upload_zilliz")
async def upload_zilliz(path: str, collection_name: str="UnNamedCollectionName"):
    
    upload_data_zilliz(path, collection_name)
    return {"info": "uploaded", "name": "collection_name"}