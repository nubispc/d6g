from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from library.catalog import get_catalog, FileType, SERVICE_GRAPH_FOLDER, NETWORK_FUNCTION_FOLDER

tags_metadata = [
    {
        "name": "catalog",
        "description": "Desire6G Service Catalog component",
    }
]

app = FastAPI(openapi_tags=tags_metadata)
ghCatalog = get_catalog()


@app.get("/catalog/{file_type}", tags=["catalog"])
async def list_files(file_type: FileType):
    if file_type is FileType.SERVICE_GRAPH:
        return ghCatalog.list_files(SERVICE_GRAPH_FOLDER)
    if file_type is FileType.NETWORK_FUNCTION:
        return ghCatalog.list_files(NETWORK_FUNCTION_FOLDER)
    raise HTTPException(status_code=400, detail="Invalid file type")


@app.post("/catalog/", tags=["catalog"])
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file name provided")
    if file.filename.endswith('.sg.yaml') or file.filename.endswith('.sg.yml'):
        folder = SERVICE_GRAPH_FOLDER
    elif file.filename.endswith('.nf.yaml') or file.filename.endswith('.nf.yml'):
        folder = NETWORK_FUNCTION_FOLDER
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if ghCatalog.file_exists(file.filename, folder):
        raise HTTPException(status_code=400, detail="File already exists")
    ghCatalog.upload_file(file_content, file.filename, folder)
    return {"message": f"File '{file.filename}' uploaded successfully to catalog"}


@app.get("/retrieve/{file_name}", tags=["catalog"])
async def get_file(file_name: str):
    if file_name.endswith('.sg.yaml') or file_name.endswith('.sg.yml'):
        folder = SERVICE_GRAPH_FOLDER
    elif file_name.endswith('.nf.yaml') or file_name.endswith('.nf.yml'):
        folder = NETWORK_FUNCTION_FOLDER
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    file_path = os.path.join(folder, file_name)
    file_content = ghCatalog.download_file(file_path)
    return {"file_name": file_name, "file_content": file_content.decode()}


@app.delete("/catalog/{file_name}", tags=["catalog"])
async def delete_file(file_name: str):
    if file_name.endswith('.sg.yaml') or file_name.endswith('.sg.yml'):
        folder = SERVICE_GRAPH_FOLDER
    elif file_name.endswith('.nf.yaml') or file_name.endswith('.nf.yml'):
        folder = NETWORK_FUNCTION_FOLDER
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    if not ghCatalog.file_exists(file_name, folder):
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    
    ghCatalog.delete_file(file_name, folder)
    return {"message": f"File '{file_name}' deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print('hi')
