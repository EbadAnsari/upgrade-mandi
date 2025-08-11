from os import makedirs

import typer
from Excel import toExcel
from PDF import PDF
from pre import loadData
from utils.config import domainConfigClass
from utils.converter import convert2TableFormat

if __name__ == "__main__":

    def run(
        file: str = typer.Option(..., "--file", "-f", help="Excel file path"),
        domain: str = typer.Option(
            "Swiggy", "--domain", "-d", help="Domain name ('Swiggy', 'Zomato', etc.)"
        ),
        invoiceVersion: int = typer.Option(
            1, "--invoice-version", "-i", help="Invoice Version"
        ),
        sheetName: str = typer.Option(
            "Sheet1",
            "--sheet-name",
            "-s",
            help="Sheet name of the Excel file (default: 'Sheet1')",
        ),
    ):
        rawDF, pdfColumns, date = loadData(file, sheetName, invoiceVersion)

        basePath = f"./output/{date.strftime('%d-%m-%Y')}"
        folderPathForPdf = basePath + "/pdfs"

        makedirs(folderPathForPdf, exist_ok=True)

        invoiceFormatedDF = convert2TableFormat(rawDF, pdfColumns, date)
        pdf = PDF(invoiceFormatedDF, date, invoiceVersion)
        pdf.buildPDF(folderPathForPdf)

        toExcel(invoiceFormatedDF, date, basePath, invoiceVersion)

    typer.run(run)
