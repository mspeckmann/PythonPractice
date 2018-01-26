import os
import csv
import Speckmann_Melinda_create_dbs
from collections import deque
import sqlite3


class AbstractRecord:

    def __init__(self, name):
        self.name = name


class BaseballStatRecord(AbstractRecord):

    def __init__(self, name, salary, G, AVG):
        self.salary = salary
        self.G = G
        self.AVG = AVG

        super(BaseballStatRecord, self).__init__(name)


    def __str__(self):
        return 'Baseball Stat Record: (Player: {0}, Salary: {1}, G: {2}, AVG: {3})'.format \
            (self.name, self.salary, self.G, self.AVG)



class StockStatRecord(AbstractRecord):

    def __init__(self, name, company_name, exchange_country, price, \
                 exchange_rate, shares_outstanding, net_income, \
                 market_value_usd, pe_ratio):
        self.company_name = company_name
        self.exchange_country = exchange_country
        self.price = price
        self.exchange_rate = exchange_rate
        self.shares_outstanding = shares_outstanding
        self.net_income = net_income
        self.market_value_usd = market_value_usd
        self.pe_ratio = pe_ratio

        super(StockStatRecord, self).__init__(name)


    def __str__(self):
        return 'Stock Stat Record: ({0}, {1}, {2}, $price={3}, $ER={4}, $SO={5}, $Net={6}, $MV={7}, $P/E={8})' \
            .format(self.name, self.company_name, self.exchange_country, \
                    self.price, self.exchange_rate, self.shares_outstanding, \
                    self.net_income, self.market_value_usd, self.pe_ratio)

class Error(Exception):
    pass

class BadData(Error):
    pass


class AbstractCSVReader:


    def __init__(self, filename, currDir = os.getcwd()):
        self.currDir = currDir
        self.filename = filename


    def row_to_record(row):
        raise NotImplementedError("Subclasses should implement this!")


    def load(self):
        fpath = os.path.join(self.currDir, self.filename)
        with open (fpath, mode = 'r') as row_in:
            reader = csv.DictReader(row_in)
            recordlist = []
            for row in reader:
                ifempty = bool(any([v=='' for v in row.values()]))
                try:
                    if ifempty == True: #ensures any cells with empty data are not added as a record
                        raise BadData
                    else:
                        recordlist.append(row)
                except BadData:
                    print ("The following record is missing data and will not be added:{0}".format(row))
        row_in.close()
        return recordlist


class BaseballCSVReader(AbstractCSVReader):

    def row_to_record(self):
        recordlist = self.load()
        #removes unwanted columns
        bkeys_keep = ('PLAYER','SALARY','G','AVG')
        unval_list = [{k: v for k, v in d.items() if k in bkeys_keep} for d in recordlist]
        i = 0
        val_list = []
        while i < len(unval_list):
            row = unval_list[i]
            try: #converts strings to integers or floats
                row['SALARY'] = int(row['SALARY'])
                row['G'] = int(row['G'])
                row['AVG'] = round(float(row['AVG']),3)
                val_list.append(row)
            except ValueError as ve:
                print ('Value could not be converted, the following record is removed:{0}'.format(row))
                print(row)
            i+=1
        return val_list


    def record(self): #this method allows for a clean print of each record
        val_list = self.row_to_record()
        i=0
        while i < len(val_list):
            row = val_list[i]
            print(BaseballStatRecord(name=row.get('PLAYER'),salary=row.get('SALARY'),G=row.get('G'),AVG=row.get('AVG')))
            i += 1
        return val_list




class StocksCSVReader(AbstractCSVReader):

    def row_to_record(self):
        unval_list = self.load()
        i = 0
        val_list = []
        while i < len(unval_list):
            row = unval_list[i]
            try:
                row['price'] = round(float(row['price']),2)
                row['exchange_rate'] = round(float(row['exchange_rate']),2)
                row['shares_outstanding'] = round(float(row['shares_outstanding']),2)
                row['net_income'] = round(float(row['net_income']),2)
                try:
                    if row.get('net_income') == 0: #ensures that there isn't any division by zero in the calculation
                        raise BadData
                        print(row)
                    else:
                        val_list.append(row)
                except BadData:
                    print ("There is a zero for net_income. The following record will not be added:{0}".format(row))
            except ValueError as ve:
                print ('Value could not be converted, the following record will be removed:{0}'.format(row))
                print(row)
            i+=1
        return val_list


    def stock_calculations(self):
        val_list = self.row_to_record()
        i = 0
        while i < len(val_list):
            row = val_list[i]
            row['market_value_usd'] = round(row['price'] * row['exchange_rate'] * row['shares_outstanding'],2)
            row['pe_ratio'] = round(row['price']/row['net_income'],2)
            if row.get('pe_ratio') == -0.0:
                row['pe_ratio'] = 0
            i += 1
        return val_list


    def record(self): #this method allows for a clean print of each record
        val_list = self.stock_calculations()
        i=0
        while i < len(val_list):
            row = val_list[i]
            print(StockStatRecord(name=row.get('ticker'),company_name=row.get('company_name'),exchange_country=row.get('exchange_country'),
                    price=row.get('price'),exchange_rate=row.get('exchange_rate'),shares_outstanding=row.get('shares_outstanding'),
                    net_income=row.get('net_income'),market_value_usd=row.get('market_value_usd'),pe_ratio=row.get('pe_ratio')))
            i += 1

class AbstractDAO:

    def __init__(self, db_name):
        self.db_name = db_name

    def insert_records(self, record_list):
        raise NotImplementedError("Subclasses should implement this!")

    def select_all(self):
        raise NotImplementedError("Subclasses should implement this!")

    def connect(self):
        conn = Speckmann_Melinda_create_dbs.CreateDB(self.db_name).create_table()
        return conn

class BaseballStatsDAO(AbstractDAO, BaseballCSVReader):

    #conn = ''

    def insert_records(self, record_list):
        #global conn
        conn = self.connect()
        db_cursor = conn.cursor()
        #record_list = BaseballCSVReader.record()
        i = 0
        while i < len(record_list):
            record = record_list[i]
            Speckmann_Melinda_create_dbs.CreateDB.bb_insert(self, db_cursor, record.get('PLAYER'), record.get('G'), record.get('AVG'), record.get('SALARY'))
            i += 1
        conn.commit()
        conn.close()
        return ('The baseball records have been successfully inserted.')

    def select_all(self):
        conn = self.connect()
        db_cursor = conn.cursor()
        deq = deque([])
        result = Speckmann_Melinda_create_dbs.CreateDB.select(self, db_cursor)
        for BaseballStatRecord in result:
            deq.append(BaseballStatRecord)
        result = Speckmann_Melinda_create_dbs.CreateDB.calc(self, db_cursor)
        bb_dict = {rows[0]:rows[1] for rows in result}
        print('Average Salary by batting average:')
        print("{" + "\n".join("AVG: {} -> avgSAL: {}".format(k, v) for k, v in bb_dict.items()) + "}")
        conn.close()
        return deq





class StockStatsDAO(AbstractDAO, BaseballCSVReader):

    def insert_records(self, record_list):
        conn = self.connect()
        db_cursor = conn.cursor()
        i = 0
        while i < len(record_list):
            record = record_list[i]
            Speckmann_Melinda_create_dbs.CreateDB.s_insert(self, db_cursor, record.get('company_name'), record.get('ticker')
                    ,record.get('exchange_country'), record.get('price'),record.get('exchange_rate'),record.get('shares_outstanding')
                    ,record.get('net_income')
                    ,record.get('market_value_usd')
                    ,record.get('pe_ratio'))
            i += 1
        conn.commit()
        conn.close()
        return ('The stock records have been successfully inserted.')


    def select_all(self):
        conn = self.connect()
        db_cursor = conn.cursor()
        deq = deque([])
        result = Speckmann_Melinda_create_dbs.CreateDB.select(self, db_cursor)
        for StockStatRecord in result:
            deq.append(StockStatRecord)
        result = Speckmann_Melinda_create_dbs.CreateDB.calc(self, db_cursor)
        stock_dict = {rows[0]:rows[1] for rows in result}
        print('Number of tickers by country:')
        print("{" + "\n".join("Country: {} -> #: {}".format(k, v) for k, v in stock_dict.items()) + "}")
        conn.close()
        return deq



if __name__ == '__main__':
    #Project Part 1 Results
    #bb_csv = BaseballCSVReader('MLB2008.csv').record()

    #List of baseball records to load
    bb_records = BaseballCSVReader('MLB2008.csv').row_to_record()
    print (bb_records)

    #Create db, table, insert records
    bb = BaseballStatsDAO('baseball.db')
    print (bb.insert_records(bb_records))

    #Select all records by deque and show average salary by batting average
    print(bb.select_all())


    #Project Part 1 Results
    #stock_csv = StocksCSVReader('StockValuations.csv').record()

    #List of stock records to load
    stock_records = StocksCSVReader('StockValuations.csv').stock_calculations()
    print(stock_records)

    #Create db, table, insert records
    stock = StockStatsDAO('stocks.db')
    print(stock.insert_records(stock_records))

    #Select all records by deque and show # of tickers by country
    print (stock.select_all())




