
# In[1]:

import pandas as pd
from dateutil.parser import parse
pd.set_option('display.width', 160)
pd.set_option('display.max_rows', 10)

PROCESSED_DATA = 'pp_processed.h5'
pp = pd.read_hdf(PROCESSED_DATA, 'pp')
print 'Loaded %s, %d records' % (PROCESSED_DATA, len(pp.index))


# Out[1]:

#     CPU times: user 4.49 s, sys: 1.85 s, total: 6.35 s
#     Wall time: 6.35 s
#     Loaded pp_processed.h5, 18809484 records
# 

# In[15]:

d = parse('2013-06-01')
new_pp = pp[pp.date > d]
new_pp


# Out[15]:

#           price                date  postcode  type    new  duration  town  district  country        lat      long
#     8    190000 2013-10-03 23:00:00  SN14 8LU     2  False         2   348       297      102  51.462176 -2.325391
#     50   137000 2013-12-13 00:00:00   B67 5HE     2  False         2  1160       294       71  52.476655 -1.975369
#     118   99950 2014-01-03 00:00:00   PE3 8QR     2  False         2    78        10       19  52.601204 -0.275785
#     153  320050 2013-08-29 23:00:00   B93 9EG     2  False         2   815       303       71  52.383015 -1.750650
#     189  132000 2013-08-26 23:00:00  TN24 0DE     2  False         2   227        83       61  51.132744  0.889082
#     205   23000 2013-09-17 23:00:00   NE6 3NP     1  False         1   988       379      125  54.969504 -1.545618
#     207  135000 2013-08-08 23:00:00   S41 0PN     2  False         2  1075        60       58  53.220567 -1.411113
#     215  355000 2013-12-19 00:00:00  BH24 1SW     3  False         2   669       315       23  50.858242 -1.776606
#     299  420000 2013-10-03 23:00:00  RG42 6LN     0  False         2   774        99        4  51.441115 -0.715472
#     320  470000 2013-12-16 00:00:00   AL4 0ES     2  False         2   420       152       63  51.758940 -0.304766
#             ...                 ...       ...   ...    ...       ...   ...       ...      ...        ...       ...
#     
#     [534737 rows x 11 columns]

# In[16]:

import json
options = json.load(open('pp_options.json', 'r'))
london_town = options['town']['LONDON']
london = new_pp[new_pp.town == london_town]
london


# Out[16]:

#             price                date  postcode  type    new  duration  town  district  country        lat      long
#     811    450000 2013-10-22 23:00:00   NW6 2DT     1  False         1   803       235       86  51.547281 -0.200192
#     2675   495000 2013-08-18 23:00:00   NW6 4SR     1  False         1   803       235       86  51.541269 -0.191070
#     2892   225000 2013-09-29 23:00:00   W12 7NY     1  False         1   803        70       86  51.510832 -0.230710
#     3238   150000 2013-12-23 00:00:00  SE17 1QQ     2  False         2   803        68       86  51.490004 -0.086361
#     3565  1060000 2013-10-20 23:00:00    N8 9EX     2  False         2   803       348       86  51.575931 -0.119902
#     4307   248000 2013-07-22 23:00:00   SE6 3TW     0  False         2   803       314       86  51.430909 -0.021619
#     4717  2075000 2013-12-03 00:00:00    W6 7EA     2  False         2   803        70       86  51.495375 -0.221325
#     4759   197000 2013-07-07 23:00:00   N16 9NH     1  False         1   803       114       86  51.553264 -0.087832
#     5375   495000 2013-06-19 23:00:00   SE3 9EP     1   True         1   803       154       86  51.459535  0.025641
#     6573   860000 2013-10-31 00:00:00  EC1V 3AP     1   True         1   803         0       86  51.525661 -0.098042
#               ...                 ...       ...   ...    ...       ...   ...       ...      ...        ...       ...
#     
#     [45255 rows x 11 columns]

# In[17]:

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

get_ipython().magic(u"time london['distance'] = london.apply(lambda row: cood_distance(central_london, (row['lat'], row['long'])), axis=1)")


# Out[17]:

#     CPU times: user 2.99 s, sys: 20.3 ms, total: 3.01 s
#     Wall time: 3 s
# 

# In[18]:

# close = london[london.distance < 12] (no need now we're selectng london first)
london_prices = london.price
london_prices.index = london.distance
london_prices


# Out[18]:

#     distance
#     3.747170    450000
#     3.196441    495000
#     4.503981    225000
#     ...
#     5.891484     490000
#     5.445006     208000
#     2.174723    1150000
#     Name: price, Length: 45255, dtype: int64

# In[19]:

import matplotlib.pyplot as plt
#get_ipython().magic(u'matplotlib inline')
london_prices.plot(style='.')
plt.ylim(0, 1e7)
plt.xlabel('Distance from central London (miles)')
plt.ylabel('House Price')
plt.title('House Price vs. Distance from Central London')
plt.show()


# Out[19]:

# image file:

# In[19]:



