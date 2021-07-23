import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import math as mth

#simulation parameters
k1 = 100
k2 = 0.7
k3 = [0.15, 0.7, 0.15]

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

subgroup_weights_C1 = dict([]) # mapping of weights for C1 subgroups
subgroup_weights_C2 = dict([]) # mapping of weights for C2 subgroups
subgroup_weights_C3 = dict([]) # mapping of weights for C3 subgroups

#C1 - worst weights
# for moodys subgroups
weights = dict([])
group_nSsubs = len(risk_groups['C1_moodys']) # get the number of subgroups contained in this group 
counter = 0 #subgroup index
for subgroup in risk_groups['C1_moodys']:
	weights[subgroup] = k1*(mth.exp(k2*counter)-k2) # increasing weights
	counter += 1
subgroup_weights_C1['worst_moodys'] = weights
# for s&p subgroups
weights = dict([])
counter = 0 #subgroup index
for subgroup in risk_groups['C1_s&p']:
	weights[subgroup] = k1*(mth.exp(k2*counter)-k2) # increasing weights
	counter += 1
subgroup_weights_C1['worst_sp'] = weights

#C2 - middle weights (concentrated in the average subgroups)
# for moodys subgroups
weights = dict([])
counter = 0 #subgroup index
for subgroup in risk_groups['C2_moodys']:
	weights[subgroup] = k3[counter]
	counter += 1
subgroup_weights_C2['avg_moodys'] = weights
# for s&p subgroups
weights = dict([])
counter = 0 #subgroup index
for subgroup in risk_groups['C2_s&p']:
	weights[subgroup] =  k3[counter]
	counter += 1
subgroup_weights_C2['avg_sp'] = weights

#C3 - best weights
# for moodys subgroups
weights = dict([])
counter = 0 #subgroup index
for subgroup in risk_groups['C3_moodys']:
	weights[subgroup] = k1*mth.exp(-k2*counter) # decreasing weights
	counter += 1
subgroup_weights_C3['best_moodys'] = weights
# for s&p subgroups
weights = dict([])
counter = 0 #subgroup index
for subgroup in risk_groups['C3_s&p']:
	weights[subgroup] = k1*mth.exp(-k2*counter) # decreasing weights
	counter += 1
subgroup_weights_C3['best_sp'] = weights


#normalize weights C1
for group_key in subgroup_weights_C1.keys():
	subgroups_agency = subgroup_weights_C1[group_key]
	weight_keys = subgroups_agency.keys()
	weights = subgroups_agency.values()
	weight_sum = sum(weights)
	weights_normalized = []
	for w in weights:
		weights_normalized.append(w/weight_sum)
	w_norm_dict = dict([])
	counter = 0
	for key in subgroups_agency.keys():
		w_norm_dict[key] = weights_normalized[counter]
		counter += 1
	subgroup_weights_C1[group_key] = w_norm_dict

#normalize weights C2
for group_key in subgroup_weights_C2.keys():
	subgroups_agency = subgroup_weights_C2[group_key]
	weight_keys = subgroups_agency.keys()
	weights = subgroups_agency.values()
	weight_sum = sum(weights)
	weights_normalized = []
	for w in weights:
		weights_normalized.append(w/weight_sum)
	w_norm_dict = dict([])
	counter = 0
	for key in subgroups_agency.keys():
		w_norm_dict[key] = weights_normalized[counter]
		counter += 1
	subgroup_weights_C2[group_key] = w_norm_dict

#normalize weights C3
for group_key in subgroup_weights_C3.keys():
	subgroups_agency = subgroup_weights_C3[group_key]
	weight_keys = subgroups_agency.keys()
	weights = subgroups_agency.values()
	weight_sum = sum(weights)
	weights_normalized = []
	for w in weights:
		weights_normalized.append(w/weight_sum)
	w_norm_dict = dict([])
	counter = 0
	for key in subgroups_agency.keys():
		w_norm_dict[key] = weights_normalized[counter]
		counter += 1
	subgroup_weights_C3[group_key] = w_norm_dict



fig, axes = plt.subplots(3, 2, figsize=(7, 7), sharex=False)

#plott C1 subgroup weights
moodys_subgroups = list(subgroup_weights_C1['worst_moodys'].keys())
df_moodys = list(zip(moodys_subgroups,list(subgroup_weights_C1['worst_moodys'].values())))
sp_subgroups = list(subgroup_weights_C1['worst_sp'].keys())
df_sp =  list(zip(sp_subgroups,list(subgroup_weights_C1['worst_sp'].values())))
df_moodys = pd.DataFrame(df_moodys, columns = [' ','worst'])
df_moodys = pd.melt(df_moodys, id_vars = ' ', var_name = 'Preference', value_name = 'Weight')
df_sp = pd.DataFrame(df_sp, columns = [' ','worst'])
df_sp = pd.melt(df_sp, id_vars = ' ', var_name = 'Preference', value_name = 'Weight')
colors = ['navy', 'darkorange']
sns.set_palette(colors)
sns.factorplot(x = ' ', y = 'Weight', hue='Preference', data = df_moodys, kind='bar', ax=axes[0, 0])
sns.factorplot(x = ' ', y = 'Weight', hue='Preference', data = df_sp, kind='bar', ax=axes[0, 1])

#plott C2 subgroup weights
moodys_subgroups = list(subgroup_weights_C2['avg_moodys'].keys())
df_moodys = list(zip(moodys_subgroups,list(subgroup_weights_C2['avg_moodys'].values())))
sp_subgroups = list(subgroup_weights_C2['avg_sp'].keys())
df_sp =  list(zip(sp_subgroups,list(subgroup_weights_C2['avg_sp'].values())))
df_moodys = pd.DataFrame(df_moodys, columns = [' ','avg'])
df_moodys = pd.melt(df_moodys, id_vars = ' ', var_name = 'Preference', value_name = 'Weight')
df_sp = pd.DataFrame(df_sp, columns = [' ','avg'])
df_sp = pd.melt(df_sp, id_vars = ' ', var_name = 'Preference', value_name = 'Weight')
colors = ['navy', 'darkorange']
sns.set_palette(colors)
sns.factorplot(x = ' ', y = 'Weight', hue='Preference', data = df_moodys, kind='bar', ax=axes[1, 0])
sns.factorplot(x = ' ', y = 'Weight', hue='Preference', data = df_sp, kind='bar', ax=axes[1, 1])

#plott C3 subgroup weights
moodys_subgroups = list(subgroup_weights_C3['best_moodys'].keys())
df_moodys = list(zip(moodys_subgroups,list(subgroup_weights_C3['best_moodys'].values())))
sp_subgroups = list(subgroup_weights_C3['best_sp'].keys())
df_sp =  list(zip(sp_subgroups,list(subgroup_weights_C3['best_sp'].values())))
df_moodys = pd.DataFrame(df_moodys, columns = [' ','best'])
df_moodys = pd.melt(df_moodys, id_vars = ' ', var_name = 'Preference', value_name = 'Weight')
df_sp = pd.DataFrame(df_sp, columns = [' ','best'])
df_sp = pd.melt(df_sp, id_vars = ' ', var_name = 'Preference', value_name = 'Weight')
colors = ['navy', 'darkorange']
sns.set_palette(colors)
sns.factorplot(x = ' ', y = 'Weight', hue='Preference', data = df_moodys, kind='bar', ax=axes[2, 0])
sns.factorplot(x = ' ', y = 'Weight', hue='Preference', data = df_sp, kind='bar', ax=axes[2, 1])

plt.show()



'''
===================================================
PLOT FOR THREE SIMULATIONS: WORST, BEST plots ONLY
==================================================
#simulation parameters
k1 = [100, 100, 100]
k2 = [0.2, 0.4, 0.7]

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

subgroup_weights_C1 = dict([]) # mapping of weights for C1 subgroups
subgroup_weights_C2 = dict([]) # mapping of weights for C2 subgroups
subgroup_weights_C3 = dict([]) # mapping of weights for C3 subgroups

for s in range(len(k1)): #loop over ALL simulations (1, 2 and 3)
	# generate sample weights associated with each subgroup
	# generate weights for class 1 subgroups
	# for moodys subgroups
	weights_best = dict([])
	weights_worst = dict([])
	group_nSsubs = len(risk_groups['C1_moodys']) # get the number of subgroups contained in this group 
	counter = 0 
	for subgroup in risk_groups['C1_moodys']:
		weights_best[subgroup] = k1[s]*mth.exp(-k2[s]*counter) # decreasing weights
		weights_worst[subgroup] = k1[s]*(mth.exp(k2[s]*counter)-k2[s]) # increasing weights
		counter += 1
	subgroup_weights_C1['best_moodys' + str(s)] = weights_best
	subgroup_weights_C1['worst_moodys'+ str(s)] = weights_worst
	# for s&p subgroups
	weights_best = dict([])
	weights_worst = dict([])
	group_nSsubs = len(risk_groups['C1_s&p']) # get the number of subgroups contained in this group 
	counter = 0 
	for subgroup in risk_groups['C1_s&p']:
		weights_best[subgroup] = k1[s]*mth.exp(-k2[s]*counter) # decreasing weights
		weights_worst[subgroup] = k1[s]*(mth.exp(k2[s]*counter)-k2[s]) # increasing weights
		counter += 1
	subgroup_weights_C1['best_sp'+ str(s)] = weights_best
	subgroup_weights_C1['worst_sp'+ str(s)] = weights_worst


#normalize weights C1
for group_key in subgroup_weights_C1.keys():
	subgroups_agency = subgroup_weights_C1[group_key]
	weight_keys = subgroups_agency.keys()
	weights = subgroups_agency.values()
	weight_sum = sum(weights)
	weights_normalized = []
	for w in weights:
		weights_normalized.append(w/weight_sum)
	w_norm_dict = dict([])
	counter = 0
	for key in subgroups_agency.keys():
		w_norm_dict[key] = weights_normalized[counter]
		counter += 1
	subgroup_weights_C1[group_key] = w_norm_dict



fig, axes = plt.subplots(3, 2, figsize=(7, 7), sharex=False)
for s in range(len(k1)): #loop over all simulations

	moodys_subgroups = list(subgroup_weights_C1['best_moodys' + str(s)].keys())
	df_moodys = list(zip(moodys_subgroups,list(subgroup_weights_C1['best_moodys'+ str(s)].values()),list(subgroup_weights_C1['worst_moodys'+ str(s)].values())))
	sp_subgroups = list(subgroup_weights_C1['best_sp' + str(s)].keys())
	df_sp = list(zip(sp_subgroups,list(subgroup_weights_C1['best_sp'+ str(s)].values()),list(subgroup_weights_C1['worst_sp'+ str(s)].values())))

	df_moodys = pd.DataFrame(df_moodys, columns = [' ','best','worst'])
	df_moodys = pd.melt(df_moodys, id_vars = ' ', var_name = 'Simulation' + str(s+1), value_name = 'Weight')
	df_sp = pd.DataFrame(df_sp, columns = [' ','best','worst'])
	df_sp = pd.melt(df_sp, id_vars = ' ', var_name = 'Simulation' + str(s+1), value_name = 'Weight')


	colors = ['navy', 'darkorange']
	sns.set_palette(colors)
	sns.factorplot(x = ' ', y = 'Weight', hue='Simulation' + str(s+1), data = df_moodys, kind='bar', ax=axes[s, 0])
	sns.factorplot(x = ' ', y = 'Weight', hue='Simulation' + str(s+1), data = df_sp, kind='bar', ax=axes[s, 1])

plt.show()


'''