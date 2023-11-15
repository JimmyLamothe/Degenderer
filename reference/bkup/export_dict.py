import pandas as pd
import json
import sys
from pathlib import Path

def json_to_df(input_json):
    # Step 1: Import a JSON file and save the dictionary to a variable
    with open(input_json, 'r') as file:
        data = json.load(file)

    # Step 2: Convert the dictionary to a DataFrame
    df = pd.DataFrame(data, columns=['Original', 'Values'])

    # Step 3: Convert the 2-list to 2 separate columns
    df[['Non-Binary', 'Opposite']] = pd.DataFrame(df['Values'].tolist(), index=df.index)

    # Step 4: Rename the columns
    df.drop(columns=['Values'], inplace=True)

    # Step 5: Export the modified DataFrame to Excel
    stem = Path(input_json).stem
    output_excel = stem + '.xlsx'
    df.to_excel(output_excel, index=False)
    print(f"DataFrame has been exported to {output_excel}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.json")
    else:
        input_json = sys.argv[1]
        json_to_df(input_json)
