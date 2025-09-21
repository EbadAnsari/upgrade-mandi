from typing import Union

from pydantic import BaseModel

from .table import CommonDomainConfig


class Swiggy(CommonDomainConfig, BaseModel):
    # supplierId: Literal["74227878"]
    pass


class Zepto(CommonDomainConfig, BaseModel):
    pass


DomainSelection = Union[Swiggy, Zepto]
