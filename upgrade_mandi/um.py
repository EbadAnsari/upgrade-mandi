from os import makedirs
from os.path import join
from typing import Optional

from Excel import toExcelSwiggy, toExcelZepto
from PDF import PDF
from pre import loadDataSwiggy, loadDataZepto
from utils import console, types
from utils.config import domainConfigClass
from utils.converter import convert2TableFormat
from Zepto_PDF import Zepto_PDF


def execSwiggy(
    file: str,
    invoiceVersion: int,
    sheetName: str,
    basePath: str,
    domain: types.DomainSelection,
):
    rawDF, pdfColumns, date = loadDataSwiggy(file, domain, sheetName)
    folderPathForSwiggyPdf = join(basePath, "Swiggy", date.toString(), "pdfs")
    folderPathForSwiggyExcel = join(basePath, "Swiggy", date.toString(), "excels")
    makedirs(folderPathForSwiggyPdf, exist_ok=True)
    makedirs(folderPathForSwiggyExcel, exist_ok=True)

    invoiceFormatedDF = convert2TableFormat(rawDF, domain, pdfColumns)
    pdf = PDF(domain, invoiceFormatedDF, date, invoiceVersion)
    pdf.buildPDF(folderPathForSwiggyPdf)

    toExcelSwiggy(
        invoiceFormatedDF, domain, date, folderPathForSwiggyExcel, invoiceVersion
    )


def execZepto(
    file: str,
    invoiceVersion: int,
    sheetName: str,
    basePath: str,
    domain: types.DomainSelection,
    date: types.Date,
):
    folderPathForZeptoPdf = join(basePath, "Zepto", date.toString(), "pdfs")
    folderPathForZeptoExcel = join(basePath, "Zepto", date.toString(), "excels")
    makedirs(folderPathForZeptoPdf, exist_ok=True)
    makedirs(folderPathForZeptoExcel, exist_ok=True)

    invoiceFormatedDF = loadDataZepto(file, sheetName)

    pdf = Zepto_PDF(domain, invoiceFormatedDF, date, invoiceVersion)
    pdf.buildPDF(folderPathForZeptoPdf)

    toExcelZepto(invoiceFormatedDF, date, folderPathForZeptoExcel, invoiceVersion)


def main(
    file: str,
    domainString: str,
    invoiceVersion: int,
    sheetName: str,
    date: Optional[types.Date],
):
    domain: types.DomainSelection = domainConfigClass[domainString.title()]

    basePath = join(".", "output")
    makedirs(basePath, exist_ok=True)

    console.clear()
    if domainString == "Swiggy":
        execSwiggy(file, invoiceVersion, sheetName, basePath, domain)
    elif domainString == "Zepto":
        execZepto(file, invoiceVersion, sheetName, basePath, domain, date)
    else:
        raise ValueError(f"Invalid domain {domainString}")
