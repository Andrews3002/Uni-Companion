import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Uni Companion')
        self.after(10, lambda: self.state('zoomed'))
        
        #courses page change 2
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.content_container = ctk.CTkFrame(self)
        self.content_container.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 1
        )
        
        self.pages = {}
        
        for ClassPage in (HomePage, MidtermPerformanceTracker, TertiaryGPATracker):
            page = ClassPage(
                parent = self.content_container, 
                controller = self
            )
            
            page.place(
                relx = 0,
                rely = 0,
                relwidth = 1, #100% width of the parent
                relheight = 1 #100% height of the parent
            )
            
            self.pages[ClassPage.__name__] = page
            
        self.open_page("HomePage")
        
    def open_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        home_wallpaper = ctk.CTkImage(
            light_image = Image.open("images/HomeWallpaper.jpg"),
            dark_image = Image.open("images/HomeWallpaper.jpg"),
            size = (1920, 1080)
        )
        
        body = ctk.CTkLabel(
            self,
            image = home_wallpaper,
            text = ""
        )
        body.pack(
            fill = "both",
            expand = "true"
        )
        
        main_frame = ctk.CTkFrame(
            body,
            # fg_color = "#f25a27",
            corner_radius = 50
        )
        main_frame.place(
            relx = 0.25,
            rely = 0.25,
            relwidth = 0.5,
            relheight = 0.5
        )
        
        main_label_frame = ctk.CTkFrame(
            main_frame,
            fg_color = "transparent",
            corner_radius = 0
        )
        main_label_frame.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 0.3
        )
        
        main_label = ctk.CTkLabel(
            main_label_frame, 
            text = "Welcome to the Uni Companion App\nSelect your desired tool",
            font = ("Impact", 40, "bold")
        )
        
        
        main_label.place(
            relx = 0,
            rely = 0.2,
            relwidth = 1,
            relheight = 0.6
        )
        
        main_buttons_frame = ctk.CTkFrame(
            main_frame,
            fg_color = "transparent",
            corner_radius = 0
        )
        main_buttons_frame.place(
            relx = 0,
            rely = 0.3,
            relwidth = 1,
            relheight = 0.7
        )
        
        midterm_performance_tracker_button = ctk.CTkButton(
            main_buttons_frame,
            text = "Midterm Performance Tracker",
            font = ("Impact", 20),
            corner_radius = 40,
            command = lambda: controller.open_page("MidtermPerformanceTracker") 
        )
        midterm_performance_tracker_button.place(
            relx = 0.2,
            rely = 0.25,
            relwidth = 0.6,
            relheight = 0.15
        )
        
        tertiary_gpa_tracker_button = ctk.CTkButton(
            main_buttons_frame, 
            text = "Tertiary GPA Tracker", 
            font = ("Impact", 20),
            corner_radius = 40,
            command = lambda: controller.open_page("TertiaryGPATracker")
        )
        tertiary_gpa_tracker_button.place(
            relx = 0.2,
            rely = 0.6,
            relwidth = 0.6,
            relheight = 0.15
        )
        
# Midterm Performance Tracker App
class MidtermPerformanceTracker(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.courses = {}
        
        if self.courses == {}:
            assignments = {}
            coursework_exams = {}
            
            assignments["assignment_1"] = {
                "name": "assignment 1",
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.06     
            }
            
            assignments["assignment_2"] = {
                "name": "assignment 2",
                "status": "WAITING",
                "score": 0.00,
                "weightage": 0.07     
            }
            
            assignments["assignment_3"] = {
                "name": "assignment 3",
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.07     
            }
                    
            coursework_exams["coursework_exam_1"] = {
                "name": "coursework exam 1",
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.15     
            }
            
            coursework_exams["coursework_exam_2"] = {
                "name": "coursework exam 2",
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.15     
            }
            
            self.courses["MATH101"] = {
                "name": "Mathematics",
                "id": "MATH101",
                "final_weightage": 0.5,
                "assignments": assignments,
                "coursework_exams": coursework_exams,
                "goal": 0.5
            }
        
        self.refresh_ui()
    
    def refresh_ui(self):
        #going through each widget that is a child of this widget in this case this widget is("self" which is "MidtermPerformanceTracker(ctk.CTkFrame)")
        for widget in self.winfo_children():
            widget.destroy()
            
        scrollable_area = ctk.CTkScrollableFrame(self)
        scrollable_area.pack(
            fill = "both",
            expand = "true"
        )
        
        ctk.CTkLabel(
            scrollable_area, 
            text = "Midterm Performance Tracker"
        ).pack()
        
        ctk.CTkButton(
            scrollable_area, 
            text = "Home", 
            command = lambda:self.controller.open_page("HomePage")
        ).pack()
        
        ctk.CTkButton(
            scrollable_area, 
            text = "Add Course", 
            command = self.create_course_form_part1
        ).pack()
        
        added_courses_div = ctk.CTkFrame(scrollable_area)
        added_courses_div.pack(fill = "x")
          
        for course in self.courses.values():
            def open_goal_tracker_page(course):
                page = GoalTrackerPage(
                    parent = self.parent, 
                    course = course, 
                    controller = self.controller
                )
                page.grid(
                    row = 0, 
                    column = 0, 
                    sticky = "nsew"
                )
                page.tkraise()
                
            def update_score(assessment):                    
                form = ctk.CTkToplevel(self)
                form.title("Update Score")
                form.transient(self)
                form.grab_set()
                form.focus()
                form.attributes("-topmost", True)
                
                ctk.CTkLabel(
                    form, 
                    text = "give how much you scored in the assessment"
                ).pack()
                
                numerator = ctk.CTkEntry(form)
                numerator.pack()
                
                ctk.CTkLabel(
                    form, 
                    text = "give total marks the assessment was out of"
                ).pack()
                
                denominator = ctk.CTkEntry(form)
                denominator.pack()
                
                def change_score(numerator, denominator):
                    score = numerator/denominator
                    score = score * assessment["weightage"]
                    assessment["score"] = score
                    assessment["status"] = "GRADED"
                    form.destroy()
                    self.refresh_ui()
                    
                ctk.CTkButton(
                    form, 
                    text = "Update", 
                    command = lambda:change_score(int(numerator.get()), int(denominator.get()))
                ).pack()
                
                ctk.CTkButton(
                    form, 
                    text = "Cancel", 
                    command = form.destroy
                ).pack()
                
            def reset_score(assessment):
                assessment["score"] = 0.0
                assessment["status"] = "WAITING"
                self.refresh_ui()
            
            def remove_course(course):
                self.courses.pop(str(course["id"]), None)
                self.refresh_ui()
            
            course_div = ctk.CTkFrame(added_courses_div)
            course_div.pack()
        
            course_title_div = ctk.CTkFrame(course_div)
            course_title_div.pack()
            
            ctk.CTkLabel(
                course_title_div,
                text = str(course["name"])
            ).pack(side = "left")
            
            ctk.CTkButton(
                course_title_div, 
                text = "Track Goal", 
                command = lambda course = course:open_goal_tracker_page(course)
            ).pack(side = "left") 
            
            ctk.CTkButton(
                course_title_div,
                text = "REMOVE COURSE",
                command = lambda course = course: remove_course(course)
            ).pack(side = "left")
            
            course_performance_div = ctk.CTkFrame(course_div)
            course_performance_div.pack()
            
            for assignment in course["assignments"].values():
                
                assignment_div = ctk.CTkFrame(course_performance_div)
                assignment_div.pack(side = "left")
                
                assignment_title_div = ctk.CTkFrame(assignment_div)
                assignment_title_div.pack()
                
                ctk.CTkLabel(
                    assignment_title_div, 
                    text = str(assignment["name"])
                ).pack()
                
                assignment_score_div = ctk.CTkFrame(assignment_div)
                assignment_score_div.pack()
                
                score = ctk.CTkLabel(
                    assignment_score_div, 
                    text = str(
                        round(
                            ((assignment["score"]/assignment["weightage"])*100),
                            1
                        )
                    )+"%"
                )
                score.pack()
                
                ctk.CTkButton(
                    assignment_score_div, 
                    text = "Update", 
                    command = lambda assignment = assignment: update_score(assignment)
                ).pack()
                
                ctk.CTkButton(
                    assignment_score_div,
                    text = "Reset",
                    command = lambda assignment = assignment: reset_score(assignment)
                ).pack()
            
            for coursework in course["coursework_exams"].values():
                
                coursework_div = ctk.CTkFrame(course_performance_div)
                coursework_div.pack(side = "left")
                
                coursework_title_div = ctk.CTkFrame(coursework_div)
                coursework_title_div.pack()
                ctk.CTkLabel(
                    coursework_title_div, 
                    text = str(coursework["name"])
                ).pack()
                
                coursework_score_div = ctk.CTkFrame(coursework_div)
                coursework_score_div.pack()
                
                score = ctk.CTkLabel(
                    coursework_score_div, 
                    text = str(
                        round(
                            ((coursework["score"]/coursework["weightage"])*100),
                            1
                        )
                    )+"%"
                )
                score.pack()
                
                ctk.CTkButton(
                    coursework_score_div, 
                    text = "Update", 
                    command = lambda coursework = coursework: update_score(coursework)
                ).pack()
                
                ctk.CTkButton(
                    coursework_score_div,
                    text = "Reset",
                    command = lambda coursework = coursework: reset_score(coursework)
                ).pack()
        
    def create_course_form_part1(self):
        #creating the CTkFrame form to enter the data for the new course
        form = ctk.CTkToplevel(self)
        form.title("Course Information")
        form.transient(self)
        form.grab_set()
        form.focus()
        form.attributes("-topmost", True)
        
        #adding labels and input fields for the info needed for each course
        ctk.CTkLabel(
            form, 
            text = "Course Name"
        ).pack()
        course_name = ctk.CTkEntry(form)
        course_name.pack()
        
        ctk.CTkLabel(
            form, 
            text = "Course ID"
        ).pack()
        course_id = ctk.CTkEntry(form)
        course_id.pack()
        
        ctk.CTkLabel(
            form, 
            text = "How much percent is your final out of?"
        ).pack()
        final_weightage = ctk.CTkEntry(form)
        final_weightage.pack()
        
        ctk.CTkLabel(
            form, 
            text = "Amount of Assignments"
        ).pack()
        num_of_assignments = ctk.CTkEntry(form)
        num_of_assignments.pack()
        
        ctk.CTkLabel(
            form, 
            text = "Amount of Coursework Exams"
        ).pack()
        num_of_coursework_exams = ctk.CTkEntry(form)
        num_of_coursework_exams.pack()
        
        def next_form():
            if float(final_weightage.get()) > 1:
                final_weightage_accurate_float_value = float(final_weightage.get()) / 100
                
            self.create_course_form_part2(
                str(course_name.get()), 
                str(course_id.get()), 
                final_weightage_accurate_float_value, 
                int(num_of_assignments.get()), 
                int(num_of_coursework_exams.get())
            )
            form.destroy()
        
        ctk.CTkButton(
            form, 
            text = "Next", 
            command = next_form
        ).pack()
        
        ctk.CTkButton(
            form, 
            text = "Cancel", 
            command = form.destroy
        ).pack()
        
    def create_course_form_part2(self, course_name, course_id, final_weightage, num_of_assignments, num_of_coursework_exams):
        #creating the form to enter the values and store them in variables
        form = ctk.CTkToplevel(self)
        form.title("Course Information")
        form.transient(self)
        form.grab_set()
        form.focus()
        form.attributes("-topmost", True)
        
        scrollable_area = ctk.CTkScrollableFrame(form)
        scrollable_area.pack(
            fill = "both",
            expand = "true"
        )
        
        assignment_weightages = []
        coursework_exam_weightages = []
        
        for i in range(1, num_of_assignments+1):
            ctk.CTkLabel(
                scrollable_area, 
                text = "How much percent of your final grade is Assignment "+ str(i) +" worth?"
            ).pack()
            weightage = ctk.CTkEntry(scrollable_area)
            weightage.pack()
            
            assignment_weightages.append(weightage)
        
        for i in range(1, num_of_coursework_exams+1):
            ctk.CTkLabel(
                scrollable_area, 
                text = "How much percent of your final grade is Coursework Exam "+ str(i) +" worth?"
            ).pack()
            weightage = ctk.CTkEntry(scrollable_area)
            weightage.pack()
            
            coursework_exam_weightages.append(weightage)
            
        #populating all the assignments and coursework exams of the created course with their relevant weightage values 
        def submit_form():
            #initializing all the assignments dictionary for later updates
            def init_assignments(num_of_assignments):
                assignments = {}
            
                for i in range(1,num_of_assignments+1):
                    assignments["assignment_" + str(i)] = {
                        "name": "assignment " + str(i),
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
                        "name": "coursework exam " + str(i),
                        "status": "WAITING",
                        "score": 0.0,
                        "weightage": 0.0     
                    }
                    
                return coursework_exams    

             # initializing variables to use in populating the dictionaries
            assignments = init_assignments(num_of_assignments)
            coursework_exams = init_coursework_exams(num_of_coursework_exams)
            
            #using variables to populate dictionaries
            self.courses[course_id] = {
                "name": course_name,
                "id": course_id,
                "final_weightage": final_weightage,
                "assignments": assignments,
                "coursework_exams": coursework_exams,
                "goal": 0.5
            }
            
            for i in range(1, num_of_assignments+1):
                weightage = float(assignment_weightages[i-1].get())
                if weightage > 1:
                    weightage = weightage / 100
                    
                self.courses[course_id]["assignments"]["assignment_"+str(i)]["weightage"] = weightage
            
            for i in range(1,num_of_coursework_exams+1):
                weightage = float(coursework_exam_weightages[i-1].get())
                if weightage > 1:
                    weightage = weightage / 100
                    
                self.courses[course_id]["coursework_exams"]["coursework_exam_" + str(i)]["weightage"] = weightage
                
            form.destroy()
            
            #updating the main page to always have an up to date list of courses after adding new courses
            self.refresh_ui()
            
        #adding to buttons at the end of the form to submit values or exit the form altogether    
        ctk.CTkButton(
            scrollable_area, 
            text = "Submit", 
            command = submit_form
        ).pack()
        
        ctk.CTkButton(
            scrollable_area, 
            text = "Cancel", 
            command = form.destroy
        ).pack()  

class GoalTrackerPage(ctk.CTkFrame):
    def __init__(self, parent, controller, course):
        super().__init__(parent)
        self.parent = parent
        self.course = course
        self.controller = controller
        self.refresh_gui()
        
    def refresh_gui(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        def edit_goal():
            def update_goal_value():
                goal = int(input_field.get())
                self.course["goal"] = goal/100
                form.destroy()
                self.refresh_gui()
        
            form = ctk.CTkToplevel(self)
            form.title("Edit Goal")
            form.transient(self)
            form.grab_set()
            form.focus()
            form.attributes("-topmost", True)
            
            ctk.CTkLabel(
                form,
                text = "What is the overall Percentage Goal you would like to achieve in this course?"
            ).pack()
            
            input_div = ctk.CTkFrame(form)
            input_div.pack()
            
            input_field = ctk.CTkEntry(input_div)
            input_field.pack(side = "left")
            
            percent_sign = ctk.CTkLabel(
                input_div,
                text = "%"
            )
            percent_sign.pack(side = "left")
            
            ctk.CTkButton(
                form,
                text = "Enter",
                command = update_goal_value
            ).pack()
            
            ctk.CTkButton(
                form,
                text = "Cancel",
                command = form.destroy
            ).pack()
        
        ctk.CTkLabel(
            self, 
            text = str(self.course["name"])
        ).pack()
        
        ctk.CTkLabel(
            self, 
            text = "Your goal for this course is to get "+str(self.course["goal"]*100)+"%"
        ).pack()
        
        ctk.CTkButton(
            self, 
            text = "Edit Goal",
            command = edit_goal
        ).pack()
        
        ctk.CTkButton(
            self, 
            text = "Back", 
            command = lambda:self.controller.open_page("MidtermPerformanceTracker")
        ).pack()
        
        goal = self.course["goal"]*100
        score_sum = 0
        goal_remainder = goal
        
        total = 100
        weightage_sum = 0
        total_remainder = total
        
        required_score_sum = 0
        
        assessments_div = ctk.CTkFrame(self)
        assessments_div.pack()
        
        for assignment in self.course["assignments"].values():
            score = assignment["score"]*100
            weightage = assignment["weightage"]*100
            
            if assignment["status"] == "GRADED":
                score_sum += score
                weightage_sum += weightage
                
        for coursework_exam in self.course["coursework_exams"].values():
            score = coursework_exam["score"]*100
            weightage = coursework_exam["weightage"]*100
            
            if coursework_exam["status"] == "GRADED":
                score_sum += score
                weightage_sum += weightage
        
        total_remainder = total - weightage_sum
        goal_remainder = goal - score_sum
        
        for assignment in self.course["assignments"].values():
            score = assignment["score"]*100
            weightage = round((assignment["weightage"]*100), 1)
            
            if assignment["status"] == "WAITING":
                required_score = round(((weightage/total_remainder)*goal_remainder), 1)
                required_score_sum += required_score
                
                assessment_div = ctk.CTkFrame(
                    assessments_div
                )
                assessment_div.pack()
        
                ctk.CTkLabel(
                    assessment_div, 
                    text = assignment["name"]+": To attain your goal you need to get at least "+str(required_score)+"/"+str(weightage)
                ).pack()
            
            else:
                required_score_sum += assignment["score"]*100
                assessment_div = ctk.CTkFrame(assessments_div)
                assessment_div.pack()
                
                ctk.CTkLabel(
                    assessment_div, 
                    text = assignment["name"]+": GRADED"
                ).pack()
            
        for coursework_exam in self.course["coursework_exams"].values():
            score = coursework_exam["score"]*100
            weightage = round((coursework_exam["weightage"]*100), 1)
            
            if coursework_exam["status"] == "WAITING":
                required_score = round(((weightage/total_remainder)*goal_remainder), 1)
                required_score_sum += required_score
                
                assessment_div = ctk.CTkFrame(assessments_div)
                assessment_div.pack()
        
                ctk.CTkLabel(
                    assessment_div, 
                    text = coursework_exam["name"]+": To attain your goal you need to get at least "+str(required_score)+"/"+str(weightage)
                ).pack()
            
            else:
                required_score_sum += coursework_exam["score"]*100
                
                assessment_div = ctk.CTkFrame(assessments_div)
                assessment_div.pack()
                
                ctk.CTkLabel(
                    assessment_div, 
                    text = coursework_exam["name"]+": GRADED"
                ).pack()
                
        required_score = round((goal - required_score_sum), 1)
        
        assessment_div = ctk.CTkFrame(assessments_div)
        assessment_div.pack()
        
        ctk.CTkLabel(
            assessment_div, 
            text = "Final: To attain your goal you need to get at least "+str(required_score)+"/"+str(self.course["final_weightage"]*100)
        ).pack()            

# Tertiary GPA Tracker App
class TertiaryGPATracker(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        ctk.CTkLabel(
            self, 
            text = "Tertiary GPA Tracker"
        ).pack()
        
        ctk.CTkButton(
            self, 
            text = "Home", 
            command = lambda:controller.open_page("HomePage")
        ).pack()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()