from os import makedirs
from os.path import join

from B2B_PDF import B2B_PDF
from utils import config, console
from utils.load import loadDateB2B
from utils.read import getSheetNames
from utils.types import date


def main(file: str, sheet_name: str, _date: date.Date | None = None) -> None:
    data = loadDateB2B(file, sheet_name)
    for key in data.keys():
        if _date is not None and key != _date.toString("-"):
            continue
        print(key)
        for customer in data[key]:
            dt = date.Date(key)
            pdf = B2B_PDF(customer, dt)
            pdf.buildPDF(f"./output/b2b/pdfs/{dt.toString('-')}")


if __name__ == "__main__":

    # exit(0)

    makedirs("./raw-sheets-dump/b2b", exist_ok=True)

    console.clear()

    file = console.select_file_from(
        join(config.PROJECT_SRC, "data", "raw", "B2B"), "*.xlsx"
    )

    sheetNames = getSheetNames(file)
    if len(sheetNames) > 1:
        sheetName = console.selectBox("Select a sheet", sheetNames)
    else:
        sheetName = sheetNames[0]

    for_all = console.yesNo("For all")
    if not for_all:
        _date = date.Date(
            console.prompt("Enter the date in DD-MM-YYYY format: ").strip()
        )

    # invoiceVersion = int(console.readInvoiceVersion())

    main(file, sheetName, _date if not for_all else None)
