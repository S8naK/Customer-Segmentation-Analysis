## Data Exploration
The second step involved exploring and understanding the structure and quality of the dataset before performing any cleaning or segmentation.
#### Steps Performed
* Invoice Inspection
	* Invoice Numbers were examined to detect invalid or canceled transactions.
	* Checked the Invoice column for any non-numeric characters (like 'C' indicating cancellation).
* Stock Code Validation
	* Ensured that product StockCode values followed the expected pattern (5-digit or alphanumeric identifiers)
	* Identified several special codes such as 'POST', 'D', 'BANK CHARGES', 'TEST001', 'gift_0001_80', 'ADJUST', 'DOT', etc. These typically represented non-sale transactions (postage, discounts, adjustments, test entries).
#### Insights
* Found negative quantities corresponding to returns or cancellations.
* Detected special StockCodes representing non-product items that may need to be excluded from RFM analysis.

## Data Cleaning
After identifying anomalies in the exploration phase, the dataset was cleaned to retain only valid sales transactions relevant for RFM segmentation.
#### Steps Performed
* Removing Cancellations and Accounting Entries
    * Canceled or accounting adjustment invoices were identified by the presence of non-numeric characters (like ‘C’ or ‘A’) in the Invoice number. These were removed to keep only valid 6-digit numeric invoices:
        ```python
        df_clean["Invoice"] = df_clean["Invoice"].astype(str)
        df_clean = df_clean[df_clean["Invoice"].str.match("^\d{6}$") == True]
        ```
* Filtering Valid Stock Codes
    * Only product-related StockCode values were retained. Excluded special codes like POST, D, TEST001, etc., by applying a validation mask:
        ```python
        mask = (
            (df_clean["StockCode"].str.match("^\d{5}$") == True)
            | (df_clean["StockCode"].str.match("^\d{5}[a-zA-Z]+$") == True)
            | (df_clean["StockCode"].str.match("^PADS$") == True)
        )
        df_clean = df_clean[mask]
        ```
* Removing Null and Invalid Records
    * Customer ID was a crucial identifier for RFM segmentation, so records with missing IDs were dropped.
    * Transactions with zero price were also removed, as they do not contribute to monetary value.
#### Post-Cleaning Summary
Approximately 23% of records were dropped during cleaning — primarily cancellations, missing IDs, or invalid stock codes.