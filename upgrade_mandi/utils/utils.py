from collections import Counter
from datetime import datetime
from typing import List

import pandas as pd

domainConfig = {
    "Swiggy": {
        "columns": {
            "Article Code": {
                "invoice-pdf": {"index": 1},
                "notion-database": True,
                "raw-sheet-name": {"name": "ITEM_CODE"},
                "notion-column-name": "Article Code",
            },
            "Date": {
                "invoice-pdf": {"heading": True},
                "notion-database": True,
                "raw-sheet-name": {"name": "Date"},
                "notion-column-name": "Date",
            },
            "Dispatched Qty": {
                "invoice-pdf": {
                    "index": 4,
                },
                "notion-database": True,
                "raw-sheet-name": {"name": "Indents"},
                "notion-column-name": "Dispatched Qty",
            },
            "Item Description": {
                "invoice-pdf": {
                    "index": 2,
                },
                "notion-database": True,
                "raw-sheet-name": {"name": "PRODUCT_NAME"},
                "notion-column-name": "Item Description",
            },
            "Invoice No": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-database": True,
                "notion-column-name": "Invoice No",
            },
            "Invoice Version": {
                "notion-database": True,
                "notion-column-name": "Invoice Version",
            },
            "Location": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-database": True,
                "raw-sheet-name": {"name": "STORE_NAME"},
                "notion-column-name": "Location",
            },
            "PO No": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-database": True,
                "notion-column-name": "PO No",
                "raw-sheet-name": {"name": "PO Number"},
            },
            "Rate": {
                "invoice-pdf": {
                    "index": 6,
                },
                "notion-database": True,
                "raw-sheet-name": {"name": "Cost"},
                "notion-column-name": "Rate",
            },
            "Recieved Qty": {
                "invoice-pdf": {
                    "index": 5,
                },
                "notion-database": False,
            },
            "Retailer": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-database": True,
                "notion-column-name": "Retailer",
                "raw-sheet-name": {"name": "Entity Name"},
            },
            "Sr": {
                "invoice-pdf": {
                    "index": 0,
                },
                "notion-database": False,
            },
            "Total Amount": {
                "invoice-pdf": {
                    "index": 7,
                },
                "notion-database": True,
                "notion-column-name": "Total Amount",
            },
            "UoM": {
                "invoice-pdf": {
                    "index": 3,
                },
                "notion-database": True,
                "raw-sheet-name": {"name": "WEIGHT"},
                "notion-column-name": "UoM",
            },
            "Vendor Name": {
                "invoice-pdf": {
                    "heading": True,
                },
                "notion-database": True,
                "notion-column-name": "Vendor Name",
                "raw-sheet-name": {"name": "VENDOR"},
            },
        },
        "input-columns": [
            "Article Code",
            "Dispatched Qty",
            "Item Description",
            "Rate",
            "Total Amount",
            "UoM",
        ],
        "database-columns": [
            "Article Code",
            "Date",
            "Dispatched Qty",
            "Invoice No",
            "Invoice Version",
            "Item Description",
            "Location",
            "Rate",
            "Total Amount",
            "UoM",
        ],
        "output-columns": [
            "Article Code",
            "Dispatched Qty",
            "Item Description",
            "Rate",
            "Recieved Qty",
            "Sr",
            "Total Amount",
            "UoM",
        ],
        "locations": {
            "Ayodhya Nagar": {
                "shipping-address": "Gadewar Lawns Plot No.31, 32, 33, 36, 37 And 38, K. H. No, 72/2, Situated At Gadewar Lawn, Shri Ram Wadi",
                "retailer": "Rajidi",
                "code": "AN",
                "storeId": "1403419",
            },
            "Byramji": {
                "shipping-address": "Unit nos - 59 to 71 Lower Ground Floor Ginger Square City Survey No - 1049",
                "retailer": "Rajidi",
                "code": "B",
                "storeId": "1392084",
            },
            "Dharampeth": {
                "shipping-address": "Plot No. 151, CTS No. 135 Puja Sabhagrah, Ravi Nagar Square, Ram Nagar",
                "retailer": "Swinsta",
                "code": "DH",
                "storeId": "1397624",
            },
            "Mahal": {
                "shipping-address": "Unit no - G-1, Plot no.58, sardar patel timber Dhantoli, NAGPUR - 440027",
                "retailer": "Rajidi",
                "code": "MH",
                "storeId": "1393571",
            },
            "Manish Nagar": {
                "shipping-address": 'Ground floor "Jayanti Mansion III", Manish nagar Nagpur Maharashtra',
                "retailer": "Rajidi",
                "code": "MN",
                "storeId": "1392532",
            },
            "Nandanvan": {
                "shipping-address": "Vinayak Tower, Lower Ground Floor, Survey No.212 Gurudev Nagar Main Road, New Nanadanvan",
                "retailer": "Swinsta",
                "code": "NA",
                "storeId": "1397035",
            },
            "Sai Mandir": {
                "shipping-address": "Khasra No 18/2, city Survey No.718, House No. 781/B, Situated at Village Ajni",
                "retailer": "Swinsta",
                "code": "S",
                "storeId": "1399707",
            },
        },
    },
    "Zepto": {
        "columns": [
            "No",
            "Article Name",
            "UoM",
            "Invoice Qty.",
            "Rate",
            "Amount",
        ],
        "locations": {
            "Gokulpeth": {"shipping-address": "", "retailer": "Dorgheria"},
            "Mahada": {"shipping-address": "", "retailer": "Dorgheria"},
            "Khamla": {"shipping-address": "", "retailer": "Dorgheria"},
            "Garoba Maidan": {"shipping-address": "", "retailer": "Dorgheria"},
            "Raghuji Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
            "Zingabai Takli": {"shipping-address": "", "retailer": "Dorgheria"},
            "Bhupesh Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
            "Besa": {"shipping-address": "", "retailer": "Dorgheria"},
        },
    },
}


def generateInvoiceId(date: datetime, domain: str, location: str, invoiceVersion: int):
    return f'{date.strftime("%d%m%Y")}U{domainConfig[domain]["locations"][location]["code"]}{invoiceVersion}'


def generatePONo(date: datetime, storeId: str, supplierId: str):
    return f'{date.strftime("%Y%m%d")}-{storeId}-{supplierId}'


def notionObject2DataFrame(notionObject):
    data = {}
    for key, value in notionObject["properties"].items():
        if value["type"] == "title":
            data[key] = value["title"][0]["plain_text"]
        elif value["type"] == "select":
            data[key] = value["select"]["name"]
        elif value["type"] == "number":
            data[key] = value["number"]
        elif value["type"] == "date":
            data[key] = value["date"]["start"]
        elif value["type"] == "formula":
            if "string" in value["formula"]:
                data[key] = value["formula"]["string"]
            elif "number" in value["formula"]:
                data[key] = value["formula"]["number"]
    return pd.DataFrame([data])


def extractPDFColumnNames(domain: str):
    return [
        columnName
        for columnName, columnValue in domainConfig[domain].items()
        if "invoice-pdf" in columnValue and "index" in columnValue["invoice-pdf"]
    ]


def nameExtracter(rightNamesList: List[str], wrongName: str) -> str:
    chances = [0] * len(rightNamesList)

    counterOriginal = Counter(wrongName.lower())
    for i, rightName in enumerate(rightNamesList):
        counterLocation = Counter(rightName.lower())
        chances[i] = (
            sum((counterOriginal & counterLocation).values())
            * 2
            / (sum(counterOriginal.values()) + sum(counterLocation.values()))
        )
    return rightNamesList[chances.index(max(chances))]
