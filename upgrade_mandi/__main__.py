from os import makedirs

from um import main
from utils import config, console
from utils.read import getSheetNames
from utils.types import date

if __name__ == "__main__":

    makedirs("./raw-sheets-dump", exist_ok=True)

    console.clear()

    file = console.selectRawExcelFile()

    sheetNames = getSheetNames(file)
    if len(sheetNames) > 1:
        sheetName = console.selectBox("Select a sheet", sheetNames)
    else:
        sheetName = sheetNames[0]
    domain = console.selectDomain()

    _date = None
    locationPo: dict[str, str] = {}
    if domain == "Zepto":
        _date = date.Date(
            console.prompt("Enter the date in DD-MM-YYYY format: ").strip()
        )
        haveInvoice = console.yeNo("Have PO no")
        if haveInvoice:
            locationPo = {
                location.name: input(f"{location.name}: ")
                for location in config.domainConfigClass["Zepto"].locations
            }

    invoiceVersion = int(console.readInvoiceVersion())
    main(file, domain, invoiceVersion, sheetName, _date, locationPo)
