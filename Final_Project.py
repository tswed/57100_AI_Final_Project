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

required_courses = ["CPSC-50100", "MATH-51000", "MATH-51100", "CPSC-59000",
                    "CPSC-51100", "CPSC-53000", "CPSC-54000", "CPSC-55000"]
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def create_term_list(terms, years=4):
    '''Create a list of term indexes for years in the future'''
    all_terms = []
    for year in range(years):
        for term in terms:
            if year*6+term <= 12:
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

def add_courses_if_needed(courses_scheduled, electives):
    num_electives = 0

    # Loop through required courses to ensure that all are taken
    for course in required_courses:
        current_courses = courses_scheduled['course_name'].tolist()

        # Check if students needs courses outside their preferences and add if needed
        if course not in current_courses:
            course_to_add = course_rotations.loc[course_rotations['course_name'] == course].iloc[0]
            courses_scheduled = courses_scheduled.append(course_to_add)

    # Get number of electives scheduled already
    for course in courses_scheduled.iterrows():
        if course[1].type == 'elective':
            num_electives = num_electives + 1

    # If student currently has less than 4 electives add up to 4 electives to courses_scheduled
    for course in electives.iterrows():
        if num_electives < 3:
            current_courses = courses_scheduled['course_name'].tolist()
            if course[1].course_name not in current_courses:
                course_to_add = course_rotations.loc[course_rotations['course_name'] == course[1].course_name].iloc[0]
                courses_scheduled = courses_scheduled.append(course_to_add)
                num_electives = num_electives + 1

    return courses_scheduled


def add_constraints():
    # Need to figure out how to allow for multiple courses per term
    problem.addConstraint(AllDifferentConstraint())

    # List of pre-requisite courses, first course must be taken before the second
    problem.addConstraint(prereq, ["CPSC-50100", "CPSC-55200"])
    problem.addConstraint(prereq, ["MATH-51000", "CPSC-59000"])
    problem.addConstraint(prereq, ["MATH-51100", "CPSC-59000"])
    problem.addConstraint(prereq, ["CPSC-50100", "CPSC-59000"])


# MAIN PROGRAM STARTS


# Load list of courses and variables from Excel
course_rotations = pd.read_excel('course_rotations.xlsx', sheet_name='course_rotations')
courses = course_rotations[course_rotations.type != 'elective']
elective_courses = course_rotations[course_rotations.type == 'elective']

#get_user_input()

data = course_rotations.copy()

min_professor_rating = 1
preferred_time = "morning"
preferred_days = ["monday", "tuesday", "wednesday", "friday"]

# Subset courses minimum rating and higher
data = data.loc[data['professor_rating'] >= min_professor_rating]

# Subset courses preferred time of day
data = data.loc[data['course_time'] == preferred_time]

# Subset courses three preferred days
data = data.loc[data['course_day'].isin(preferred_days)]

final_schedule = add_courses_if_needed(data, elective_courses)

# Instantiate CSP object
problem = Problem()

for r, row in final_schedule.iterrows():
    test = list(row[row == 'Y'].index)
    problem.addVariable(row.course_name, create_term_list(list(row[row == 'Y'].index)))

add_constraints()

# Get solutions
csp_solutions = problem.getSolutions()

# Get first solution in dict
solution = pd.Series(csp_solutions[0])

print("Number of Possible Degree Plans is " + str(len(csp_solutions)))
print()
print(solution)