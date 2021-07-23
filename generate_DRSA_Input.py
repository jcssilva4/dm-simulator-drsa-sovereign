import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
# include RawData class member functions
from RawData import DataExplorer

'''
We want to build the following data sets:
countryRisk_DRSA_1990.isf
countryRisk_DRSA_1991.isf
...
...
...
countryRisk_DRSA_2020.isf

An example of a file of this type is presented below:
=====================================================
'countryRisk_YYYY.xlsx'
=====================================================
**ATTRIBUTES

+ at1: (continuous), prefdirection  # domain = continuous  #prefdirection = gain/cost
+ at2: [a, b, c, d], prefdirection # domain = discrete 
.
.
.
+ atn: domain_type, prefdirection 
+ d: [1, 2, 3], cost, decision # decision attribute

decision: d

**PREFERENCES

at1: gain
.
.
.
atn: gain
d: cost

**EXAMPLES

Example_1: at1(1), at2(1), ..., atn(1), decisionClass(1)
Example_2: at1(2), at2(2), ..., atn(2), decisionClass(2)
.
.
.
Example_k: at1(k), at2(k), ..., atn(k), decisionClass(k)

**END
=====================================================
'''

#file parameters
minYear = 2014
maxYear = 2019
script_dir = os.path.dirname(__file__)

# model parameters YOU need to specify
'''
at1: GDP per capita (current US$)	
at2: Exports of goods and services (% of GDP)	
at3: Gross savings (% of GDP)	
at4: Foreign direct investment, net inflows (BoP, current US$)	
at5: GDP (current US$)	
at6: Total reserves (includes gold, current US$)	
at7: GNI per capita, Atlas method (current US$)	
at8: Lending interest rate (%)	
at9: Real interest rate (%)
'''
# selected criteria (important for reduct extraction)

criteriaSet = ["GDP per capita (current US$)", "Exports of goods and services (% of GDP)", 
"Gross savings (% of GDP)", "Foreign direct investment, net inflows (BoP, current US$)",
"GDP (current US$)", "Total reserves (includes gold, current US$)", 
"GNI per capita, Atlas method (current US$)", "Lending interest rate (%)", "Real interest rate (%)"] 

# criteria with pref direction = cost
cost_criteria = ["Lending interest rate (%)", "Real interest rate (%)"]
discrete_criteria = dict([]) # discrete domain dictionary 
# example domains["attX"] = "[a, b, c, d]" # the discrete domain is a string
prefDir = dict([])
decision = [1, 2, 3] #decision attribute domain
firstExecution = 1 # boolean variable used to associate discrete domain and prefDir to each criteria

for year in range(0, maxYear-minYear+1):
	print("generating DRSA data for " + str(minYear + year))
	# open countryRisk file associated with minYear+year
	path = os.path.join(script_dir, "countryRisk_" + str(minYear + year) + ".xlsx")
	DB = pd.ExcelFile(path) #open the data base
	critDB = DB.parse("Sheet1") #choose a sheet and parse it...
	# convert countryRisk sheet into drsa input file
	# open drsa file for current year
	base_dataSet = open("inputData/drsa/drsa_countryRisk_" + str(minYear + year) + ".isf","w")

	# write information about attributes
	line = "**ATTRIBUTES\n"
	#print(line)
	base_dataSet.writelines(line)
	atCounter = 1
	for i in critDB.columns[1:len(critDB.columns)-5]:
		if(firstExecution):
			# get prefDir
			prefDir[i] = "gain"
			if(i in cost_criteria):
				prefDir[i] = "cost"
			# get Domain
			domain = "(continuous)"
			if(i in discrete_criteria.keys()):
				domain = discrete_criteria[i]
		if(i in criteriaSet):
			# write attribute information
			line = "\n+ at" + str(atCounter) + ": " + str(domain) + ", " + prefDir[i]
			#print(line)
			base_dataSet.writelines(line)
		atCounter += 1
	#write decision attribute info
	line = "\n+ d: " + str(decision) + ", cost, decision\n" 
	#print(line)
	base_dataSet.writelines(line)
	line = "\ndecision: d\n" 
	#print(line)
	base_dataSet.writelines(line)

	# write information about attributes preference direction
	line = "\n**PREFERENCES\n"
	#print(line)
	base_dataSet.writelines(line)
	firstExecution = 0 # all model parameters were processed
	atCounter = 1
	for i in critDB.columns[1:len(critDB.columns)-5]:
		if(i in criteriaSet):
			# write prefDir information
			line = "\nat" + str(atCounter) + ": " + prefDir[i]
			#print(line)
			base_dataSet.writelines(line)
		atCounter += 1

	# write decision examples
	line = "\n\n**EXAMPLES\n" 
	#print(line)
	base_dataSet.writelines(line)
	n_evaluatedCountries = 0 #number of countries evaluated in all criteria
	n_countries_class = dict([]) #number of countries per class
	for d in decision: #initialize n_countries_class
		n_countries_class[str(d)] = 0
	for i in range(0, len(critDB)):
		if(not(np.isnan(critDB.iloc[i, len(critDB.columns)-1]))): #check if this country was classified
			#line = "\nExample_" + str(i + 1) + ": "
			objName = critDB.iloc[i,0] 
			objName = objName.replace(".", "")
			objName = objName.replace(",", "")
			objName = objName.replace("'", "_")
			objName = objName.replace(" ", "_")
			line = "\n" + objName + ": "			
			missingValue = 0 # assume this country was evaluated in all criteria
			for j in range(1, len(critDB.columns)-5):
				if(critDB.columns[j] in criteriaSet): # check if criterion j is included in the selected criteria set
					if(np.isnan(critDB.iloc[i, j])):
						missingValue = 1
						break
					line = line + str(critDB.iloc[i,j]) + ", " # add atj(i)
			line = line + str(int(critDB.iloc[i, len(critDB.columns)-1])) # decisionClass(i)
			#print(line)
			if(not(missingValue)): # if this country was evaluated in all criteria
				base_dataSet.writelines(line)
				n_evaluatedCountries += 1
				n_countries_class[str(int(critDB.iloc[i, len(critDB.columns)-1]))] += 1 
	#EOF
	line = "\n\n**END\n"
	#print(line)
	base_dataSet.writelines(line)
	print("number of countries: " + str(n_evaluatedCountries))
	for d in decision: # print country proportion per class
		print("C{}: {:.2f}%".format(d, (n_countries_class[str(d)]/n_evaluatedCountries)*100))

