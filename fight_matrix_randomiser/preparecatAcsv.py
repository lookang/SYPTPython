# This Python script loads a CSV file, replaces the substring '_A' in the row index with an empty string, and saves the modified DataFrame both in the current directory and one level up in the folder structure as new CSV files


import pandas as pd

# Load the CSV file
df = pd.read_csv('Assignment matrix.csv', index_col=0)

# Replace '_A' with an empty string in all rows and columns
df.index = df.index.str.replace('_A', '')

# Save the modified DataFrame to a new CSV file
df.to_csv('cat_A Assignment matrix.csv')
# Save the modified DataFrame one level up in the folder structure
df.to_csv('../cat_A Assignment matrix.csv')
print(df)
