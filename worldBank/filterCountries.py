import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
criteria_files = ["1_gdpGrowth.xls","2_gdpPerCapta.xls","3_currAccBlnc.xls","4_inflation.xls"]
baseYear_colIdx = 4 
baseYear = 1960
minYear = 2010
maxYear = 2016
selectedYears = range(minYear, maxYear + 1)
countries = []
'''
A data block consists of a column in a criteria file for a specific year 
We want to build the following data sets:
worldBankData_1990.xlsx
worldBankData_1991.xlsx
...
...
...
worldBankData_2016.xlsx
worldBankData_2017.xlsx
worldBankData_2018.xlsx

An example of a file of this type is presented below:
=====================================================
'worldBankData_YYYY.xlsx'
=====================================================
Country    Criterion_1     . . .  Criterion_M
Cntry1	   Crit1(Cntry1)   . . .  CritM(Cntry1) 
Cntry2     Crit1(Cntry2)   . . .  CritM(Cntry2) 
.
.
.
CntryN     Crit1(CntryN)   . . .  CritM(CntryN) 
=====================================================
'''

firstSheet = 1 #used to get country list
for year in selectedYears:
	dataset = dict([])
	for criterion in criteria_files:
		print ("reading " + criterion + " column: " + str(year))
		path = os.path.join(script_dir, criterion)
		DB = pd.ExcelFile(path) #open the data base
		critDB = DB.parse("Data") #choose a sheet and parse it...
		cols = critDB.columns
		#rows = critDB.lines
		if(firstSheet): #if first sheet to be read, then get country list and year list
			countries =critDB[cols[0]] #choose a sheet and parse it...
			countries = countries[3:] # remove trash info
			cntryTmp = []
			for country in countries:
				cntryTmp.append(country)
			countries = cntryTmp #convert countries from index() object into a vector of strings
			firstSheet = 0
		#print(critDB.iloc[3:, baseYear_colIdx + (year - baseYear)])
		critVals_YYYY = critDB.iloc[3:, baseYear_colIdx + (year - baseYear)]
		dataset[str(criterion)] = critVals_YYYY
	print(dataset)
	dataset['Country'] = countries
	df = pd.DataFrame(dataset)
	#s = pd.Series(countries)
	df.set_index('Country', inplace = True) # set countries names as dataframe's index (row name)
	print(df)
	df.to_excel("countryRisk_{}.xlsx".format(year))
	#read risk files here and add to criterionValues_forThisYear
	#for country in countries:
	# read risk file and generate a riskClassVec
	#dataset[tostring(risk_class)] = riskClassVec

'''
cols = procFraudDB.columns
ilct_prc = procFraudDB.loc[procFraudDB[cols[7]] == 'LICITACAO'] # select all procurement (LICITACAO) rows
totalIlicts = len(ilct_prc.index) # get total num of proc ilicits
print(totalIlicts)
ilct_cnt = ilct_prc.groupby(cols[8]) # group by ilicit type
ilct_cnt = ilct_cnt.size() # count the num of elements for each ilicit group
ilct_cnt_sorted = ilct_cnt.sort_values(ascending = False) # sort in descending order
print(ilct_cnt_sorted)
ilct_jcnt = ilct_prc.groupby(cols[12]) # group by justification
ilct_jcnt = ilct_jcnt.size() # count the num of elements for each justification group
ilct_jcnt_sorted = ilct_jcnt.sort_values(ascending = False) # sort in descending order
print(ilct_jcnt_sorted)
print("total " + str(len(ilct_jcnt_sorted)))

agg_ilct_num = 0#aggregated ilicit num
data_range = 0.8 # data span (represents X% of all data available)
idx_ilct = 0 # initialize iterator
while (agg_ilct_num < 0.8):
	agg_ilct_num += (ilct_cnt_sorted[idx_ilct]/totalIlicts)
	idx_ilct += 1
	print(agg_ilct_num)
print('ok')

#plot barplot
fig = sns.barplot(x = [i for i in ilct_cnt_sorted.index[0:idx_ilct]], y = ilct_cnt_sorted[0:idx_ilct])
#plt.figure(figsize = [18,24])
plt.title('Most frequent ilicits (80% of all ilicits)')
fig.set_xticklabels(fig.get_xticklabels(), rotation=45, fontsize = 8)
plt.show()

ilct_prc = ilct_prc.loc[ilct_prc[cols[8]].isin(ilct_cnt_sorted.index[0:idx_ilct])] # select all procurement (LICITACAO) rows that are associated with the most frequent ilicit types
print(len(ilct_prc.index)/totalIlicts)
'''