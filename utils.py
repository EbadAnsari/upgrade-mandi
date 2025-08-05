from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

config = {
    "Swiggy": {
        "input-columns": [
            "Article Code",
            "Item Description",
            "UoM",
            "Dispatched Qty",
            "Rate",
            "Total Amount",
        ],
        "output-columns": [
            "Sr",
            "Article Code",
            "Item Description",
            "UoM",
            "Dispatched Qty",
            "Recieved Qty",
            "Rate",
            "Total Amount",
        ],
        "locations": {
            "Nandanvan": {
                "shipping-address": 'Vinayak Tower", Lower Ground Floor, Survey No.212 Gurudev Nagar Main Road, New Nanadanvan',
                "retailer": "Swinsta",
                "code": "NA",
            },
            "Dharampeth": {
                "shipping-address": "Plot No. 151, CTS No. 135 Puja Sabhagrah, Ravi Nagar Square, Ram Nagar",
                "retailer": "Swinsta",
                "code": "DH",
            },
            "Mahal": {
                "shipping-address": "Unit no - G-1, Plot no.58, sardar patel timber Dhantoli, NAGPUR- 440027",
                "retailer": "Rajidi",
                "code": "MH",
            },
            "Ayodhya Nagar": {
                "shipping-address": "Gadewar Lawns Plot No.31, 32, 33, 36, 37 And 38,K. H. No, 72/2, Situated At Gadewar Lawn, Shri Ram Wadi",
                "retailer": "Rajidi",
                "code": "AN",
            },
            "Sai Mandir": {
                "shipping-address": "Khasra No 18/2, city Survey No.718, House No. 781/B, Situated at Village Ajni",
                "retailer": "Swinsta",
                "code": "S",
            },
            "Manish Nagar": {
                "shipping-address": 'Ground floor "Jayanti Mansion III", Manish nagar  Nagpur Maharashtra',
                "retailer": "Rajidi",
                "code": "MN",
            },
            "Byramji": {
                "shipping-address": 'Unit nos - 59 to 71 Lower Ground Floor Ginger Square" City Survey No - 1049',
                "retailer": "Rajidi",
                "code": "B",
            },
        },
    },
    "Zepto": {
        "columns": [
            "No",
            "Article Name",
            "UoM",
            "Invoice Qty.",
            "Rate",
            "Amount",
        ],
        "locations": {
            "Gokulpeth": {"shipping-address": "", "retailer": "Dorgheria"},
            "Mahada": {"shipping-address": "", "retailer": "Dorgheria"},
            "Khamla": {"shipping-address": "", "retailer": "Dorgheria"},
            "Garoba Maidan": {"shipping-address": "", "retailer": "Dorgheria"},
            "Raghuji Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
            "Zingabai Takli": {"shipping-address": "", "retailer": "Dorgheria"},
            "Bhupesh Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
            "Besa": {"shipping-address": "", "retailer": "Dorgheria"},
        },
    },
}


def generateInvoiceId(date: datetime, domain: str, location: str, invoiceVersion: int):
    return f'{date.strftime("%d%m%Y")}U{config[domain]["locations"][location]["code"]}{invoiceVersion}'

def generatePONo(date: datetime, storeId: str, supplierId: str):
    return f"{date.strftime("")}"