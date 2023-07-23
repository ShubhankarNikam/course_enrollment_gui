import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


def fet_and_dis_course():
    con = sqlite3.connect("course_enrollment.db")
    cursor = con.cursor()
    cursor.execute("SELECT id, title, description, instructor FROM courses")
    global courses
    courses = cursor.fetchall()
    con.close()

    c_listbox.delete(0, "end")
    for course in courses:
        c_listbox.insert("end", course[1])

def enroll_student():
    sel_index = c_listbox.curselection()
    if not sel_index:
        return

    c_id = courses[sel_index[0]][0]
    
    c_title = courses[sel_index[0]][1]

    con = sqlite3.connect("course_enrollment.db")
    cursor = con.cursor()

    cursor.execute("SELECT COUNT(*) FROM enrollments WHERE c_id=?", (c_id,))
    current_enrollments = cursor.fetchone()[0]
    
    cursor.execute("SELECT capacity FROM courses WHERE id=?", (c_id,))
    
    max_capacity = cursor.fetchone()[0]

    if current_enrollments < max_capacity:
        student_name = student_name_entry.get()
        if not student_name:
            messagebox.showwarning("Missing Information", "Please enter your name.")
            return

        cursor.execute("INSERT INTO enrollments (c_id, student_name) VALUES (?, ?)", (c_id, student_name))
    
        con.commit()
        status_label.config(text=f"Enrolled in {c_title}.")
    
    else:
        status_label.config(text=f"The course {c_title} is full. Enrollment closed.")

    con.close()

student_root = tk.Tk()

student_root.title("Student - Course Enrollment")

style = ttk.Style()

course_frame = ttk.LabelFrame(student_root, text="Available Courses", padding=10)
course_frame.pack(padx=10, pady=10, fill="both", expand=True)

c_listbox = tk.Listbox(course_frame, selectmode="SINGLE", height=10, width=40)

c_listbox.pack(fill="both", expand=True)

fet_and_dis_course()

enroll_frame = ttk.LabelFrame(student_root, text="Enrollment", padding=10)
enroll_frame.pack(padx=10, pady=10)
student_name_label = ttk.Label(enroll_frame, text="Enter Your Name:")
student_name_label.grid(row=0, column=0, padx=5, pady=5)
student_name_entry = ttk.Entry(enroll_frame, width=30)
student_name_entry.grid(row=0, column=1, padx=5, pady=5)
enroll_button = ttk.Button(enroll_frame, text="Enroll", command=enroll_student)
enroll_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
status_label = ttk.Label(student_root, text="", foreground="green")
status_label.pack()





student_root.mainloop()
