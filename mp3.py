#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#@author: Thomas Swed
#created: February 23, 2019
#Artificial Intelligence 1 – CPSC 57100
#Spring I - 2019
#Machine Problem 3 - Course Planning using a Constraint Satisfaction Problem (mp3.py)

import numpy as np
import pandas as pd
from constraint import *


#Dictionary to lookup values and print corresponding term for each course
terms_dic =	{
  100 : "Not Taken",
  200 : "Not Taken",
  300 : "Not Taken",
  400 : "Not Taken",
  500 : "Not Taken",
  600 : "Not Taken",
  700 : "Not Taken",
  800 : "Not Taken",
   1 : "Year 1 Fall 1",
   2 : "Year 1 Fall 2",
   3 : "Year 1 Spring 1",
   4 : "Year 1 Spring 2",
   5 : "Year 1 Summer 1",
   6 : "Year 1 Summer 2",
   7 : "Year 2 Fall 1",
   8 : "Year 2 Fall 2",
   9 : "Year 2 Spring 1",
   10 : "Year 2 Spring 2",
   11 : "Year 2 Summer 1",
   12 : "Year 2 Summer 2",
   13 : "Year 3 Fall 1",
   14 : "Year 3 Fall 2"
}

#List of courses, and possible terms offered for each course
#100-800 courses are electives, 3 of which must be taken
courses = { "CPSC-50100": [1,2,3,5,7,8,9,11,13,14],
            "MATH-51000": [1,3,5,7,9,11,13],
            "MATH-51100": [2,4,8,10,14],
            "MATH-51200": [4,10],
            "CPSC-51000": [1,5,7,11,13],
            "CPSC-51100": [1,3,5,7,9,11,13],
            "CPSC-53000": [2,5,8,11,14],
            "CPSC-54000": [2,3,8,9,14],
            "CPSC-55000": [1,5,7,11,13],
            "CPSC-50600": [100,1,3,5,7,9,11,13],
            "CPSC-51700": [200,2,8,14],
            "CPSC-52500": [300,2,4,6,8,10,12,14],
            "CPSC-55200": [400,2,8,14],
            "CPSC-55500": [500,1,4,7,10,13],
            "CPSC-57100": [600,3,9],
            "CPSC-57200": [700,5,11],
            "CPSC-57400": [800,4,10],
            "CPSC-59000": [2,4,5,8,10,11,14]}

#Define pre-requisite function to ensure that course_before occurs before course_after
def prereq(course_before, course_after):
    return course_before < course_after

problem = Problem()

#Add list of courses and possible terms as variables
for key, value in courses.items():
    problem.addVariable(key, value)

#Add constraint for not taking 5 of the 8 possible electives
problem.addConstraint(SomeInSetConstraint([100,200,300,400,500,600,700,800], 5, True),
                      ["CPSC-50600", "CPSC-51700", "CPSC-52500", "CPSC-55200", "CPSC-55500",
                       "CPSC-57100", "CPSC-57200", "CPSC-57400"])

#Students may only take one course per term
problem.addConstraint(AllDifferentConstraint())

#List of pre-requisite courses, first course must be taken before the second
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-51100"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-55200"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-51000"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-53000"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-54000"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-55000"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-51700"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-55200"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-55500"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-57100"])
problem.addConstraint(prereq, ["CPSC-57100", "CPSC-57200"])
problem.addConstraint(prereq, ["CPSC-57100", "CPSC-57400"])
problem.addConstraint(prereq, ["MATH-51100", "MATH-51200"])
problem.addConstraint(prereq, ["MATH-51000", "CPSC-59000"])
problem.addConstraint(prereq, ["MATH-51100", "CPSC-59000"])
problem.addConstraint(prereq, ["MATH-51200", "CPSC-59000"])
problem.addConstraint(prereq, ["CPSC-50100", "CPSC-59000"])
problem.addConstraint(prereq, ["CPSC-51000", "CPSC-59000"])
problem.addConstraint(prereq, ["CPSC-51100", "CPSC-59000"])
problem.addConstraint(prereq, ["CPSC-53000", "CPSC-59000"])
problem.addConstraint(prereq, ["CPSC-54000", "CPSC-59000"])
problem.addConstraint(prereq, ["CPSC-55000", "CPSC-59000"])

#Get solution
csp_solutions = problem.getSolutions()
solution = pd.Series(csp_solutions[0])

#Print header
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: Thomas Swed")
print()
print("START TERM = Year 1 Fall 1")
print("Number of Possible Degree Plans is " + str(len(csp_solutions)))
print()

#Sort the solution
sorted_solution = sorted(solution.items(), key=lambda kv: kv[1])

#Print courses not taken
for key, value in sorted_solution:
    if (value >= 100):
        print(key + " " + terms_dic.get(value))

#Print remaining courses
for key, value in sorted_solution:
    if (value < 100):
        print(key + " " + terms_dic.get(value))