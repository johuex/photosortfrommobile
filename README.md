# photosortfrommobile
Sorting photos by month and year from Samsung mobile to PC.

## How to launch
Launch these lines in project root directory (for *NIX):
```
virtualenv venv --python=python3.11
source ./venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## How it works
* Choose input and output directory;
* Read all filenames in input directory;
* Set mask for sorting by year and month of filename;
* Copying this file to 'yyyy/yyyy_mm' folder in output directory;
* If file's name doesn't match the pattern template, then copy it to 'not_sorted' folder in output directory;
* Done!

## Limitations:
1. There should be no other folders in input folder - only photos or videos :(


