import pandas as pd
import numpy as np
import os
import datetime

class DataExplorer:
	def __init__(self, minYear, maxYear, risk_groups):
    	# world bank DB constants
		self.WORLD_BANK_BASE_YEAR_COL_IDX = 4
		self.WORLD_BANK_BASE_YEAR = 1960
		self.lag = 1 # lag (in years) with respect to credit risk agencies evaluation
		# associated parameters to generate datasets
		self.minYear = minYear
		self.maxYear = maxYear
		self.selectedYears = range(minYear, maxYear + 1)
		# model parameters
		self.risk_groups = risk_groups
		# initialize some auxiliary vars
		self.countries = [] #contains all countries
		self.histPerformance_sNp = dict([]) # historical performance of each country evaluated by S&P
		self.histPerformance_moodys = dict([]) # historical performance of each country evaluated by Moodys
		self.model_histPerformance_sNp = dict([]) # model historical performance of each country based on Moodys eval
		self.model_histPerformance_moodys = dict([]) # model historical performance of each country based on S&P eval
		self.datasets = [] #contains all datasets for the selected years

	def readWorldBankDB(self, criteria_files):
		script_dir = os.path.dirname(__file__)
		criteria_files
		baseYear_colIdx = self.WORLD_BANK_BASE_YEAR_COL_IDX
		baseYear = self.WORLD_BANK_BASE_YEAR
		for year in self.selectedYears:
			lagged_year = year - self.lag
			dataset = dict([])
			for criterion in criteria_files:
				print ("reading " + criterion + " column: " + str(lagged_year)) # we use worldBank[year-1] data to predict label[year]
				path = os.path.join(script_dir, criterion)
				DB = pd.ExcelFile(path) #open the data base
				critDB = DB.parse("Data") #choose a sheet and parse it...
				metacritDB = DB.parse("Metadata - Indicators") #choose a sheet and parse it...
				criterionName = metacritDB.iloc[0,1]
				cols = critDB.columns
				#rows = critDB.lines
				if(len(self.countries) < 1): #if first sheet to be read, then get country list and year list
					print("getting countries...")
					self.countries =critDB[cols[0]] #choose a sheet and parse it...
					self.countries = self.countries[3:] # remove trash info
					cntryTmp = []
					for country in self.countries:
						cntryTmp.append(country)
					self.countries = cntryTmp #convert countries from index() object into a vector of strings
					firstSheet = 0
				#print(critDB.iloc[3:, baseYear_colIdx + (year - baseYear)])
				critVals_YYYY = critDB.iloc[3:, baseYear_colIdx + (lagged_year - baseYear)]
				dataset[criterionName] = critVals_YYYY
			#print(dataset)
			dataset['Country'] = self.countries
			self.datasets.append(dataset)

	def readStdNPoorsDB(self, stdNPoorsFolder):
		script_dir = os.path.dirname(__file__)
		# open the country list
		countryList_path = os.path.join(script_dir, stdNPoorsFolder + "/country_list.xlsx")
		countryListDB = pd.ExcelFile(countryList_path) #open the data base
		countryList = countryListDB.parse("Plan1")
		for i in range(0, len(countryList)):
			if(countryList.iloc[i,1] == "ok"): # check if S&P DB contains country i data
				#print("reading " + str(countryList.iloc[i,0]) + ".xlsx")
				# get country i historical performance analyzed by S&P 
				relative_path = "/" + str(countryList.iloc[i,0]) + ".xlsx"
				country_path = os.path.join(script_dir, stdNPoorsFolder + relative_path)
				countryDB = pd.ExcelFile(country_path) #open the data base
				planNames = countryDB.sheet_names
				if(planNames[0] == "Plan1"):
					country = countryDB.parse("Plan1")
				else:
					country = countryDB.parse("Planilha1")
				#get ratings over the years
				stdNpoors_rating = dict([]) # the rating variable is a dictionary: rating[YYYY] = RATING_VALUE
				rating_dates = [] #year with different ratings. We get the most recent ratings for each year 
				currentRatingYear = 0 # initialize the current year of analysis
				currentRating = "" # initialize the  most recent rating for the current year of analysis
				all_years = self.selectedYears
				all_years = list(all_years)
				for j in range(0, len(country)):
					dateObj = pd.to_datetime(country.iloc[j,1])
					if(dateObj.year != currentRatingYear): # if current analysis year changed...
						currentRatingYear = dateObj.year # update the year of analysis
						currentRating = country.iloc[j,0] # update the rating for the current year of analysis
						# update the rating dictionary of this country 
						years_rated = 0 #how many years to remove?
						for year in reversed(all_years):
							if(year>=currentRatingYear):
								stdNpoors_rating[year] = currentRating # assign a rating for this year
								years_rated += 1 # this year cannot be used anymore
						for r in range(0, years_rated):
							all_years.pop() # remove the last element
				self.histPerformance_sNp[str(countryList.iloc[i,0])] = stdNpoors_rating
				self.model_histPerformance_sNp[str(countryList.iloc[i,0])] = self.getModelClassification('S&P', stdNpoors_rating)
		# print historical ratings for each country
		#for country in self.histPerformance_sNp:
		#	print(country + str(self.histPerformance_sNp[country]))

	def readMoodysDB(self, moodysFolder):
		script_dir = os.path.dirname(__file__)
		# open the country list
		countryList_path = os.path.join(script_dir, moodysFolder + "/country_list.xlsx")
		countryListDB = pd.ExcelFile(countryList_path) #open the data base
		countryList = countryListDB.parse("Plan1")
		for i in range(0, len(countryList)):
			if(countryList.iloc[i,1] == "ok"): # check if moody's DB contains country i data
				# get country i historical performance analyzed by moody's
				relative_path = "/" + str(countryList.iloc[i,0]) + ".xlsx"
				country_path = os.path.join(script_dir, moodysFolder + relative_path)
				countryDB = pd.ExcelFile(country_path) #open the data base
				country = countryDB.parse("Plan1")
				#get ratings over the years
				moodys_rating = dict([]) # the rating variable is a dictionary: rating[YYYY] = RATING_VALUE
				rating_dates = [] # year with different ratings. We get the most recent ratings for each year 
				currentRatingYear = 0 # initialize the current year of analysis
				currentRating = "" # initialize the  most recent rating for the current year of analysis
				all_years = self.selectedYears
				all_years = list(all_years)
				for j in range(0, len(country)):
					dateObj = pd.to_datetime(country.iloc[j,0])
					if(dateObj.year != currentRatingYear): # if current analysis year changed...
						currentRatingYear = dateObj.year # update the year of analysis
						currentRating = country.iloc[j,2] # update the rating for the current year of analysis
						# update the rating dictionary of this country 
						years_rated = 0 #how many years to remove?
						for year in reversed(all_years):
							if(year>=currentRatingYear):
								moodys_rating[year] = currentRating # assign a rating for this year
								years_rated += 1 # this year cannot be used anymore
						for r in range(0, years_rated):
							all_years.pop() # remove the last element
				self.histPerformance_moodys[str(countryList.iloc[i,0])] = moodys_rating
				self.model_histPerformance_moodys[str(countryList.iloc[i,0])] = self.getModelClassification('Moodys', moodys_rating)
		# print historical ratings for each country
		#for country in self.histPerformance_moodys:
		#	print(country + str(self.histPerformance_moodys[country]))

	def getModelClassification(self, agency, rating_dict):
		hist_ratings_model = dict([])
		if(agency == "S&P"):
			for year in rating_dict: # look over all ratings
				if(rating_dict[year] in self.risk_groups['C1_s&p']): # class 1?
					hist_ratings_model[year] = 1
				if(rating_dict[year] in self.risk_groups['C2_s&p']): # class 2?
					hist_ratings_model[year] = 2
				if(rating_dict[year] in self.risk_groups['C3_s&p']): # class 3?
					hist_ratings_model[year] = 3
				#if(rating_dict[year] in self.risk_groups['C4_s&p']): # class 3?
				#	hist_ratings_model[year] = 4
		if(agency == "Moodys"):
			for year in rating_dict: # look over all ratings
				if(rating_dict[year] in self.risk_groups['C1_moodys']): # class 1?
					hist_ratings_model[year] = 1
				if(rating_dict[year] in self.risk_groups['C2_moodys']): # class 2?
					hist_ratings_model[year] = 2
				if(rating_dict[year] in self.risk_groups['C3_moodys']): # class 3?
					hist_ratings_model[year] = 3
				#if(rating_dict[year] in self.risk_groups['C4_moodys']): # class 3?
				#	hist_ratings_model[year] = 4											
		return hist_ratings_model

	def getRatingCol(self, year, agency, modelClassfication):
		ratings_YYYY = []
		if(agency == "S&P"):
			for country in self.countries: # look over all countries
				if(country in self.histPerformance_sNp): # if this country was evaluated by S&P
					ratingHistory = []
					if(modelClassfication):
						ratingHistory = self.model_histPerformance_sNp[country]
					else:
						ratingHistory = self.histPerformance_sNp[country]
					if(year in ratingHistory): # if this country was evaluated in that year...
						ratings_YYYY.append(ratingHistory[year])
					else:
						ratings_YYYY.append("")
				else:
					ratings_YYYY.append("")
		if(agency == "Moodys"):
			for country in self.countries: # look over all countries
				if(country in self.histPerformance_moodys): # if this country was evaluated by moodys
					ratingHistory = []
					if(modelClassfication):
						ratingHistory = self.model_histPerformance_moodys[country]
					else:
						ratingHistory = self.histPerformance_moodys[country]
					if(year in ratingHistory): # if this country was evaluated in that year...
						ratings_YYYY.append(ratingHistory[year])
					else:
						ratings_YYYY.append("")
				else:
					ratings_YYYY.append("")
		#print(ratings_YYYY)
		return ratings_YYYY

	def getFinalClass(self, sNpClasf, moodysClasf, type):
		finalClasf = []
		for i in range(0, len(sNpClasf)): #loop over all countries
			#guarantee that all values are integers
			sNp_C = int(sNpClasf[i]) if not(sNpClasf[i] == '') else 0 
			moodys_C = int(moodysClasf[i]) if not(moodysClasf[i] == '') else 0 
			if (sNp_C + moodys_C) > 0 : # if at least one rating was assigned to this country...
				if(type == "Worst"): # get worst case classification 
					finalClasf.append(max([sNp_C, moodys_C]))
			else:
				finalClasf.append('')
		return finalClasf

	def generateDatasets(self):
		year = 0
		for dataset in self.datasets:
			dataset['Moodys Rating'] =  self.getRatingCol(self.selectedYears[year], "Moodys", 0)
			dataset['S&P Rating'] =  self.getRatingCol(self.selectedYears[year], "S&P", 0)
			dataset['modelClass_Moodys'] =  self.getRatingCol(self.selectedYears[year], "Moodys", 1)
			dataset['modelClass_S&P'] =  self.getRatingCol(self.selectedYears[year], "S&P", 1)
			dataset['modelClass_WorstCase'] =  self.getFinalClass(dataset['modelClass_S&P'], dataset['modelClass_Moodys'], "Worst")
			df = pd.DataFrame(dataset)
			#s = pd.Series(self.countries)
			df.set_index('Country', inplace = True) # set countries names as dataframe's index (row name)
			#print(df)
			df.to_excel("countryRisk_{}.xlsx".format(self.selectedYears[year]))
			year += 1
			#read risk files here and add to criterionValues_forThisYear
			#for country in countries:
			# read risk file and generate a riskClassVec
			#dataset[tostring(risk_class)] = riskClassVec



