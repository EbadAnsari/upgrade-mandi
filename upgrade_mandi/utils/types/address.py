from pydantic import BaseModel


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
