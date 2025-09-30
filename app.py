from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil, os, io

from extractor import process_pdf_files
from ai_service import ask_ai  # AI integration

app = FastAPI()

UPLOAD_FOLDER = "invoices"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Static and template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload_web/")
async def upload_pdfs_web(
    files: list[UploadFile] = File(...),
    fields: str = Form(...),
    analyze: bool = Form(False)
):
    """
    Upload PDFs, extract fields, return Excel, optionally return AI insights.
    """
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(file_path)

    fields_list = [f.strip() for f in fields.split(",")]

    # Call PDF extractor
    output_excel = process_pdf_files(saved_files, fields_list)

    with open(output_excel, 'rb') as f:
        excel_bytes = f.read()

    # Clean up uploaded PDFs
    for file_path in saved_files:
        os.remove(file_path)

    # If analyze requested, return AI insights
    if analyze:
        try:
            prompt = (
                f"Here is extracted invoice data with fields {fields_list}. "
                "Provide a summary, highlight anomalies, and suggest insights."
            )
            ai_response = ask_ai(prompt)
            return JSONResponse({"ai_insights": ai_response})
        except Exception as e:
            return JSONResponse({"error": str(e)})

    # Otherwise, return Excel
    response = StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=extracted_data.xlsx"}
    )

    os.remove(output_excel)
    return response


@app.get("/ask-ai/")
def ask_ai_endpoint(question: str):
    """
    Ask AI directly with a custom question.
    """
    try:
        answer = ask_ai(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/ai_suggest/")
def ai_suggest_endpoint():
    """
    Suggest invoice fields for extraction via AI.
    """
    try:
        prompt = (
            "You are an AI assistant. Suggest the most common fields to extract from invoices "
            "like Invoice Number, Date, Amount, Customer Name."
        )
        ai_response = ask_ai(prompt)
        suggested_fields = [f.strip() for f in ai_response.split(",") if f.strip()]
        return JSONResponse({"fields": suggested_fields})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
