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

## Get student’s preferred time of day to attend courses
#preferred_times = input("Do you prefer morning, afternoon, or night courses?")
#
## Get student's max number of courses in one term
#max_term_courses = int(input("What is the max number of courses you would like to take in one term? (4 max)"))
#
## Get student's minimum professor rating
#min_professor_rating = int(input("What is the minimum professor rating you will accept? (5 = highest)"))
#
## Get student's top three preferred days of the week and assign to array
#preferred_days = [] 
#max_preferred_days = 3
#while len(preferred_days) < max_preferred_days:
#    day = input("What are your top three preferred days of the week to attend courses.")
#    preferred_days.append(day)

#Dictionary to lookup values and print corresponding term for each course
terms_dic =	{
     1: "Taken",
     3: "Taken",
     2: "Not Taken",
     4: "Not Taken"
}

#List of courses, and possible terms offered for each course
#100-800 courses are electives, 3 of which must be taken
courses = { "CPSC-50100 Morning": [1, 2],
            "CPSC-50100 Evening": [3, 4],

            "CPSC-50200 Morning": [1, 2],
            "CPSC-50200 Evening": [3, 4],
            
            "CPSC-50300 Morning": [1, 2],
            "CPSC-50300 Evening": [3, 4],
    
            "CPSC-50400 Morning": [1, 2],
            "CPSC-50400 Evening": [3, 4] }
            

# Define pre-requisite function to ensure that course_before occurs before course_after
# def prereq(course_before, course_after):
#    return course_before < course_after

problem = Problem()

# Add list of courses and possible terms as variables
for key, value in courses.items():
    problem.addVariable(key, value)

# Add constraint for not taking 5 of the 8 possible electives
problem.addConstraint(InSetConstraint([1, 4]))

#Add constraint for not taking 5 of the 8 possible electives
#problem.addConstraint(SomeInSetConstraint([100,200,300,400,500,600,700,800], 5, True),
#                      ["CPSC-50600","CPSC-51700","CPSC-52500","CPSC-55200","CPSC-55500","CPSC-57100","CPSC-57200","CPSC-57400"])

# problem.addConstraint(SomeInSetConstraint([200]))

# problem.addConstraint(NotInSetConstraint([200]))

# Students may only take one course per term
#problem.addConstraint(AllDifferentConstraint())

# List of pre-requisite courses, first course must be taken before the second
# problem.addConstraint(prereq, ["CPSC-50100", "CPSC-51100"])

# Get solution
csp_solutions = problem.getSolutions()

solution = pd.Series(csp_solutions[0])

# Sort the solution
sorted_solution = sorted(solution.items(), key=lambda kv: kv[1])

# Print courses not taken
#for key, value in sorted_solution:
#    if (value >= 100):
#        print(key + " " + terms_dic.get(value))

# Print remaining courses
for key, value in sorted_solution:
    if (value < 100):
        print(key + " " + terms_dic.get(value))