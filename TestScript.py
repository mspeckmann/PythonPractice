import pandas as pd
import pandas.io.sql as psql
import pybgt
import DB_and_Tables
import SQL_Queries
import sys

reload(sys)
sys.setdefaultencoding('utf8')


conn = pybgt.create_connection(server='10.0.2.129', database = 'TaxonomyDB')
conn2 = pybgt.create_connection(server='10.0.2.38', database = DB_and_Tables.DB)

SQ = SQL_Queries.Queries()

#Library.Area
def LibraryArea():
    Area_q = SQ.LibraryArea()
    Area_df = psql.read_sql(Area_q[0], conn)

    #Fix file issues
    Area_df['Name'] = Area_df['Name'].str.replace("'","''")

    pybgt.execute_query(conn2, Area_q[1], results=False, verbose=False)

    x = 0
    while x < len(Area_df):
        Area_i = "Insert into {0} Values({1},'{2}',{3});" \
                 "Insert into {0} Values (1, 'All Areas', 0)".format(DB_and_Tables.Area, Area_df['Id'][x], Area_df['Name'][x],Area_df['SortOrder'][x])
        pybgt.execute_query(conn2, Area_i, results=False, verbose=False)
        x += 1
    print "{0} Table has been added".format(DB_and_Tables.Area)

#Library.State
def LibraryState():
    State_q = SQ.LibraryState()
    State_df = psql.read_sql(State_q[0], conn)
    pybgt.execute_query(conn2, State_q[1], results=False, verbose=False)

    x = 0
    while x < len(State_df):
        State_i = "Insert into {0} Values ({1},{2},'{3}','{4}',{5})".format(DB_and_Tables.State, State_df['Id'][x],State_df['CountryId'][x]
                            ,State_df['Name'][x],State_df['Code'][x],State_df['SortOrder'][x])
        pybgt.execute_query(conn2, State_i, results=False, verbose=False)
        x += 1
    pybgt.execute_query(conn2, State_q[2], results=False, verbose=False)
    print "{0} Table has been added".format(DB_and_Tables.State)

#Library.StateArea
def LibraryStateArea():
    sa_q = SQ.LibraryStateArea()
    sa_msa_df = psql.read_sql(sa_q[0], conn)
    sa_state_df = psql.read_sql(sa_q[1], conn)
    #combine MSA and state
    sa_df = pd.concat([sa_msa_df, sa_state_df])
    #add id column and values
    sa_df['Id'] = range(500, len(sa_df) + 500)
    pybgt.execute_query(conn2, sa_q[2], results=False, verbose=False)

    x = 0
    while x < len(sa_df):
        sa_i = "Insert into {0} Values ({1},'{2}',{3},{4},{5},{6})".format(DB_and_Tables.StateArea, sa_df['Id'][x],sa_df['AreaCode'][x]
                    ,sa_df['Display'][x],sa_df['IsDefault'][x],sa_df['StateId'][x],sa_df['AreaId'][x])
        pybgt.execute_query(conn2, sa_i, results=False, verbose=False)
        x += 1
    pybgt.execute_query(conn2, sa_q[3], results=False, verbose=False)
    print "{0} Table has been added".format(DB_and_Tables.StateArea)

#Library.CareerArea
def LibraryCareerArea():
    CareerArea_q = SQ.LibraryCareerArea()
    CareerArea_df = psql.read_sql(CareerArea_q[0], conn)
    pybgt.execute_query(conn2, CareerArea_q[1], results=False, verbose=False)

    x = 0
    while x < len(CareerArea_df):
        CareerArea_i = "Insert into {0} Values({1},'{2}',{3});".format(DB_and_Tables.CareerArea, CareerArea_df['Id'][x], CareerArea_df['Name'][x], CareerArea_df['LocalisationId'][x])
        pybgt.execute_query(conn2, CareerArea_i, results=False, verbose=False)
        x += 1
    print "{0} Table has been added".format(DB_and_Tables.CareerArea)

#Library.Degree
def LibraryDegree():
    Degree_q = SQ.LibraryDegree()
    Degree_df = psql.read_sql(Degree_q[0], conn)
    pybgt.execute_query(conn2, Degree_q[1], results=False, verbose=False)

    x = 0
    while x < len(Degree_df):
        Degree_i = "Insert into {0} Values({1},'{2}','{3}',{4},{5});".format(DB_and_Tables.Degree,
                    Degree_df['Id'][x], Degree_df['Name'][x], Degree_df['RcipCode'][x], Degree_df['IsDegreeArea'][x], Degree_df['IsClientData'][x])
        pybgt.execute_query(conn2, Degree_i, results=False, verbose=False)
        x += 1
    #add two columns that are both NULL
    pybgt.execute_query(conn2, Degree_q[2], results=False, verbose=True)
    print "{0} Table has been added".format(DB_and_Tables.Degree)

#Library.DegreeEducationLevel
def LibraryDegreeEducationLevel():
    del_q = SQ.LibraryDegreeEducationLevel()
    del_df = psql.read_sql(del_q[0], conn)
    #add id column and values
    del_df['Id'] = range(50000, len(del_df) + 50000)
    pybgt.execute_query(conn2, del_q[1], results=False, verbose=False)

    x = 0
    while x < len(del_df):
        del_i = "Insert into {0} Values ({1},{2},{3},'{4}',{5},{6})".format(DB_and_Tables.Deg_Ed_Level, del_df['Id'][x],del_df['EducationLevel'][x],del_df['DegreesAwarded'][x]
                ,del_df['Name'][x],del_df['ExcludeFromReport'][x],del_df['DegreeId'][x])
        pybgt.execute_query(conn2, del_i, results=False, verbose=False)
        x += 1

    #alter NA and AA name to include apostrophe s
    pybgt.execute_query(conn2, del_q[2], results=False, verbose=False)
    print "{0} Table has been added".format(DB_and_Tables.Deg_Ed_Level)

#Library.DegreeAlias
def LibraryDegreeAlias():
    dega_q = SQ.LibraryDegreeAlias()
    pybgt.execute_query(conn2, dega_q[0], results=False, verbose=False)
    pybgt.execute_query(conn2, dega_q[1], results=False, verbose=False)
    print "{0} Table has been added".format(DB_and_Tables.Deg_Alias)

#Library.InternshipCategory
def LibraryInternshipCategory():
    ic_q = SQ.LibraryInternshipCategory()
    ic_df = psql.read_sql(ic_q[0], conn)
    #Add LensFilterId
    ic_df['LensFilterId'] = ic_df['Id']
    pybgt.execute_query(conn2, ic_q[1], results=False, verbose=False)

    x = 0
    while x < len(ic_df):
        ic_i = "Insert into {0} Values ({1},'{2}',{3},{4})".format(DB_and_Tables.Intern_Cat, ic_df['Id'][x],ic_df['Name'][x]
                            ,ic_df['LocalisationId'][x],ic_df['LensFilterId'][x])
        pybgt.execute_query(conn2, ic_i, results=False, verbose=False)
        x += 1
    print "{0} Table has been added".format(DB_and_Tables.Intern_Cat)

#Library.Employer
def LibraryEmployer():
    emp_q = SQ.LibraryEmployer()
    emp_df = psql.read_sql(emp_q[0], conn)
    #fixes apostrophe in Employer Name
    emp_df1 = emp_df.replace("'", "''", regex=True)
    pybgt.execute_query(conn2, emp_q[1], results=False, verbose=False)

    x = 0
    while x < len(emp_df1):
        emp_i = "Insert into {0} Values ({1},'{2}')".format(DB_and_Tables.Employer, emp_df1['Id'][x], emp_df1['Name'][x])
        pybgt.execute_query(conn2, emp_i, results=False, verbose=False)
        x += 1
    print "{0} Table has been added".format(DB_and_Tables.Employer)




if __name__ == '__main__':
    #LibraryArea()
    #LibraryState()
    LibraryStateArea()
    #LibraryCareerArea()
    #LibraryDegree()
    #LibraryDegreeEducationLevel()
    #LibraryDegreeAlias()
    #LibraryInternshipCategory()
    #LibraryEmployer()
