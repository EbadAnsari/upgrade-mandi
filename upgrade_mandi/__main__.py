from os import makedirs

from report import rawToReport
from sticker import rawToSticker
from um import main
from utils import config, console
from utils.read import getSheetNames
from utils.types import date

if __name__ == "__main__":

    makedirs("./raw-sheets-dump", exist_ok=True)

    console.clear()

    domain = console.selectDomain(
        list(config.domainConfigClass.keys()) + ["Report", "Sticker"]
    )
    _date = None
    locationPo: dict[str, str] = {}
    if domain == "Zepto":
        _date = date.Date(
            console.prompt("Enter the date in DD-MM-YYYY format: ").strip()
        )
        haveInvoice = console.yesNo("Have PO no")
        if haveInvoice:
            locationPo = {
                location.name: input(f"{location.name}: ")
                for location in config.domainConfigClass["Zepto"].locations
            }

    shelfLifeFileName = console.select_file_from("./shelf-life", "*.xlsx")
    _shelfLifeSheetNames = getSheetNames(shelfLifeFileName)
    if len(_shelfLifeSheetNames) > 1:
        shelfLifeSheetName = console.selectBox("Select a sheet", _shelfLifeSheetNames)
    else:
        shelfLifeSheetName = _shelfLifeSheetNames[0]

    nxFileName = console.select_file_from("./nx", "*.xlsx")
    _nxSheetNames = getSheetNames(nxFileName)
    if len(_nxSheetNames) > 1:
        nxSheetName = console.selectBox("Select a sheet", _nxSheetNames)
    else:
        nxSheetName = _nxSheetNames[0]

    file = console.selectRawExcelFile()
    sheetNames = getSheetNames(file)
    if len(sheetNames) > 1:
        sheetName = console.selectBox("Select a sheet", sheetNames)
    else:
        sheetName = sheetNames[0]

    if domain == "Report":
        # Handle the "Raw to Report" domain
        rawToReport(file)
    elif domain == "Sticker":
        # Sticker data
        rawToSticker(
            file,
            sheetName,
            shelfLifeFileName,
            shelfLifeSheetName,
            nxFileName,
            nxSheetName,
        )
    else:
        invoiceVersion = int(console.readInvoiceVersion())
        main(file, domain, invoiceVersion, sheetName, _date, locationPo)
