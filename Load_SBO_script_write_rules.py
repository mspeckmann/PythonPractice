import os
import csv
import pandas as pd
import serial as Serial
import glob
import numpy as np
from datetime import datetime

def _load():
    list_ = []
    sbo_frame = pd.DataFrame()
    dir = '//phsbsapp2/bsc_drop/SBOPathway'
    allfiles = glob.glob(dir + '/*.csv')
    for file_ in allfiles:
        df1 = pd.read_csv(file_, sep='|')
        list_.append(df1)
    sbo_frame = pd.concat(list_)
    sbo_frame.to_csv('Raw_Collection.csv', index=False, sep=',')
    print ('Raw File Extracted')
    return sbo_frame

def unique_value(row):
    if row['Question Id'] == '1':
        val = 1
    else:
        val = 0
    return val

def new_qid(row):
    if row['Question Id'] == '1':
        val = 1
    elif row['Question Id'] == '5':
        val = 2
    elif row['Question Id'] == '6':
        val = 3
    elif row['Question Id'] == '9':
        val = 4
    elif row['Question Id'] == '9a':
        val = 5
    elif row['Question Id'] == '10':
        val = 6
    elif row['Question Id'] == '10a':
        val = 7
    elif row['Question Id'] == '11':
        val = 8
    elif row['Question Id'] == '14':
        val = 9
    elif row['Question Id'] == '15':
        val = 10
    elif row['Question Id'] == '16':
        val = 11
    elif row['Question Id'] == '17':
        val = 12
    elif row['Question Id'] == '18':
        val = 13
    elif row['Question Id'] == '19':
        val = 14
    elif row['Question Id'] == '20':
        val = 15
    elif row['Question Id'] == '21':
        val = 16
    elif row['Question Id'] == '22':
        val = 17
    elif row['Question Id'] == '23':
        val = 18
    elif row['Question Id'] == '24':
        val = 19
    elif row['Question Id'] == '25':
        val = 20
    else:
        val = 0
    return val

def is_failed(row):
    if row['Is_Failed'] == '1':
        val = 1
    else:
        val = 0

def mmyyyy(row):
    t = datetime.strptime(row['Admit Date'], '%m/%d/%Y %I:%M %p')
    t = str(t.strftime("'%b %Y'"))
    return t



def _cleanup():
    sbo_frame = pd.DataFrame(_load())
    sbo_frame.drop_duplicates(keep='last', subset = ['Pathway Id','Patient External Id','Patient LastName'
        ,'Patient FirstName','CSN','MRN','Admit Date','Question Id'], inplace=True)
    a = ['Xxxxbwhcptest']
    sbo_frame = sbo_frame[~sbo_frame['Patient LastName'].isin(a)]
    a = ['Unenrolled']
    sbo_frame = sbo_frame[~sbo_frame['Enrollment Status'].isin(a)]
    #a = ['None']
    #sbo_frame = sbo_frame[~sbo_frame['Completion Status'].isin(a)]
    sbo_frame['Is Failed'] = sbo_frame['Is Failed'].astype(float)
    sbo_frame['Unique Identifier'] = sbo_frame.apply(unique_value, axis = 1)
    #sbo_frame['Unique Identifier'] = np.where(sbo_frame['Question Id'] == '1', '1', '0')
    sbo_frame['New Q Id'] = sbo_frame.apply(new_qid, axis = 1)
    sbo_frame['Full Name'] = sbo_frame['Patient LastName'].map(str) + ', ' + sbo_frame['Patient FirstName']
    sbo_frame['MMYYYY'] = sbo_frame.apply(mmyyyy, axis = 1)
    sbo_frame.to_csv('CP_SBO_Dashboard.csv', index=False, sep=',')
    print('Dashboard File Extracted')
    return sbo_frame

def _list():
    sbo_frame = pd.DataFrame(_cleanup())
    sbo_frame.drop_duplicates(keep='last', subset = ['Patient External Id','Patient LastName'
        ,'Patient FirstName','CSN','MRN'], inplace=True)
    col_list = ['Full Name','CSN','MRN','Completion Status','Is Failed']
    sbo_frame = sbo_frame[col_list]
    sbo_frame.to_csv('Cases.csv', index=False, sep=',')
    print('Case List Extracted')
    return sbo_frame




print(_list())





