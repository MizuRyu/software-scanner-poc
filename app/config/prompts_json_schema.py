DELIVERY_JSON_FORMAT = """
{
    "DeliveryNotes": [
        {
            "DeliveryId": "Delivery ID",
            "Recipient": "Customer Name",
            "Address": "Customer Address",
            "TEL": "Customer Phone Number",
            "FAX": "Customer Fax Number",
            "DeliveryDate": "Issue Date",
            "Publisher": "Issuer",
            "Subtotal": "Price Excluding Tax",
            "Tax": "Tax Amount",
            "Total": "Total Amount",
            "Remarks": "Remarks"
        }
    ],
    "ProductDetails": [
        {
            "DeliveryId": "Delivery ID",
            "ProductName": "Product Name",
            "Quantity": "Quantity",
            "Unit": "Unit",
            "UnitPrice": "Unit Price",
            "TotalPrice": "Total Price",
            "Origin": "Origin",
            "Remarks": "Remarks"
        }
    ]
}
"""


BILL_JSON_FORMAT = """
{
    "Bill": [
        {
            "BillId": "Bill ID",
            "Recipient": "Customer Name",
            "Subject": "Subject Name",
            "Address": "Customer Address",
            "TEL": "Customer Phone Number",
            "FAX": "Customer Fax Number",
            "BillDate": "Issue Date",
            "Publisher": "Issuer",
            "Subtotal": "Price Excluding Tax",
            "Tax": "Tax Amount",
            "Total": "Total Amount",
            "BankDetails": "Bank Details",
            "Remarks": "Remarks"
        }
    ],
    "BillDetails": [
        {
            "BillId": "Bill ID",
            "ItemName": "Item Name",
            "Quantity": "Quantity",
            "UnitPrice": "Unit Price",
            "TotalPrice": "Total Price",
            "Remarks": "Remarks"
        }
    ]
}
"""

QUOTATION_JSON_FORMAT = """
{
    "Quotation": [
        {
            "QuotationId": "Quotation ID",
            "Date": "Issue Date",
            "Subject": "Subject",
            "ClientName": "Client Name",
            "Address": "Client Address",
            "Tel": "Client Phone Number",
            "Fax": "Client Fax Number",
            "Publisher": "Issuer"
            "Subtotal": "Price Excluding Tax",
            "Tax": "Tax Amount",
            "Total": "Total Amount",
            "Remarks": "Remarks"
        }
    ],
    "QuotationDetails": [
        {
            "QuotationId": "Quotation ID",
            "ItemName": "Item Name",
            "Quantity": "Quantity",
            "UnitPrice": "Unit Price",
            "TotalPrice": "Total Price",
            "Remarks": "Remarks"
        }
    ]
}
"""