from datetime import datetime
from typing import List

import pandas as pd

from .config import domainConfigClass
from .utils import generateInvoiceId, generatePONo


def conver2TableFormat(
    df: pd.DataFrame,
    selectedColumns: List[str],
    date: datetime,
    invoiceVersion: int = 1,
):
    return {
        location.locationName: {
            "dataFrame": df[df["Location"] == location.locationName][
                selectedColumns
            ].reset_index(drop=True),
            "invoiceNumber": generateInvoiceId(date, location.code, invoiceVersion),
            "poNo": generatePONo(date, location.storeId, domainConfigClass.supplierId),
            "shippingAddress": location.shippingAddress,
            "retailer": location.retailer,
        }
        for location in domainConfigClass.locations
    }
