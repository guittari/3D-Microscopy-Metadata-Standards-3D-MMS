import regex as re
import json
import numpy as np

import pandas as pd

# ============ Extract csv files from excel template ==========
# input_excel_file = "input_files/brain_microscopy_metadata_entry_template.xlsm"
input_excel_file = "brain-metadata-validation/json_schemas/input_files/brain_microscopy_metadata_entry_template.xlsm"

df = pd.read_excel(input_excel_file, sheet_name=None, skiprows=2)
for key in df.keys():
    if key=="README" or key=="dropdown":
        continue
    else:
        # df[key].to_csv(f'output_files/120321/{key}_120321.csv', index=False)
        output_file = f'brain-metadata-validation/json_schemas/output_files/120821/{key.lower()}_120821.csv'
        with open(output_file, 'w+') as f:
            df[key].to_csv(f, index=False)
        
# Read in component csv files and convert to a record in dictionary format

record = {}

# =========== List Components =============
list_record_components = ['Contributors', 'Publications', 'Funders'] # components that allow multiple entries (multiple contributors, funders, etc.)
object_record_components = ['Instrument', 'Dataset', "Specimen", "Image"] # components that do not allow multiple entries (instrument, etc.)

for c in list_record_components + object_record_components:
    # df = pd.read_csv(f"input_files/BIL_DOI_datasets_MM_{c.lower()}.csv")
    # df = pd.read_csv(f"output_files/120321/{c.lower()}_120321.csv")
    df = pd.read_csv(f"brain-metadata-validation/json_schemas/output_files/120821/{c.lower()}_120821.csv")
    object_list = [] # keeps track of record entries

    arrayCols = [re.search('^[a-zA-Z]*', x)[0] for x in df.columns if re.search('array$', x)] # identify columns which are arrays (can have multiple values)
    # csvCols = [re.search('^[a-zA-Z]*', x)[0] for x in df.columns if re.search('csv$', x)]
    csvCols = [x.split('+')[0] for x in df.columns if '+' in x]
    df.columns = [re.search('^[a-zA-Z1-9]*', x)[0] for x in df.columns] # clean up column names

    id_col = [col for col in df.columns if (re.search('Name$', col) or re.search('relatedIdentifier$', col))] # identify the unique id column if there is one
    if len(id_col) == 1:
        id_col = id_col[0]
    else:
        id_col = None
    used_ids = {} # keeps tracked of existing unique identifiers

    # create a dict for each row (entry) in the df and add it to a list
    for i in range(len(df)): # Go through rows in dataframe
        record_dict = df.iloc[i].to_dict() # current row represented as a dictionary
        for col in df.columns:

            try:
                record_dict[col] = float(record_dict[col])
            except:
                pass
            # print(record_dict[col], type(record_dict[col]))
            if type(record_dict[col]) not in [str, list] and record_dict[col] is not None and np.isnan(record_dict[col]):
                record_dict[col] = None
            if col in csvCols and record_dict[col] != None:
                record_dict[col] = record_dict[col].split('|')
                for j,k in enumerate(record_dict[col]):
                    try:
                        record_dict[col][j] = float(k)
                    except:
                        pass
            # elif col in csvCols and col == None:

            if col in arrayCols:
                record_dict[col] = [record_dict[col]]


        if id_col is not None and record_dict[id_col] in used_ids.keys():  # If tan entry with the same id already exists
            # Append information in the array columns to an existing entry
            for col in arrayCols:
                object_list[used_ids[record_dict[id_col]]][col] += record_dict[col]
                object_list[used_ids[record_dict[id_col]]][col] = list(set(object_list[used_ids[record_dict[id_col]]][col]))

        elif id_col is not None and record_dict[id_col] not in used_ids.keys():  # add id to used_ids
            object_list.append(record_dict)
            used_ids[record_dict[id_col]] = len(object_list) - 1
        else:
            object_list.append(record_dict)

    if c in list_record_components:
        record[c] = object_list
    if c in object_record_components:
        record[c] = object_list[0]

with open("output_files/BIL_DOI_datasets_MM_120321.json", "w") as f:
    json.dump(record, f)

with open("output_files/BIL_DOI_datasets_MM_112321_2.json", "r") as f:
    r = json.load(f)
