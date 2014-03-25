import pandas as pd
import numpy as np
import json, os, zipfile
pd.set_option('display.width', 160)
pd.set_option('display.max_rows', 10)

POSTCODES_CSV = 'postcodes.csv'
POSTCODES_HDF5 = 'postcodes.h5'
POSTCODES_HDF5_ZIP = 'postcodes.h5.zip'

PP_CSV = 'pp-complete.csv'
PP_CSV_ABBREV = 'pp-head.csv'
PP_COLUMNS = 'columns.json'
PROCESSED_DATA = 'pp_processed.h5'
OPTIONS_JSON = 'pp_options.json'

def generate_postcodes_HDF5(fname = POSTCODES_CSV):
    """
    generates an hdf5 file of postcodes mapped to lats and longs.
    file from http://www.doogal.co.uk/UKPostcodes.php
    """
    print 'reading %s...' % fname
    df = pd.read_csv(fname, low_memory=False)
    pc = pd.DataFrame(df['Postcode'])
    pc.columns = ['postcode']
    pc['lat']=df['Latitude']
    pc['long']=df['Longitude']
    pc = pc[~pc.lat.isnull()][~pc.long.isnull()]
    pc = pc.set_index('postcode')
    store = pd.HDFStore(POSTCODES_HDF5, 'w')
    store['pc'] = pc
    store.close()
    print 'postcode data succesfully converted and saved to %s' % POSTCODES_HDF5

class PricePaid(object):
    """
    processes the land registry price paid csv file.
    """
    remove_cols = ['paon', 'saon', 'street', 'locality',]
    option_cols = ['type', 'duration', 'town', 'district', 'country']
    options = {}
    
    def __init__(self, pp_fname, column_json_name = PP_COLUMNS):
        self.columns = json.load(open(column_json_name, 'r'))
        self._pp_fname = pp_fname
        
    def load_df(self):
        """
        load load the csv file and process columns.
        """
        self.df = pd.read_csv(self._pp_fname, header = None)
        print 'loaded csv, rows: %d, processing...' % len(self.df.values)
        self.df.columns = self.columns
        self.df = self.df.drop('id', 1)
        self.df['price'] = self.df.price.astype(int)
        self.df['date'] = self.df.date.astype('datetime64[ns]')
        self.df['postcode'] = self.df.postcode.fillna('-')
        self.df = self.df.drop('record_status', 1)
        print 'processed main columns, removing extranious...'
        for col in self.remove_cols:
            self.df = self.df.drop(col, 1)
        print 'processed option columns...'
        self.df['new'] = self.df.new == 'Y'
        for col_name in self.option_cols:
            self._option_column(col_name)
    
    def get_latlong(self, pc_hdf5_fname = POSTCODES_HDF5):
        print 'loading postcode file...'
        self._pc = pd.read_hdf(pc_hdf5_fname, 'pc')
        print 'loaded %s, searching for lats and longs...' % pc_hdf5_fname
        self.df['lat'] = np.nan
        self.df['long'] = np.nan
        errors = 0
        total = float(len(self.df.values))
        for i, pc in enumerate(self.df.postcode.values):
            if i % 1e4 == 0 and i > 0:
                print 'processed %d postcodes, %0.2f%%' % (i, float(i)/total*100.0)
            if pc != '-':
                result = self._find_lat_long(pc)
                if result:
                    self.df['lat'][i], self.df['long'][i] = result
                else:
                    errors +=1
        print 'postcodes not found: %d' % (errors)
        
    def save(self, fname = PROCESSED_DATA):
        store = pd.HDFStore(fname, 'w')
        store.put('pp', self.df, format='table')
        store.close()
        print 'DataFrame saved to %s' % fname
    
    def save_options(self, fname = OPTIONS_JSON):
        json.dump(self.options, open(fname, 'w'), indent=2)
        print 'Options saved to %s' % fname

    def _option_column(self, col_name):
        col = self.df[col_name]
        options = {v:i for i, v in enumerate(set(col.tolist()))}
        print 'found %d options for %s' % (len(options), col_name)
        self.options[col_name] = options
        self.df[col_name] = col.apply(lambda v: options.get(v, -1))

    def _find_lat_long(self, pc):
        try:
            result = self._pc.loc[pc.strip()]
        except KeyError, e:
            #print 'Postcode not found: %r' % pc
            return
        else:
            return (result.lat, result.long)

if __name__ == '__main__':
    """
    csv file downloaded from:
    http://www.landregistry.gov.uk/market-trend-data/public-data/price-paid-data/download
    """
    fname = PP_CSV
    """
    To test you can create an abbreviated list csv file and try with that, in linux:
    >> head -n 100000 pp-complete.csv >> pp-head.csv
    or similar
    """
    #fname = PP_CSV_ABBREV
    if os.path.exists(POSTCODES_HDF5_ZIP):
        print 'extracting %s from %s...' % (POSTCODES_HDF5, POSTCODES_HDF5_ZIP)
        zipfile.ZipFile(POSTCODES_HDF5_ZIP).extract(POSTCODES_HDF5)
    if not os.path.exists(POSTCODES_HDF5):
        print '%s does not exist, generating it...' % POSTCODES_HDF5
        generate_postcodes_HDF5()
    pp = PricePaid(fname)
    pp.load_df()
    pp.save_options()
    pp.get_latlong()
    pp.save()
    print pp.df
