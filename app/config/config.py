from app.config.prompts import BILL_SYSTEM_PROMPT_EN, SYSTEM_PROMPT_EN, QUOTATION_SYSTEM_PROMPT_EN

DOCUMENT_TYPE_MAPPING = {
    'bill': '請求書',
    'deliveryNote': '納品書',
    'quotation': '見積書'
}

DOCUMENT_TYPE_MAPPING_PROMPT = {
    'bill': BILL_SYSTEM_PROMPT_EN,
    'deliveryNote': SYSTEM_PROMPT_EN,
    'quotation': QUOTATION_SYSTEM_PROMPT_EN
}