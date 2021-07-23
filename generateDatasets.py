import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
# include RawData class member functions
from RawData import DataExplorer

'''
We want to build the following data sets:
countryRisk_1990.xlsx
countryRisk_1991.xlsx
...
...
...
countryRisk_2016.xlsx
countryRisk_2017.xlsx
countryRisk_2018.xlsx

An example of a file of this type is presented below:
=====================================================
'countryRisk_YYYY.xlsx'
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

# files parameters
# using criteria selected according to de Lima Silva et al (2018) method
criteria_files = [
"worldBank/2_gdpPerCapta.xls",
"worldBank/5_exportGnS.xls",
"worldBank/6_grossSav.xls",
"worldBank/8_foreignDirectInvest.xls",
"worldBank/9_gdpMktp.xls",
"worldBank/10_totalResrv.xls",
"worldBank/11_gniPerCapta.xls",
"worldBank/12_lenIntRate.xls",
"worldBank/15_realIntRate.xls"
]
standardNpoors_folder = "standard_and_poors"
moodys_folder = "moodys"
minYear = 2010
maxYear = 2019

# model specificiations
risk_groups = dict([])

# class 1
risk_groups['C1_moodys'] =  ['Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3']
risk_groups['C1_s&p'] =  ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-']
# class 2
risk_groups['C2_moodys'] = ['Baa1', 'Baa2', 'Baa3']
risk_groups['C2_s&p'] = ['BBB+', 'BBB', 'BBB-']
# class 3
risk_groups['C3_moodys'] = ['Ba1', 'Ba2', 'Ba3', 'B1', 'B2', 'B3', 'Caa1', 'Caa2', 'Caa3', 'Ca', 'C']
risk_groups['C3_s&p'] = ['BB+', 'BB', 'BB-', 'B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D']

'''
# class 1
risk_groups['C1_moodys'] =  ['Aaa', 'Aa1', 'Aa2', 'Aa3', 'A1', 'A2', 'A3']
risk_groups['C1_s&p'] =  ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-']
# class 2
risk_groups['C2_moodys'] = ['Baa1', 'Baa2', 'Baa3']
risk_groups['C2_s&p'] = ['BBB+', 'BBB', 'BBB-']
# class 3
risk_groups['C3_moodys'] = ['Ba1', 'Ba2', 'Ba3']
risk_groups['C3_s&p'] = ['BB+', 'BB', 'BB-']

risk_groups['C4_moodys'] = ['B1', 'B2', 'B3', 'Caa1', 'Caa2', 'Caa3', 'Ca', 'C']
risk_groups['C4_s&p'] = ['B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D']
'''

# process data
data = DataExplorer(minYear, maxYear, risk_groups)
print("get world bank data...")
data.readWorldBankDB(criteria_files)
print("get S&P data...")
data.readStdNPoorsDB(standardNpoors_folder)
print("get moodys data...")
data.readMoodysDB(moodys_folder)
print("generateDatasets")
data.generateDatasets()


#how to drop rows with missing values?
# https://thispointer.com/pandas-drop-rows-from-a-dataframe-with-missing-values-or-nan-in-columns/
