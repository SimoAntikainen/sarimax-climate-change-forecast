# SARIMAX-climate-change-forecast

SARIMAX-models have been used to predict climate locally at short time scales. This notebook explores the possibility of using these models to predict global climate change at long time scales. Altought SARIMAX-models cannot take into account all the different factors behind climate change, the created models itself should be easily explainable to non-experts and allow the easy creation of new scenarios.  

## Prequisites

`pip install numpy pandas matplotlib sklearn statsmodels pmdarima`

## Data Sources

### Combined Land-Surface Air and Sea-Surface Water Temperature Anomalies (Land-Ocean Temperature Index, LOTI)

GISTEMP Team, 2019: GISS Surface Temperature Analysis (GISTEMP). NASA Goddard Institute for Space Studies. Dataset accessed 18 Feb 2019 at https://data.giss.nasa.gov/gistemp/.

Hansen, J., R. Ruedy, M. Sato, and K. Lo, 2010: Global surface temperature change, Rev. Geophys., 48, RG4004, doi:10.1029/2010RG000345.

###  Mauna Loa CO2 monthly mean data

Dr. Pieter Tans, NOAA/ESRL (www.esrl.noaa.gov/gmd/ccgg/trends/) and Dr. Ralph Keeling, Scripps Institution of Oceanography (scrippsco2.ucsd.edu/). Dataset accessed 18 Feb 2019

### The Oceanic Niño Index (ONI) 

NOAA. Dataset accessed 18 Feb 2019 at https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt. 


### Sunspot Number
Sunspot data from the World Data Center SILSO, Royal Observatory of Belgium, Brussel. Dataset accessed 18 Feb 2019 at http://www.sidc.be/silso/datafiles#total. 


