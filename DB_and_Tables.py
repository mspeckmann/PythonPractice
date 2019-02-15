#List of db and tables

#Destination
DB = 'FocusRefresh33'
Area = ('[{0}].[dbo].[Library.Area1]').format(DB)
State = ('[{0}].[dbo].[Library.State1]').format(DB)
StateArea = ('[{0}].[dbo].[Library.StateArea1]').format(DB)
CareerArea = ('[{0}].[dbo].[Library.CareerArea1]').format(DB)
Degree = ('[{0}].[dbo].[Library.Degree1]').format(DB)
Deg_Ed_Level = ('[{0}].[dbo].[Library.DegreeEducationLevel1]').format(DB)
Deg_Alias = ('[{0}].[dbo].[Library.DegreeAlias1]').format(DB)
Intern_Cat = ('[{0}].[dbo].[Library.InternshipCategory1]').format(DB)
Employer = ('[{0}].[dbo].[Library.Employer1]').format(DB)


#KA Analytics Tables
DB2 = 'TaxonomyDB'
BGTMSA = ('[{0}].[geo].[bgtmsas_id]').format(DB2)
STATE = ('[{0}].[geo].[states_id]').format(DB2)
CAREERAREA2 = ('[{0}].[bgot].[careerareas_id]').format(DB2)
BGTCIP = ('[{0}].[major].[bgtcips_id]').format(DB2)
BGTCIP_BGTOCC_XW = ('[{0}].[major].[bgtcips_bgtoccs_xw]').format(DB2)


DB3 = 'Penguin'
INTERN_CAT = ('[{0}].[internship].[InternshipCategory]').format(DB3)
EMPLOYER = ('[{0}].[employer].[employer_id]').format(DB3)