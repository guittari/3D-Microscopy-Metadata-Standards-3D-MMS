import json
import yaml
import argparse
from jsonschema import validate, exceptions
from jsonschema.validators import Draft7Validator

# ========================================== Script Information ===========================================
'''
This script takes an input JSON file containing metadata for a specified Category and validates
that data against its corresponding JSON schema.  Any discrepancies between the metadata structure and its schema will
be displayed on the command line as a ValidationError along with relevant info about where the issue is.
The input JSON file should be placed in the directory, .../json_schemas/input_files/data.xlsm

'''

# ========================================== Functions ===========================================
def load_schema(category):
    with open("json_schemas/schemas/"+category+"_schema.json", "r") as f:
        schema = json.load(f)

    return schema

def load_input_file(input_file_name):
    with open("json_schemas/schema_tests/"+input_file_name, "r") as f:
        instance = json.load(f)

    return instance

# =========================== Reading input parameters =======================================
with open('config.yaml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

parser = argparse.ArgumentParser(description='Run the validator.')
parser.add_argument('-c', '--category',
                    choices=['contributors',
                    'dataset',
                    'testing',
                    'image',
                    'instrument',
                    'publication',
                    'record',
                    'specimen'],
                    default=cfg['category'],
                    help='Metadata category to validate')
parser.add_argument('-i', '--input_file_name',
                    default=cfg['input_file_name'],
                    help='Tell which input data file to validate.')


args = parser.parse_args()
input_category = args.category.capitalize()
input_file_name = args.input_file_name

instance = load_input_file(input_file_name)
schema = load_schema(input_category)

# =========================== Initializing Category dict =======================================
# creating a dictionary as "master" list with categories and their respective expected columns
categories_dict = {
    "projects": [ "ID", "Name", "Title", "ShortTitle", "Description", "Protocol", "BossDBURIs", "GrantNumber", "Grant Name", "PublicationDOI", "Year", "License", "Keywords"],
    "collections": [ "ID", "Name", "BOSSDBURI", "Title", "Description", "Public", "Creator", "Contributors", "DateCreated", "DateModified", "License", "Organization", "GrantNumber", "R24Name", "R24Link", "Version", "Species", "Experiments"],
    "experiments": [ "ID", "ExperimentName", "BCDCCollection", "BOSSDBURI", "SampleType", "SpeciesCommonName", "SpeciesTaxonomyID", "GenoType", "SubjectID", "Age", "Sex", "Modality", "Technique", "AnatomicalStructure", "ParentSpecimenID", "ParentSpecimentType", "SubspecimentQuantity", "Investigator", "Description", "BICCNDeliveryQuarter", "Protocol", "Public", "Creator", "Contributors", "DateCreated", "DateModified", "License", "ImageLocation", "CoordinateFrame", "Version", "Channels"],
    "channels": [ "ID", "Name", "BCDCCollection", "BossDBURI", "Description", "ArchiveURL", "Creator", "DateCreated", "ChannelType", "DataType", "Public", "Contributors", "License"]
}

# =========================== Checking and returning any ValidationErrors =======================================
print(f'\nValidating submitted instance for category: "{input_category}"...')

try:
    validate(instance=instance, schema=schema)
    print('No errors found')
except exceptions.ValidationError:
    v = Draft7Validator(schema)
    error_list = sorted(v.iter_errors(instance), key=str)
    print(f"Validation error(s) found: {len(error_list)}")
    i = 1
    for error in error_list:
        if input_category == "Record":
            category = list(set(error.schema_path).intersection(list(categories_dict.keys())))[0]
        else:
            category = input_category
        property = list(set(error.schema_path).intersection(categories_dict[category]))
        if len(property) == 0:
            property = "missing"
        print(f"\nError {i}:")
        print(f"Category: {''.join(category)}")        
        print(f"Property: {''.join(property)}")
        print(error.message)
        i += 1
