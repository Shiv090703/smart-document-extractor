# InvoiceExtractor

A web-based tool for extracting structured data from PDF invoices using FastAPI, with OCR fallback for scanned documents.

## Features

- Upload multiple PDF invoices via web interface
- Extract user-defined fields (e.g., Invoice Number, Date, Amount, Customer Name)
- Supports both text-based and scanned/image-based PDFs
- Handles multiple invoices per PDF
- Removes duplicate invoices
- Exports extracted data to Excel (.xlsx)
- Simple web UI for easy use

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd InvoiceExtractor
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install system dependencies:
   - **Tesseract OCR**: Download and install from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Poppler**: Install via conda (`conda install -c conda-forge poppler`) or your system's package manager

## Usage

1. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

2. Open your browser and go to `http://127.0.0.1:8000`

3. Upload PDF files and specify the fields to extract (comma-separated, e.g., "Invoice Number, Billing Date, Customer Name, Amount")

4. Download the extracted data as an Excel file

## Project Structure

- `app.py`: Main FastAPI application
- `extractor.py`: PDF processing and data extraction logic
- `create_test_pdf.py`: Script to generate sample invoices for testing
- `templates/index.html`: Web interface template
- `static/`: Static files (CSS, JS, etc.)
- `requirements.txt`: Python dependencies

## API Endpoints

- `GET /`: Home page
- `POST /upload_web/`: Upload PDFs and extract data

## Testing

Run `create_test_pdf.py` to generate sample invoices in the `invoices/` folder for testing.

## License

[Add your license here]
