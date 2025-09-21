from os import makedirs
from os.path import join
from typing import Optional

import pandas as pd
from Excel import toExcelSwiggy, toExcelZepto
from PDF import PDF
from pre import loadDataSwiggy, loadDataZepto
from utils import console
from utils.config import domainConfigClass
from utils.converter import convert2TableFormat
from utils.types import date
from utils.types import domain as d
from Zepto_PDF import Zepto_PDF


def execSwiggy(
    file: str,
    invoice_version: int,
    sheet_name: str,
    base_path: str,
    domain: d.DomainSelection,
):
    rawDF, pdfColumns, date = loadDataSwiggy(file, sheet_name, domain)
    folderPathForSwiggyPdf = join(base_path, "Swiggy", date.toString(), "pdfs")
    folderPathForSwiggyExcel = join(base_path, "Swiggy", date.toString(), "excels")
    makedirs(folderPathForSwiggyPdf, exist_ok=True)
    makedirs(folderPathForSwiggyExcel, exist_ok=True)

    domain.invoiceVersion = invoice_version

    invoice_formated_df = convert2TableFormat(rawDF, domain, pdfColumns)
    pdf = PDF(domain, invoice_formated_df, date)
    pdf.buildPDF(folderPathForSwiggyPdf)

    toExcelSwiggy(invoice_formated_df, domain, date, folderPathForSwiggyExcel)


def execZepto(
    file: str,
    invoice_version: int,
    sheet_name: str,
    base_path: str,
    domain: d.DomainSelection,
    date: date.Date,
    location_po: dict[str, str] = {},
):

    # creating output directories
    folder_path_for_zepto_pdf = join(base_path, "Zepto", date.toString(), "pdfs")
    folder_path_for_zepto_excel = join(base_path, "Zepto", date.toString(), "excels")
    makedirs(folder_path_for_zepto_pdf, exist_ok=True)
    makedirs(folder_path_for_zepto_excel, exist_ok=True)

    # load and format the raw sheet of Zepto domain
    invoice_formated_df = loadDataZepto(file, sheet_name, domain)

    domain.invoiceVersion = invoice_version

    pdf = Zepto_PDF(domain, invoice_formated_df, date, location_po)
    pdf.buildPDF(folder_path_for_zepto_pdf)

    toExcelZepto(
        invoice_formated_df,
        domain,
        date,
        folder_path_for_zepto_excel,
        location_po,
    )


def main(
    file: str,
    domain_string: str,
    invoice_version: int,
    sheet_name: str,
    date: Optional[date.Date],
    location_po: dict[str, str] = {},
    df: pd.DataFrame = pd.DataFrame(),
):
    domain: d.DomainSelection = domainConfigClass[domain_string.title()]

    base_path = join(".", "output")
    makedirs(base_path, exist_ok=True)

    console.clear()
    if domain_string == "Swiggy":
        execSwiggy(file, invoice_version, sheet_name, base_path, domain)
    elif domain_string == "Zepto":
        execZepto(
            file, invoice_version, sheet_name, base_path, domain, date, location_po
        )
    else:
        raise ValueError(f"Invalid domain {domain_string}")
