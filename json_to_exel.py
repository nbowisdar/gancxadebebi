import json

import pandas as pd

# Sample JSON data
with open('full_data_all_improved.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert JSON data to DataFrame
df = pd.json_normalize(data)

# Create a DataFrame with expanded phone numbers
df['phone_numbers'] = df['phone_numbers'].apply(lambda x: ', '.join(x))

# Save to Excel
file_path = 'output.xlsx'
df.to_excel(file_path, index=False)

