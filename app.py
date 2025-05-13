import tkinter as tk
import csv
import io

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Uni Companion')
        self.state("zoomed")
        
        self.content_container = tk.Frame(self)
        self.content_container.pack(fill="both", expand=True)
        
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        self.pages = {}
        
        for ClassPage in (HomePage, MidtermPerformanceTracker, TertiaryGPATracker):
            page = ClassPage(parent=self.content_container, controller=self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[ClassPage.__name__] = page
            self.open_page("HomePage")
        
    def open_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()
        
        
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        #configuring the grid to make every cell responsive
        for i in range(0,9):
            self.grid_rowconfigure(i, weight=1)
        for i in range(0,4):
            self.grid_columnconfigure(i, weight=1)
            
        #creating a section for the Head Text
        div1 = tk.Frame(self)
        div1.grid(row=0, rowspan=1, column=0, columnspan=5, sticky="nsew")
        
        main_label= tk.Label(div1, text="Select Your Desired Tool")
        main_label.pack(fill="both", expand=True)
        
        #creating a second section for the buttons
        div2 = tk.Frame(self)
        div2.grid(row=1, rowspan=7, column=0, columnspan=5, sticky="ns")
        
        midterm_performance_tracker_button = tk.Button(div2, text="Midterm Performance Tracker", command=lambda: controller.open_page("MidtermPerformanceTracker"), padx=200)
        midterm_performance_tracker_button.pack(side="left", padx=100, fill="y", expand=True)
        
        tertiary_gpa_tracker_button = tk.Button(div2, text="Tertiary GPA Tracker", command=lambda: controller.open_page("TertiaryGPATracker"), padx=230)
        tertiary_gpa_tracker_button.pack(side="left", padx=100, fill="y", expand=True)
        
class MidtermPerformanceTracker(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.courses = {}
        
        tk.Label(self, text="Midterm Performance Tracker").pack()
        tk.Button(self, text="Home", command=lambda:controller.open_page("HomePage")).pack()
        tk.Button(self, text="Add Course", command=self.open_course_form).pack()
        tk.Button(self, text="Print Courses as CSV", command=self.export_courses_as_csv).pack()
        
    def open_course_form(self):
        #creating the frame form to enter the data for the new course
        course_form = tk.Toplevel(self)
        course_form.title("Course Information")
        course_form.grab_set()
        
        #adding labels and input fields for the info needed for each course
        tk.Label(course_form, text="Course Name").pack()
        course_name = tk.Entry(course_form)
        course_name.pack()
        
        tk.Label(course_form, text="Course Code").pack()
        course_code = tk.Entry(course_form)
        course_code.pack()
        
        tk.Label(course_form, text="Final Weightage in Percentage").pack()
        final_weightage = tk.Entry(course_form)
        final_weightage.pack()
        
        tk.Label(course_form, text="Amount of Assignments").pack()
        num_of_assignments = tk.Entry(course_form)
        num_of_assignments.pack()
        
        tk.Label(course_form, text="Amount of Coursework Exams").pack()
        num_of_coursework_exams = tk.Entry(course_form)
        num_of_coursework_exams.pack()
        
        tk.Button(course_form, text="Next", command=lambda:self.submit_data(
            course_form = course_form,
            course_name=str(course_name.get()), 
            course_code=str(course_code.get()), 
            final_weightage=float(final_weightage.get()),
            num_of_assignments=int(num_of_assignments.get()),
            num_of_coursework_exams=int(num_of_coursework_exams.get()))).pack()
        
        tk.Button(course_form, text="Cancel", command=lambda: course_form.destroy()).pack()
        
    def submit_data(self, course_form, course_name, course_code, final_weightage, num_of_assignments, num_of_coursework_exams):
        self.create_course(course_name, course_code, final_weightage, num_of_assignments, num_of_coursework_exams)
        course_form.destroy()
        
    def create_course(self, course_name, course_code, final_weightage, num_of_assignments, num_of_coursework_exams):
        assignments = self.create_assignments(num_of_assignments)
        coursework_exams = self.create_coursework_exams(num_of_coursework_exams)
        
        if final_weightage > 1:
            final_weightage = final_weightage / 100
        
        self.courses[course_code] = {
            "name": course_name,
            "course_code": course_code,
            "final_weightage": final_weightage,
            "assignments": assignments,
            "coursework_exams": coursework_exams
        }
        
        course_form = tk.Toplevel(self)
        course_form.title("Course Information")
        course_form.grab_set()
        
        assignment_weightages = []
        coursework_exam_weightages = []
        
        for i in range(1, num_of_assignments+1):
            tk.Label(course_form, text="How much percent of your final grade is Assignment "+ str(i) +" worth?").pack()
            weightage = tk.Entry(course_form)
            weightage.pack()
            
            assignment_weightages.append(weightage)
        
        for i in range(1, num_of_coursework_exams+1):
            tk.Label(course_form, text="How much percent of your final grade is Coursework Exam "+ str(i) +" worth?").pack()
            weightage = tk.Entry(course_form)
            weightage.pack()
            
            coursework_exam_weightages.append(weightage)
            
        def end_form():
            for i in range(1, num_of_assignments+1):
                weightage = float(assignment_weightages[i-1].get())
                if weightage > 1:
                    weightage = weightage / 100
                    
                self.courses[course_code]["assignments"]["assignment_"+str(i)]["weightage"] = weightage
            
            for i in range(1,num_of_coursework_exams+1):
                weightage = float(coursework_exam_weightages[i-1].get())
                if weightage > 1:
                    weightage = weightage / 100
                    
                self.courses[course_code]["coursework_exams"]["coursework_exam_" + str(i)]["weightage"] = weightage
                
            course_form.destroy()
            
        tk.Button(course_form, text="Submit", command=end_form).pack()
        
    def create_assignments(self, num_of_assignments):
        assignments = {}
    
        for i in range(1,num_of_assignments+1):
            assignments["assignment_" + str(i)] = {
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.0     
            }
            
        return assignments
        
    def create_coursework_exams(self, num_of_coursework_exams):
        coursework_exams = {}
    
        for i in range(1,num_of_coursework_exams+1):
            coursework_exams["coursework_exam_" + str(i)] = {
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.0     
            }
            
        return coursework_exams      

    def export_courses_as_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)

        # Write headers
        writer.writerow(["Course Code", "Course Name", "Final Weightage", "Component Type", "Component Name", "Status", "Score", "Weightage"])

        # Write course data
        for course_code, data in self.courses.items():
            course_name = data["name"]
            final_weightage = data["final_weightage"]

            # Assignments
            for key, assignment in data["assignments"].items():
                writer.writerow([course_code, course_name, final_weightage, "Assignment", key,
                                assignment["status"], assignment["score"], assignment["weightage"]])

            # Coursework Exams
            for key, exam in data["coursework_exams"].items():
                writer.writerow([course_code, course_name, final_weightage, "Coursework Exam", key,
                                exam["status"], exam["score"], exam["weightage"]])

        print(output.getvalue())
        output.close()
    
        
class TertiaryGPATracker(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Tertiary GPA Tracker").pack()
        tk.Button(self, text="Home", command=lambda:controller.open_page("HomePage")).pack()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()

        