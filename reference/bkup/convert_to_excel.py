import pandas as pd
import json

def pronouns_to_df(input_json):
    # Step 1: Import a JSON file and save to a variable
    with open(input_json, 'r') as file:
        data = json.load(file)

    # Step 2: Convert to a DataFrame
    df = pd.DataFrame(data, columns=['Original', 'Values'])

    # Step 3: Convert 2-list to 2 separate columns
    df[['NB', 'Opposite']] = pd.DataFrame(df['Values'].tolist(), index=df.index)

    # Step 4: Rename the columns
    df.drop(columns=['Values'], inplace=True)

    return df

def list_to_df(input_json):
    # Step 1: Import a JSON file and save to a variable
    with open(input_json, 'r') as file:
        data = json.load(file)
    return pd.Series(data)
    
female_pronouns = pronouns_to_df('FEMALE_PRONOUN_DICT.json')
female_pronouns['Match case'] = True
male_pronouns = pronouns_to_df('MALE_PRONOUN_DICT.json')
male_pronouns['Match case'] = True
names = pd.DataFrame()
names['Female'] = list_to_df('girl_names.json')
names['NB'] = list_to_df('nb_names.json')
names['Male'] = list_to_df('boy_names.json')
exclusions = pd.DataFrame()
exclusions['Common'] = list_to_df('COMMON_WORDS.json')
exclusions['Warning'] = list_to_df('WARNING_WORDS.json')

with pd.ExcelWriter('reference.xlsx', engine='xlsxwriter') as writer:
    female_pronouns.to_excel(writer, sheet_name='Female pronouns', index=False)
    male_pronouns.to_excel(writer, sheet_name='Male pronouns', index=False)
    names.to_excel(writer, sheet_name='Names', index=False)
    exclusions.to_excel(writer, sheet_name='Exclusions', index=False)
    worksheet = writer.sheets['Female pronouns']
    worksheet.autofit()
    worksheet = writer.sheets['Male pronouns']
    worksheet.autofit()
    worksheet = writer.sheets['Names']
    worksheet.autofit()
    worksheet = writer.sheets['Exclusions']
    worksheet.autofit()
