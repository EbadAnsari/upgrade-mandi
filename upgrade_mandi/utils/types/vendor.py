from typing import Literal, Optional, Union

from pydantic import BaseModel

from .mobile import Mobile


class VendorConfig(BaseModel):
    name: Union[Literal["Upgrade Mandi"]]
    code: str
    email: str
    mobile: Mobile
    dispatchedAddress: Optional[str] = None
    supplierId: Optional[str] = None
