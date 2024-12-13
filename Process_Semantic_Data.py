import pandas as pd

data = pd.read_csv("fetched_data.csv")

data_cleaned = data.drop_duplicates(subset=["doi"])
data_cleaned = data_cleaned.dropna(subset=["doi", "authors", "title"])
data_cleaned.to_csv("fetched_data_cleaned.csv", index=False)

print("Duplicates removed and cleaned file saved.")
