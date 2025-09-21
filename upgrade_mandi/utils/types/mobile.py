from pydantic import BaseModel


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
