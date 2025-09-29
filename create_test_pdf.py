from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import os, random, datetime

output_folder = r"C:\Users\shiva\Desktop\InvoiceExtractor\invoices"
os.makedirs(output_folder, exist_ok=True)

customers = ["ABC Traders", "XYZ Enterprises", "LMN Corp", "PQR Ltd", "STU Co"]
extra_fields_options = [
    None,
    {"Tax": "$50", "Discount": "$20"},
    {"Payment Terms": "Net 30", "Late Fee": "$10"},
    {"PO Number": "PO12345", "Ship Via": "FedEx"}
]

# Function to create image-based "scanned" invoice
def create_scanned_invoice(file_name, invoices):
    img = Image.new('RGB', (600, 800), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    
    y = 20
    for inv in invoices:
        draw.text((50, y), "INVOICE", font=font, fill="black"); y += 30
        draw.text((50, y), f"Invoice Number: {inv['invoice_no']}", font=font, fill="black"); y += 20
        draw.text((50, y), f"Billing Date: {inv['billing_date']}", font=font, fill="black"); y += 20
        draw.text((50, y), f"Customer Name: {inv['customer']}", font=font, fill="black"); y += 20
        draw.text((50, y), f"Amount: ${inv['amount']}", font=font, fill="black"); y += 20
        if inv['extra_fields']:
            for k,v in inv['extra_fields'].items():
                draw.text((50, y), f"{k}: {v}", font=font, fill="black")
                y += 20
        draw.text((50, y+10), "Thank you for your business!", font=font, fill="black"); y += 40
    img.save(os.path.join(output_folder, file_name), "PDF", resolution=100.0)
    print(f"✅ Created scanned PDF: {file_name}")

# Function to create text PDF with random formatting
def create_text_invoice(file_name, invoices):
    pdf = FPDF()
    for inv in invoices:
        pages = random.choice([1,2])
        for _ in range(pages):
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Invoice Number: {inv['invoice_no']}", ln=True)
            pdf.cell(200, 10, txt=f"Billing Date: {inv['billing_date']}", ln=True)
            pdf.cell(200, 10, txt=f"Customer Name: {inv['customer']}", ln=True)
            pdf.cell(200, 10, txt=f"Amount: ${inv['amount']}", ln=True)
            if inv['extra_fields']:
                for k,v in inv['extra_fields'].items():
                    pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt="Thank you for your business!\n" * random.randint(1,3))
    pdf.output(os.path.join(output_folder, file_name))
    print(f"✅ Created text PDF: {file_name}")

# Generate 10 diverse PDFs
for i in range(1, 11):
    num_invoices = random.choice([1,2])  # Multiple invoices per PDF
    invoices = []
    for _ in range(num_invoices):
        invoice_no = f"INV-{random.randint(1000,9999)}"
        billing_date = (datetime.date.today() - datetime.timedelta(days=random.randint(0,30))).isoformat()
        customer = random.choice(customers)
        amount = round(random.uniform(1000, 5000), 2)
        extra_fields = random.choice(extra_fields_options)
        invoices.append({
            "invoice_no": invoice_no,
            "billing_date": billing_date,
            "customer": customer,
            "amount": amount,
            "extra_fields": extra_fields
        })
    file_name = f"invoice_{i}.pdf"

    if i % 3 == 0:
        create_scanned_invoice(file_name, invoices)
    else:
        create_text_invoice(file_name, invoices)
