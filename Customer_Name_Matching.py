import pandas as pd
import numpy as np
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from collections import defaultdict

data1 = pd.read_excel("Lombard_Regular & TP_Brokerage_Apr'24(Statement).xlsx", sheet_name="RAW STATEMENT")
data2 = pd.read_excel("LOMBARD_REPORT_APRIL_24-25 TILL 07.06.2024(Saiba Dump).xls", engine='xlrd')

# data1.shape -> (316, 51)
# data2.shape -> (432, 119)

c1 = data1["INSURED_CUSTOMER_NAME"].unique()
c2 = data2["CustName"].unique()
print(len(c1), len(c2))


def preprocess_name(name):
    # Define a list of words to omit
    words_to_omit = [
        'industry', 'industries', 'corp', 'corporation', 'inc', 'incorporated', 'foundation',
        'company', 'co', 'limited', 'ltd', 'pvt', 'llc', 'llp', 'and', 'pvtltd', '&', 'm/s', 'ms'
    ]

    # Remove common titles and suffixes, and unwanted characters
    name = re.sub(r'\b(Mr|Ms|Ltd|LLP|Pvt|Private|Limited|LLC|LTD|Llp|ltd|lp|PLLP|Pllp|P.L.C.|ms|m/s|pvtltd)\b', '',
                  name, flags=re.IGNORECASE)
    # Normalize "and", "AND", "And", "&" to "and"
    name = re.sub(r'\b(and|AND|And|&)\b', 'and', name, flags=re.IGNORECASE)
    # Remove dots (.) and commas (,)
    name = re.sub(r'[.,]', '', name)
    # Remove words to omit
    for word in words_to_omit:
        name = re.sub(r'\b' + word + r'\b', '', name, flags=re.IGNORECASE)
    # Remove spaces and make lowercase
    name = re.sub(r'\s+', '', name).lower()
    return name


def compute_similarity(data1, data2, threshold=80):
    names1 = pd.Series(data1['INSURED_CUSTOMER_NAME'].unique()).astype(str).apply(preprocess_name)
    names2 = pd.Series(data2['CustName'].unique()).astype(str).apply(preprocess_name)

    results = {}
    for name1 in names1:
        for name2 in names2:
            similarity = fuzz.ratio(name1, name2)
            if similarity >= threshold:
                if similarity not in results:
                    results[similarity] = []
                results[similarity].append((name1, name2))

    return results


# Compute similarity with a threshold of 80%
similarity_dict = compute_similarity(data1, data2, threshold=80)

c = 0

# Sort the similarity_dict by keys in descending order
sorted_similarity_dict = dict(sorted(similarity_dict.items(), key=lambda item: item[0], reverse=True))

# Display results
for similarity, pairs in sorted_similarity_dict.items():
    print(f"Similarity {similarity}%:")
    for pair in pairs:
        c += 1
        print(f"  {pair[0]} - {pair[1]}")

print(f"Total: {c}")

per = (129/432)*100
print(f"{per:.2f}%")