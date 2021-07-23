import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
# include RawData class member functions
from RawData import DataExplorer
from random import choices

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
baseYear = 2014
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

# simulation parameters - type of decision examples
#We divide the DM population into three categories:
# DMs that tends to choose countries classified in the best subgroups of each group (bestPicker)
# DMs that tends to choose countries classified in the worst subgroups of each group (worstPicker)
# DMs that randomly allocates countries to the reference set (randomPicker)
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

nSims = 30 # number of refSets/testSets per DM
simulation_RandomRef9 = dict([]) #contain dictionary of reference sets # ex.: simulation_RandomRef['sim_X'] 
simulation_RandomRef18 = dict([]) #contain dictionary of reference sets # ex.: simulation_RandomRef18['sim_X'] 
simulation_RandomRef36 = dict([]) #contain dictionary of reference sets # ex.: simulation_RandomRef36['sim_X'] 
population = dict([])
population['1'] = [] # list of indexes of countries that belong to C1
population['2'] = [] # list of indexes of countries that belong to C2
population['3'] = [] # list of indexes of countries that belong to C3



# get populations and population elements' weights
# open countryRisk file associated with minYear = baseYear
path = os.path.join(script_dir, "countryRisk_" + str(baseYear) + ".xlsx")
DB = pd.ExcelFile(path) #open the data base
critDB = DB.parse("Sheet1") #choose a sheet and parse it...
for i in range(0, len(critDB)): # start filling class populations
	if(not(np.isnan(critDB.iloc[i, len(critDB.columns)-1]))): #check if this country was classified
		#line = "\nExample_" + str(i + 1) + ": "
		missingValue = 0 # assume this country was evaluated in all criteria
		for j in range(1, len(critDB.columns)-5):
			if(critDB.columns[j] in criteriaSet): # check if criterion j is included in the selected criteria set
				if(np.isnan(critDB.iloc[i, j])):
					missingValue = 1
					break
		#print(line)
		if(not(missingValue)): # if this country was evaluated in all criteria, include in the population
			clss = str(int(critDB.iloc[i, len(critDB.columns)-1]))
			population[clss] = population[clss] + [i] # update clss population

#generate refSet simulations for each refSet size
for s in range(nSims):
	# random (no weighted sampling)
	c1_objs = np.random.choice(a = population['1'], size = 3, replace = False) #sample n decision examples for this group
	c2_objs = np.random.choice(a = population['2'], size = 3, replace = False) #sample n decision examples for this group
	c3_objs = np.random.choice(a = population['3'], size = 3, replace = False) #sample n decision examples for this group
	simulation_RandomRef9['sim_' + str(s)] = c1_objs.tolist() + c2_objs.tolist()  + c3_objs.tolist() 
	# random (no weighted sampling)
	c1_objs = np.random.choice(a = population['1'], size = 6, replace = False) #sample n decision examples for this group
	c2_objs = np.random.choice(a = population['2'], size = 6, replace = False) #sample n decision examples for this group
	c3_objs = np.random.choice(a = population['3'], size = 6, replace = False) #sample n decision examples for this group
	simulation_RandomRef18['sim_' + str(s)] = c1_objs.tolist() + c2_objs.tolist()  + c3_objs.tolist() 
	# random (no weighted sampling)
	c1_objs = np.random.choice(a = population['1'], size = 12, replace = False) #sample n decision examples for this group
	c2_objs = np.random.choice(a = population['2'], size = 12, replace = False) #sample n decision examples for this group
	c3_objs = np.random.choice(a = population['3'], size = 12, replace = False) #sample n decision examples for this group
	simulation_RandomRef36['sim_' + str(s)] = c1_objs.tolist() + c2_objs.tolist()  + c3_objs.tolist() 

#write data sets
# for the base year we write a training set and a test set using the simulation results
# for the other years we only write test sets by using all countries evaluated in the selected critera

aggPop = population['1'] + population['2'] + population['3'] #  aggregated population
for s in range(nSims):
	print("generating DRSA data for simulation " + str(s + 1) + " / base year: " + str(baseYear))
	# convert countryRisk sheet into drsa input file
	# open drsa file for current year
	rand9_base_dataSet = open("inputData/drsa/simulation_wrt_RefSetSize/rand9/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")
	rand18_base_dataSet = open("inputData/drsa/simulation_wrt_RefSetSize/rand18/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")
	rand36_base_dataSet = open("inputData/drsa/simulation_wrt_RefSetSize/rand36/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")
	rand9_test_dataSet = open("inputData/drsa/simulation_wrt_RefSetSize/rand9/test/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")
	rand18_test_dataSet = open("inputData/drsa/simulation_wrt_RefSetSize/rand18/test/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")
	rand36_test_dataSet = open("inputData/drsa/simulation_wrt_RefSetSize/rand36/test/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")

	# write information about attributes
	line = "**ATTRIBUTES\n"
	#print(line)
	rand9_base_dataSet.writelines(line)
	rand9_test_dataSet.writelines(line)
	rand18_base_dataSet.writelines(line)
	rand18_test_dataSet.writelines(line)
	rand36_base_dataSet.writelines(line)
	rand36_test_dataSet.writelines(line)
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
			rand9_base_dataSet.writelines(line)
			rand9_test_dataSet.writelines(line)
			rand18_base_dataSet.writelines(line)
			rand18_test_dataSet.writelines(line)
			rand36_base_dataSet.writelines(line)
			rand36_test_dataSet.writelines(line)
		atCounter += 1
	#write decision attribute info
	line = "\n+ d: " + str(decision) + ", cost, decision\n" 
	#print(line)
	rand9_base_dataSet.writelines(line)
	rand9_test_dataSet.writelines(line)
	rand18_base_dataSet.writelines(line)
	rand18_test_dataSet.writelines(line)
	rand36_base_dataSet.writelines(line)
	rand36_test_dataSet.writelines(line)
	line = "\ndecision: d\n" 
	#print(line)
	rand9_base_dataSet.writelines(line)
	rand9_test_dataSet.writelines(line)
	rand18_base_dataSet.writelines(line)
	rand18_test_dataSet.writelines(line)
	rand36_base_dataSet.writelines(line)
	rand36_test_dataSet.writelines(line)

	# write information about attributes preference direction
	line = "\n**PREFERENCES\n"
	#print(line)
	rand9_base_dataSet.writelines(line)
	rand9_test_dataSet.writelines(line)
	rand18_base_dataSet.writelines(line)
	rand18_test_dataSet.writelines(line)
	rand36_base_dataSet.writelines(line)
	rand36_test_dataSet.writelines(line)
	firstExecution = 0 # all model parameters were processed
	atCounter = 1
	for i in critDB.columns[1:len(critDB.columns)-5]:
		if(i in criteriaSet):
			# write prefDir information
			line = "\nat" + str(atCounter) + ": " + prefDir[i]
			#print(line)
			rand9_base_dataSet.writelines(line)
			rand9_test_dataSet.writelines(line)
			rand18_base_dataSet.writelines(line)
			rand18_test_dataSet.writelines(line)
			rand36_base_dataSet.writelines(line)
			rand36_test_dataSet.writelines(line)
		atCounter += 1

	# write decision examples
	line = "\n\n**EXAMPLES\n" 
	#print(line)
	rand9_base_dataSet.writelines(line)
	rand9_test_dataSet.writelines(line)
	rand18_base_dataSet.writelines(line)
	rand18_test_dataSet.writelines(line)
	rand36_base_dataSet.writelines(line)
	rand36_test_dataSet.writelines(line)
	for i in simulation_RandomRef9['sim_' + str(s)]: # simulate a bestpicker DM refSet
			#line = "\nExample_" + str(i + 1) + ": "
			objName = critDB.iloc[i,0] 
			objName = objName.replace(".", "")
			objName = objName.replace(",", "")
			objName = objName.replace("'", "_")
			objName = objName.replace(" ", "_")
			line = "\n" + objName + ": "			
			for j in range(1, len(critDB.columns)-5):
				line = line + str(critDB.iloc[i,j]) + ", " # add atj(i)
			line = line + str(int(critDB.iloc[i, len(critDB.columns)-1])) # decisionClass(i)
			if(not(missingValue)): # if this country was evaluated in all criteria
				rand9_base_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	rand9_base_dataSet.writelines(line)
	rand9_testSet = list(set(aggPop) - set(simulation_RandomRef9['sim_' + str(s)]))
	for i in rand9_testSet: # simulate a bestpicker DM testSet
			#line = "\nExample_" + str(i + 1) + ": "
			objName = critDB.iloc[i,0] 
			objName = objName.replace(".", "")
			objName = objName.replace(",", "")
			objName = objName.replace("'", "_")
			objName = objName.replace(" ", "_")
			line = "\n" + objName + ": "			
			for j in range(1, len(critDB.columns)-5):
				line = line + str(critDB.iloc[i,j]) + ", " # add atj(i)
			line = line + str(int(critDB.iloc[i, len(critDB.columns)-1])) # decisionClass(i)
			if(not(missingValue)): # if this country was evaluated in all criteria
				rand9_test_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	rand9_test_dataSet.writelines(line)
	for i in simulation_RandomRef18['sim_' + str(s)]: # simulate a worstpicker DM refSet
			#line = "\nExample_" + str(i + 1) + ": "
			objName = critDB.iloc[i,0] 
			objName = objName.replace(".", "")
			objName = objName.replace(",", "")
			objName = objName.replace("'", "_")
			objName = objName.replace(" ", "_")
			line = "\n" + objName + ": "			
			for j in range(1, len(critDB.columns)-5):
				line = line + str(critDB.iloc[i,j]) + ", " # add atj(i)
			line = line + str(int(critDB.iloc[i, len(critDB.columns)-1])) # decisionClass(i)
			if(not(missingValue)): # if this country was evaluated in all criteria
				rand18_base_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	rand18_base_dataSet.writelines(line)
	rand18_testSet = list(set(aggPop) - set(simulation_RandomRef18['sim_' + str(s)]))
	for i in rand18_testSet: # simulate a worstpicker DM testSet
			#line = "\nExample_" + str(i + 1) + ": "
			objName = critDB.iloc[i,0] 
			objName = objName.replace(".", "")
			objName = objName.replace(",", "")
			objName = objName.replace("'", "_")
			objName = objName.replace(" ", "_")
			line = "\n" + objName + ": "			
			for j in range(1, len(critDB.columns)-5):
				line = line + str(critDB.iloc[i,j]) + ", " # add atj(i)
			line = line + str(int(critDB.iloc[i, len(critDB.columns)-1])) # decisionClass(i)
			if(not(missingValue)): # if this country was evaluated in all criteria
				rand18_test_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	rand18_test_dataSet.writelines(line)
	for i in simulation_RandomRef36['sim_' + str(s)]: # simulate a randompicker DM refSet
			#line = "\nExample_" + str(i + 1) + ": "
			objName = critDB.iloc[i,0] 
			objName = objName.replace(".", "")
			objName = objName.replace(",", "")
			objName = objName.replace("'", "_")
			objName = objName.replace(" ", "_")
			line = "\n" + objName + ": "			
			for j in range(1, len(critDB.columns)-5):
				line = line + str(critDB.iloc[i,j]) + ", " # add atj(i)
			line = line + str(int(critDB.iloc[i, len(critDB.columns)-1])) # decisionClass(i)
			if(not(missingValue)): # if this country was evaluated in all criteria
				rand36_base_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	rand36_base_dataSet.writelines(line)
	rand36_testSet = list(set(aggPop) - set(simulation_RandomRef36['sim_' + str(s)]))
	for i in rand36_testSet: # simulate a randompicker DM testSet
			#line = "\nExample_" + str(i + 1) + ": "
			objName = critDB.iloc[i,0] 
			objName = objName.replace(".", "")
			objName = objName.replace(",", "")
			objName = objName.replace("'", "_")
			objName = objName.replace(" ", "_")
			line = "\n" + objName + ": "			
			for j in range(1, len(critDB.columns)-5):
				line = line + str(critDB.iloc[i,j]) + ", " # add atj(i)
			line = line + str(int(critDB.iloc[i, len(critDB.columns)-1])) # decisionClass(i)
			if(not(missingValue)): # if this country was evaluated in all criteria
				rand36_test_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	rand36_test_dataSet.writelines(line)
