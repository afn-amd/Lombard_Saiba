import pandas as pd
import numpy as np

data1 = pd.read_excel("Lombard_Regular & TP_Brokerage_Apr'24(Statement).xlsx", sheet_name="RAW STATEMENT")
data2 = pd.read_excel("LOMBARD_REPORT_APRIL_24-25 TILL 07.06.2024(Saiba Dump).xls", engine='xlrd')

# data1.shape -> (316, 51)
# data2.shape -> (432, 119)

"""print("Columns in Lombard statement:\n", data1.columns)
print("\nColumns in Saiba Dump:")
cols = data2.columns
for col in cols:
    print(col)"""

#u1 = data1["INSURED_CUSTOMER_NAME"].unique()
#print(sorted(u1))
#u2 = data2["CustName"].unique()
#print(u2)
"""Customers' Names are different in both. 
Unique Value Counts:
173 in Lambord Statement [print(len(sorted(u1)))]
211 in Saiba Dump [print(len(u2))]"""

#u1 = data1["POL_NUM_TXT"].unique()
#print(sorted(u1))
#u2 = data2["PolicyNo"].unique()
#print(u2)
"""93 Policy Numbers are the same. From Lombard Statement "POL_NUM_TXT" is equivalent to "PolicyNo" in Saiba Dump.
Unique Value Counts:
293 in Lambord Statement [print(len(sorted(u1)))]
168 in Saiba Dump [print(len(u2))]"""

#u1 = data1["PRODUCT_NAME"].unique()
#print(sorted(u1))
#u2 = data2["Policy Type"].unique()
#print(u2)
""""PRODUCT_NAME" in the Lombard sheet is equivalent to "Policy Type" in Saiba Dump. Only 1 data matches completely in both "GROUP PERSONAL ACCIDENT".
Unique Value Counts:
27 in Lambord Statement [print(len(sorted(u1)))]
45 in Saiba Dump [print(len(u2))]"""