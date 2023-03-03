## Overview
The goal of this work is to eliminate issues found by manually entering connectomic data for our desired query. The metadata fields are organized into categories: projects,collections,experiments,and channels. 

### Configuration file
A `config.yaml` file is provided where a user can specify input files and categories for the Data Conversion and Validator scripts.  Parameters corresponding to each script are as follows:

`convert_and_extract_from_csv.py`
- input_excel_file: specifies which Excel workbook to use

`json_schema_validator.py`
- category: specifies which metadata category to validate against
- input_file_name: specifies which input JSON file to validate

Input files should be placed in the directory `json_schemas/input_files`.


## Data Conversion and Validation usage

### Purpose
The conversion script is used to convert input datasets in Excel form to a JSON format, which is then run through a JSON Schema validator to confirm that the data meets criteria.  After converting the datasets from Excel to JSON formats, the validator will check the newly generated JSON file against pre-defined JSON schemas.  Any resulting discrepancies or errors will be displayed on the command line terminal.

### Usage
To run the conversion script, from the main directory, run the following in the command line.

```
python convert_and_extract_from_csv.py
```

This will use the configuration found in `config.yaml`.  To specify a different input excel file from the command line, use the `-i` argument, as detailed in the Command Line Options section.  An example of specifying from the command line for a different Excel sheet, named "example_metadata_file_here.xlsx", is below.

```
python convert_and_extract_from_csv.py -i example_metadata_file_here.xlsx
```

```
usage: convert_and_extract_from_csv.py [-h] [-i INPUT_EXCEL_FILE]

Run the conversion script.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_EXCEL_FILE, --input_excel_file INPUT_EXCEL_FILE       
                        Tell which input Excel file to convert. 
```

## Validator usage
The JSON Validator takes in a user's submitted data in JSON form and compares its contents to the specifications of the corresponding categorical JSON schema, returning a message indicating if any errors found and along with details of found errors.

### Purpose
The validator can be used to confirm submitted data, whether a full dataset or individual category, meets the submission criteria found for each category found on the DORY website.

### Usage
To run the validator, from the main directory, run the following in the command line.

```
python json_schema_test.py
```

This will use the configuration found in `config.yaml`.  To specify a different input file or category from the command line, use the `-i` or `-c` arguments, respectively, as detailed in the Command Line Options section.  An example of specifying from the command line for the category `testing` is below.

```
python json_schema_validator.py -c testing -i testing_test.json
```

```
usage: json_schema_test.py [-h] [-i INPUT_FILE_NAME]
                           [-c {projects,collections,experiments,channels}]

Run the annotators.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE_NAME, --input_file_name INPUT_FILE_NAME
                        Tell which input data file to validate.
  -c {projects,collections,experiments,channels}, --category {projects,collections,experiments,channels}
                        Metadata category to validate
```
