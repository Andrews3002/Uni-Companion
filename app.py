import tkinter as tk
import customtkinter as ctk
from PIL import Image

class Button(ctk.CTkButton):
    def __init__(self, parent, **variants):
        defaults = {          
        }
        defaults.update(variants)
        super().__init__(parent, **defaults)
        
class Frame(ctk.CTkFrame):
    def __init__(self, parent, **variants):
        defaults = {
            "fg_color" : "transparent"
        }
        defaults.update(variants)
        super().__init__(parent, **defaults)
        
class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, **variants):
        defaults = {
            "fg_color" : "transparent"
        }
        defaults.update(variants)
        super().__init__(parent, **defaults)
        
class Label(ctk.CTkLabel):
    def __init__(self, parent, **variants):
        defaults = {
            "fg_color" : "transparent"
        }
        defaults.update(variants)
        super().__init__(parent, **defaults)
        
class TopLevel(ctk.CTkToplevel):
    def __init__(self, parent, **variants):
        defaults = {
        }
        defaults.update(variants)
        super().__init__(parent, **defaults) 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Uni Companion')
        self.after(10, lambda: self.state('zoomed'))
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("mytheme.json")
        
        self.content_container = Frame(self)
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

class HomePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        home_wallpaper = ctk.CTkImage(
            light_image = Image.open("images/HomeWallpaper.jpg"),
            dark_image = Image.open("images/HomeWallpaper.jpg"),
            size = (1920, 1080)
        )
        
        body = Label(
            self,
            image = home_wallpaper,
            text = ""
        )
        body.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 1
        )
        
        main_frame = Frame(
            body,
            fg_color = "#242323"
        )
        main_frame.place(
            relx = 0.25,
            rely = 0.25,
            relwidth = 0.5,
            relheight = 0.5
        )
        
        main_label_frame = Frame(main_frame)
        main_label_frame.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 0.3
        )
        
        main_label = Label(
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
        
        main_buttons_frame = Frame(main_frame)
        main_buttons_frame.place(
            relx = 0,
            rely = 0.3,
            relwidth = 1,
            relheight = 0.7
        )
        
        midterm_performance_tracker_button = Button(
            main_buttons_frame,
            text = "Midterm Performance Tracker",
            font = ("Impact", 20),
            command = lambda: controller.open_page("MidtermPerformanceTracker") 
        )
        midterm_performance_tracker_button.place(
            relx = 0.2,
            rely = 0.25,
            relwidth = 0.6,
            relheight = 0.15
        )
        
        tertiary_gpa_tracker_button = Button(
            main_buttons_frame, 
            text = "Tertiary GPA Tracker", 
            font = ("Impact", 20),
            command = lambda: controller.open_page("TertiaryGPATracker")
        )
        tertiary_gpa_tracker_button.place(
            relx = 0.2,
            rely = 0.6,
            relwidth = 0.6,
            relheight = 0.15
        )
        
# Midterm Performance Tracker App
class MidtermPerformanceTracker(Frame):
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
    
    def refresh_ui(self, selectedCourse = None):
        #going through each widget that is a child of this widget in this case this widget is("self" which is "MidtermPerformanceTracker(Frame)")
        for widget in self.winfo_children():
            widget.destroy()
            
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
            
        def remove_course(course):
                self.courses.pop(str(course["id"]), None)
                self.refresh_ui()
            
        toolbar_frame = Frame(
            self,
            fg_color = "#242323"
        )
        toolbar_frame.place(
            relx = 0,
            rely = 0,
            relwidth = 0.2,
            relheight = 1
        )
        
        toolbarLogo_frame = Frame(toolbar_frame)
        toolbarLogo_frame.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 0.3
        )
        
        logo = ctk.CTkImage(
            light_image = Image.open("images/Logo.png"),
            dark_image = Image.open("images/Logo.png"),
            size = (400, 400)
        )
        
        toolbarLogo_label = Label(
            toolbarLogo_frame,
            text="",
            image = logo
        )
        toolbarLogo_label.pack(
            fill="both",
            expand="true"
        )
        
        toolbarContent_frame = Frame(toolbar_frame)
        toolbarContent_frame.place(
            relx = 0,
            rely = 0.3,
            relwidth = 1,
            relheight = 0.7
        )
        
        home_button = Button(
            toolbarContent_frame, 
            text = "HOME",
            font = ("Impact", 20),
            command = lambda:self.controller.open_page("HomePage"),
            width = 250,
            height = 50
        )
        home_button.pack(
            pady = 30
        )
        
        addCourse_button = Button(
            toolbarContent_frame, 
            text = "ADD COURSE",
            font = ("Impact", 20),
            command = self.create_course_form_part1,
            width = 250,
            height = 50
        )
        addCourse_button.pack(
            pady = 30
        )
        
        trackGoal_button = Button(
            toolbarContent_frame, 
            text = "TRACK GOAL",
            font = ("Impact", 20),
            state = "disabled",
            width = 250,
            height = 50
        )
        trackGoal_button.pack(
            pady = 30
        )
        
        removeCourse_button = Button(
            toolbarContent_frame,
            text = "REMOVE COURSE",
            font = ("Impact", 20),
            state = "disabled",
            width = 250,
            height = 50
        )
        removeCourse_button.pack(
            pady = 30
        )
        
        if selectedCourse:
            trackGoal_button.configure(
                state = "normal",
                command = lambda: open_goal_tracker_page(selectedCourse)
            )
            
            removeCourse_button.configure(
                state = "normal",
                command = lambda: remove_course(selectedCourse)
            )
        
        coursesList_frame = ScrollableFrame(
            self,
            fg_color = "#18016b"
        )
        coursesList_frame.place(
            relx = 0.2,
            rely = 0,
            relwidth = 0.8,
            relheight = 1
        )
        
        def unselectCourse(event):
            self.refresh_ui(selectedCourse = None)
        
        coursesList_frame.bind(
            "<Button-1>",
            unselectCourse
        )
          
        for course in self.courses.values():
            def update_score(assessment):                    
                form = ctk.CTkToplevel(self)
                form.title("Update Score")
                form.transient(self)
                if form.winfo_exists():
                    form.grab_set()
                    form.focus()
                    form.attributes("-topmost", True)
                
                Label(
                    form, 
                    text = "give how much you scored in the assessment",
                    font = ("Impact", 20)
                ).pack()
                
                numerator = ctk.CTkEntry(form)
                numerator.pack()
                
                Label(
                    form, 
                    text = "give total marks the assessment was out of",
                    font = ("Impact", 20)
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
                    
                Button(
                    form, 
                    text = "Update",
                    font = ("Impact", 20),
                    command = lambda:change_score(int(numerator.get()), int(denominator.get()))
                ).pack()
                
                Button(
                    form, 
                    text = "Cancel",
                    font = ("Impact", 20),
                    command = form.destroy
                ).pack()
                
            def reset_score(assessment):
                assessment["score"] = 0.0
                assessment["status"] = "WAITING"
                self.refresh_ui()
            
            if selectedCourse and selectedCourse == course:
                course_frame = Frame(
                    coursesList_frame,
                    border_width = 3,
                    border_color = "#f5007a",
                    fg_color = "#242323",
                    height = 270,
                    width = 1400,
                    corner_radius = 30
                )
            else:
                course_frame = Frame(
                    coursesList_frame,
                    border_width = 2,
                    border_color = "black",
                    fg_color = "#242424",
                    height = 270,
                    width = 1400,
                    corner_radius = 20
                )
            course_frame.pack(
                pady = 50,
            )
    
            def selectCourse_Handler(course):
                def selectCourse(event):
                    self.refresh_ui(selectedCourse = course)
                return selectCourse
            
            course_frame.bind(
                "<Button-1>", 
                selectCourse_Handler(course)
            )
        
            courseName_frame = Frame(
                course_frame
            )
            courseName_frame.place(
                relx = 0.005,
                rely = 0.05,
                relwidth = 0.99,
                relheight = 0.2
            )
            
            courseName_frame.bind(
                "<Button-1>", 
                selectCourse_Handler(course)
            )
            
            courseName_label = Label(
                courseName_frame,
                font = ("Impact", 40),
                text = str(course["name"])
            )
            courseName_label.pack()
            
            courseNameButtonBorder_frame = Frame(
                courseName_frame,
                height = 3,
                fg_color = "black"
            )
            courseNameButtonBorder_frame.pack(
                fill="x"
            )
            
            courseName_label.bind(
                "<Button-1>", 
                selectCourse_Handler(course)
            )
            
            coursePerformance_frame = Frame(
                course_frame
            )
            coursePerformance_frame.place(
                relx = 0.005,
                rely = 0.25,
                relwidth = 0.99,
                relheight = 0.71
            )
            
            coursePerformance_frame.bind(
                "<Button-1>", 
                selectCourse_Handler(course)
            )
            
            coursePerformance_centeringFrame = Frame(coursePerformance_frame)
            coursePerformance_centeringFrame.pack(
                expand = True
            )
            
            for assignment in course["assignments"].values():
                
                assignment_frame = Frame(
                    coursePerformance_centeringFrame,
                    width = 200,
                    height = 170,
                    # border_width = 5,
                    # border_color = "black",
                    corner_radius = 10
                )
                assignment_frame.pack(
                    side = "left",
                    padx = 10,
                    pady = 10
                )
                
                if selectedCourse and selectedCourse == course:
                    assignmentTitle_frame = Frame(assignment_frame)
                    assignmentTitle_frame.place(
                        relx = 0.1,
                        rely = 0,
                        relwidth = 0.8,
                        relheight = 0.3
                    )
                    
                    assignmentTitle_centeringFrame = Frame(assignmentTitle_frame)
                    assignmentTitle_centeringFrame.pack(expand = True)
                    
                    assignment_title_Label = Label(
                        assignmentTitle_centeringFrame,
                        font = ("Impact", 20),
                        text = str(assignment["name"])
                    )
                    assignment_title_Label.pack()
                
                    assignmentScore_frame = Frame(assignment_frame)
                    assignmentScore_frame.place(
                        relx = 0.1,
                        rely = 0.3,
                        relwidth = 0.8,
                        relheight = 0.7,
                    )
                    
                    assignmentScore_centeringFrame = Frame(assignmentScore_frame)
                    assignmentScore_centeringFrame.pack(expand = True)
                
                    score = Label(
                        assignmentScore_centeringFrame,
                        font = ("Impact", 20),
                        text = str(
                            round(
                                ((assignment["score"]/assignment["weightage"])*100),
                                1
                            )
                        )+"%"
                    )
                    score.pack()
                    
                    update_button = Button(
                        assignmentScore_centeringFrame, 
                        text = "Update",
                        font = ("Impact", 20), 
                        command = lambda assignment = assignment: update_score(assignment)
                    )
                    update_button.pack(
                        pady = 5
                    )
                    
                    reset_button = Button(
                        assignmentScore_centeringFrame,
                        text = "Reset",
                        font = ("Impact", 20),
                        command = lambda assignment = assignment: reset_score(assignment)
                    )
                    reset_button.pack()
                else:
                    assignmentTitle_frame = Frame(assignment_frame)
                    assignmentTitle_frame.place(
                        relx = 0.1,
                        rely = 0,
                        relwidth = 0.8,
                        relheight = 0.3
                    )
                    
                    assignmentTitle_centeringFrame = Frame(assignmentTitle_frame)
                    assignmentTitle_centeringFrame.pack(expand = True)
                    
                    assignment_title_Label = Label(
                        assignmentTitle_centeringFrame, 
                        text = str(assignment["name"]),
                        font = ("Impact", 20)
                    )
                    assignment_title_Label.pack()
                
                    assignmentScore_frame = Frame(assignment_frame)
                    assignmentScore_frame.place(
                        relx = 0.1,
                        rely = 0.3,
                        relwidth = 0.8,
                        relheight = 0.7,
                    )
                    
                    assignmentScore_centeringFrame = Frame(assignmentScore_frame)
                    assignmentScore_centeringFrame.pack(expand = True)
                
                    score = Label(
                        assignmentScore_centeringFrame, 
                        text = str(
                            round(
                                ((assignment["score"]/assignment["weightage"])*100),
                                1
                            )
                        )+"%",
                        font = ("Impact", 20)
                    )
                    score.pack()
            
            for coursework in course["coursework_exams"].values():
                coursework_frame = Frame(
                    coursePerformance_centeringFrame,
                    width = 200,
                    height = 170,
                    # border_width = 5,
                    # border_color = "black",
                    corner_radius = 10
                )
                coursework_frame.pack(
                    side = "left",
                    padx = 10,
                    pady = 10
                )
                
                if selectedCourse and selectedCourse == course:
                    courseworkTitle_frame = Frame(coursework_frame)
                    courseworkTitle_frame.place(
                        relx = 0.1,
                        rely = 0,
                        relwidth = 0.8,
                        relheight = 0.3
                    )
                    
                    courseworkTitle_centeringFrame = Frame(courseworkTitle_frame)
                    courseworkTitle_centeringFrame.pack(expand = True)
                    
                    courseworkTitle_label = Label(
                        courseworkTitle_centeringFrame, 
                        text = str(coursework["name"]),
                        font = ("Impact", 20),
                    )
                    courseworkTitle_label.pack()
                    
                    courseworkScore_frame = Frame(coursework_frame)
                    courseworkScore_frame.place(
                        relx = 0.1,
                        rely = 0.3,
                        relwidth = 0.8,
                        relheight = 0.7
                    )
                    
                    courseworkScore_centeringFrame = Frame(courseworkScore_frame)
                    courseworkScore_centeringFrame.pack(expand = True)
                
                    score_label = Label(
                        courseworkScore_centeringFrame, 
                        text = str(
                            round(
                                ((coursework["score"]/coursework["weightage"])*100),
                                1
                            )
                        )+"%",
                        font = ("Impact", 20)
                    )
                    score_label.pack()
                
                    update_button = Button(
                        courseworkScore_centeringFrame, 
                        text = "Update",
                        font = ("Impact", 20),
                        command = lambda coursework = coursework: update_score(coursework)
                    )
                    update_button.pack(
                        pady = 5
                    )
                
                    reset_button = Button(
                        courseworkScore_centeringFrame,
                        text = "Reset",
                        font = ("Impact", 20),
                        command = lambda coursework = coursework: reset_score(coursework)
                    )
                    reset_button.pack()
                else:
                    courseworkTitle_frame = Frame(coursework_frame)
                    courseworkTitle_frame.place(
                        relx = 0.1,
                        rely = 0,
                        relwidth = 0.8,
                        relheight = 0.3
                    )
                    
                    courseworkTitle_centeringFrame = Frame(courseworkTitle_frame)
                    courseworkTitle_centeringFrame.pack(expand = True)
                    
                    courseworkTitle_label = Label(
                        courseworkTitle_centeringFrame, 
                        text = str(coursework["name"]),
                        font = ("Impact", 20)
                    )
                    courseworkTitle_label.pack()
                    
                    courseworkScore_frame = Frame(coursework_frame)
                    courseworkScore_frame.place(
                        relx = 0.1,
                        rely = 0.3,
                        relwidth = 0.8,
                        relheight = 0.7
                    )
                    
                    courseworkScore_centeringFrame = Frame(courseworkScore_frame)
                    courseworkScore_centeringFrame.pack(expand = True)
                
                    score_label = Label(
                        courseworkScore_centeringFrame, 
                        text = str(
                            round(
                                ((coursework["score"]/coursework["weightage"])*100),
                                1
                            )
                        )+"%",
                        font = ("Impact", 20)
                    )
                    score_label.pack()
        
    def create_course_form_part1(self):
        #creating the CTkFrame form to enter the data for the new course
        form = ctk.CTkToplevel(self)
        form.title("Course Information")
        form.transient(self)
        if form.winfo_exists():
            form.grab_set()
            form.focus()
            form.attributes("-topmost", True)
        
        #adding labels and input fields for the info needed for each course
        Label(
            form, 
            text = "Course Name",
            font = ("Impact", 20)
        ).pack()
        course_name = ctk.CTkEntry(form)
        course_name.pack()
        
        Label(
            form, 
            text = "Course ID",
            font = ("Impact", 20)
        ).pack()
        course_id = ctk.CTkEntry(form)
        course_id.pack()
        
        Label(
            form, 
            text = "How much percent is your final out of?",
            font = ("Impact", 20)
        ).pack()
        final_weightage = ctk.CTkEntry(form)
        final_weightage.pack()
        
        Label(
            form, 
            text = "Amount of Assignments",
            font = ("Impact", 20)
        ).pack()
        num_of_assignments = ctk.CTkEntry(form)
        num_of_assignments.pack()
        
        Label(
            form, 
            text = "Amount of Coursework Exams",
            font = ("Impact", 20)
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
        
        Button(
            form, 
            text = "Next",
            font = ("Impact", 20),
            command = next_form
        ).pack()
        
        Button(
            form, 
            text = "Cancel",
            font = ("Impact", 20),
            command = form.destroy
        ).pack()
        
    def create_course_form_part2(self, course_name, course_id, final_weightage, num_of_assignments, num_of_coursework_exams):
        #creating the form to enter the values and store them in variables
        form = ctk.CTkToplevel(self)
        form.title("Course Information")
        form.transient(self)
        if form.winfo_exists():
            form.grab_set()
            form.focus()
            form.attributes("-topmost", True)
        
        scrollable_area = ScrollableFrame(form)
        scrollable_area.pack(
            fill = "both",
            expand = "true"
        )
        
        assignment_weightages = []
        coursework_exam_weightages = []
        
        for i in range(1, num_of_assignments+1):
            Label(
                scrollable_area, 
                text = "How much percent of your final grade is Assignment "+ str(i) +" worth?",
                font = ("Impact", 20)
            ).pack()
            weightage = ctk.CTkEntry(scrollable_area)
            weightage.pack()
            
            assignment_weightages.append(weightage)
        
        for i in range(1, num_of_coursework_exams+1):
            Label(
                scrollable_area, 
                text = "How much percent of your final grade is Coursework Exam "+ str(i) +" worth?",
                font = ("Impact", 20)
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
        Button(
            scrollable_area, 
            text = "Submit",
            font = ("Impact", 20),
            command = submit_form
        ).pack()
        
        Button(
            scrollable_area, 
            text = "Cancel",
            font = ("Impact", 20),
            command = form.destroy
        ).pack()  

class GoalTrackerPage(Frame):
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
            if form.winfo_exists():
                form.grab_set()
                form.focus()
                form.attributes("-topmost", True)
            
            Label(
                form,
                text = "What is the overall Percentage Goal you would like to achieve in this course?",
                font = ("Impact", 20)
            ).pack()
            
            input_div = Frame(form)
            input_div.pack()
            
            input_field = ctk.CTkEntry(input_div)
            input_field.pack(side = "left")
            
            percent_sign = Label(
                input_div,
                text = "%",
                font = ("Impact", 20)
            )
            percent_sign.pack(side = "left")
            
            Button(
                form,
                text = "Enter",
                font = ("Impact", 20),
                command = update_goal_value
            ).pack()
            
            Button(
                form,
                text = "Cancel",
                font = ("Impact", 20),
                command = form.destroy
            ).pack()
        
        Label(
            self, 
            text = str(self.course["name"]),
            font = ("Impact", 20)
        ).pack()
        
        Label(
            self, 
            text = "Your goal for this course is to get "+str(self.course["goal"]*100)+"%",
            font = ("Impact", 20)
        ).pack()
        
        Button(
            self, 
            text = "Edit Goal",
            font = ("Impact", 20),
            command = edit_goal
        ).pack()
        
        Button(
            self, 
            text = "Back",
            font = ("Impact", 20),
            command = lambda:self.controller.open_page("MidtermPerformanceTracker")
        ).pack()
        
        goal = self.course["goal"]*100
        score_sum = 0
        goal_remainder = goal
        
        total = 100
        weightage_sum = 0
        total_remainder = total
        
        required_score_sum = 0
        
        assessments_div = Frame(self)
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
                
                assessment_div = Frame(
                    assessments_div
                )
                assessment_div.pack()
        
                Label(
                    assessment_div, 
                    text = assignment["name"]+": To attain your goal you need to get at least "+str(required_score)+"/"+str(weightage),
                    font = ("Impact", 20)
                ).pack()
            
            else:
                required_score_sum += assignment["score"]*100
                assessment_div = Frame(assessments_div)
                assessment_div.pack()
                
                Label(
                    assessment_div, 
                    text = assignment["name"]+": GRADED",
                    font = ("Impact", 20)
                ).pack()
            
        for coursework_exam in self.course["coursework_exams"].values():
            score = coursework_exam["score"]*100
            weightage = round((coursework_exam["weightage"]*100), 1)
            
            if coursework_exam["status"] == "WAITING":
                required_score = round(((weightage/total_remainder)*goal_remainder), 1)
                required_score_sum += required_score
                
                assessment_div = Frame(assessments_div)
                assessment_div.pack()
        
                Label(
                    assessment_div, 
                    text = coursework_exam["name"]+": To attain your goal you need to get at least "+str(required_score)+"/"+str(weightage),
                    font = ("Impact", 20)
                ).pack()
            
            else:
                required_score_sum += coursework_exam["score"]*100
                
                assessment_div = Frame(assessments_div)
                assessment_div.pack()
                
                Label(
                    assessment_div, 
                    text = coursework_exam["name"]+": GRADED",
                    font = ("Impact", 20)
                ).pack()
                
        required_score = round((goal - required_score_sum), 1)
        
        assessment_div = Frame(assessments_div)
        assessment_div.pack()
        
        Label(
            assessment_div, 
            text = "Final: To attain your goal you need to get at least "+str(required_score)+"/"+str(self.course["final_weightage"]*100),
            font = ("Impact", 20)
        ).pack()            

# Tertiary GPA Tracker App
class TertiaryGPATracker(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        Label(
            self, 
            text = "Tertiary GPA Tracker",
            font = ("Impact", 20)
        ).pack()
        
        Button(
            self, 
            text = "Home",
            font = ("Impact", 20),
            command = lambda:controller.open_page("HomePage")
        ).pack()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()