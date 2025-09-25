from typing import Union

from utils.types import database
from utils.types import domain as d
from utils.types import invoice, location, mobile, table, vendor

domainConfigClass: dict[str, Union[d.Swiggy, d.Zepto]] = {
    "Swiggy": d.Swiggy(
        domainName="Swiggy",
        vendor=vendor.VendorConfig(
            name="Upgrade Mandi",
            code="U",
            email="ankushmisal7387@gmail.com",
            mobile=mobile.Mobile(countryCode="+91", number="1234567890"),
            supplierId="74227878",
            dispatchedAddress=None,
        ),
        columns=[
            table.ColumnConfig(
                columnName="Article Code",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Article Code", index=1),
                rawSheet=table.RawSheetConfig(columnName="ITEM_CODE"),
                database=database.DatabaseConfig(columnName="Article Code"),
            ),
            table.ColumnConfig(
                columnName="Date",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Date", heading=True),
                rawSheet=table.RawSheetConfig(columnName="Date"),
                database=database.DatabaseConfig(columnName="Date"),
            ),
            table.ColumnConfig(
                columnName="Dispatched Qty",
                invoicePdf=invoice.InvoicePdfConfig(
                    columnName="Dispatched Qty", index=4
                ),
                rawSheet=table.RawSheetConfig(columnName="Indents"),
                database=database.DatabaseConfig(columnName="Dispatched Qty"),
            ),
            table.ColumnConfig(
                columnName="Item Description",
                invoicePdf=invoice.InvoicePdfConfig(
                    columnName="Item Description", index=2
                ),
                rawSheet=table.RawSheetConfig(columnName="PRODUCT_NAME"),
                database=database.DatabaseConfig(columnName="Item Description"),
            ),
            table.ColumnConfig(
                columnName="Invoice No",
                invoicePdf=invoice.InvoicePdfConfig(
                    columnName="Invoice No", heading=True
                ),
                database=database.DatabaseConfig(columnName="Invoice No"),
            ),
            table.ColumnConfig(
                columnName="Invoice Version",
                database=database.DatabaseConfig(columnName="Invoice Version"),
            ),
            table.ColumnConfig(
                columnName="Location",
                invoicePdf=invoice.InvoicePdfConfig(
                    columnName="Location", heading=True
                ),
                rawSheet=table.RawSheetConfig(columnName="STORE_NAME"),
                database=database.DatabaseConfig(columnName="Location"),
            ),
            table.ColumnConfig(
                columnName="PO No",
                invoicePdf=invoice.InvoicePdfConfig(columnName="PO No", heading=True),
                rawSheet=table.RawSheetConfig(columnName="PO Number"),
                database=database.DatabaseConfig(columnName="PO No"),
            ),
            table.ColumnConfig(
                columnName="Rate",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Rate", index=6),
                rawSheet=table.RawSheetConfig(columnName="Cost"),
                database=database.DatabaseConfig(columnName="Rate"),
            ),
            table.ColumnConfig(
                columnName="Recieved Qty",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Recieved Qty", index=5),
            ),
            table.ColumnConfig(
                columnName="Retailer",
                invoicePdf=invoice.InvoicePdfConfig(
                    columnName="Retailer", heading=True
                ),
                rawSheet=table.RawSheetConfig(columnName="Entity Name"),
                database=database.DatabaseConfig(columnName="Retailer"),
            ),
            table.ColumnConfig(
                columnName="Sr",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Sr", index=0),
            ),
            table.ColumnConfig(
                columnName="Total Amount",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Total Amount", index=7),
                # rawSheet=table.RawSheetConfig(columnName="Total"),
                database=database.DatabaseConfig(columnName="Total Amount"),
            ),
            table.ColumnConfig(
                columnName="UoM",
                invoicePdf=invoice.InvoicePdfConfig(columnName="UoM", index=3),
                rawSheet=table.RawSheetConfig(columnName="WEIGHT"),
                database=database.DatabaseConfig(columnName="UoM"),
            ),
            table.ColumnConfig(
                columnName="Vendor Name",
                invoicePdf=invoice.InvoicePdfConfig(
                    columnName="Vendor Name", heading=True
                ),
                rawSheet=table.RawSheetConfig(columnName="VENDOR"),
                database=database.DatabaseConfig(columnName="Vendor Name"),
            ),
        ],
        locations=[
            location.Location(
                name="Amravati",
                shippingAddress="Ground floor Nazul Plot No. 72 Nazul Sheet No. 46d Sabanis Plot Kawar Nagar To Rukhmini Nagar Road Amravati 444606",
                retailer="Rajidi Retail Pvt Ltd",
                code="AMD",
                storeId="1402771",
            ),
            location.Location(
                name="Ayodhya Nagar",
                shippingAddress="Gadewar Lawns Plot No.31, 32, 33, 36, 37 And 38, K. H. No, 72/2, Situated At Gadewar Lawn, Shri Ram Wadi",
                retailer="Rajidi Retail Pvt Ltd",
                code="AN",
                storeId="1403419",
            ),
            location.Location(
                name="Byramji",
                shippingAddress="Unit nos - 59 to 71 Lower Ground Floor Ginger Square City Survey No - 1049",
                retailer="Rajidi Retail Pvt Ltd",
                code="B",
                storeId="1392084",
            ),
            location.Location(
                name="Dharampeth",
                shippingAddress="Plot No. 151, CTS No. 135 Puja Sabhagrah, Ravi Nagar Square, Ram Nagar",
                retailer="Swinsta Ent Private Limited",
                code="DH",
                storeId="1397624",
            ),
            location.Location(
                name="Mahal",
                shippingAddress="Unit no - G-1, Plot no.58, sardar patel timber Dhantoli, NAGPUR - 440027",
                retailer="Rajidi Retail Pvt Ltd",
                code="MH",
                storeId="1393571",
            ),
            location.Location(
                name="Manish Nagar",
                shippingAddress='Ground floor "Jayanti Mansion III", Manish nagar Nagpur Maharashtra',
                retailer="Rajidi Retail Pvt Ltd",
                code="MN",
                storeId="1392532",
            ),
            location.Location(
                name="Nandanvan",
                shippingAddress="Vinayak Tower, Lower Ground Floor, Survey No.212 Gurudev Nagar Main Road, New Nanadanvan",
                retailer="Swinsta Ent Private Limited",
                code="NA",
                storeId="1397035",
            ),
            location.Location(
                name="Sai Mandir",
                shippingAddress="Khasra No 18/2, city Survey No.718, House No. 781/B, Situated at Village Ajni",
                retailer="Swinsta Ent Private Limited",
                code="S",
                storeId="1399707",
            ),
        ],
    ),
    "Zepto": d.Zepto(
        domainName="Zepto",
        vendor=vendor.VendorConfig(
            name="Upgrade Mandi",
            code="UM",
            email="ankushmisal7387@gmail.com",
            dispatchedAddress="Plot no 147 Bajrang Nagar, Manewada, Nagpur-440027",
            mobile=mobile.Mobile(countryCode="+91", number="7385994320"),
            supplierId=None,
        ),
        columns=[
            table.ColumnConfig(
                columnName="Article Name",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Article Name", index=1),
                rawSheet=table.RawSheetConfig(columnName="Product Name"),
                database=database.DatabaseConfig(columnName="Article Name"),
            ),
            table.ColumnConfig(
                columnName="Invoice Qty.",
                invoicePdf=invoice.InvoicePdfConfig(columnName="Invoice Qty.", index=2),
                database=database.DatabaseConfig(columnName="Invoice Qty."),
            ),
            table.ColumnConfig(
                columnName="No",
                invoicePdf=invoice.InvoicePdfConfig(columnName="No", index=0),
            ),
            table.ColumnConfig(
                columnName="Rate",
                invoicePdf=invoice.InvoicePdfConfig(columnName="No", index=0),
            ),
            table.ColumnConfig(
                columnName="Recieved Qty.",
                invoicePdf=invoice.InvoicePdfConfig(columnName="No", index=0),
            ),
            table.ColumnConfig(
                columnName="UoM",
                invoicePdf=invoice.InvoicePdfConfig(columnName="UoM", index=2),
                rawSheet=table.RawSheetConfig(columnName="UoM"),
                database=database.DatabaseConfig(columnName="UoM"),
            ),
            table.ColumnConfig(
                columnName="Vendor Name",
                rawSheet=table.RawSheetConfig(columnName="Vendor Name"),
                database=database.DatabaseConfig(columnName="Vendor Name"),
            ),
        ],
        locations=[
            location.Location(
                name="Besa",
                shippingAddress="Drogheria Sellers Pvt Ltd, DS-NAG-Besa Kh. No. 82/3 Jayanti Nagari VII, Nagpur (Urban), Nagpur Nagpur 440037",
                retailer="Dorgheria",
                code="B",
            ),
            location.Location(
                name="Bhupesh Nagar",
                shippingAddress="Drogheria Sellers Pvt Ltd, DS-NAG-Bhupesh Nagar 236/B/28 & 236/B/28/A, Gorewada Road, Yogendra Nagar, Near Blue Daimond School, Nagpur. Maharashtra Maharashtra Nagpur 440013",
                retailer="Dorgheria",
                code="BN",
            ),
            location.Location(
                name="Garoba Maidan",
                shippingAddress="Drogheria Sellers Pvt Ltd, DS-NAG-Garoba Maidan, NIT Plot No. 1125 to 1135, 1191 to 1199, H. No. 1288/H/6, 1288/H/7, Near Jagnade Square, KDK College Road, Nandanwan, Nagpur 440009",
                retailer="Dorgheria",
                code="GM",
            ),
            location.Location(
                name="Gokulpeth",
                shippingAddress="DROGHERIA SELLERS PVT LTD,DS-NAG-Gokulpeth 151 Agrawal building, Ravi nagarsquare ,Gokul peth ward, Nagpur 440033",
                retailer="Dorgheria",
                code="G",
            ),
            location.Location(
                name="Jaripatka",
                shippingAddress="DROGHERIA SELLERS PVT LTD,DS-NAG-Jaripatka The sec bezonbag pragatisheel kamgar gruh nirman sahkari sunstha bezonbag Nagpur - 4400004",
                retailer="Dorgheria",
                code="J",
            ),
            location.Location(
                name="Khamala",
                shippingAddress="Drogheria Sellers Pvt Ltd, DS-NAG-Khamala Nagpur",
                retailer="Dorgheria",
                code="K",
            ),
            location.Location(
                name="Raghuji Nagar",
                shippingAddress="Drogheria Sellers Pvt Ltd, DS-NAG-Raghuji Nagar Pragati Sabhgruh, Krida Chowk, Hanuman Nagar, Nagpur, Maharashtra 440024 Nagpur 440024",
                retailer="Dorgheria",
                code="R",
            ),
            location.Location(
                name="Zingabai Takali",
                shippingAddress="Drogheria Sellers Pvt Ltd, DS-NAG-Zingabai Takali Pandurang Mangal Karyalaya, 561/A, Grenada Bandhu Nagar, Zingabai Takali, Nagpur 440030",
                retailer="Dorgheria",
                code="Z",
            ),
        ],
    ),
}


# domainConfig = {
#     "Swiggy": {
#         "columns": {
#             "Article Code": {
#                 "invoice-pdf": {"index": 1},
#                 "raw-sheet-name": {"name": "ITEM_CODE"},
#                 "notion-column-name": "Article Code",
#             },
#             "Date": {
#                 "invoice-pdf": {"heading": True},
#                 "raw-sheet-name": {"name": "Date"},
#                 "notion-column-name": "Date",
#             },
#             "Dispatched Qty": {
#                 "invoice-pdf": {
#                     "index": 4,
#                 },
#                 "raw-sheet-name": {"name": "Indents"},
#                 "notion-column-name": "Dispatched Qty",
#             },
#             "Item Description": {
#                 "invoice-pdf": {
#                     "index": 2,
#                 },
#                 "raw-sheet-name": {"name": "PRODUCT_NAME"},
#                 "notion-column-name": "Item Description",
#             },
#             "Invoice No": {
#                 "invoice-pdf": {
#                     "heading": True,
#                 },
#                 "notion-column-name": "Invoice No",
#             },
#             "Invoice Version": {
#                 "notion-column-name": "Invoice Version",
#             },
#             "location.Location": {
#                 "invoice-pdf": {
#                     "heading": True,
#                 },
#                 "raw-sheet-name": {"name": "STORE_NAME"},
#                 "notion-column-name": "location.Location",
#             },
#             "PO No": {
#                 "invoice-pdf": {
#                     "heading": True,
#                 },
#                 "notion-column-name": "PO No",
#                 "raw-sheet-name": {"name": "PO Number"},
#             },
#             "Rate": {
#                 "invoice-pdf": {
#                     "index": 6,
#                 },
#                 "raw-sheet-name": {"name": "Cost"},
#                 "notion-column-name": "Rate",
#             },
#             "Recieved Qty": {
#                 "invoice-pdf": {
#                     "index": 5,
#                 },
#                 "notion-database": False,
#             },
#             "Retailer": {
#                 "invoice-pdf": {
#                     "heading": True,
#                 },
#                 "notion-column-name": "Retailer",
#                 "raw-sheet-name": {"name": "Entity Name"},
#             },
#             "Sr": {
#                 "invoice-pdf": {
#                     "index": 0,
#                 },
#                 "notion-database": False,
#             },
#             "Total Amount": {
#                 "invoice-pdf": {
#                     "index": 7,
#                 },
#                 "notion-column-name": "Total Amount",
#             },
#             "UoM": {
#                 "invoice-pdf": {
#                     "index": 3,
#                 },
#                 "raw-sheet-name": {"name": "WEIGHT"},
#                 "notion-column-name": "UoM",
#             },
#             "Vendor Name": {
#                 "invoice-pdf": {
#                     "heading": True,
#                 },
#                 "notion-column-name": "Vendor Name",
#                 "raw-sheet-name": {"name": "VENDOR"},
#             },
#         },
#         "input-columns": [
#             "Article Code",
#             "Dispatched Qty",
#             "Item Description",
#             "Rate",
#             "Total Amount",
#             "UoM",
#         ],
#         "database-columns": [
#             "Article Code",
#             "Date",
#             "Dispatched Qty",
#             "Invoice No",
#             "Invoice Version",
#             "Item Description",
#             "location.Location",
#             "Rate",
#             "Total Amount",
#             "UoM",
#         ],
#         "output-columns": [
#             "Article Code",
#             "Dispatched Qty",
#             "Item Description",
#             "Rate",
#             "Recieved Qty",
#             "Sr",
#             "Total Amount",
#             "UoM",
#         ],
#         "locations": {
#             "Ayodhya Nagar": {
#                 "shipping-address": "Gadewar Lawns Plot No.31, 32, 33, 36, 37 And 38, K. H. No, 72/2, Situated At Gadewar Lawn, Shri Ram Wadi",
#                 "retailer": "Rajidi",
#                 "code": "AN",
#                 "storeId": "1403419",
#             },
#             "Byramji": {
#                 "shipping-address": "Unit nos - 59 to 71 Lower Ground Floor Ginger Square City Survey No - 1049",
#                 "retailer": "Rajidi",
#                 "code": "B",
#                 "storeId": "1392084",
#             },
#             "Dharampeth": {
#                 "shipping-address": "Plot No. 151, CTS No. 135 Puja Sabhagrah, Ravi Nagar Square, Ram Nagar",
#                 "retailer": "Swinsta",
#                 "code": "DH",
#                 "storeId": "1397624",
#             },
#             "Mahal": {
#                 "shipping-address": "Unit no - G-1, Plot no.58, sardar patel timber Dhantoli, NAGPUR - 440027",
#                 "retailer": "Rajidi",
#                 "code": "MH",
#                 "storeId": "1393571",
#             },
#             "Manish Nagar": {
#                 "shipping-address": 'Ground floor "Jayanti Mansion III", Manish nagar Nagpur Maharashtra',
#                 "retailer": "Rajidi",
#                 "code": "MN",
#                 "storeId": "1392532",
#             },
#             "Nandanvan": {
#                 "shipping-address": "Vinayak Tower, Lower Ground Floor, Survey No.212 Gurudev Nagar Main Road, New Nanadanvan",
#                 "retailer": "Swinsta",
#                 "code": "NA",
#                 "storeId": "1397035",
#             },
#             "Sai Mandir": {
#                 "shipping-address": "Khasra No 18/2, city Survey No.718, House No. 781/B, Situated at Village Ajni",
#                 "retailer": "Swinsta",
#                 "code": "S",
#                 "storeId": "1399707",
#             },
#         },
#     },
#     "Zepto": {
#         "columns": [
#             "No",
#             "Article Name",
#             "UoM",
#             "Invoice Qty.",
#             "Rate",
#             "Amount",
#         ],
#         "locations": {
#             "Gokulpeth": {"shipping-address": "", "retailer": "Dorgheria"},
#             "Mahada": {"shipping-address": "", "retailer": "Dorgheria"},
#             "Khamla": {"shipping-address": "", "retailer": "Dorgheria"},
#             "Garoba Maidan": {"shipping-address": "", "retailer": "Dorgheria"},
#             "Raghuji Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
#             "Zingabai Takli": {"shipping-address": "", "retailer": "Dorgheria"},
#             "Bhupesh Nagar": {"shipping-address": "", "retailer": "Dorgheria"},
#             "Besa": {"shipping-address": "", "retailer": "Dorgheria"},
#         },
#     },
# }
