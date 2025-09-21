from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .column import ColumnDefaultConfig
from .database import DatabaseConfig
from .invoice import InvoicePdfConfig
from .location import Location
from .vendor import VendorConfig


class RawSheetConfig(ColumnDefaultConfig, BaseModel):
    pass


class ColumnConfig(ColumnDefaultConfig, BaseModel):
    invoicePdf: Optional[InvoicePdfConfig] = None
    rawSheet: Optional[RawSheetConfig] = None
    database: Optional[DatabaseConfig] = None


class CommonDomainConfig(BaseModel):
    vendor: VendorConfig
    columns: List[ColumnConfig] = Field(default_factory=list)
    locations: List[Location] = Field(default_factory=list)
    domainName: Union[Literal["Swiggy"], Literal["Zepto"]] = None
    invoiceVersion: int = 1
