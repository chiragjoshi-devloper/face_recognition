#import subprocess
import tkinter as tk
from tkinter import messagebox
#import numpy as np
import face_recognition
import os
import cv2
import csv
from PIL import Image, ImageTk
from datetime import datetime
from tkinter.scrolledtext import ScrolledText

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("FACE ID ATTENDANCE")
        self.root.geometry("1200x520+350+100")
        self.root.configure(bg="#FFA500")
        self.login_frame = self.create_login_frame()
        self.known_people_directory = r"E:\softwareproject\knownpeople"
        self.attendance_csv_path = os.path.join(os.getcwd(), "attendance.csv")

    def show_frame(self, frame):
        frame.tkraise()

    def create_login_frame(self):
        login_frame = tk.Frame(self.root, bg="#FFA500")

        tk.Label(login_frame, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("Helvetica", 16), fg="white",
                 bg="#FFA500").place(relx=0.5, rely=0.1, anchor='center')
        tk.Button(login_frame, text="Teacher Login", command=self.teacher_function).place(relx=0.5, rely=0.3, anchor='center')
        tk.Button(login_frame, text="Student Login", command=self.student_function).place(relx=0.5, rely=0.4, anchor='center')

        login_frame.place(x=0, y=0, relwidth=1, relheight=1)
        return login_frame

    def teacher_function(self):
        teacher_frame = tk.Frame(self.root, bg="#FFA500")

        tk.Label(teacher_frame, text="Teacher Login Page", font=("Helvetica", 16), fg="white", bg="#FFA500").place(
            relx=0.5, rely=0.1, anchor='center')

        password_entry = tk.Entry(teacher_frame, show="*", font=("Helvetica", 12))
        password_entry.place(relx=0.5, rely=0.3, anchor='center')

        login_button = tk.Button(teacher_frame, text="Login", command=lambda: self.check_teacher_password(teacher_frame, password_entry.get()))
        login_button.place(relx=0.5, rely=0.4, anchor='center')

        tk.Button(teacher_frame, text="Back", command=lambda: [teacher_frame.destroy(), self.login_frame_function()]).place(relx=0.5, rely=0.5, anchor='center')

        teacher_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(teacher_frame)

    def check_teacher_password(self, frame, entered_password):
        if entered_password == "1234":
            self.teacher_home_frame(frame)
        else:
            print("Incorrect password")

    def teacher_home_frame(self, previous_frame):
        teacher_home_frame = tk.Frame(self.root, bg="#FFA500")

        tk.Label(teacher_home_frame, text="Teacher Home Page", font=("Helvetica", 16), fg="white", bg="#FFA500").place(
            relx=0.5, rely=0.1, anchor='center')
        tk.Button(teacher_home_frame, text="Check Attendance", command=self.check_attendance).place(relx=0.5, rely=0.3, anchor='center')
        tk.Button(teacher_home_frame, text="Register Student", command=self.register_student).place(relx=0.5, rely=0.4, anchor='center')
        tk.Button(teacher_home_frame, text="Back",
                  command=lambda: [teacher_home_frame.destroy(), previous_frame.destroy(), self.login_frame_function()]).place(relx=0.5, rely=0.5, anchor='center')

        teacher_home_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(teacher_home_frame)

    def check_attendance(self):
        check_attendance_frame = tk.Frame(self.root, bg="#FFA500")
        tk.Label(check_attendance_frame, text="Check Attendance", font=("Helvetica", 16), fg="white", bg="#FFA500").place(relx=0.5, rely=0.1, anchor='center')
        attendance_text = ScrolledText(check_attendance_frame, width=60, height=15, wrap=tk.WORD)
        attendance_text.place(relx=0.5, rely=0.5, anchor='center')

        try:
            with open(self.attendance_csv_path, "r") as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header if exists
                rows = list(reader)
                if not rows:
                    attendance_text.insert(tk.END, "No attendance records yet.")
                else:
                    attendance_content = "\n".join([", ".join(row) for row in rows])
                    attendance_text.insert(tk.END, attendance_content)
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "The attendance file is not found.")

        tk.Button(check_attendance_frame, text="Back", command=lambda: [check_attendance_frame.destroy(), self.login_frame_function()]).place(x=750, y=400, anchor='center')
        check_attendance_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(check_attendance_frame)

    def register_student(self):
        register_student_frame = tk.Frame(self.root, bg="#FFA500")

        tk.Label(register_student_frame, text="Register Student", font=("Helvetica", 16), fg="white", bg="#FFA500").place(
            relx=0.5, rely=0.1, anchor='center')

        capture_image_button = tk.Button(register_student_frame, text="Capture Image", command=self.capture_image)
        capture_image_button.place(relx=0.5, rely=0.3, anchor='center')

        self.image_label = tk.Label(register_student_frame, text="No Image", font=("Helvetica", 12), bg="#FFA500")
        self.image_label.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(register_student_frame, text="Enter Student's Name:", font=("Helvetica", 12), bg="#FFA500").place(relx=0.5, rely=0.6, anchor='center')


        self.name_entry = tk.Entry(register_student_frame, font=("Helvetica", 12))
        self.name_entry.place(relx=0.5, rely=0.7, anchor='center')

        self.register_button = tk.Button(register_student_frame, text="Register", command=self.register_captured_image)
        self.register_button.place_forget()

        tk.Button(register_student_frame, text="Back", command=lambda: [register_student_frame.destroy(), self.login_frame_function()]).place(relx=0.5, rely=0.9, anchor='center')

        register_student_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(register_student_frame)

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        self.resized_frame = cv2.resize(frame, (300, 225))

        pil_image = Image.fromarray(cv2.cvtColor(self.resized_frame, cv2.COLOR_BGR2RGB))

        tk_image = ImageTk.PhotoImage(pil_image)

        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

        self.register_button.place(relx=0.5, rely=0.8, anchor='center')

    def register_captured_image(self):
        entered_name = self.name_entry.get()

        directory = r"E:\softwareproject\knownpeople"
        image_path = os.path.join(directory, f"{entered_name}.jpg")

        pil_image = Image.fromarray(cv2.cvtColor(self.resized_frame, cv2.COLOR_BGR2RGB))

        pil_image.save(image_path, format="JPEG")

        success_message = f"Student {entered_name} registered successfully!"
        messagebox.showinfo("Registration Success", success_message)

        print(f"Registering Captured Image with the name: {entered_name}")

    def student_function(self):
        student_frame = tk.Frame(self.root, bg="#FFA500")

        tk.Label(student_frame, text="Student Login Page", font=("Helvetica", 16), fg="white", bg="#FFA500").place(relx=0.5, rely=0.1, anchor='center')
        tk.Button(student_frame, text="Back",
                  command=lambda: [student_frame.destroy(), self.login_frame_function()]).place(x=600, y=400, anchor='center')
        tk.Button(student_frame, text="Login", command=self.student_login).place(x=600, y=440, anchor='center')

        student_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(student_frame)

    def student_login(self):
        temp_image_path = "temp_image.jpg"
        self.capture_temp_image(temp_image_path)

        known_people_directory = r"E:\softwareproject\knownpeople"

        known_face_encodings = []
        known_face_names = []

        for filename in os.listdir(known_people_directory):
            image_path = os.path.join(known_people_directory, filename)
            known_image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(known_image)

            if face_encodings:
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])

        unknown_image = face_recognition.load_image_file(temp_image_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        if not unknown_encodings:  # If no face is detected
            messagebox.showinfo("No Face Detected", "No face detected in the captured image. Try again.")
            os.remove(temp_image_path)
            return  # Stop execution here

        unknown_encoding = unknown_encodings[0]

        matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding)

        if any(matches):
            matched_name = known_face_names[matches.index(True)]
            attendance_message = f"Attendance marked for {matched_name}"
            messagebox.showinfo("Attendance Marked", attendance_message)
            self.write_attendance(matched_name)
        else:
            messagebox.showinfo("Student Not Recognized", "Student isn't recognized in the known images.")

        self.display_temp_image(temp_image_path)
        os.remove(temp_image_path)

    def display_temp_image(self, image_path):
        pil_image = Image.open(image_path)

        tk_image = ImageTk.PhotoImage(pil_image)

        display_window = tk.Toplevel(self.root)
        display_window.title("Captured Image")

        image_label = tk.Label(display_window, image=tk_image)
        image_label.image = tk_image
        image_label.pack()

    def capture_temp_image(self, image_path):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        cv2.imwrite(image_path, frame)

    def write_attendance(self, student_name):
        file_exists = os.path.isfile(self.attendance_csv_path)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.attendance_csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "DateTime"])
            writer.writerow([student_name, current_datetime])

    def login_frame_function(self):
        self.login_frame.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()