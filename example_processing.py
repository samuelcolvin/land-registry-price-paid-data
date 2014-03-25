
# In[1]:

import pandas as pd
from dateutil.parser import parse
pd.set_option('display.width', 160)
pd.set_option('display.max_rows', 10)

PROCESSED_DATA = 'pp_processed.h5'
get_ipython().magic(u"time pp = pd.read_hdf(PROCESSED_DATA, 'pp')")
print 'Loaded %s, %d records' % (PROCESSED_DATA, len(pp.values))


# Out[1]:

#     CPU times: user 4.8 s, sys: 1.77 s, total: 6.58 s
#     Wall time: 6.58 s
#     Loaded pp_processed.h5, 18809484 records
# 

# In[3]:

import math
def cood_distance(latlong1, latlong2):
    """
    from http://www.johndcook.com/python_longitude_latitude.html
    """
    lat1, long1 = latlong1
    lat2, long2 = latlong2
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    miles = arc*3960
    return miles

central_london = (51.518175, -0.126661)


# In[4]:

d = parse('2013-11-01')
new_pp = pp[pp.date > d]
print new_pp


# Out[4]:

#            price       date  postcode  type    new  duration  town  district  country        lat      long
#     50    137000 2013-12-13   B67 5HE     2  False         2  1160       294       71  52.476655 -1.975369
#     118    99950 2014-01-03   PE3 8QR     2  False         2    78        10       19  52.601204 -0.275785
#     215   355000 2013-12-19  BH24 1SW     3  False         2   669       315       23  50.858242 -1.776606
#     320   470000 2013-12-16   AL4 0ES     2  False         2   420       152       63  51.758940 -0.304766
#     335    46500 2013-12-20  CA15 8JP     0  False         2  1039        76       59  54.705779 -3.484528
#     578   276000 2013-11-19   SS1 2UD     0  False         2   166        65       88  51.537212  0.736627
#     683   214950 2013-11-08  RG12 7WH     2  False         2   774        99        4  51.395194 -0.744688
#     799   225000 2013-11-29  CM13 2UG     2  False         2   482       188      108  51.617661  0.332266
#     915   122500 2013-11-15  IP25 6GY     2  False         2  1165       309       49  52.568563  0.854093
#     1281  248000 2013-11-14  CT18 7PL     3  False         2   740       246       61  51.112947  1.156807
#              ...        ...       ...   ...    ...       ...   ...       ...      ...        ...       ...
#     
#     [165535 rows x 11 columns]
# 

# In[5]:

get_ipython().magic(u"time new_pp['distance'] = new_pp.apply(lambda row: cood_distance(central_london, (row['lat'], row['long'])), axis=1)")


# Out[5]:

#     CPU times: user 11.2 s, sys: 28.6 ms, total: 11.2 s
#     Wall time: 11.1 s
# 

# In[6]:

close = new_pp[new_pp.distance < 12]
london_prices = close.price
london_prices.index = close.distance
london_prices


# Out[6]:

#     distance
#     2.607082     150000
#     8.767019     200000
#     4.366583    2075000
#     ...
#     3.909407    270000
#     9.394478    697000
#     8.246070    425000
#     Name: price, Length: 19063, dtype: int64

# In[12]:

import matplotlib.pyplot as plt
# enable running it as pure python
try: eval('%matplotlib inline')
except: pass
london_prices.plot(style='.')
plt.ylim(0, 1e7)
plt.xlabel('Distance from central London (miles)')
plt.ylabel('House Price')
plt.title('House Price vs. Distance from Central London')
plt.show()


# Out[12]:

# image file:

# In[ ]:



