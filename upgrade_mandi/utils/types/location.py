from typing import Optional

from pydantic import BaseModel

from .date import Date


class Location(BaseModel):
    name: str
    shippingAddress: str
    retailer: str
    code: str
    storeId: Optional[str] = None

    def poNo(self, date: Date, supplierId: str) -> str:
        return f'{date.toString(sep="", order="YMD")}-{self.storeId}-{supplierId}'

    def invoiceNo(self, date: Date, vendorCode: str, invoiceVersion: int) -> str:
        return f'{date.toString(sep="")}{vendorCode}{self.code}{invoiceVersion}'
