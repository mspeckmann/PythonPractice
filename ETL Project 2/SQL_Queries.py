import DB_and_Tables

#List of Queries for

class Queries:

    #Library.Area
    def LibraryArea(self):
        extract = '''
        SELECT [Id]
              ,[BGTMSAName] as Name
              ,SortOrder = 1    
        FROM {0}
        where IsLI = 1 and PrimaryStateId not in (55,56,57,58,59,60,61)
        order by Id;
        '''.format(DB_and_Tables.BGTMSA)

        create = '''
        Create Table {0} (
        Id int not null
        , Name nvarchar(150) not null
        , SortOrder int not null
        , Primary Key (Id));
        '''.format(DB_and_Tables.Area)

        return extract, create

    #Library.State
    def LibraryState(self):
        extract = '''Select st.Id
	                     ,  CountryId = 13370
	                     ,  st.StateName as Name
	                     ,  st.State as Code
	                     ,  SortOrder = 1
                     From {0} st (nolock)
                     WHERE Id not in (53,54,55,56,57,58,59,60,61)'''.format(DB_and_Tables.STATE)

        create = '''Create Table {0} (
                    Id bigint not null
                    , CountryId bigint not null
                    , Name nvarchar(50) not null
                    , Code nvarchar(2) not null
                    , SortOrder int not null
                    , Primary Key (Id));'''.format(DB_and_Tables.State)

        update = '''Update {0}
                    Set Name = 'All States' , Code = '' , SortOrder = 0
                    where Id = 1'''.format(DB_and_Tables.State)

        return extract, create, update

    #Library.StateArea
    def LibraryStateArea(self):
        #MSA
        extract1 = '''Select [BGTMSA] as AreaCode
                        ,  Display = 1
                        ,  IsDefault = 0
                        ,  [PrimaryStateId] as StateId
                        ,  [Id] as AreaId
                     FROM {0}
                     where IsLI = 1
                     order by Id;'''.format(DB_and_Tables.BGTMSA)
        #State
        extract2 = '''Select FIPSState as AreaCode
                        ,  Display = 1
                        ,  IsDefault = 0
                        ,  Id as StateId
                        ,  AreaId = 1
                      From {0}
                      where Id not in (1,53,54,55,56,57,58,59,60,61)'''.format(DB_and_Tables.STATE)

        create = '''Create Table {0} (
                    Id bigint not null
                    ,AreaCode nvarchar(max) not null
                    ,Display bit not null
                    ,IsDefault bit not null
                    ,StateId bigint not null
                    ,AreaId int not null
                    ,Primary Key (Id)
                    );'''.format(DB_and_Tables.StateArea)
        #Nationwide
        insert = '''Insert into {0}
                    Values (499, '0', 1, 0, 1, 1)'''.format(DB_and_Tables.StateArea)

        return extract1, extract2, create, insert

    #Library.CareerArea
    def LibraryCareerArea(self):
        extract = '''
        SELECT [Id]
              ,[CareerAreaName] as Name
              ,LocalisationId = 12090
        FROM {0}
        WHERE Id != 1;'''.format(DB_and_Tables.CAREERAREA2)

        create = '''Create Table {0} (
        Id int not null
        ,  Name nvarchar(200) not null
        , LocalisationId bigint not null
        , Primary Key (Id));
        '''.format(DB_and_Tables.CareerArea)

        return extract, create

    #Library.Degree
    def LibraryDegree(self):
        extract = ''' 
        SELECT [Id]
              ,[BGTCIPTitle] as Name
              ,[BGTCIPCode] as RcipCode
              ,IsDegreeArea = 0
              ,IsClientData = 0
        FROM {0}
        WHERE Id != 1'''.format(DB_and_Tables.BGTCIP)

        create = '''Create Table {0} (
        Id int not null
        ,  Name nvarchar(200) not null
        ,  RcipCode nvarchar(10)
        ,  IsDegreeArea bit not null
        ,  IsClientData bit not null
        ,  Primary Key (Id));  
        '''.format(DB_and_Tables.Degree)

        alter = '''ALTER Table {0}
                   ADD ClientDataTag nvarchar(100);
                   ALTER Table {0}
                   ADD Tier int;'''.format(DB_and_Tables.Degree)

        return extract, create, alter

    #Library.DegreeEducationLevel
    def LibraryDegreeEducationLevel(self):
        extract = '''
        SELECT a.EducationLevel
        ,a.DegreesAwarded
        ,a.Name
        ,a.ExcludeFromReport
        ,a.DegreeId
        from (
            Select distinct xw.bgtcipid as DegreeId 
                ,  Id = NULL
                ,  case when xw.degreelevel != 21 then xw.degreelevel
                        when xw.degreelevel = 21 then 18
                        end as EducationLevel
                ,  DegreesAwarded = 0
                ,  case when xw.degreelevel = 16 then concat('Bachelors Degree - ', cip.BGTCIPTitle)
                        when xw.degreelevel = 18 then concat('Graduate/Professional Degree - ', cip.BGTCIPTitle)
                        when xw.degreelevel = 21 then concat('Graduate/Professional Degree - ', cip.BGTCIPTitle)
                        when xw.degreelevel = 13 then concat('Certificate - ', cip.BGTCIPTitle)
                        when xw.degreelevel = 14 then concat('Associates Degree - ', cip.BGTCIPTitle)
                        end as Name
                ,  ExcludeFromReport = 0 
            From {0} xw (nolock)
            left join {1} cip (nolock) on cip.id = xw.bgtcipid
            ) a;'''.format(DB_and_Tables.BGTCIP_BGTOCC_XW, DB_and_Tables.BGTCIP)

        create = '''Create Table {0} (
        Id int not null
        ,  EducationLevel int not null
        ,  DegreesAwarded int not null
        ,  Name nvarchar(200)
        ,  ExcludedFromReport bit not null
        ,  DegreeId bigint not null
        ,  Primary Key (Id)  
        );'''.format(DB_and_Tables.Deg_Ed_Level)

        update = '''Update {0}
                    SET Name = REPLACE(Name, 'Bachelors', 'Bachelor''s')
                    WHERE Name LIKE '%Bachelors%';
                    Update {0}
                    SET Name = REPLACE(Name, 'Associates', 'Associate''s')
                    WHERE Name LIKE '%Associates%';'''.format(DB_and_Tables.Deg_Ed_Level)

        return extract, create, update

    #Library.DegreeAlias
    def LibraryDegreeAlias(self):
        create = '''Select IDENTITY(int,20000,1) as Id
	                ,  edlev.name as AliasExtended
	                ,  edlev.educationlevel as EducationLevel
	                ,  deg.name as Alias
	                ,  deg.id as DegreeId
	                ,  edlev.id as DegreeEducationLevelId
                    into {0}
                    From {1} deg (nolock)
                    left join {2} edlev (nolock) on edlev.degreeid = deg.id
                    where edlev.name is not NULL'''.format(DB_and_Tables.Deg_Alias, DB_and_Tables.Degree, DB_and_Tables.Deg_Ed_Level)

        alter = '''Alter Table {0}
                   Alter Column Id bigint not null;

                   Alter Table {0}
                   Alter Column AliasExtended nvarchar(400) not null;

                   Alter Table {0}
                   Alter Column EducationLevel int not null;

                   Alter Table {0}
                   Alter Column Alias nvarchar(max) not null;

                   Alter Table {0}
                   Alter Column DegreeId bigint not null;

                   Alter Table {0}
                   Alter Column DegreeEducationLevelId bigint not null;

                   Alter Table {0}
                   ADD PRIMARY KEY (ID);'''.format(DB_and_Tables.Deg_Alias)

        return create, alter

    #Library.InternshipCategory
    def LibraryInternshipCategory(self):
        extract = '''SELECT [Id]
                    ,[Name]
                    ,[LocalisationId] = 12090
                    FROM {0}'''.format(DB_and_Tables.INTERN_CAT)

        create = '''Create Table {0} (
                    Id int not null
                  , Name nvarchar(100) not null
                  , LocalisationId bigint not null
                  , LensFilterId int
                  ,  Primary Key (Id))'''.format(DB_and_Tables.Intern_Cat)

        return extract, create

    #Library.Employer
    def LibraryEmployer(self):
        extract = '''SELECT [EmployerId] as Id
                    ,[Employer] as Name
                    FROM {0}
                    order by EmployerId'''.format(DB_and_Tables.EMPLOYER)

        create = '''Create Table {0} (
                    Id bigint not null
                    ,  Name nvarchar(200) not null
                    ,  Primary Key (Id))'''.format(DB_and_Tables.Employer)

        return extract, create

