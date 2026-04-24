from pathlib import Path
from PyPDF2 import PdfReader
from pdf import PDFData

def main():
    # current_path = Path(__file__).resolve().parent

    pdf_path = "src/files/2024.pdf"

    # print("Using file:", pdf_path)
    pdf_data = PDFData(pdf_path)

    pdf_data.get_essential_data()
    # pdf_data.get_AIFR()

    # print(pdf_data.get_other_data())




if __name__ == "__main__":
    main()