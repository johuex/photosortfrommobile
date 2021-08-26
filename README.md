# photosortfrommobile
Sorting photos by month and year from Samsung mobile to PC.

## How it works
* User chooses input and output directory;
* In input directory program read file's name;
* By template yyyymmdd_hhmmss.jpg read year and month;
* Copying this file to 'yyyy/yyyy_mm' folder of output directory;
* If file's name doesn't match the pattern template, then copy it to 'not_sorted' folder of output directory;
* Done!

## Bugs:
1. Doesn't update progressBar;
2. By clicking "Close program" sorting process doesn't kill :(
3. There should be no other folders in input folder - only photos and videos :(


