# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# @author: Thomas Swed, James Marquez, Hasan Rauf, Muhammad Sheikh
# created: February 20, 2019
# Artificial Intelligence 1 – CPSC 57100
# Spring I - 2019
# Final Course Project
# Constraint Satisfiability Algorithm for Interactive Student Scheduling

import numpy as np
import pandas as pd
from constraint import *

required_courses = ["CPSC-50100", "MATH-51000", "MATH-51100", "MATH-51200", "CPSC-51000", "CPSC-51100",
                    "CPSC-53000", "CPSC-54000", "CPSC-55000", "CPSC-50600", "CPSC-51700", "CPSC-52500",
                    "CPSC-55200", "CPSC-55500", "CPSC-57100", "CPSC-57200", "CPSC-57400", "CPSC-59000"]
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def create_term_list(terms, years=4):
    '''Create a list of term indexes for years in the future'''
    all_terms = []
    for year in range(years):
        for term in terms:
            if year*6+term <= 14:
                all_terms.append(year*6+term)
    return all_terms


def get_days(message):
    input_days = input(message)
    actual_days = []

    # Parse input into list as comma separated values
    split_days = input_days.split(',')

    # Remove whitespace from input
    for day in split_days:
        day = day.strip()
        day = day.lower()

        # Validate user input to ensure a weekday is selected
        if day not in weekdays:
            get_days("Incorrect weekdays: " + day + " is not a valid day. Please enter 3 days of the week between monday and friday.")
            break

        actual_days.append(day)

    return actual_days


def get_user_input():
    # Get student’s preferred time of day to attend courses
    global preferred_time
    preferred_time = input("Do you prefer morning, afternoon, or night courses?")

    # Get student's max number of courses in one term
    global max_term_courses
    max_term_courses = int(input("What is the max number of courses you would like to take in one term? (4 max)"))

    # Get student's minimum professor rating
    global min_professor_rating
    min_professor_rating = int(input("What is the minimum professor rating you will accept? (5 = highest)"))

    # Get student's top three preferred days of the week and assign to array
    global preferred_days
    preferred_days = get_days("What are your top three preferred days of the week to attend courses (separate days with commas).")


#Define pre-requisite function to ensure that course_before occurs before course_after
def prereq(course_before, course_after):
    return course_before < course_after

def add_courses_if_needed(courses_scheduled):
    for course in required_courses:
        current_courses = courses_scheduled['course_name'].tolist()

        if course not in current_courses:
            course_to_add = course_rotations.loc[course_rotations['course_name'] == course].iloc[0]
            courses_scheduled = courses_scheduled.append(course_to_add)

    return courses_scheduled


def add_constraints():
    # Students may only take one course per term
    problem.addConstraint(AllDifferentConstraint())

    # List of pre-requisite courses, first course must be taken before the second
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

    # Add constraint for not taking 5 of the 8 possible electives
    # problem.addConstraint(SomeInSetConstraint([100, 200, 300, 400, 500, 600, 700, 800], 5, True),
    #                       ["CPSC-50600", "CPSC-51700", "CPSC-52500", "CPSC-55200", "CPSC-55500",
    #                        "CPSC-57100", "CPSC-57200", "CPSC-57400"])

# MAIN PROGRAM STARTS

# Load list of courses and variables from Excel
course_rotations = pd.read_excel('course_rotations.xlsx', sheet_name='course_rotations')

get_user_input()

data = course_rotations.copy()

# Subset courses minimum rating and higher
data = data.loc[data['professor_rating'] >= min_professor_rating]

# Subset courses preferred time of day
data = data.loc[data['course_time'] == preferred_time]

# Subset courses three preferred days
data = data.loc[data['course_day'].isin(preferred_days)]

final_schedule = add_courses_if_needed(data)

# Instantiate CSP object
problem = Problem()

for r, row in final_schedule.iterrows():
    test = list(row[row == 'Y'].index)
    problem.addVariable(row.course_name, create_term_list(list(row[row == 'Y'].index)))

# add_constraints()

# Get solutions
csp_solutions = problem.getSolutions()

# Get first solution in dict
solution = pd.Series(csp_solutions[0])

print("Number of Possible Degree Plans is " + str(len(csp_solutions)))
print()
print(solution)