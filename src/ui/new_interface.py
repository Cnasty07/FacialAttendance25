import datetime
import tkinter as tk
from tkinter import Label, Button , ttk 
import cv2
from PIL import Image, ImageTk
import threading

class FacialAttendanceSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Attendance System")
        self.root.geometry("800x600")

        # Title
        self.title_label = Label(root, text="Facial Attendance System", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)
        
        # FIXME: Implement the class list from the database
        # Class List
        # classes_list = ClassTable("./database/school.db").read_all()
        # print(classes_list)

        def on_select(event):
            selected_item = self.class_list.get()
        self.class_list = ttk.Combobox(root,values= ["Math 101","Math 102","Math 103","Math 104","Math 105"])
        self.class_list.set("Select Class")
        self.class_list.bind("<<ComboboxSelected>>",on_select)
        self.class_list.pack(pady=10)

        # Camera Feed Frame
        self.camera_frame = Label(root)
        self.camera_frame.pack(pady=10, expand=True, fill="both")

        # Record Attendance Button
        self.record_button = Button(
            root,
            text="Record Attendance",
            font=("Helvetica", 14),
            command=self.record_attendance  # Placeholder for the method to be hooked up later
        )
        self.record_button.pack(pady=10)

        # Initialize camera and thread
        self.cap = cv2.VideoCapture(0)  # Open the default camera (index 0)
        self.running = True
        self.update_camera()

    def update_camera(self):
        """Update the camera feed in the GUI."""
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            # Convert BGR (OpenCV) to RGB (Pillow)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

            # Update the frame
            self.camera_frame.configure(image=frame_image)
            self.camera_frame.image = frame_image

        # Schedule the next update
        self.root.after(10, self.update_camera)
    
    def confirm_attendance(self, student_name, class_name):
        """Method for attendance confirmation window."""
        self.confirm_window = tk.Toplevel(self.root)
        self.confirm_window.title("Attendance Confirmation")
        self.confirm_window.geometry("400x200")

        # Generate current date and time
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Create confirmation message
        message = (f"Successfully recorded student {student_name} "
                f"on {formatted_time} for class {class_name}.")

        self.confirmation_label = Label(
            self.confirm_window,
            text=message,
            font=("Helvetica", 12),
            wraplength=350,
            justify="center"
        )
        self.confirmation_label.pack(pady=20)

        # Close Button for the confirmation window
        close_button = Button(self.confirm_window, text="Close", command=self.confirm_window.destroy)
        close_button.pack(pady=10)

    def record_attendance(self):
        """Method to simulate attendance recording and open the confirmation window."""
        # Simulate getting student name and class name (replace this with real data later)
        student_name = "John Doe"
        class_name = "Math 101"

        # Open the confirmation window
        threading.Thread(target=self.confirm_attendance, args=(student_name, class_name)).start()


    def close(self):
        """Clean up resources when the application is closed."""
        self.running = False
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacialAttendanceSystemApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
