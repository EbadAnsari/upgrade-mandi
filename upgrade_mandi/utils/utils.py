from collections import Counter
from datetime import datetime
from typing import List

import pandas as pd

from .config import domainConfig


def generateInvoiceId(date: datetime, code: str, invoiceVersion: int):
    return f'{date.strftime("%d%m%Y")}U{code}{invoiceVersion}'


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
    return rightNamesList[chances.index(max(chances))]
    return rightNamesList[chances.index(max(chances))]
