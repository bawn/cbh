from cbh import db
from cbh.pdf import PDFData
from cbh import dashboard

def main():

    # Initialize the database
    if not db.check_db_exists():
        db.initialize_db()
        get_data_from_pdf()
        run_dashboard()
    else:
        print("Database already exists. Skipping PDF data extraction.")
        run_dashboard()
        
    
def get_data_from_pdf():
    for year in [2020, 2025]:
        pdf_data = PDFData(year)
        result = pdf_data.get_essential_data()
        db.save_to_db(year, *result)

def run_dashboard():
    dashboard.create_dashboard()


if __name__ == "__main__":
    main()
