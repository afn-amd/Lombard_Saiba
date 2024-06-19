import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from collections import defaultdict

data1 = pd.read_excel("Lombard_Regular & TP_Brokerage_Apr'24(Statement).xlsx", sheet_name="RAW STATEMENT")
data2 = pd.read_excel("LOMBARD_REPORT_APRIL_24-25 TILL 07.06.2024(Saiba Dump).xls", engine='xlrd')

# data1.shape -> (316, 51)
# data2.shape -> (432, 119)

c1 = data1["POL_NUM_TXT"].unique()
c2 = data2["PolicyNo"].unique()

def compute_similarity(column1, column2, threshold=0):
    # Get unique values and filter out NaN or None values
    unique_col1 = [x for x in column1.unique() if pd.notnull(x) and isinstance(x, str)]
    unique_col2 = [x for x in column2.unique() if pd.notnull(x) and isinstance(x, str)]

    similarities = []
    detailed_matches = []

    for val1 in unique_col1:
        # Find the best match for val1 in unique_col2
        best_match = process.extractOne(val1, unique_col2, scorer=fuzz.ratio)
        if best_match:
            score = best_match[1]
            # Only consider matches above the threshold
            if score >= threshold:
                similarities.append(score)
                detailed_matches.append((val1, best_match[0], score))

    # Calculate the average similarity score
    if similarities:
        average_similarity = sum(similarities) / len(similarities)
    else:
        average_similarity = 0

    return average_similarity, detailed_matches

# Compute the similarity between the two columns with a threshold of 70
similarity_percentage, matches = compute_similarity(data1['POL_NUM_TXT'], data2['PolicyNo'], threshold=70)
print(f"The average similarity percentage between the two columns is: {similarity_percentage:.2f}%")

# Grouping matches by similarity percentage
grouped_matches = defaultdict(list)

for match in matches:
    id1, id2, similarity = match
    grouped_matches[similarity].append((id1, id2))

# Printing the grouped matches
for similarity, pairs in sorted(grouped_matches.items(), reverse=True):
    print(f"Similarity: {similarity}%")
    for id1, id2 in pairs:
        print(f"{id1} - {id2}")
    print("\n")

count_100_percent = sum(1 for match in matches if match[2] == 100)
print(f"Number of data entries with 100% similarity: {count_100_percent}")

per = (93/432)*100
print(f"{per:.2f}%")