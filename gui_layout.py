from tkinter import *
import mysql.connector
from mysql.connector import Error

root = Tk()
root.title(" GPA Calculator ")

try:
    database_check = """CREATE DATABASE IF NOT EXISTS student_gpa"""
    global connection
    connection = mysql.connector.connect(host ='localhost',user='root',password='123456')
    global cursor
    cursor = connection.cursor()
    cursor.execute(database_check)
    set_database = """USE STUDENT_GPA"""
    cursor.execute(set_database)
    create_table = """CREATE TABLE IF NOT EXISTS GPAS (Name VARCHAR(250), GPA FLOAT)"""
    cursor.execute(create_table)
except Error as e:
    errorMessage(2)


def sql_data_entry():
    """
        Enters the data of each student into the database. Throws an error message if anything goes wrong.
    """
    try:
        mySql_insert_query = """INSERT INTO GPAS VALUES 
                                  (%s, %s) """
        recordTuple = (str(name_entry.get()), gpa)
        cursor.execute(mySql_insert_query, recordTuple)
        connection.commit()
        cursor.close()
    except Error as e:
        errorMessage(3)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def display_database():
    try:
        sql_select_Query = "select * from GPAS ORDER BY GPA"
        display.delete(1.0, END)
        display.insert(END, "+-----------------------+--------+\n" +
                       "| NAME OF STUDENT       |   GPA  |\n" +
                       "+-----------------------+--------+\n")
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()

        for row in records:
            display.insert(END, " " + str(row[0]) + "               " + str(row[1]) + "\n")
    except Error as e:
        errorMessage(4)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


def errorMessage(msg):
    if msg == 1:
        display.insert(1.0, " There has been an error in the input values of the grades and credit values.")
    elif msg == 2:
        display.insert(1.0, "There has been an error in database initialization.")
    elif msg == 3:
        display.insert(1.0, "Looks like there has been a malfunction while entering data into the DATABASE.")
    elif msg ==4:
        display.insert(1.0, "Error reading data from MySQL table")


def clearGrades():
    e11.delete(0, END)
    e21.delete(0, END)
    e31.delete(0, END)
    e41.delete(0, END)
    e51.delete(0, END)
    e61.delete(0, END)
    e71.delete(0, END)
    e81.delete(0, END)


def calculate():
    try:
        grades = []
        credits = []
        g1 = e11.get()
        g2 = e21.get()
        g3 = e31.get()
        g4 = e41.get()
        g5 = e51.get()
        g6 = e61.get()
        g7 = e71.get()
        g8 = e81.get()
        grades.extend([g1, g2, g3, g4, g5, g6, g7, g8])
        credits.extend([float(e12.get()), float(e22.get()), float(e32.get()), float(e42.get()), float(e52.get()),
                        float(e62.get()), float(e72.get()), float(e82.get())])

        def gpacalc(grade_list, credit_list):
            gradetomarks = []
            total = 0
            fincredits = 0
            '''
            for count in range(len(grade_list)):
                if grade_list[count] == 'B':
                    gradetomarks.append(6)
                elif grade_list[count] == 'B+':
                    gradetomarks.append(7)
                elif grade_list[count] == 'A':
                    gradetomarks.append(8)
                elif grade_list[count] == 'A+':
                    gradetomarks.append(9)
                elif grade_list[count] == 'O':
                    gradetomarks.append(10)
                elif grade_list[count] == 'C':
                    gradetomarks.append(5)
                elif grade_list[count] == 'F':
                    gradetomarks.append(0)
            '''
            grade2credit = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0}
            for gs in grade_list:
                gradetomarks.append(grade2credit[gs])

            for count in range(len(gradetomarks)):
                total += gradetomarks[count] * credit_list[count]

            for gpa in credit_list:
                fincredits += int(gpa)
            finalgpa = total / fincredits
            fingpa = str(round(finalgpa, 2))
            return fingpa

        global gpa
        gpa = gpacalc(grades, credits)
        clearGrades()
        res_entry.delete(0, END)
        res_entry.insert(string=gpa, index=0)
        display.delete(1.0, END)
        display.insert(1.0, "\n Name: " + name_entry.get() + "\n Grade Point Average: " + gpa +
                       "\n Data entered Successfully in the Database. \n")

    except ValueError:
        errorMessage(1)

    sql_data_entry()


def clearAll():
    e11.delete(0, END)
    e12.delete(0, END)
    e21.delete(0, END)
    e22.delete(0, END)
    e31.delete(0, END)
    e32.delete(0, END)
    e41.delete(0, END)
    e42.delete(0, END)
    e51.delete(0, END)
    e52.delete(0, END)
    e61.delete(0, END)
    e62.delete(0, END)
    e71.delete(0, END)
    e72.delete(0, END)
    e81.delete(0, END)
    e82.delete(0, END)
    display.delete(1.0, END)


header1 = Label(root, text="Subjects", font="Verdana 12 bold", padx=5, pady=5).grid(row=0, column=0)
header2 = Label(root, text="Grades", font="Verdana 12 bold", padx=5, pady=5).grid(row=0, column=1)
header3 = Label(root, text="Credits", font="Verdana 12 bold", padx=5, pady=5).grid(row=0, column=2)

sub1 = Label(root, text="Subject 1: ", padx=5, pady=5)
sub1.grid(row=1, column=0)
e11 = Entry(root, width=40, justify="center", bd=5)
e11.grid(row=1, column=1)
e12 = Entry(root, width=40, justify="center", bd=5)
e12.grid(row=1, column=2)

sub2 = Label(root, text="Subject 2: ", padx=5, pady=5)
sub2.grid(row=2, column=0)
e21 = Entry(root, width=40, justify="center", bd=5)
e21.grid(row=2, column=1)
e22 = Entry(root, width=40, justify="center", bd=5)
e22.grid(row=2, column=2)

sub3 = Label(root, text="Subject 3: ", padx=5, pady=5)
sub3.grid(row=3, column=0)
e31 = Entry(root, width=40, justify="center", bd=5)
e31.grid(row=3, column=1)
e32 = Entry(root, width=40, justify="center", bd=5)
e32.grid(row=3, column=2)

sub4 = Label(root, text="Subject 4: ", padx=5, pady=5)
sub4.grid(row=4, column=0)
e41 = Entry(root, width=40, justify="center", bd=5)
e41.grid(row=4, column=1)
e42 = Entry(root, width=40, justify="center", bd=5)
e42.grid(row=4, column=2)

sub5 = Label(root, text="Subject 5: ", padx=5, pady=5)
sub5.grid(row=5, column=0)
e51 = Entry(root, width=40, justify="center", bd=5)
e51.grid(row=5, column=1)
e52 = Entry(root, width=40, justify="center", bd=5)
e52.grid(row=5, column=2)

sub6 = Label(root, text="Subject 6: ", padx=5, pady=5)
sub6.grid(row=6, column=0)
e61 = Entry(root, width=40, justify="center", bd=5)
e61.grid(row=6, column=1)
e62 = Entry(root, width=40, justify="center", bd=5)
e62.grid(row=6, column=2)

sub7 = Label(root, text="Subject 7: ", padx=5, pady=5)
sub7.grid(row=7, column=0)
e71 = Entry(root, width=40, justify="center", bd=5)
e71.grid(row=7, column=1)
e72 = Entry(root, width=40, justify="center", bd=5)
e72.grid(row=7, column=2)

sub8 = Label(root, text="Subject 8: ", padx=5, pady=5)
sub8.grid(row=8, column=0)
e81 = Entry(root, width=40, justify="center", bd=5)
e81.grid(row=8, column=1)
e82 = Entry(root, width=40, justify="center", bd=5)
e82.grid(row=8, column=2)

emp = Label(root, text=" ").grid(row=9, column=0)

# Calculate Button
cal = Button(root, text="Calculate", width=25, command=calculate, bd=5)
cal.grid(row=11, column=1)
# Database Button
show_databases = Button(root, text="Show Database", width=25, bd=5, command=display_database)
show_databases.grid(row=11, column=2)
# Clear Button
clear = Button(root, text="Clear All", width=25, bd=5, command=clearAll)
clear.grid(row=11, column=0)

# Name Entry Box
name_label = Label(root, text=" Enter your Name: ", padx=5, pady=5)
name_label.grid(row=10, column=0)

name_entry = Entry(root, width=25, bd=5)
name_entry.grid(row=10, column=1)

res = Label(root, text="Final GPA : ", padx=5, pady=5)
res.grid(row=12, column=0)

res_entry = Entry(root, width=15, justify="center", bd=5)
res_entry.grid(row=12, column=1)

emp1 = Label(root, text=" ").grid(row=13, column=0)
t1 = Frame(master=root, bd=5)
t1.grid(row=14, column=1)

S = Scrollbar(t1)
display = Text(t1, height=15, width=75, wrap=WORD)
S.pack(side=RIGHT, fill=Y)
display.pack(side=LEFT, fill=Y)
S.config(command=display.yview)
display.config(yscrollcommand=S.set)
root.mainloop()
