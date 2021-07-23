import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
# include RawData class member functions
from RawData import DataExplorer
from random import choices
import math as mth

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
risk_groups['C3_moodys'] = ['Ba1', 'Ba2', 'Ba3']
risk_groups['C3_s&p'] = ['BB+', 'BB', 'BB-']

risk_groups['C4_moodys'] = ['B1', 'B2', 'B3', 'Caa1', 'Caa2', 'Caa3', 'Ca', 'C']
risk_groups['C4_s&p'] = ['B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D']

nSims = 30 # number of refSets/testSets per DM
simulation_worstPicker_DM = dict([]) 
population = dict([])
population_weights = dict([]) # list of subjective sample weights (Depends on the DM type) of countries that belong to a certain porpulation
population['1'] = [] # list of indexes of countries that belong to C1
population_weights['1_worst'] = [] 
subgroup_weights_C1 = dict([]) # mapping of weights for C1 subgroups
population['2'] = [] # list of indexes of countries that belong to C2
population_weights['2_worst'] = [] 
subgroup_weights_C2 = dict([]) # mapping of weights for C2 subgroups
population['3'] = [] # list of indexes of countries that belong to C3
population_weights['3_worst'] = [] 
subgroup_weights_C3 = dict([]) # mapping of weights for C3 subgroups
population['4'] = [] # list of indexes of countries that belong to C3
population_weights['4_worst'] = [] 
subgroup_weights_C4 = dict([]) # mapping of weights for C3 subgroups

#k1 = constant to tune weights # the higher, the more importance the best subgroups will have
#k2 = constant to tune weights # the higher, higher will be the difference between subgroup importance
# dec example type simulation 1
#k1 = 100
#k2 = 0.2
# dec example type simulation 2
#k1 = 100
#k2 = 0.4
# dec example type simulation 3
k1 = 100 
k2 = 0.7 
#k3 = [0.15, 0.7, 0.15] #used to generate the final ref set (middle)
k3 = [0.45, 0.1, 0.45] #used to generate the final ref set (borders)
k4 = [0.3, 0.15, 0.05, 0.05, 0.15, 0.3]
#k3 = [0.33333, 0.33333, 0.33333] #used to generate the final ref set (equally likely)

# generate sample weights associated with each subgroup
# generate weights for class 1 subgroups
weights_worst = dict([])
group_nSsubs = len(risk_groups['C1_moodys']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C1_moodys']:
	weights_worst[subgroup] = k1*(mth.exp(k2*counter)-k2) # increasing weights
	counter += 1
group_nSsubs = len(risk_groups['C1_s&p']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C1_s&p']:
	weights_worst[subgroup] = k1*(mth.exp(k2*counter)-k2) # increasing weights
	counter += 1
subgroup_weights_C1['worst'] = weights_worst

# generate weights for class 2 subgroups
weights_worst = dict([])
group_nSsubs = len(risk_groups['C2_moodys']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C2_moodys']:
	weights_worst[subgroup] = k3[counter] # used to generate the final ref set
	counter += 1
group_nSsubs = len(risk_groups['C2_s&p']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C2_s&p']:
	weights_worst[subgroup] = k3[counter] # used to generate the final ref set
	counter += 1
subgroup_weights_C2['worst'] = weights_worst

# generate weights for class 3 subgroups
weights_worst = dict([])
group_nSsubs = len(risk_groups['C3_moodys']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C3_moodys']:
	weights_worst[subgroup] = k4[counter] # used to generate the final ref set
	counter += 1
group_nSsubs = len(risk_groups['C3_s&p']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C3_s&p']:
	weights_worst[subgroup] = k4[counter] # used to generate the final ref set
	counter += 1
subgroup_weights_C3['worst'] = weights_worst

# generate weights for class 5 subgroups
weights_worst = dict([])
group_nSsubs = len(risk_groups['C4_moodys']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C4_moodys']:
	weights_worst[subgroup] = k1*mth.exp(-k2*counter) # used to generate the final ref set
	counter += 1
group_nSsubs = len(risk_groups['C4_s&p']) # get the number of subgroups contained in this group 
counter = 0 
for subgroup in risk_groups['C4_s&p']:
	weights_worst[subgroup] = k1*mth.exp(-k2*counter) # used to generate the final ref set
	counter += 1
subgroup_weights_C4['worst'] = weights_worst

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
			#get associated sample weight for this country
			if(clss == '1'):
				weights_worst = subgroup_weights_C1['worst']
			if(clss == '2'):
				weights_worst = subgroup_weights_C2['worst']
			if(clss == '3'):
				weights_worst = subgroup_weights_C3['worst']
			if(clss == '4'):
				weights_worst = subgroup_weights_C4['worst']
			# get weights for each DM type
			final_weight_worst = []
			# get moody's weight
			if(critDB.iloc[i, len(critDB.columns)-5] in weights_worst.keys()): #check if NaN
				moodyclss = critDB.iloc[i, len(critDB.columns)-5]
				final_weight_worst += [weights_worst[moodyclss]]
			# get sp weight
			if(critDB.iloc[i, len(critDB.columns)-4] in weights_worst.keys()): #check if NaN
				spclss = critDB.iloc[i, len(critDB.columns)-4]
				final_weight_worst += [weights_worst[spclss]]
			# finalweight = mean between weights
			final_weight_worst = np.mean(final_weight_worst)
			# assign the respective subjective weights for this country
			population_weights[clss + "_worst"] = population_weights[clss + "_worst"] + [final_weight_worst]


#normalize weights 
weight_keys = population_weights.keys()
for weight_key in weight_keys:
	weights = population_weights[weight_key]
	weight_sum = sum(weights)
	weights_normalized = []
	for w in weights:
		weights_normalized.append(w/weight_sum)
	population_weights[weight_key] = weights_normalized

#generate refSet simulations for each DM
#size reference set = 36 - 12 per class
nDecExamples = 12
for s in range(nSims):
	# worst
	print(len(population['4']))
	c1_objs = np.random.choice(a = population['1'], size = nDecExamples, replace = False, p = population_weights['1_worst']) #sample n decision examples from this group
	c2_objs = np.random.choice(a = population['2'], size = nDecExamples, replace = False, p = population_weights['2_worst']) #sample n decision examples for this group
	c3_objs = np.random.choice(a = population['3'], size = nDecExamples, replace = False, p = population_weights['3_worst']) #sample n decision examples for this group
	c4_objs = np.random.choice(a = population['4'], size = nDecExamples, replace = False, p = population_weights['4_worst']) #sample n decision examples for this group
	simulation_worstPicker_DM['sim_' + str(s)] = c1_objs.tolist() + c2_objs.tolist()  + c3_objs.tolist() + c4_objs.tolist() 

#write data sets
# for the base year we write a training set and a test set using the simulation results
# for the other years we only write test sets by using all countries evaluated in the selected critera

aggPop = population['1'] + population['2'] + population['3'] #  aggregated population
for s in range(nSims):
	print("generating DRSA data for simulation " + str(s + 1) + " / base year: " + str(baseYear))
	# convert countryRisk sheet into drsa input file
	# open drsa file for current year
	worst_base_dataSet = open("inputData/drsa/simulation_wrt_class4/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")
	worst_test_dataSet = open("inputData/drsa/simulation_wrt_class4/test/drsa_countryRisk_" + str(baseYear) + "_sim" + str(s + 1) + ".isf","w")

	# write information about attributes
	line = "**ATTRIBUTES\n"
	#print(line)
	worst_base_dataSet.writelines(line)
	worst_test_dataSet.writelines(line)
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
			best_base_dataSet.writelines(line)
			best_test_dataSet.writelines(line)
			worst_base_dataSet.writelines(line)
			worst_test_dataSet.writelines(line)
		atCounter += 1
	#write decision attribute info
	line = "\n+ d: " + str(decision) + ", cost, decision\n" 
	#print(line)
	best_base_dataSet.writelines(line)
	best_test_dataSet.writelines(line)
	worst_base_dataSet.writelines(line)
	worst_test_dataSet.writelines(line)
	line = "\ndecision: d\n" 
	#print(line)
	best_base_dataSet.writelines(line)
	best_test_dataSet.writelines(line)
	worst_base_dataSet.writelines(line)
	worst_test_dataSet.writelines(line)

	# write information about attributes preference direction
	line = "\n**PREFERENCES\n"
	#print(line)
	best_base_dataSet.writelines(line)
	best_test_dataSet.writelines(line)
	worst_base_dataSet.writelines(line)
	worst_test_dataSet.writelines(line)
	firstExecution = 0 # all model parameters were processed
	atCounter = 1
	for i in critDB.columns[1:len(critDB.columns)-5]:
		if(i in criteriaSet):
			# write prefDir information
			line = "\nat" + str(atCounter) + ": " + prefDir[i]
			#print(line)
			best_base_dataSet.writelines(line)
			best_test_dataSet.writelines(line)
			worst_base_dataSet.writelines(line)
			worst_test_dataSet.writelines(line)
		atCounter += 1

	# write decision examples
	line = "\n\n**EXAMPLES\n" 
	#print(line)
	best_base_dataSet.writelines(line)
	best_test_dataSet.writelines(line)
	worst_base_dataSet.writelines(line)
	worst_test_dataSet.writelines(line)
	for i in simulation_bestPicker_DM['sim_' + str(s)]: # simulate a bestpicker DM refSet
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
				best_base_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	best_base_dataSet.writelines(line)
	best_testSet = list(set(aggPop) - set(simulation_bestPicker_DM['sim_' + str(s)]))
	for i in best_testSet: # simulate a bestpicker DM testSet
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
				best_test_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	best_test_dataSet.writelines(line)
	for i in simulation_worstPicker_DM['sim_' + str(s)]: # simulate a worstpicker DM refSet
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
				worst_base_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	worst_base_dataSet.writelines(line)
	worst_testSet = list(set(aggPop) - set(simulation_worstPicker_DM['sim_' + str(s)]))
	for i in worst_testSet: # simulate a worstpicker DM testSet
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
				worst_test_dataSet.writelines(line)
	#EOF
	line = "\n\n**END\n"
	worst_test_dataSet.writelines(line)
'''
#write test sets
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
	for i in simulation_winnerPicker_DM: # simulate a winnerPicker DM
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

'''