from datetime import datetime
from typing import List

import pandas as pd
from type.domain_types import Swiggy

from .config import domainConfigClass
from .utils import generateInvoiceId, generatePONo


def convert2TableFormat(
    df: pd.DataFrame,
    domain: Swiggy,
    selectedColumns: List[str],
    # date: datetime,
    # invoiceVersion: int = 1,
):
    if domain.domainName == "Swiggy":
        return {
            location.locationName: {
                "data-frame": df[df["Location"] == location.locationName][
                    selectedColumns
                ].reset_index(drop=True),
                # "invoice-number": generateInvoiceId(
                #     date, location.code, invoiceVersion
                # ),
                # "po-no": generatePONo(date, location.storeId, domain.supplierId),
                # "shipping-address": location.shippingAddress,
                # "retailer": location.retailer,
            }
            for location in domain.locations
        }
