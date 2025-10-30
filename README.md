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

## Feature Engineering and Data Preparation
This stage focused on transforming transactional data into meaningful customer-level features using the RFM (Recency, Frequency, Monetary) model, identifying outliers, and preparing the data for clustering.
#### Steps Performed
* Creating RFM Metrics: Each customer's purchasing behavior was summarized using three key dimensions:
    * Monetary Value (M): Total amount spent
    * Frequency (F): Number of unique purchase transactions
    * Recency (R): Days since the last purchase
    
| Customer ID |	MonetaryValue |	Frequency |	LastInvoiceDate | Recency |
| :------- | :------: | :-------: | :------: | -------: |
| 12346.00 |	169.36 |	2 |	2023-06-28 13:53:00 |	164 |
| 12347.00 |	1323.32 |	2 |	2023-12-07 14:57:00 |	2 |
| 12348.00 |	221.16 |	1 |	2023-09-27 14:59:00 |	73 |
| 12349.00 |	2221.14 |	2 |	2023-10-28 08:23:00 |	42 |
| 12351.00 |	300.93 |	1 |	2023-11-29 15:23:00 |	10 |

* Outlier Detection and Removal: To ensure robust clustering, statistical outliers were detected using the Interquartile Range (IQR) method for both Monetary Value and Frequency
* Data Scaling: To bring all RFM features to a comparable scale, Z-score normalization was applied using StandardScaler.
* A 3D scatter plot was created to visualize customer distribution across Monetary, Frequency, and Recency dimensions, helping confirm cluster separability and data balance before modeling.

![Before Segmentation](images/1_before_segmentation.png)
#### Result
- Clean, customer-level dataset with standardized RFM features.
- Outliers removed to maintain cluster quality.
- Data ready for K-Means clustering.