#install needed packages
install.packages("tidyverse")
install.packages("tidyr")
install.packages("stringr")



# Load packages into accessible memory:
# dplyr - filter, select, mutate, summarize, arrange
# tidyr - gather, spread
# stringr - str_detect
library("dplyr")
library("tidyr")
library("stringr")



# Read data
qdata=read.csv("QCombined.csv")
names(qdata) = c("Date Time In", "Email", "Name", "Location", "Course", "Concept", "Helped", "Helped Time", "Center", "Semester")

# Clean course data

# Remove all spaces
qdirty = qdata %>% filter(str_detect(Course," "))
qclean = qdata %>% filter(!str_detect(Course," "))
noSpaces = gsub(" ","", qdirty$Course)
qdirty = qdirty %>% mutate(noSpaces)
qdirty$Course=qdirty$noSpaces
qdirty$noSpaces=NULL #delete the old column
rm(noSpaces) #remove used variable
newqdata=rbind(qdirty,qclean) #put the data back together

#Make all letters uppercase
qdirty = newqdata %>% filter(str_detect(Course,"[[:lower:]]"))
qclean = newqdata %>% filter(!str_detect(Course,"[[:lower:]]"))
upperCase = qdirty$Course %>% toupper()
qdirty = qdirty %>% mutate(upperCase)
qdirty$Course=qdirty$upperCase
qdirty$upperCase=NULL #delete the old column
rm(upperCase) #remove used variable
newqdata=rbind(qdirty,qclean) #put the data back together

#remove used variables
rm(qdirty)
rm(qclean)

#create new files with clean and dirty data for each center
#make a list of all existing centers by finding each unique center code
centers = unique(qdata$Center)

#for all unique centers, create the new files

#define the function to separate clean and dirty entries and paste the rows to their respective files
f = function(x, newCenterName, output1, output2){
  if(x[9] == centerName){
    #if the data is clean, add it to the clean data file
    if(grepl("[[:upper:]][[:upper:]][[:upper:]][[:digit:]][[:digit:]][[:digit:]]", x[5]))
      cat(paste(x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10], sep=","), file = output1, append = TRUE, fill = TRUE)
    #otherwise the data is dirty, add it to the dirty data file
    else
      cat(paste(x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10], sep=","), file = output2, append = TRUE, fill = TRUE)
  }
}

#for every unique center, apply the function to each row in qdata
for(centerName in centers){
  #create the new filenames based on center
  centerNameClean = paste(centerName, "Clean.csv", sep = "_")
  centerNameDirty = paste(centerName, "Dirty.csv", sep = "_")
  
  #Add the label row to each file
  cat(paste("Date Time In", "Email", "Name", "Location", "Course", "Concept", "Helped", "Helped Time", "Center", "Semester",sep=","), file = centerNameClean, fill = TRUE)
  cat(paste("Date Time In", "Email", "Name", "Location", "Course", "Concept", "Helped", "Helped Time", "Center", "Semester",sep=","), file = centerNameDirty, fill = TRUE)
  
  #apply the function with respective clean and dirty output files
  apply(qdata, 1, f, newCenterName = centerName, output1 = centerNameClean, output2 = centerNameDirty)
}

rm(centerName)
rm(centerNameClean)
rm(centerNameDirty)
rm(centers)

# Clean course data
#qdata[,5] = gsub(" ", "", qdata[,5]) # Remove all spaces
#qdata[,5] = gsub("(\\w*)", "\\U\\1\\U\\2", qdata[,5], perl=TRUE) #Make all letters uppercase
#all courses of the form AAA### are clean,the rest are dirty
#dirty = grep("[[:upper:]][[:upper:]][[:upper:]][[:digit:]][[:digit:]][[:digit:]]", qdata[,5], ignore.case=FALSE, invert=TRUE, value=TRUE)
#clean = grep("[[:upper:]][[:upper:]][[:upper:]][[:digit:]][[:digit:]][[:digit:]]", qdata[,5], ignore.case=FALSE, invert=FALSE, value=TRUE)


#Other methods you will use:
# names()
# separate()
# filter()
# na.omit()
# mutate()-----
# gsub()
# rbind()
# cbind()
# apply()
# rm()

