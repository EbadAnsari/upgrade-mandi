from dataclasses import dataclass, field
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class Date(BaseModel):
    date: int = Field(gt=0, lt=32)
    month: int = Field(gt=0, lt=13)
    year: int

    def __init__(cls, dateString: str):
        split = dateString.split("-")
        if len(split) != 3:
            raise ValueError(f"Invalid date string: {dateString}")

        date, month, year = map(int, [num.strip() for num in split])

        super().__init__(date=date, month=month, year=year)

    def toString(
        self,
        sep="-",
        order: Union[Literal["DMY"], Literal["MDY"], Literal["YMD"]] = "DMY",
    ):
        date = f"{'0' if self.date < 10 else ''}{self.date}"
        month = f"{'0' if self.month < 10 else ''}{self.month}"

        if order == "DMY":
            return f"{date}{sep}{month}{sep}{self.year}"
        elif order == "MDY":
            return f"{month}{sep}{date}{sep}{self.year}"
        elif order == "YMD":
            return f"{self.year}{sep}{month}{sep}{date}"
        else:
            raise ValueError(f"Invalid order: {order}")


class ColumnDefaultConfig(BaseModel):
    """
    Default configuration for columns.
    This class is used to define the default settings for columns in the domain configuration.
    """

    """ Defines the column name for the configuration."""
    columnName: str = None


class Mobile(BaseModel):
    countryCode: str
    number: str

    @property
    def plain(self):
        return f"{self.countryCode}{self.number}"

    @property
    def withSpaces(self):
        chunks = [self.number[i : i + 3] for i in range(0, len(self.number), 3)]
        return f"{self.countryCode} {' '.join(chunks)}"

    @property
    def withHyphens(self):
        chunks = [self.number[i : i + 3] for i in range(0, len(self.number), 3)]
        return f"{self.countryCode}-{'-'.join(chunks)}"

    @property
    def withDots(self):
        chunks = [self.number[i : i + 3] for i in range(0, len(self.number), 3)]
        return f"{self.countryCode}.{' .'.join(chunks)}"

    @property
    def witBrackets(self):
        first = self.number[:3]
        second = self.number[3:6]
        third = self.number[6:]
        return f"{self.countryCode} ({first}) {second}-{third}"

    @property
    def e164(self):
        return f"{self.countryCode}{self.number}"

    def __str__(self):
        return self.format_plain()


class RawSheetConfig(ColumnDefaultConfig, BaseModel):
    pass


class InvoicePdfConfig(ColumnDefaultConfig, BaseModel):
    index: Optional[int] = None
    heading: Optional[bool] = None


class DatabaseConfig(ColumnDefaultConfig, BaseModel):
    columnName: Optional[str]


class ColumnConfig(ColumnDefaultConfig, BaseModel):
    invoicePdf: Optional[InvoicePdfConfig] = None
    rawSheet: Optional[RawSheetConfig] = None
    database: Optional[DatabaseConfig] = None


# DROGHERIA SELLERS PVT LTD,
# DS-NAG-Gokulpeth
# 151 Agrawal building,
# Ravi NagarSquare,
# Gokul peth ward,
# Nagpur 440033


class Address(BaseModel):
    street: str
    # area: str
    city: str
    # state: str
    postal_code: str
    country: str

    def __str__(self):
        # How the address is displayed
        return f"{self.street}, {self.area}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


class VendorConfig(BaseModel):
    name: Union[Literal["Upgrade Mandi"]]
    code: str
    email: str
    mobile: Mobile
    dispatchedAddress: Optional[str] = None
    supplierId: Optional[str] = None


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


class CommonDomainConfig:
    vendor: VendorConfig
    columns: List[ColumnConfig] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    domainName: Union[Literal["Swiggy"], Literal["Zepto"]] = None
    invoiceVersion: int = 1


class Swiggy(CommonDomainConfig, BaseModel):
    # supplierId: Literal["74227878"]
    pass


class Zepto(CommonDomainConfig, BaseModel):
    pass


DomainSelection = Union[Swiggy, Zepto]
