land-registry-price-paid-data
=============================

Converting UK Land registry house price data to Python Pandas DataFrame.

The results of running `csv_to_HDF5.py` is a `1.7 Gb` HDF5 file suitable for importing into Pandas, it contains 18809484 rows and the following columns:

* price
* date
* postcode
* type
* new
* duration
* town
* district
* county
* lat
* long

See [here](http://www.landregistry.gov.uk/market-trend-data/public-data/price-paid-faq#m18) for a description of the columns - note some columns have been removed to save space and loading time.

type, duration, town, district and county are converted to ints, they can be mapped to their original values using `pp_options.json`.

Latitudide and Longitudes are generated from Postcode mapping, see below.

To run `csv_to_HDF5.py` you need to download the massive price paid csv file from the Land Registry, it's available for download from here:

    http://www.landregistry.gov.uk/market-trend-data/public-data/price-paid-data/download

`csv_to_HDF5.py` assumes you have `pp-complete.csv` in the working directory. 

It also assumes you have either `postcodes.h5.zip`, `postcodes.h5` or `postcodes.csv` in the working directory, this is used to find latitude and longitudes for postcodes. The zip file is included in this repo and is extract to `postcodes.h5` the first time the script is run. If these are not present the latter is generated from the csv file which in turn is available from [here](http://www.doogal.co.uk/UKPostcodes.php), the csv file is an (almost) complete list of UK postcodes. There are currently 2342 missing out of 18809484.

On my computer (Intel i7-3770, 16GB ram, OS: Ubuntu 13.10 64bit) this takes 41 minutes to run and uses about 8-10Gb of RAM.


### Example

To demonstrate that this isn't completely pointless, `example_processing.ipynb` (and it's plain python sister) demconstrate loading the DataFrame and plotting house price vs. distance from central london for houses purchased since June 2013 within the city of London.