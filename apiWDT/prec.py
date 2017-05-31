## https://github.com/wdtinc/skywise-insight-py
## 

import json
from skywiseinsight import InsightResource

#### DEGREE DAYS
from skywiseinsight import Gdd as gdd
from skywiseinsight import Gdd as cdd
from skywiseinsight import Gdd as hdd

#### PRECIPITATION
from skywiseinsight import DailyPrecipitation as dp
from skywiseinsight import HourlyPrecipitation as hp

#### RELATIVE HUMIDITY
from skywiseinsight import HourlyRelativeHumidity as hrh

#### SOLAR RADIATION
from skywiseinsight import DailySolarRadiation as dsr
from skywiseinsight import HourlySolarRadiation as hsr

#### TEMPERATURE
from skywiseinsight import HourlyTemperature as ht
from skywiseinsight import DailyHighTemperature as dht
from skywiseinsight import DailyLowTemperature as dlt
from skywiseinsight import HourlyDewpoint as hd

#### WIND
from skywiseinsight import HourlyWindSpeed as hws
from skywiseinsight import HourlyWindDirection as hwd


#### EVAPOTRANSPIRATION
from skywiseinsight import DailyEtShortCrop as desc
from skywiseinsight import DailyEtTallCrop as detc
from skywiseinsight import HourlyEtShortCrop as hesc
from skywiseinsight import HourlyEtTallCrop as hetc

#### Application ID and Keys
InsightResource.set_user('72bd6b2d')
InsightResource.set_password('1bf9b8a0fba009655e4bca9f446877cf')

# Enter latitude & longitude 
Lat = 19.532691
Long = -98.845705

#### DEGREE DAYS
# Growing Degree Days
var_gdd = json.dumps(gdd.location(Lat, Long).json())
print '\nGrowing Degree Days\n', var_gdd

# Cooling Degree Days
var_cdd = json.dumps(cdd.location(Lat, Long).json())
print '\nCooling Degree Days\n', var_cdd

# Heating Degree Days
var_hdd = json.dumps(hdd.location(Lat, Long).json())
print '\nHeating Degree Days\n', var_hdd

#### PRECIPITATION
# Daily Precipitation
var_dp = json.dumps(dp.location(Lat, Long).json())
print '\nDaily Precipitation\n', var_dp

# Hourly Precipitation
var_hp = json.dumps(hp.location(Lat, Long).json())
print '\nHourly Precipitation\n', var_hp

#### RELATIVE HUMIDITY
# Hourly Relative Humidity
var_hrh = json.dumps(hrh.location(Lat, Long).json())
print '\nHourly Relative Humidity\n', var_hrh

### SOLAR RADIATION
# Daily Solar Radiation
var_dsr = json.dumps(dsr.location(Lat, Long).json())
print '\nDaily Solar Radiation\n', var_dsr

# Hourly Solar Radiation
var_hsr = json.dumps(hsr.location(Lat, Long).json())
print '\nHourly Solar Radiation\n', var_hsr
#print json.dumps(hsr.json())

#### TEMPERATURE
# Hourly Temperature
var_ht = json.dumps(ht.location(Lat, Long).json())
print '\nHourly Temperature\n', var_ht

# Daily High Temperature
var_dht = json.dumps(dht.location(Lat, Long).json())
print '\nDaily High Temperature\n', var_dht

# Daily Low Temperature
var_dlt = json.dumps(dlt.location(Lat, Long).json())
print '\nDaily Low Temperature\n', var_dlt

# Hourly Dewpoint
var_hd = json.dumps(hd.location(Lat, Long).json())
print '\nHourly Dewpoint\n', var_hd

#### WIND
# Hourly Wind Speed
var_hws = json.dumps(hws.location(Lat, Long).json())
print '\nHourly Wind Speed\n', var_hws

# Hourly Wind Direction
var_hwd = json.dumps(hwd.location(Lat, Long).json())
print '\nHourly Wind Direction\n', var_hwd

#### EVAPOTRANSPIRATION
# Daily Evapotranspiration Short Crop
var_desc = json.dumps(desc.location(Lat, Long).json())
print '\nDaily Evapotranspiration Short Crop\n', var_desc

# Daily Evapotranspiration Tall Crop
var_detc = json.dumps(detc.location(Lat, Long).json())
print '\nDaily Evapotranspiration Tall Crop\n', var_detc

# Hourly Evapotranspiration Short Crop
var_hesc = json.dumps(hesc.location(Lat, Long).json())
print '\nHourly Evapotranspiration Short Crop\n', var_hesc

# Hourly Evapotranspiration Tall Crop
var_hetc = json.dumps(hetc.location(Lat, Long).json())
print '\nHourly Evapotranspiration Tall Crop\n', var_hetc
