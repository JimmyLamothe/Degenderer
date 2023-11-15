import pandas as pd
import json
import sys
from pathlib import Path

def df_to_json(input_excel):
    # Step 1: Import the Excel file into a DataFrame
    df = pd.read_excel(input_excel)

    # Step 2: Restructure the DataFrame
    df['Values'] = df[['Non-Binary', 'Opposite']].values.tolist()
    df.drop(columns=['Non-Binary', 'Opposite'], inplace=True)

    # Step 3: Convert the DataFrame to a list of lists
    data = df[['Original', 'Values']].values.tolist()
    
    # Step 4: Export the dictionary to a JSON file
    stem = Path(input_excel).stem
    output_json = stem + '.json'
    with open(output_json, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"Dictionary has been exported to {output_json}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.xlsx")
    else:
        input_excel = sys.argv[1]
        df_to_json(input_excel)
