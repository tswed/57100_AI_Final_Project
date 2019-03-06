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

required_courses = ["Course A", "Course B", "Course C", "Course D"]
weekday_values = { "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5}


class Course:
    def __init__(self, course_name, professor_rating, course_time, course_day, type, terms):
        self.course_name = course_name
        self.professor_rating = professor_rating
        self.course_time = course_time
        self.course_day = course_day
        self.type = type
        self.terms = terms

    def __lt__(self, other):  #less than
        return self.professor_rating < other.professor_rating

    def __hash__(self):
        return self.course_name.__hash__()


def create_term_list(terms, years=4):
    '''Create a list of term indexes for years in the future'''
    all_terms = []
    for year in range(years):
        for term in terms:
            if year*3+term <= 11:
                all_terms.append(year*3+term)
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
        if day not in weekday_values.keys():
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


def get_best_course_to_add(available_courses):
    best_rating = 1

    # check for course with highest rated professor to add to students schedule
    for c in available_courses.iterrows():
        if c[1].professor_rating >= best_rating:
            best_rating = c[1].professor_rating
            best_course = Course(c[1].course_name, c[1].professor_rating, c[1].course_time,
                                 c[1].course_day, c[1].type, create_term_list(list(c[1][c[1] == 'Y'].index)))

    return best_course


def add_electives(courses_scheduled, electives, current_courses):
    num_electives = 1

    # Add up to 4 electives to courses_scheduled if they meet students preferences
    for course in electives.iterrows():
        if course[1].course_time == preferred_time and course[1].professor_rating >= min_professor_rating:
            if course[1].course_day in preferred_days and num_electives <= 4:
                courses_scheduled.append(Course(course[1].course_name, course[1].professor_rating,
                                                course[1].course_time, course[1].course_day, course[1].type,
                                                create_term_list(list(course[1][course[1] == 'Y'].index))))
                num_electives = num_electives + 1

    # Update courses_scheduled to include the electives just added
    for course in courses_scheduled:
        current_courses.append(course.course_name)

    # Add electives if student has not met minimum required 4 electives
    for course in electives.iterrows():
        if course[1].course_name not in current_courses and num_electives <= 4:
            courses_scheduled.append(Course(course[1].course_name, course[1].professor_rating,
                                            course[1].course_time, course[1].course_day, course[1].type,
                                            create_term_list(list(course[1][course[1] == 'Y'].index))))
            num_electives = num_electives + 1


# Check if there are extra courses outside those required and remove from schedule if found
def remove_courses_if_needed(courses_scheduled):
    for course in courses_scheduled:
        if course.course_name not in required_courses and course.type != 'elective':
            courses_scheduled.remove(course)

    return courses_scheduled


def add_courses_if_needed(courses_scheduled, electives):
    current_courses = []

    for course in courses_scheduled:
        current_courses.append(course.course_name)

    # Loop through required courses to ensure that all are taken
    for course in required_courses:
        # Check if students needs courses outside their preferences and add if needed
        if course not in current_courses:
            courses_to_add = course_rotations.loc[course_rotations['course_name'] == course]
            courses_scheduled.append(get_best_course_to_add(courses_to_add))

    add_electives(courses_scheduled, electives, current_courses)

    return courses_scheduled


# Load dataFrame data into an array of objects to allow for easier filtering
def convert_to_object_array(data):
    course_array_list = []

    # Loop over filtered dataFrame information to create an object for each row
    for course in data.iterrows():
        temp_course = Course(course[1].course_name, course[1].professor_rating, course[1].course_time,
                                 course[1].course_day, course[1].type, create_term_list(list(course[1][course[1] == 'Y'].index)))

        course_array_list.append(temp_course)

    return course_array_list

def add_constraints():
    # Need to figure out how to allow for multiple courses per term
    problem.addConstraint(AllDifferentConstraint())

    # List of pre-requisite courses, first course must be taken before the second
    problem.addConstraint(prereq, ["Course A", "Course B"])
    problem.addConstraint(prereq, ["Course A", "Course C"])
    problem.addConstraint(prereq, ["Course A", "Course D"])
    problem.addConstraint(prereq, ["Course B", "Course D"])

    problem.addConstraint(SomeInSetConstraint([1, 2], 2, True))


# MAIN PROGRAM STARTS

# Load list of courses and variables from Excel
course_rotations = pd.read_excel('course_rotations.xlsx', sheet_name='course_rotations')
elective_courses = course_rotations.loc[course_rotations.type == 'elective']
course_rotations = course_rotations.loc[course_rotations.type != 'elective']

#get_user_input()

data = course_rotations.copy()

min_professor_rating = 3
preferred_time = "morning"
preferred_days = ["monday", "tuesday", "wednesday", "friday"]

# Subset courses minimum rating and higher
data = data.loc[data['professor_rating'] >= min_professor_rating]

# Subset courses preferred time of day
data = data.loc[data['course_time'] == preferred_time]

# Subset courses three preferred days
data = data.loc[data['course_day'].isin(preferred_days)]

course_array = convert_to_object_array(data)

final_schedule = add_courses_if_needed(course_array, elective_courses)
final_schedule = remove_courses_if_needed(final_schedule)

# Instantiate CSP object
problem = Problem()

for row in final_schedule:
    problem.addVariable(row.course_name, row.terms)

add_constraints()

# Get solutions
csp_solutions = problem.getSolutions()

# Get first solution in dict
solution = pd.Series(csp_solutions[0])

print("Number of Possible Degree Plans is " + str(len(csp_solutions)))
print()
print(solution)