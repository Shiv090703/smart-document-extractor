def process_pdf_files(file_list, fields_list):
    """
    Extracts user-defined fields from a list of PDF files, supports multiple invoices per PDF,
    removes duplicates, and saves them in Excel.
    """
    import pdfplumber, pandas as pd, re, os

    all_data = []
    os.makedirs("temp_images", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    output_excel = os.path.join("output", "extracted_data.xlsx")

    for pdf_path in file_list:
        full_text = ""

        # Extract text
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        # OCR fallback
        if not full_text.strip():
            try:
                from pdf2image import convert_from_path
                from PIL import Image
                import pytesseract
                pages = convert_from_path(pdf_path)
                for i, page in enumerate(pages):
                    image_path = f"temp_images/{os.path.basename(pdf_path)}_page_{i}.png"
                    page.save(image_path, "PNG")
                    text = pytesseract.image_to_string(Image.open(image_path))
                    full_text += text + "\n"
            except Exception as e:
                print(f"OCR failed due to missing dependencies or error: {e}. Skipping OCR.")
                # If OCR fails, proceed without it; full_text remains empty or partial

        # Split into invoice blocks (only when "Invoice Number:" exists)
        blocks = re.split(r"(?=Invoice Number:\s*INV-\d+)", full_text, flags=re.IGNORECASE)

        seen_invoices = set()
        for block in blocks:
            if not block.strip():
                continue

            row = {"File Name": os.path.basename(pdf_path)}

            for field in fields_list:
                # stricter regex: capture only until line break
                pattern = rf"{field}[:\-]?\s*([^\n]+)"
                match = re.search(pattern, block, re.IGNORECASE)
                row[field] = match.group(1).strip() if match else ""

            # Skip if no invoice number found
            inv_no = row.get("Invoice Number", "")
            if inv_no and inv_no in seen_invoices:
                continue  # avoid duplicates
            if inv_no:
                seen_invoices.add(inv_no)

            if any(row[field] for field in fields_list):
                all_data.append(row)

    # Save to Excel
    df = pd.DataFrame(all_data)
    df.to_excel(output_excel, index=False)

    # Clean temp images
    for temp_file in os.listdir("temp_images"):
        os.remove(os.path.join("temp_images", temp_file))

    return output_excel
