from sqlalchemy.orm import Session

from app.models import DeliveryNote, ProductDetail, Bill, BillDetail, Quotation, QuotationDetail, engine
from logging import getLogger

class DatabaseHandler:
    def __init__(self) -> None:
        self.session = Session(bind=engine)
        self.logger = getLogger("software-scanner")
    def insert_delivery_note_data(self, delivery_notes, product_details):
        try:
            for note in delivery_notes:
                print("note", note)
                delivery_note = self.create_delivery_note_instance(note)
                self.session.add(delivery_note)
            for detail in product_details:
                product_detail = self.create_product_detail_instance(detail)
                self.session.add(product_detail)
            self.session.commit()
            self.logger.info("DeliveryNotes Data Inserted Successfully")
        except Exception as e:
            self.logger.error(f"Insert Delivery Note Data Error: {e}")
            self.session.rollback()

    def insert_bill_data(self, bills, bill_details):
        try:
            for bill in bills:
                bill_record = self.create_bill_instance(bill)
                print("bill_record", bill_record)
                self.session.add(bill_record)
            for detail in bill_details:
                bill_detail = self.create_bill_detail_instance(detail)
                self.session.add(bill_detail)
            self.session.commit()
            self.logger.info("Bill Data Inserted Successfully")
        except Exception as e:
            self.logger.error(f"Insert Bill Data Error: {e}")
            self.session.rollback()

    def insert_quotation_data(self, quotation, quotation_details):
        try:
            quotation_record = self.create_quotation_instance(quotation)
            self.session.add(quotation_record)
            for detail in quotation_details:
                quotation_detail = self.create_quotation_detail_instance(detail)
                self.session.add(quotation_detail)
            self.session.commit()
            self.logger.info("Quotation Data Inserted Successfully")
        except Exception as e:
            self.logger.error(f"Insert Quotation Data Error: {e}")
            self.session.rollback()
            
    def create_delivery_note_instance(self, data) -> DeliveryNote:
        """Helper DeliveryNote instance creation method"""
        return DeliveryNote(
            DeliveryId=data['DeliveryId'],
            Recipient=data['Recipient'],
            Address=data['Address'],
            TEL=data['TEL'],
            FAX=data['FAX'],
            DeliveryDate=data['DeliveryDate'],
            Publisher=data['Publisher'],
            Subtotal=float(data['Subtotal']),
            Tax=float(data['Tax']),
            Total=float(data['Total']),
            Remarks=data['Remarks']
        )

    def create_product_detail_instance(self, data) -> ProductDetail:
        """Helper Product Detail instance creation method"""
        return ProductDetail(
            DeliveryId=data['DeliveryId'],
            ProductName=data['ProductName'],
            Quantity=float(data['Quantity']),
            Unit=data['Unit'],
            UnitPrice=float(data['UnitPrice']),
            TotalPrice=float(data['TotalPrice']),
            Origin=data['Origin'],
            Remarks=data['Remarks']
        )
    
    def create_bill_instance(self, data) -> Bill:
        """Helper Bill instance creation method"""
        return Bill(
            BillId=data['BillId'],
            Recipient=data['Recipient'],
            Subject=data['Subject'],
            Address=data['Address'],
            TEL=data['TEL'],
            FAX=data['FAX'],
            BillDate=data['BillDate'],
            Publisher=data['Publisher'],
            Subtotal=float(data['Subtotal']),
            Tax=float(data['Tax']),
            Total=float(data['Total']),
            BankDetails=data['BankDetails'],
            Remarks=data['Remarks']
        )
    
    def create_bill_detail_instance(self, data) -> BillDetail:
        """Helper Bill Detail instance creation method"""
        return BillDetail(
            BillId=data['BillId'],
            ItemName=data['ItemName'],
            Quantity=float(data['Quantity']),
            UnitPrice=float(data['UnitPrice']),
            TotalPrice=float(data['TotalPrice']),
            Remarks=data['Remarks']
        )
    
    def create_quotation_instance(self, data) -> Quotation:
        """Helper Quotation instance creation method"""
        return Quotation(
            QuotationId=data['QuotationId'],
            Date=data['Date'],
            Subject=data['Subject'],
            ClientName=data['ClientName'],
            Address=data['Address'],
            Tel=data['Tel'],
            Fax=data['Fax'],
            Publisher=data['Publisher'],
            Subtotal=float(data['Subtotal']),
            Tax=float(data['Tax']),
            Total=float(data['Total']),
            Remarks=data['Remarks']
        )
    
    def create_quotation_detail_instance(self, data) -> QuotationDetail:
        """Helper Quotation Detail instance creation method"""
        return QuotationDetail(
            QuotationId=data['QuotationId'],
            ItemName=data['ItemName'],
            Quantity=float(data['Quantity']),
            UnitPrice=float(data['UnitPrice']),
            TotalPrice=float(data['TotalPrice']),
            Remarks=data['Remarks']
        )

    def fetch_data(self, table):
        return self.session.query(table).all()

    def close(self):
        self.session.close()