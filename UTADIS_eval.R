library (MCDA)

# performance table
initTable <- read.xlsx("C:/Users/julio/Google Drive/1stRev DRSA_4OR/data/countryRisk_2014_MCDAcomparison.xlsx", sheetName = "Plan1")
countrNames <- initTable[, 1]
performanceTable <- rbind(initTable[,2:10])
rownames(performanceTable) <- countrNames

# ranks of the alternatives
alternativesAssignments <- c("low","low","low","low","low","low","low","low","low","low", 'low', 'low',
                             "medium","medium","medium","medium","medium","medium","medium","medium","medium","medium", "medium", "medium",
                             "speculative","speculative","speculative","speculative","speculative","speculative","speculative","speculative","speculative","speculative","speculative","speculative")
names(alternativesAssignments) <- c("Malaysia", "Japan", "Botswana", "Chile", "Oman", "China", "Israel", "Korea, Rep.", "Czech Republic", "Singapore", "Netherlands",
                                   "Qatar","Malta", "Aruba","Azerbaijan", "Italy", "Brazil", "Mauritius", "Romania", "Peru", "South Africa", "Russian Federation",
                                   "Bahamas, The", "Uruguay", "Bulgaria","Indonesia", "Bangladesh", "Armenia", "Angola", "Guatemala", "Costa Rica", "Croatia", "Kenya",
                                   "Georgia", "Bolivia","Hungary")
alternativesAssignments
#criteria to max or to min
criteriaMinMax <- c("max","max","max","max","max","max","max","min","min")
names(criteriaMinMax) <- colnames(performanceTable)
# number of break points for each criterion
criteriaNumberOfBreakPoints <- c(5,5,5,5,5,5,5,5,5)
names(criteriaNumberOfBreakPoints) <- colnames(performanceTable)

# ranks of the categories
categoriesRanks <- c(1,2,3)
names(categoriesRanks) <- c("low","medium","speculative")

#run method
x <- UTADIS(performanceTable, criteriaMinMax, criteriaNumberOfBreakPoints, 
          alternativesAssignments, categoriesRanks,0.1)


classification <- numeric()
for (i in 1:length(x$overallValues)){
  if (x$overallValues[i] >= x$categoriesLBs['low']){
    classification[names(x$overallValues[i])] <- 1
  }else{
    if(x$overallValues[i] >= x$categoriesLBs['medium']){
      classification[names(x$overallValues[i])] <- 2
    } else{
      classification[names(x$overallValues[i])] <- 3
    }
  }
} 
classification
clsf_table <- rbind(classification)
clsf_table <- t(clsf_table)
