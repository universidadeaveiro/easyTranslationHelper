# easyTranslationHelper
Set of features aiming to facilitate translating a project, written in Python.

## Requirements

None. All necessary features are provided by Python's builtin modules

## Usage

### Required inputs
- Select a file to use as a base for the translation (base file).
- Select a second file to use to update base file (e.g. previous version of translated file containing only a subset of current base file keys)

For more information run the scripts help command:
```
EThelper.py -h
```

## Features

- **Get different keys:** Get keys from base file that do not exist in aux file
- **Full parsing:** compose translation file by updating info from base file with data from aux file. This is the default behaviour
- **Parse starting from key:** compose translation file by updating info from base file with data from aux file. String translation is done starting on the line where the provided key (if present) is found
- **Parse starting from line:** compose translation file by updating info from base file with data from aux file. String translation is done starting on the provided line (if valid)
- **Export results into custom output file**
- **Select file encoding:** Select base and aux file file enconding (output file's encoding is set to 'UTF-8')
- **Select key/value separators:** Select base, aux and output file key/value separator.
  - Base file separator defaults to '='
  - Aux file separator defaults to '='
  - Output file separator defaults to base file separator
