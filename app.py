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
        tk.Button(self, text="Add Course", command=self.create_course_form_part1).pack()
        tk.Button(self, text="Print Courses as CSV", command=self.export_courses_as_csv).pack()
        
    def create_course_form_part1(self):
        #creating the frame form to enter the data for the new course
        form = tk.Toplevel(self)
        form.title("Course Information")
        form.grab_set()
        
        #adding labels and input fields for the info needed for each course
        tk.Label(form, text="Course Name").pack()
        course_name = tk.Entry(form)
        course_name.pack()
        
        tk.Label(form, text="Course Code").pack()
        course_code = tk.Entry(form)
        course_code.pack()
        
        tk.Label(form, text="Final Weightage in Percentage").pack()
        final_weightage = tk.Entry(form)
        final_weightage.pack()
        
        tk.Label(form, text="Amount of Assignments").pack()
        num_of_assignments = tk.Entry(form)
        num_of_assignments.pack()
        
        tk.Label(form, text="Amount of Coursework Exams").pack()
        num_of_coursework_exams = tk.Entry(form)
        num_of_coursework_exams.pack()
        
        def next_form():
            if float(final_weightage.get()) > 1:
                final_weightage_accurate_float_value = float(final_weightage.get()) / 100
                
            self.create_course_form_part2(str(course_name.get()), str(course_code.get()), final_weightage_accurate_float_value, int(num_of_assignments.get()), int(num_of_coursework_exams.get()))
            form.destroy()
        
        tk.Button(form, text="Next", command=next_form).pack()
        tk.Button(form, text="Cancel", command=form.destroy).pack()
        
    def create_course_form_part2(self, course_name, course_code, final_weightage, num_of_assignments, num_of_coursework_exams):
        #creating the form to enter the values and store them in variables
        form = tk.Toplevel(self)
        form.title("Course Information")
        form.grab_set()
        
        assignment_weightages = []
        coursework_exam_weightages = []
        
        for i in range(1, num_of_assignments+1):
            tk.Label(form, text="How much percent of your final grade is Assignment "+ str(i) +" worth?").pack()
            weightage = tk.Entry(form)
            weightage.pack()
            
            assignment_weightages.append(weightage)
        
        for i in range(1, num_of_coursework_exams+1):
            tk.Label(form, text="How much percent of your final grade is Coursework Exam "+ str(i) +" worth?").pack()
            weightage = tk.Entry(form)
            weightage.pack()
            
            coursework_exam_weightages.append(weightage)
            
        #populating all the assignments and coursework exams of the created course with their relevant weightage values 
        def submit_form():
            #initializing all the assignments dictionary for later updates
            def init_assignments(num_of_assignments):
                assignments = {}
            
                for i in range(1,num_of_assignments+1):
                    assignments["assignment_" + str(i)] = {
                        "status": "WAITING",
                        "score": 0.0,
                        "weightage": 0.0     
                    }
                    
                return assignments
            
            #initializing all the coursework exams dictionary for later updates
            def init_coursework_exams(num_of_coursework_exams):
                coursework_exams = {}
            
                for i in range(1,num_of_coursework_exams+1):
                    coursework_exams["coursework_exam_" + str(i)] = {
                        "status": "WAITING",
                        "score": 0.0,
                        "weightage": 0.0     
                    }
                    
                return coursework_exams    

             # initializing variables to use in populating the dictionaries
            assignments = init_assignments(num_of_assignments)
            coursework_exams = init_coursework_exams(num_of_coursework_exams)
            
            #using variables to populate dictionaries
            self.courses[course_code] = {
                "name": course_name,
                "course_code": course_code,
                "final_weightage": final_weightage,
                "assignments": assignments,
                "coursework_exams": coursework_exams,
                "goal": 0.5
            }
            
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
                
            form.destroy()
            
        #adding to buttons at the end of the form to submit values or exit the form altogether    
        tk.Button(form, text="Submit", command=submit_form).pack()
        tk.Button(form, text="Cancel", command=form.destroy).pack()  
           
class TertiaryGPATracker(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Tertiary GPA Tracker").pack()
        tk.Button(self, text="Home", command=lambda:controller.open_page("HomePage")).pack()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()

        