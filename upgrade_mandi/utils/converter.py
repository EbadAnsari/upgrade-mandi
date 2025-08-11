from datetime import datetime
from typing import List

import pandas as pd

from .config import domainConfigClass
from .utils import generateInvoiceId, generatePONo


def convert2TableFormat(
    df: pd.DataFrame,
    selectedColumns: List[str],
    date: datetime,
    invoiceVersion: int = 1,
):
    return {
        location.locationName: {
            "data-frame": df[df["Location"] == location.locationName][
                selectedColumns
            ].reset_index(drop=True),
            "invoice-number": generateInvoiceId(date, location.code, invoiceVersion),
            "po-no": generatePONo(date, location.storeId, domainConfigClass.supplierId),
            "shipping-address": location.shippingAddress,
            "retailer": location.retailer,
        }
        for location in domainConfigClass.locations
    }
