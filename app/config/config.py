import os
from app.config.prompts_json_schema import DELIVERY_JSON_FORMAT, BILL_JSON_FORMAT, QUOTATION_JSON_FORMAT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'sqlite', 'docdata.db')

DOCUMENT_TYPE_MAPPING = {
    'bill': '請求書',
    'deliveryNote': '納品書',
    'quotation': '見積書',
    'other': 'その他'
}

DOCUMENT_TYPE_MAPPING_JSON = {
    'deliveryNote': DELIVERY_JSON_FORMAT,
    'bill': BILL_JSON_FORMAT,
    'quotation': QUOTATION_JSON_FORMAT,
    'other': ''
}