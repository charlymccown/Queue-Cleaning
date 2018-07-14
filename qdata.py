#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:05:39 2018

@author: charlyzite
"""

#Use commented R code and rewrite into Python
# install needed packages
# install.packages("tidyverse")
# install.packages("tidyr")
# install.packages("stringr")
# # Load packages into accessible memory:
# # dplyr - filter, select, mutate, summarize, arrange
# # tidyr - gather, spread
# # stringr - str_detect
# library("dplyr")
# library("tidyr")
# library("stringr")

import scipy as sp
import numpy as np
import pandas as pd
import re 



"""Read data and change column names"""
#qdata=read.csv("QCombined.csv")
# names(qdata) = c("Date Time In", "Email", "Name", "Location", "Course", "Concept", "Helped", "Helped Time", "Center", "Semester")

qdata = pd.read_csv('QCombinedPy.csv') #read in the dataset to a data frame using pandas
qdata.columns = ['Date Time In', 'Email', 'Name', 'Location', 'Course', 'Concept', 'Helped', 'Helped Time', 'Center', 'Semester']


"""Clean course data"""
"""Remove all spaces"""
# qdirty = qdata %>% filter(str_detect(Course," "))
# qclean = qdata %>% filter(!str_detect(Course," "))
# noSpaces = gsub(" ","", qdirty$Course)
# qdirty = qdirty %>% mutate(noSpaces)
# qdirty$Course=qdirty$noSpaces
# qdirty$noSpaces=NULL #delete the old column
# rm(noSpaces) #remove used variable
# newqdata=rbind(qdirty,qclean) #put the data back together

qdirty = qdata[qdata['Course'].str.contains(' ', na = False, regex = False)] #course has a space
qclean = qdata[qdata['Course'].str.contains(' ', na = False, regex = False) == False] #course does not have a space
noSpaces = qdirty['Course'].str.replace(" ","")        #remove spaces from all dirty courses
qdirty = qdirty.assign(cleanedCourse = noSpaces)   #mutate the new cleaned course column on the dirty dataset
qdirty['Course'] = qdirty['cleanedCourse']         #set the old course column equal to the new one
qdirty = qdirty.drop('cleanedCourse', 1)           #delete the used column
newqdata = qclean.append(qdirty)                   #append the now clean data to the new clean data


"""Make all letters uppercase"""
# qdirty = newqdata %>% filter(str_detect(Course,"[[:lower:]]"))
# qclean = newqdata %>% filter(!str_detect(Course,"[[:lower:]]"))
# upperCase = qdirty$Course %>% toupper()
# qdirty = qdirty %>% mutate(upperCase)
# qdirty$Course=qdirty$upperCase
# qdirty$upperCase=NULL #delete the old column
# rm(upperCase) #remove used variable
# newqdata=rbind(qdirty,qclean) #put the data back together

qdirty = newqdata[(newqdata['Course'].str).contains('[a-z]+', na = False, regex = True)] #course has a lowercase
qclean = newqdata[(newqdata['Course'].str).contains('[a-z]+', na = False, regex = True) == False] #course does not have a lowercase
upperCase = qdirty['Course'].str.upper()             #make all lowercase letters uppercase
qdirty = qdirty.assign(cleanedCourse = upperCase)  #mutate the new cleaned course column on the dirty dataset
qdirty['Course'] = qdirty['cleanedCourse']         #set the old course column equal to the new one
qdirty = qdirty.drop('cleanedCourse', 1)           #delete the used column
newqdata = qclean.append(qdirty)                   #append the now clean data to the new clean data


"""remove redundant variables"""
# rm(qdirty)
# rm(qclean)
#

#I think this is done by Python



"""create new files with clean and dirty data for each center"""
"""make a list of all existing centers by finding each unique center code"""
# centers = unique(newqdata$Center)

centers = set(newqdata.Center)  #make the list a set to have only unique centers



"""create a new clean and dirty dataframe for each center"""
# for(centername in centers){
#   #make a new data frame for the given center
#   centerFrame = newqdata %>% filter(str_detect(Center,centername))
#   #from that data frame, separate the clean from the dirty into two more data frames
#   centerFrameClean = centerFrame  %>% filter(grepl("^[[:upper:]][[:upper:]][[:upper:]][[:digit:]][[:digit:]][[:digit:]]$", Course))
#   centerFrameDirty = centerFrame  %>% filter(!grepl("^[[:upper:]][[:upper:]][[:upper:]][[:digit:]][[:digit:]][[:digit:]]$", Course))
#   #write the resulting data frames to csv files
#   write.csv(centerFrameClean, file = paste(centername, "Clean.csv", sep = "_"))
#   write.csv(centerFrameDirty, file = paste(centername, "Dirty.csv", sep = "_"))
# }
#

for centername in centers :
   #make a new data frame for the given center
   centerFrame = newqdata[newqdata['Center'] == centername]
   centerFrame.reset_index()
   #from that data frame, separate the clean from the dirty into two more data frames
   centerFrameClean = centerFrame[(centerFrame['Course'].str).contains('^[A-Z][A-Z][A-Z][0-9][0-9][0-9]$', na = False, regex = True)]
   centerFrameClean = centerFrameClean.sort_values('Date Time In')
   #centerFrameClean.reset_index()
   
   centerFrameDirty = centerFrame[(centerFrame['Course'].str).contains('^[A-Z][A-Z][A-Z][0-9][0-9][0-9]$', na = False, regex = True) == False]
   centerFrameDirty = centerFrameDirty.sort_values('Date Time In')
   #centerFrameDirty.reset_index()
    
   #write the resulting data frames to csv files
   centerFrameClean.to_csv(centername + "_" + "Clean.csv")
   centerFrameDirty.to_csv(centername + "_" + "Dirty.csv")
   
 
    

"""remove redundant varaibles"""
# rm(centerFrame)
# rm(centerFrameClean)
# rm(centerFrameDirty)
# rm(centername)
# rm(centers)

#Done by Python?