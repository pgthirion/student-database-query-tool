import sqlite3
import json
import xml.etree.ElementTree as ET

# Function to store data as JSON
def store_data_as_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to store data as XML
def store_data_as_xml(data, filename):
    root = ET.Element("data")
    for item in data:
        entry = ET.SubElement(root, "entry")
        for key, value in item.items():
            ET.SubElement(entry, key).text = str(value)
    tree = ET.ElementTree(root)
    tree.write(filename)

def offer_to_store(data):
    choice = input("Would you like to store this result (Y/N)? ").strip().lower()
    if choice == "y":
        filename = input("Specify filename. Must end in .xml or .json: ")
        ext = filename.split(".")[-1]
        if ext == 'xml':
            converted_data = [{"course_name": row[0]} for row in data]
            store_data_as_xml(converted_data, filename)
        elif ext == 'json':
            converted_data = [{"course_name": row[0]} for row in data]
            store_data_as_json(converted_data, filename)
        else:
            print("Invalid file extension. Please use .xml or .json")

def execute_query_and_display(cursor, query):
    cursor.execute(query)
    data = cursor.fetchall()
    if data:
        for row in data:
            print(row[0])
        offer_to_store(data)  # Offer to save the result as XML or JSON
    else:
        print("No results found.")

# Function to look up address information
def lookup_address(cur, first_name, last_name):
    query = f"SELECT street, city FROM Student AS s " \
            f"JOIN Address AS a ON s.address_id = a.address_id " \
            f"WHERE s.first_name = ? AND s.last_name = ?"
    
    data = cur.execute(query, (first_name, last_name)).fetchall()
    
    if data:
        print("Address information:")
        for row in data:
            street, city = row
            print(f"Street: {street}\nCity: {city}\n")
    else:
        print("No address information found for the given student.")

# Main function
def main():
    conn = sqlite3.connect("HyperionDev.db")
    cur = conn.cursor()

    usage = '''
    What would you like to do?
    vs - View subjects by student_id
    la - Look up address by first name and surname
    lr - List reviews by student_id
    lc - List courses by teacher_id
    lnc - List students who haven't completed their course
    lf - List students who have completed course with <=30 marks
    e - Exit
    Type your option here: '''

    print("Welcome to the data querying app!")

    while True:
        user_input = input(usage).strip().split(" ")
        command = user_input[0]

        if command == 'vs':
            # Get student_id from user input
            if len(user_input) != 2:
                print("The 'vs' command requires a student_id argument.")
                continue
            student_id = user_input[1]
            
            # Construct query to retrieve course names
            query = f"SELECT course_name FROM Course c JOIN StudentCourse sc ON c.course_code = sc.course_code WHERE sc.student_id = '{student_id}'"
            
            # Execute query and display course names
            execute_query_and_display(cur, query)

        
        elif command == "la":
            # Get first name and last name from user input
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            
            # Look up address information and display
            lookup_address(cur, first_name, last_name)
            offer_to_store(data)
        elif command == 'lc':
            # Get teacher_id from user input
            if len(user_input) != 2:
                print("The 'lc' command requires a teacher_id argument.")
                continue
            teacher_id = user_input[1]
            
            # Construct query to retrieve course names taught by the given teacher
            query = f"SELECT course_name FROM Course WHERE teacher_id = '{teacher_id}'"
            
            # Execute query and display course names
            execute_query_and_display(cur, query)
       
        elif command == 'lr':
            # Get student_id from user input
            if len(user_input) != 2:
                print("The 'lr' command requires a student_id argument.")
                continue
            student_id = user_input[1]
            
            # Construct query to retrieve review details
            query = f"SELECT completeness, efficiency, style, documentation, review_text FROM Review WHERE student_id = '{student_id}'"
            
            # Execute query and display review details
            cur.execute(query)
            data = cur.fetchall()
            if data:
                print("Reviews for student:")
                for row in data:
                    completeness, efficiency, style, documentation, review_text = row
                    print(f"Completeness: {completeness}\nEfficiency: {efficiency}\nStyle: {style}\nDocumentation: {documentation}\nReview Text: {review_text}\n")
            else:
                print("No reviews found for the given student.")
      
        elif command == 'lnc':
            # Construct query to retrieve students who haven't completed their course
            query = "SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_name FROM Student s " \
                    "JOIN StudentCourse sc ON s.student_id = sc.student_id " \
                    "JOIN Course c ON sc.course_code = c.course_code " \
                    "WHERE sc.is_complete = 0"
            
            # Execute query and display results
            cur.execute(query)
            data = cur.fetchall()

            if data:
                print("Students who haven't completed their course:")
                for row in data:
                    student_id, first_name, last_name, email, course_name = row
                    print(f"Student ID: {student_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nCourse Name: {course_name}\n")
            else:
                print("No results found.")
        
        elif command == 'lf':
            # Construct query to retrieve students who have completed the course with a mark of 30 or below
            query = "SELECT s.student_id, s.first_name, s.last_name, s.email, c.course_name, sc.mark FROM Student s " \
                    "JOIN StudentCourse sc ON s.student_id = sc.student_id " \
                    "JOIN Course c ON sc.course_code = c.course_code " \
                    "WHERE sc.is_complete = 1 AND sc.mark <= 30"
            
            # Execute query and display results
            cur.execute(query)
            data = cur.fetchall()

            if data:
                print("Students who have completed the course with a mark of 30 or below:")
                for row in data:
                    student_id, first_name, last_name, email, course_name, mark = row
                    print(f"Student ID: {student_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nCourse Name: {course_name}\nMark: {mark}\n")
            else:
                print("No results found.")
        
        elif command == 'e':
            # Exit the program
            print("Program exited successfully!")
            break
        
        else:
            print(f"Incorrect command: '{command}'")

if __name__ == "__main__":
    main()
