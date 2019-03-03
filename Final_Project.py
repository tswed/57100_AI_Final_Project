# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# @author: Thomas Swed
# created: February 23, 2019
# Artificial Intelligence 1 – CPSC 57100
# Spring I - 2019
# Final Course Project
# Constraint Satisfiability Algorithm for Interactive Student Scheduling

import numpy as np
import pandas as pd
from constraint import *

# Load list of courses and variables from Excel
course_rotations = pd.read_excel('course_rotations.xlsx', sheet_name='course_rotations')

# Get student’s preferred time of day to attend courses
preferred_time = input("Do you prefer morning, afternoon, or night courses?")

# Get student's max number of courses in one term
max_term_courses = int(input("What is the max number of courses you would like to take in one term? (4 max)"))

# Get student's minimum professor rating
min_professor_rating = int(input("What is the minimum professor rating you will accept? (5 = highest)"))

# Get student's top three preferred days of the week and assign to array
preferred_days = [] 
max_preferred_days = 3
while len(preferred_days) < max_preferred_days:
    day = input("What are your top three preferred days of the week to attend courses.")
    preferred_days.append(day)

data = course_rotations.copy()

# Subset courses minimum rating and higher
data = data.loc[data['professor_rating'] >= min_professor_rating]

# Subset courses preferred time of day
data = data.loc[data['course_time'] == preferred_time]

# Subset courses three preferred days
data = data.loc[data['course_day'].isin(preferred_days)]

# Assign filter list of courses to variable
filtered_course_list = data.iloc[:,0]

# Instantiate CSP object
problem = Problem()

# Add filtered list of courses as variables
problem.addVariables(filtered_course_list, [0, 1])

# Get solutions
csp_solutions = problem.getSolutions()

# Get first solution in dict
solution = pd.Series(csp_solutions[0])

print("Number of Possible Degree Plans is " + str(len(csp_solutions)))
print()
print(solution)