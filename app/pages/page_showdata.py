import streamlit as st
import pandas as pd

from app.sqlite.sqliteDB import DatabaseHandler
from app.models import DeliveryNote, ProductDetail, Bill, BillDetail, Quotation, QuotationDetail

db_handler = DatabaseHandler()

st.title("登録履歴")
st.write("Show DB data here")

# TODO: DBの中身を表示する

def display_data(table, title, max_display=10):
    st.subheader(title)
    data = db_handler.fetch_data(table)
    if data:
        
        data_dicts = [row.__dict__ for row in data]
        for row in data_dicts:
            if '_sa_instance_state' in row:
                del row['_sa_instance_state']

        df = pd.DataFrame(data_dicts)
        df_display = df.head(max_display)

        st.dataframe(df_display)
    else:
        st.write("No data found")

display_data(DeliveryNote, "DeliveryNotes")
display_data(ProductDetail, "ProductDetails")
display_data(Bill, "Bill")
display_data(BillDetail, "BillDetails")
display_data(Quotation, "Quotation")
display_data(QuotationDetail, "QuotationDetails")

db_handler.close()