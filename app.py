from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil, os
from extractor import process_pdf_files

app = FastAPI()

UPLOAD_FOLDER = "invoices"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Static and template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Home page
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle uploads from form
@app.post("/upload_web/")
async def upload_pdfs_web(files: list[UploadFile] = File(...), fields: str = Form(...)):
    saved_files = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(file_path)

    # Convert user input fields to list
    fields_list = [f.strip() for f in fields.split(",")]

    # Call updated extractor
    output_excel = process_pdf_files(saved_files, fields_list)

    return FileResponse(
        output_excel,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename="extracted_data.xlsx"
    )
