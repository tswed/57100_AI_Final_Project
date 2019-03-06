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

required_courses = ["Course A", "Course B", "Course C", "Course D",
                    "Course E", "Course F", "Course G"]
weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]

#Dictionary to lookup values and print corresponding semester for each course
semesters =	{
   1 : "Year 1 Fall",
   2 : "Year 1 Spring",
   3 : "Year 1 Summer",
   4 : "Year 2 Fall",
   5 : "Year 2 Spring",
   6 : "Year 2 Summer",
   7 : "Year 3 Fall",
   8 : "Year 3 Spring",
   9 : "Year 3 Summer",
   10 : "Year 4 Fall",
   11 : "Year 4 Spring",
   12 : "Year 4 Summer"
}


class Course:
    def __init__(self, course_name, professor_rating, course_time, course_day, type, terms):
        self.course_name = course_name
        self.professor_rating = professor_rating
        self.course_time = course_time
        self.course_day = course_day
        self.type = type
        self.terms = terms

    # Less than function
    def __lt__(self, other):
        return self.professor_rating < other.professor_rating

    # Hash function
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


# Function to display a message to the user and get an array of three days the user
# would like to take classes on.  Validation is also performed to verify spelling/correct days
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


# This performs user input validation to ensure the user is entering a number between 1 and 4
def get_classes_per_semester(message):
    while True:
        try:
            input_classes_per_semester = int(input(message))
        except:
            # Display error message if input cannot be cast to an int
            print("Invalid number, please enter a digit between 1 and 4: ")
            continue
        else:
            break

    # Validate that the input number is between 1 and 4
    if input_classes_per_semester < 1 or input_classes_per_semester > 4:
        get_classes_per_semester("Please input a number between 1 and 4 (1-4): ")

    return input_classes_per_semester


# This performs user input validation to ensure the user is entering a number between 1 and 5
def get_professor_rating(message):
    while True:
        try:
            input_professor_rating = int(input(message))
        except:
            # Display error message if input cannot be cast to an int
            print("Invalid number, please enter a digit between 1 and 5: ")
            continue
        else:
            break

    # Validate that the input number is between 1 and 5
    if input_professor_rating < 1 or input_professor_rating > 5:
        get_professor_rating("Please input a number between 1 and 5 (1-5): ")

    return input_professor_rating


# Function to display messages to the user to get preferences on time of day,
# day of week, max number of courses per semester, and professor rating
def get_user_input():
    # Get student’s preferred time of day to attend courses
    global preferred_time
    preferred_time = input("Do you prefer morning, afternoon, or night courses?")

    # Get student's number of courses to take per semester
    global classes_per_semester
    classes_per_semester = get_classes_per_semester("How many courses would you like to take in one semester? (3 max - 2 recommended)")

    # Get student's minimum professor rating
    global min_professor_rating
    min_professor_rating = get_professor_rating("What is your preferred professor rating? (5 = highest)")

    # Get student's top three preferred days of the week and assign to array
    global preferred_days
    preferred_days = get_days("What are your top three preferred days of the week to attend courses (separate days with commas).")


# Define pre-requisite function to ensure that course_before occurs before course_after
def prereq(course_before, course_after):
    return course_before < course_after


# This determines which of the potential courses has the highest professor rating
# and returns that course as a Course object
def get_best_course_to_add(potential_courses):
    best_rating = 1

    # check for course with highest rated professor to add to students schedule
    for c in potential_courses.iterrows():
        if c[1].professor_rating >= best_rating:
            best_rating = c[1].professor_rating
            best_course = Course(c[1].course_name, c[1].professor_rating, c[1].course_time,
                                 c[1].course_day, c[1].type, create_term_list(list(c[1][c[1] == 'Y'].index)))

    return best_course


# Determines the elective with the highest professor
# rating of the potential electives passed in and returns it
def get_best_elective(potential_electives):
    best_rating = 1

    # Check for elective with highest professor rating and set as best course
    for c in potential_electives:
        if c.professor_rating >= best_rating:
            best_rating = c.professor_rating
            best_course = c

    return best_course


# Students must take 4 electives, this
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
    while num_electives <= 4:
        possible_electives = []

        # Create list of possible electives to add
        for course in electives.iterrows():
            if course[1].course_name not in current_courses:
                possible_electives.append(Course(course[1].course_name, course[1].professor_rating,
                                                 course[1].course_time, course[1].course_day, course[1].type,
                                                 create_term_list(list(course[1][course[1] == 'Y'].index))))

        # Get elective course with the highest professor rating to add to list
        course_to_add = get_best_elective(possible_electives)
        courses_scheduled.append(course_to_add)

        # Add resulting elective course to current course list
        current_courses.append(course_to_add.course_name)
        num_electives = num_electives + 1


# Check if there are extra courses outside those required and remove from schedule if found
def remove_courses_if_needed(courses_scheduled):
    final_courses = []

    for course in courses_scheduled:
        # Only add course to new list of final courses if it is required or an elective
        # Electives have already been set to be only 4
        if course.course_name in required_courses or course.type == 'elective':
            final_courses.append(course)

    return final_courses


# Lookup course object using course name to display results
def get_course_info(result_course):
    for course in final_schedule:
        if course.course_name == result_course:
            return course


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
    final_courses = []

    for course in final_schedule:
        final_courses.append(course.course_name)

    # List of pre-requisite courses, first course must be taken before the second
    problem.addConstraint(prereq, ["Course A", "Course B"])
    problem.addConstraint(prereq, ["Course A", "Course C"])
    problem.addConstraint(prereq, ["Course A", "Course D"])
    problem.addConstraint(prereq, ["Course B", "Course D"])

    # Course A must be taken in the first semester, Course B in the second
    problem.addConstraint(SomeInSetConstraint([1], 1, True), ["Course A"])
    problem.addConstraint(SomeInSetConstraint([2], 1, True), ["Course B"])

    # If students take 3 courses per semester, they will finish early, so there are fewer constraints
    # summers are only allowed one course
    if classes_per_semester == 3:
        problem.addConstraint(SomeInSetConstraint([1], classes_per_semester, True))
        problem.addConstraint(SomeInSetConstraint([2], classes_per_semester, True))
        problem.addConstraint(SomeInSetConstraint([3], 1, True))
        problem.addConstraint(SomeInSetConstraint([4], classes_per_semester, True))
        problem.addConstraint(SomeInSetConstraint([5], 1, True))

    # Students will take exactly the number of courses specified each semester, 2 in this case,
    # with the exception of summers, where they will take 1 course
    if classes_per_semester == 2:
        problem.addConstraint(SomeInSetConstraint([1], classes_per_semester, True))
        problem.addConstraint(SomeInSetConstraint([2], classes_per_semester, True))
        problem.addConstraint(SomeInSetConstraint([3], 1, True))
        problem.addConstraint(SomeInSetConstraint([4], classes_per_semester, True))
        problem.addConstraint(SomeInSetConstraint([5], classes_per_semester, True))
        problem.addConstraint(SomeInSetConstraint([6], 1, True))
        problem.addConstraint(SomeInSetConstraint([7], 1, True))

    # If student chooses to take only one course per semester
    if classes_per_semester == 1:
        problem.addConstraint(AllDifferentConstraint())

# MAIN PROGRAM STARTS

# Load list of courses and variables from Excel
course_rotations = pd.read_excel('course_rotations.xlsx', sheet_name='course_rotations')
elective_courses = course_rotations.loc[course_rotations.type == 'elective']
course_rotations = course_rotations.loc[course_rotations.type != 'elective']

get_user_input()

data = course_rotations.copy()

# min_professor_rating = 4
# classes_per_semester = 3
# preferred_time = "morning"
# preferred_days = ["monday", "wednesday", "friday"]

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

#If no solution is found, let the user know to expand their preferences
if len(csp_solutions) == 0:
    print("It looks like we couldn't find a schedule that matches your preferences, "
          "please try again with fewer restrictions.")
else:
    # Get first solution in dict
    solution = pd.Series(csp_solutions[0])
    # Sort the solution
    sorted_solution = sorted(solution.items(), key=lambda kv: kv[1])

    print("Number of Possible Degree Plans is " + str(len(csp_solutions)))
    print()

    #Print courses
    for key, value in sorted_solution:
        print(key + " " + semesters.get(value) + ", " + get_course_info(key).course_day
              + " " + get_course_info(key).course_time + ", Professor Rating: "
              + str(get_course_info(key).professor_rating))