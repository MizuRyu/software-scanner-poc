## About Excel Data

### DeliveryNotes テーブル:
このテーブルは請求書の情報を格納します。

| カラム名 | 説明 |
| --- | --- |
| DeliveryId | 納品書ID |
| Recipient | 顧客名 |
| DeliveryDate | 発行日 |
| Publisher | 発行者 |
| Subtotal | 税抜価格 |
| Tax | 税額 |
| Total | 総計 |

### ProductDetails テーブル:
このテーブルは製品の詳細情報を格納します。

| カラム名 | 説明 |
| --- | --- |
| DeliveryId | 納品書ID |
| ProductName | 商品の名前 |
| Unit | 単位 |
| UnitPrice | 単価 |
| Quantity | 数量 |
| TotalPrice | 金額 |
| Origin | 産地 |