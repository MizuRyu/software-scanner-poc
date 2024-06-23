from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from app.config.config import SQLITE_DB_PATH

Base = declarative_base()

class DeliveryNote(Base):
    __tablename__ = 'DeliveryNotes'
    DeliveryId = Column(String, primary_key=True)
    Recipient = Column(String)
    Address = Column(String)
    TEL = Column(String)
    FAX = Column(String)
    DeliveryDate = Column(String)
    Publisher = Column(String)
    Subtotal = Column(Float)
    Tax = Column(Float)
    Total = Column(Float)
    Remarks = Column(String)
    products = relationship("ProductDetail", back_populates="delivery_note")

class ProductDetail(Base):
    __tablename__ = 'ProductDetails'
    id = Column(Integer, primary_key=True)
    DeliveryId = Column(String, ForeignKey('DeliveryNotes.DeliveryId'))
    ProductName = Column(String)
    Quantity = Column(Float)
    Unit = Column(String)
    UnitPrice = Column(Float)
    TotalPrice = Column(Float)
    Origin = Column(String)
    Remarks = Column(String)
    delivery_note = relationship("DeliveryNote", back_populates="products")

class Bill(Base):
    __tablename__ = 'Bill'
    BillId = Column(String, primary_key=True)
    Recipient = Column(String)
    Subject = Column(String)
    Address = Column(String)
    TEL = Column(String)
    FAX = Column(String)
    BillDate = Column(String)
    Publisher = Column(String)
    Subtotal = Column(Float)
    Tax = Column(Float)
    Total = Column(Float)
    BankDetails = Column(String)
    Remarks = Column(String)
    bill_details = relationship("BillDetail", back_populates="bill")

class BillDetail(Base):
    __tablename__ = 'BillDetails'
    id = Column(Integer, primary_key=True)
    BillId = Column(String, ForeignKey('Bill.BillId'))
    ItemName = Column(String)
    Quantity = Column(Float)
    UnitPrice = Column(Float)
    TotalPrice = Column(Float)
    Remarks = Column(String)
    bill = relationship("Bill", back_populates="bill_details")

class Quotation(Base):
    __tablename__ = 'Quotation'
    QuotationId = Column(String, primary_key=True)
    Date = Column(String)
    Subject = Column(String)
    ClientName = Column(String)
    Address = Column(String)
    Tel = Column(String)
    Fax = Column(String)
    Publisher = Column(String)
    Subtotal = Column(Float)
    Tax = Column(Float)
    Total = Column(Float)
    Remarks = Column(String)
    quotation_details = relationship("QuotationDetail", back_populates="quotation")

class QuotationDetail(Base):
    __tablename__ = 'QuotationDetails'
    id = Column(Integer, primary_key=True)
    QuotationId = Column(String, ForeignKey('Quotation.QuotationId'))
    ItemName = Column(String)
    Quantity = Column(Float)
    UnitPrice = Column(Float)
    TotalPrice = Column(Float)
    Remarks = Column(String)
    quotation = relationship("Quotation", back_populates="quotation_details")

# init DB
engine = create_engine(f'sqlite:///{SQLITE_DB_PATH}')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
