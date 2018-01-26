import sqlite3
from contextlib import closing
from collections import defaultdict
import os

class CreateDB:
    def __init__(self, db_name, currDir = os.getcwd()):
        self.db_name = db_name
        self.currDir = currDir


    def create_db(self):

        try:
            self.db_conn = sqlite3.connect(self.db_name)
            self.db_cursor = self.db_conn.cursor()
        except sqlite3.Error as e:
            print(e)


    def create_table(self):
        self.create_db()
        c = self.db_cursor
        try:
            if self.db_name == 'baseball.db':
                c.execute('''CREATE TABLE baseball_stats
                            (player_name text, games_played integer, average real, salary real)''')
                print ('The database {0} and table baseball_stats has been created.'.format(self.db_name))
            elif self.db_name == 'stocks.db':
                c.execute('''CREATE TABLE stocks_stats
                            (company_name text, ticker text, exchange_country text, price real, 
                            exchange_rate real, shares_outstanding real, net_income real,
                            market_value_usd real, pe_ratio real)''')
                print ('The database {0} and table stocks_stats has been created.'.format(self.db_name))

            else:
                c.execute(input('Type out a CREATE TABLE statement:'))
                print ('Your custom table has been created.')
        except sqlite3.OperationalError:
            pass
        self.db_conn.commit()
        return self.db_conn


    def bb_insert(self, c, w, x, y, z):

        c.execute("INSERT INTO baseball_stats VALUES (?,?,?,?)", (w,x,y,z))


    def s_insert(self, c, r, s, t, u, v, w, x, y, z):

        c.execute("INSERT INTO stocks_stats VALUES (?,?,?,?,?,?,?,?,?)", (r, s, t, u, v, w, x, y,z))


    def select(self, c):
        '''
        Select all the records from the database.
        Return them as a list of tuples.
        '''
        if self.db_name == 'baseball.db':
            result = c.execute('''Select * FROM baseball_stats''')
        elif self.db_name == 'stocks.db':
            result = c.execute('''Select * FROM stocks_stats''')
        else:
            result = c.execute(input('Type out a SELECT * statement:'))
        return result


    def calc(self, c):
        if self.db_name == 'baseball.db':
            result = c.execute('''Select average, ROUND(AVG(salary),2) from baseball_stats group by average''')
        elif self.db_name == 'stocks.db':
            result = c.execute('''Select exchange_country, count(ticker) from stocks_stats group by exchange_country''')
        return result


#if __name__ == '__main__':
    #salaries = defaultdict(list)
    #CreateDB.create_db("baseball.db")

