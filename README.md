# Student Database Query Tool

A Python command-line interface (CLI) designed to interact with the `HyperionDev.db` SQLite database. This tool allows administrators to search for student addresses, view course reviews, and identify students who are failing or have not completed their courses.

## Features

* **Database Querying:** Execute complex SQL queries via simple short-codes.
* **Data Export:** Option to save query results to **JSON** or **XML** format.
* **Search Functionality:**
    * Find addresses by student name.
    * View all subjects taken by a specific student.
    * View all reviews written by a specific student.
* **Reporting:**
    * List students who have not completed their courses.
    * List students who scored 30 marks or below.

## Prerequisites

* Python 3.x
* SQLite3 (Included with Python)

## Installation

1.  **Download:**
    * Click the green **<> Code** button.
    * Select **Download ZIP**.
    * Extract the files.

2.  **Verify Database:**
    * Ensure `HyperionDev.db` is in the same folder as `lookup.py`.
    * *Optional:* You can recreate the database from scratch by running the SQL commands in `create_database.sql`.

## Usage

Run the script from your terminal:

    python lookup.py

### Command Menu

Once the program is running, you can use the following codes:

* `vs` - **View Subjects:** View all courses taken by a student (Requires `student_id`).
* `la` - **Lookup Address:** Find a student's address by First Name and Last Name.
* `lr` - **List Reviews:** View all reviews submitted by a student (Requires `student_id`).
* `lc` - **List Courses:** View all courses taught by a teacher (Requires `teacher_id`).
* `lnc` - **List Incomplete:** Show all students who have not marked their course as complete.
* `lf` - **List Failures:** Show all students who scored 30 marks or less.
* `e` - **Exit:** Close the program.

### Exporting Data

After running a query (like `la`), the program will ask:
`Would you like to store this result (Y/N)?`

If you select **Y**, you can save the output as a file (e.g., `results.json` or `report.xml`).

## Database Schema

The database consists of the following tables:
* `Address` (Street, City, Province)
* `Student` (Personal details, linked to Address)
* `Teacher` (Personal details, linked to Address)
* `Course` (Course info, linked to Teacher)
* `StudentCourse` (Grades, Completion status, Junction table)
* `Review` (Course reviews by students)
