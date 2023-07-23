import sqlite3
import tkinter as tk
from tkinter import ttk


def get_connection():
    return sqlite3.connect("course_enrollment.db")

def create_c_table():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL, instructor TEXT NOT NULL, capacity INTEGER NOT NULL)"
    )
    con.commit()
    con.close()

def create_enrl_table():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, c_id INTEGER NOT NULL, student_name TEXT NOT NULL)"
    )
    con.commit()
    con.close()

def add_course():
    
    title = c_title_entry.get()
    
    description = c_description_entry.get()
   
    instructor = c_instructor_entry.get()
    capacity = int(c_capacity_entry.get())

    con = get_connection()
   
    cursor = con.cursor()
    
    cursor.execute(
        "INSERT INTO courses (title, description, instructor, capacity) VALUES (?, ?, ?, ?)",
        (title, description, instructor, capacity),
    )
    con.commit()
   
    con.close()

    c_title_entry.delete(0, tk.END)
    
    c_description_entry.delete(0, tk.END)
    
    c_instructor_entry.delete(0, tk.END)
    c_capacity_entry.delete(0, tk.END)

    fet_and_dis_course()

def fet_and_dis_course():
    con = get_connection()
    
    cursor = con.cursor()
    cursor.execute("SELECT * FROM courses")
    
    courses = cursor.fetchall()
    
    con.close()

    courses_tree.delete(*courses_tree.get_children())
    for course in courses:
        courses_tree.insert("", "end", values=course)

def update_course():
    sel_index = courses_tree.focus()
    if not sel_index:
        return

    c_id = int(courses_tree.item(sel_index, "values")[0])
    current_title = courses_tree.item(sel_index, "values")[1]  # Get the current title

    title = c_title_entry.get()
    description = c_description_entry.get()
    instructor = c_instructor_entry.get()
    capacity = c_capacity_entry.get()

    if capacity:
        try:
            capacity = int(capacity)
        except ValueError:
            status_label.config(text="Invalid capacity. Please enter a valid number.", fg="red")
            return

    con = get_connection()
    cursor = con.cursor()
    
    cursor.execute(
        "UPDATE courses SET title=?, description=?, instructor=?, capacity=? WHERE id=?",
        (title, description, instructor, capacity, c_id),
    )
    
    con.commit()
    con.close()

    status_label.config(text="Course updated successfully.", fg="green")
    fet_and_dis_course()

    c_title_entry.delete(0, tk.END)
    c_description_entry.delete(0, tk.END)
    c_instructor_entry.delete(0, tk.END)
    c_capacity_entry.delete(0, tk.END)

    # Display the current title in the title entry field
    c_title_entry.insert(0, current_title)

def fetch_and_display_students(event):
    sel_index = courses_tree.focus()
    if not sel_index:
        return

    c_id = int(courses_tree.item(sel_index, "values")[0])

    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT student_name FROM enrollments WHERE c_id=?", (c_id,))
    students = cursor.fetchall()
    con.close()

    students_tree.delete(*students_tree.get_children())
    for student in students:
        students_tree.insert("", "end", values=(student[0],))

def reset_database():
    con = get_connection()
    cursor = con.cursor()
   
    cursor.execute("DELETE FROM courses")
    cursor.execute("DELETE FROM enrollments")
    con.commit()
   
    con.close()

    c_title_entry.delete(0, tk.END)
    c_description_entry.delete(0, tk.END)
    c_instructor_entry.delete(0, tk.END)

    c_capacity_entry.delete(0, tk.END)

    courses_tree.delete(*courses_tree.get_children())
    students_tree.delete(*students_tree.get_children())

admin_root = tk.Tk()
admin_root.title("Admin Panel")

course_frame = tk.Frame(admin_root)
course_frame.pack(pady=20)

c_title_label = tk.Label(course_frame, text="Title:")

c_title_label.grid(row=0, column=0, padx=10)
c_title_entry = tk.Entry(course_frame)
c_title_entry.grid(row=0, column=1, padx=10)

c_description_label = tk.Label(course_frame, text="Description:")
c_description_label.grid(row=1, column=0, padx=10)

c_description_entry = tk.Entry(course_frame)

c_description_entry.grid(row=1, column=1, padx=10)

c_inst_label = tk.Label(course_frame, text="Instructor:")

c_inst_label.grid(row=2, column=0, padx=10)
c_instructor_entry = tk.Entry(course_frame)
c_instructor_entry.grid(row=2, column=1, padx=10)

c_capacity_label = tk.Label(course_frame, text="Capacity:")

c_capacity_label.grid(row=3, column=0, padx=10)
c_capacity_entry = tk.Entry(course_frame)
c_capacity_entry.grid(row=3, column=1, padx=10)

add_c_button = tk.Button(course_frame, text="Add Course", command=add_course)
add_c_button.grid(row=4, columnspan=2, pady=10)

update_c_buttonn = tk.Button(course_frame, text="Update Course", command=update_course)
update_c_buttonn.grid(row=5, columnspan=2, pady=10)

reset_database_button = tk.Button(course_frame, text="Reset Database", command=reset_database)
reset_database_button.grid(row=6, columnspan=2, pady=10)

columns = ("ID", "Title", "Description", "Instructor", "Capacity")

courses_tree = ttk.Treeview(admin_root, columns=columns, show="headings", height=10)
courses_tree.pack(pady=20)

for col in columns:
    courses_tree.heading(col, text=col)

fet_and_dis_course()

courses_tree.bind("<<TreeviewSelect>>", fetch_and_display_students)

students_frame = tk.Frame(admin_root)
students_frame.pack(pady=20)

# Label for enrolled students
students_label = tk.Label(students_frame, text="Enrolled Students:", font=("Helvetica", 16))
students_label.pack(pady=10)

students_columns = ("Student Name",)
students_tree = ttk.Treeview(students_frame, columns=students_columns, show="headings", height=10)
students_tree.pack()

for col in students_columns:
    students_tree.heading(col, text=col)

admin_root.mainloop()
