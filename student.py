import sqlite3
import tkinter as tk
from tkinter import ttk


def get_connection():
    return sqlite3.connect("course_enrollment.db")


def fet_course():
    
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    con.close()
    courses_tree.delete(*courses_tree.get_children())


    for course in courses:
        courses_tree.insert("", "end", values=course)


def enrl_course():
    select_index = courses_tree.focus()
    if not select_index:
  
        return
    course_id = int(courses_tree.item(select_index, "values")[0])
    
    course_title = courses_tree.item(select_index, "values")[1]
  
    student_name = std_entry.get()
  
  
    con = get_connection()
    cursor = con.cursor()
  
  
    cursor.execute("SELECT COUNT(*) FROM enrollments WHERE course_id=?", (course_id,))
    enrl_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT capacity FROM courses WHERE id=?", (course_id,))
  
    capacity = cursor.fetchone()[0]


    if enrl_cnt >= capacity:
        sts_lbl.config(text="Course is already full. Cannot enroll.", fg="red")
    else:
        cursor.execute("INSERT INTO enrollments (course_id, student_name) VALUES (?, ?)", (course_id, student_name))
        con.commit()
        con.close()

        sts_lbl.config(text=f"Enrolled in {course_title} successfully.", fg="green")
        fet_course()

        std_entry.delete(0, tk.END)
stud_root = tk.Tk()
stud_root.title("Student Panel")
eenrl_frame = tk.Frame(stud_root)


eenrl_frame.pack(pady=20)
std_lbl = tk.Label(eenrl_frame, text="Student Name:")

std_lbl.grid(row=0, column=0, padx=10)

std_entry = tk.Entry(eenrl_frame)


std_entry.grid(row=0, column=1, padx=10)
enrl_bt = tk.Button(eenrl_frame, text="Enroll", command=enrl_course)


enrl_bt.grid(row=1, columnspan=2, pady=10)
columns = ("ID", "Title", "Description", "Instructor", "Capacity")

courses_tree = ttk.Treeview(stud_root, columns=columns, show="headings", height=10)


courses_tree.pack(pady=20)


for col in columns:
    courses_tree.heading(col, text=col)
fet_course()


sts_lbl = tk.Label(stud_root, text="", fg="green", font=("Helvetica", 12))


sts_lbl.pack()






stud_root.mainloop()
