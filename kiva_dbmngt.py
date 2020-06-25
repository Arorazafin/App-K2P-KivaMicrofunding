import pandas as pd
import numpy as np
import json
import glob
from sqlalchemy import create_engine
import psycopg2
from collections import defaultdict
import sys
from past.builtins import xrange
import time


class DBKiva(object):

    def __init__(self):
        self.cols = ['id', 'name','original_language',
                    'translated_description','funded_amount',
                    'loan_amount','status','image_id','video_id',
                    'activity','sector','use','country_code','town',
                    'partner_id','posted_time','planned_expiration_time',
                    'disbursed_time','funded_time','term_in_months',
                    'lender_count','tags']

        self.min_date = '2012-01-25'  # date kiva expiration policy implemented
        self.df = pd.DataFrame()  # pandas dataframe of loan data
        self.sql = defaultdict()  # info for connecting to postgres db
        self.tables = []  # sql tables storing the loan data
        self.sql_engine = None  # used with sqlalchemy
        self.query = ''

    def import_json(self, files):
        '''
        import json file
        '''

        with open(files) as f:
            dic = json.load(f)
        self.df = pd.DataFrame(dic)

    def import_csv(self, files):
        '''
        import csv file
        '''
        self.df = pd.read_csv(files, sep=',')

    def transform_dates(self):
        '''
        Converts dates to datetime objects.
        **Drops loans posted before expiration policy implemented '2012-01-25'**.
        '''
        self.df['posted_time'] = pd.to_datetime(self.df.posted_time)
        self.df['planned_expiration_time'] = pd.to_datetime(self.df.planned_expiration_time)
        self.df['disbursed_time'] = pd.to_datetime(self.df.disbursed_time)
        self.df['funded_time'] = pd.to_datetime(self.df.funded_time)

        #drop
        mask = (self.df['posted_time'] > self.min_date) & (self.df['posted_time'] <= self.df.posted_time.max())
        self.df = self.df[mask]


    def get_borrowers(self):
        '''
        transform dict borrowers column into string
        '''
        self.df['borrowers'] = list(map(lambda x: json.dumps(x), self.df['borrowers']))

    def transform_df(self):
        '''
        Transforms the dataframe using the 2 methods above
        '''

        self.df =self.df [self.cols]
        self.df = self.df.drop_duplicates(['id'])
        self.df = self.df.set_index('id')

        self.transform_dates()
        #self.get_borrowers()


    def setup_sql(self, user, pw, db='kiva', host='localhost', port='5432'):
        '''
        sets up sql connection for exporting and loading from sql
        must be run before export_to_sql, load_from_sql, or merge_db
        '''
        self.sql['db'] = db
        self.sql['user'] = user
        self.sql['pw'] = pw
        self.sql['host'] = host
        self.sql['port'] = str(port)
        self.tables = []
        engstr = 'postgresql://%s:%s@%s:%s/%s' % (user, pw, host, port, db)
        self.sql_engine = create_engine(engstr)

    def run_query(self):
        '''
        Executes self.query. Used by export_to_sql
        '''
        conn = psycopg2.connect(dbname=self.sql['db'], user=self.sql['user'],
                                host=self.sql['host'], password=self.sql['pw'])
        c = conn.cursor()
        c.execute(self.query)
        conn.commit()
        conn.close()
        self.query = ''

    def export_to_sql(self, table):
        '''
        input name of table to insert the pandas dataframe self.df
        using the sql db, user, and pw input by the setup sql function
        '''
        self.query += 'DROP TABLE if exists %s' % table
        self.run_query()
        self.df.to_sql(table, self.sql_engine)
        self.tables.append(table)


    def run_importTableFromFile(self, fileName, fileType, user, pw, db='kiva', host='localhost',
                     port='5432'):
        '''
        Imports, transforms, and loads loan data into sql.
        Address is folder containing json files from kiva api.
        '''
        t_start = time.perf_counter()

        if fileType == 'json':
            jsfile = 'data/%s.json' % fileName
            print('-Json file found: ',jsfile)
            self.import_json(files=jsfile)
            print('-json files converted to df')
        elif fileType == 'csv':
            csvfile = 'data/%s.csv' % fileName
            print('-csv file found: ',csvfile)
            self.import_csv(files=csvfile)
            print('-csv files converted to df')

        table_name = fileName
        
        if fileName == 'loans':
            self.transform_df()
            print('-df laons transformed')

        print('-SQL DB to be created ...')
        self.setup_sql(user, pw, db=db, host=host, port=port)
        self.export_to_sql(table_name)

        print('-Table {} created in the DB'.format(table_name))
        print('-Features list integrated in the table : ',list(self.df.columns)) 
        print('-Shape of the table : ',self.df.shape) 
        print('-Process all done')

        t_end = time.perf_counter()
        deltaT= t_end - t_start
        minutes, secondes = divmod(deltaT, 60)
        print('-Table created on {:02d}mn{:02d}sec'.format(int(minutes),int(secondes)))

    def run_updateLoansTable_untilNow()

        #select the last posted_time in the loan table

        #define the query for API

        #request url from api

        #run uptadeTable and merge the table with exesting table
    
    def run_updateLoansTable_status()
        #select id with "fundraising"
        #define query for API
        #request url from api
        #write and update table



if __name__ == '__main__':
    '''
    Input address of the folder where the unzipped kiva loan json files
    are located and postgres username and password. Optional: input postgres
    db namek, host, port, batch size, competing_loans boolean, table nam
    ex: dbkiva_mngt.py folder username password
    '''
    
    dbkiva = DBKiva()
    dbkiva.create_db(*sys.argv[1:])
