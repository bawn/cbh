from pathlib import Path
from PyPDF2 import PdfReader
from pdf import PDFData

def main():
    # current_path = Path(__file__).resolve().parent

    pdf_path = "src/files/2025.pdf"

    # print("Using file:", pdf_path)
    pdf_data = PDFData(pdf_path)

    print(pdf_data.get_grain_received())

    # print(pdf_data.get_other_data())




if __name__ == "__main__":
    main()