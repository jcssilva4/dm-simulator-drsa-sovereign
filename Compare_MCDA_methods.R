#install.packages("MCDA")
library (MCDA)

# Entries for UTADIS
documentation_url_1 <- "https://www.rdocumentation.org/packages/MCDA/versions/0.0.20/topics/UTADIS"

# UTADIS(performanceTable, criteriaMinMax, 
#        criteriaNumberOfBreakPoints, 
#        alternativesAssignments, categoriesRanks, epsilon, 
#        criteriaLBs=NULL, criteriaUBs=NULL,
#        alternativesIDs = NULL, criteriaIDs = NULL,
#        categoriesIDs = NULL)


# Entries for MRSortInferenceExact
documentation_url_2 <- "https://www.rdocumentation.org/packages/MCDA/versions/0.0.20/topics/MRSortInferenceExact"


# MRSortInferenceExact(performanceTable, assignments, 
#                      categoriesRanks, criteriaMinMax, 
#                      veto = FALSE, readableWeights = FALSE,
#                      readableProfiles = FALSE,
#                      alternativesIDs = NULL, criteriaIDs = NULL,
#                      solver = "glpk",
#                      cplexTimeLimit = NULL, cplexIntegralityTolerance = NULL, cplexThreads = NULL)


# Entries for MRSortInferenceExact
documentation_url_3 <- "https://www.rdocumentation.org/packages/MCDA/versions/0.0.20/topics/MRSortInferenceExact"
# MRSortInferenceApprox(performanceTable, assignments, categoriesRanks, criteriaMinMax, 
#                       veto = FALSE, alternativesIDs = NULL, criteriaIDs = NULL,
#                       timeLimit = 60, populationSize = 20, mutationProb = 0.1)