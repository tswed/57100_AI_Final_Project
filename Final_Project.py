#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 20:59:01 2019

@author: 
02/28/2019
Spring 1, 2019
Artificial Intelligence
Final Course Project
Constraint Satisfiability Algorithm for Interactive Student Scheduling 
"""

# Import packages
from constraint import *
import numpy as np
import pandas as pd


# Get student’s preferred time of day to attend courses
preferred_times = input("Do you prefer morning, afternoon, or night courses?")
print(preferred_times)

# Get student's max number of courses in one term
max_term_courses = int(input("What is the max number of courses you would like to take in one term? (4 max)"))
print(max_term_courses )

# Get student's minimum professor rating
min_professor_rating = int(input("What is the minimum professor rating you will accept? (5 = highest)"))
print(min_professor_rating)

# Get student's top three preferred days of the week and assign to array
preferred_days = [] 
max_preferred_days = 3
while len(preferred_days) < max_preferred_days:
    day = input("What are your top three preferred days of the week to attend courses.")
    preferred_days.append(day)
    print(preferred_days)
    

# Instantiate Problem object
#problem = Problem()
#
#problem.addVariable()
#
#Define constraint function to assign variable precedence over another variable
#def func(a, b):
#    return a < b

#problem.addConstraint()

# Do not repeat courses
#problem.addConstraint(AllDifferentConstraint())

# Get solutions
#sols = problem.getSolutions()

# Get first solution
#s = pd.Series(sols[0])

############################            
#### Program starts here ###
############################   

# Print out the header info
