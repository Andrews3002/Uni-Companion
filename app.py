import os
import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import ctypes

# Windows API constants
GWL_STYLE = -16
WS_MAXIMIZEBOX = 0x00010000
WS_THICKFRAME = 0x00040000

def disable_maximize_button(hwnd):
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style &= ~WS_MAXIMIZEBOX  # Disable maximize button
    style &= ~WS_THICKFRAME   # Disable resizing via border
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
    ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0020)

myappid = 'uni-companion.gui.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
        self.state('zoomed')
        
        self.iconbitmap("Logo.ico") 
                        
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
        
        self.update_idletasks()

        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        disable_maximize_button(hwnd)

        self.resizable(False, False)
        
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
            fg_color = "#242222"
        )
        main_frame.place(
            relx = 0.5,
            rely = 0,
            anchor = "n",
            relwidth = 0.4,
            relheight = 1
        )
        
        logo = ctk.CTkImage(
            light_image = Image.open("images/Logo.png"),
            dark_image = Image.open("images/Logo.png"),
            size = (600, 600)
        )
        
        logo_label = Label(
            main_frame, 
            text = "",
            image = logo
        )
        logo_label.place(
            relx = 0.5,
            rely = 0.25,
            anchor = "center",
            relwidth = 1,
            relheight = 0.5
        )
        
        main_buttons_frame = Frame(main_frame)
        main_buttons_frame.place(
            relx = 0.5,
            rely = 0.7,
            anchor = "center",
            relwidth = 1,
            relheight = 0.5
        )
        
        midterm_performance_tracker_button = Button(
            main_buttons_frame,
            text = "Midterm Performance Tracker",
            font = ("Impact", 20),
            command = lambda: controller.open_page("MidtermPerformanceTracker") 
        )
        midterm_performance_tracker_button.place(
            relx = 0.2,
            rely = 0.1,
            relwidth = 0.6,
            relheight = 0.13
        )
        
        tertiary_gpa_tracker_button = Button(
            main_buttons_frame, 
            text = "Tertiary GPA Tracker", 
            font = ("Impact", 20),
            command = lambda: controller.open_page("TertiaryGPATracker")
        )
        tertiary_gpa_tracker_button.place(
            relx = 0.2,
            rely = 0.4,
            relwidth = 0.6,
            relheight = 0.13
        )
        
        def width_resize(event):
            new_width = controller.winfo_width()
            new_size = int(new_width/3.2)
            new_font_size = int(new_width/96)
            
            logo.configure(
                size = (new_size, new_size)
            )
            
            midterm_performance_tracker_button.configure(
                font = ("Impact", new_font_size)
            )
            
            tertiary_gpa_tracker_button.configure(
                font = ("Impact", new_font_size)
            )
            
        self.bind(
            "<Configure>",
            width_resize
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
                "name": "Assignment 1",
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.06     
            }
            
            assignments["assignment_2"] = {
                "name": "Assignment 2",
                "status": "WAITING",
                "score": 0.00,
                "weightage": 0.07     
            }
            
            assignments["assignment_3"] = {
                "name": "Assignment 3",
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.07     
            }
                    
            coursework_exams["coursework_exam_1"] = {
                "name": "Coursework Exam 1",
                "status": "WAITING",
                "score": 0.0,
                "weightage": 0.15     
            }
            
            coursework_exams["coursework_exam_2"] = {
                "name": "Coursework Exam 2",
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
            
        main_width = self.winfo_width()
        main_height = self.winfo_height()

        def open_goal_tracker_page(course):
            page = GoalTrackerPage(
                parent = self.parent, 
                course = course, 
                controller = self.controller
            )
            page.place(
                relx = 0,
                rely = 0,
                relwidth = 1,
                relheight = 1
            )
            page.tkraise()
            
        def remove_course(course):
                self.courses.pop(str(course["id"]), None)
                self.refresh_ui()
            
        toolbar_frame = Frame(
            self,
            fg_color = "#242222"
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
        
        window_width = self.controller.winfo_width()
        new_size = int(window_width/4.8)
        new_font_size = int(window_width/96)
        
        logo = ctk.CTkImage(
            light_image = Image.open("images/Logo.png"),
            dark_image = Image.open("images/Logo.png"),
            size = (new_size, new_size)
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
            command = lambda:self.controller.open_page("HomePage"),
            font = ("Impact", new_font_size)
        )
        home_button.place(
            relx = 0.5,
            rely = 0.1,
            anchor = "center",
            relwidth = 0.7,
            relheight = 0.08
        )
        
        addCourse_button = Button(
            toolbarContent_frame, 
            text = "ADD COURSE",
            font = ("Impact", new_font_size),
            command = self.create_course_form_part1
        )
        addCourse_button.place(
            relx = 0.5,
            rely = 0.3,
            anchor = "center",
            relwidth = 0.7,
            relheight = 0.08
        )
        
        trackGoal_button = Button(
            toolbarContent_frame, 
            text = "TRACK GOAL",
            font = ("Impact", new_font_size),
            state = "disabled"
        )
        trackGoal_button.place(
            relx = 0.5,
            rely = 0.5,
            anchor = "center",
            relwidth = 0.7,
            relheight = 0.08
        )
        
        def confirm_remove_course(course):
            form = TopLevel(self)
            form.title("Remove Course")
            form.transient(self)
            if form.winfo_exists():
                form.grab_set()
                form.focus()
                form.attributes("-topmost", True)
                
            width = 700
            height = 150
                
            # Get the screen dimensions
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Calculate center position
            x = int((screen_width / 2) - (width / 2))
            y = int((screen_height / 2) - (height / 2))

            # Set size and position
            form.geometry(f"{width}x{height}+{x}+{y}")
            
            Label(
                form,
                text = "Are you sure you want to remove this course?",
                font = ("Impact", 20)
            ).pack()
            
            Button(
                form,
                text = "Yes",
                font = ("Impact", 20),
                command = lambda: remove_course(course)
            ).pack(
                pady = 10
            )
            
            Button(
                form,
                text = "Cancel",
                font = ("Impact", 20),
                command = form.destroy
            ).pack()
        
        removeCourse_button = Button(
            toolbarContent_frame,
            text = "REMOVE COURSE",
            font = ("Impact", new_font_size),
            state = "disabled"
        )
        removeCourse_button.place(
            relx = 0.5,
            rely = 0.7,
            anchor = "center",
            relwidth = 0.7,
            relheight = 0.08
        )
        
        def width_resize(event):
            new_width = self.controller.winfo_width()
            new_size = int(new_width/4.8)
            new_font_size = int(new_width/96)
            
            logo.configure(
                size = (new_size, new_size)
            )
            
            home_button.configure(
                font = ("Impact", new_font_size)
            )
            
            addCourse_button.configure(
                font = ("Impact", new_font_size)
            )
            
            trackGoal_button.configure(
                font = ("Impact", new_font_size)
            )
            
            removeCourse_button.configure(
                font = ("Impact", new_font_size)
            )
            
        self.bind(
            "<Configure>",
            width_resize
        )
        
        if selectedCourse:
            trackGoal_button.configure(
                state = "normal",
                command = lambda: open_goal_tracker_page(selectedCourse)
            )
            
            removeCourse_button.configure(
                state = "normal",
                command = lambda: confirm_remove_course(selectedCourse)
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
                form = TopLevel(self)
                form.title("Update Score")
                form.transient(self)
                if form.winfo_exists():
                    form.grab_set()
                    form.focus()
                    form.attributes("-topmost", True)
                    
                width = 400
                height = 210
                    
                # Get the screen dimensions
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()

                # Calculate center position
                x = int((screen_width / 2) - (width / 2))
                y = int((screen_height / 2) - (height / 2))

                # Set size and position
                form.geometry(f"{width}x{height}+{x}+{y}")
                
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
                ).pack(
                    pady=10
                )
                
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
                    fg_color = "#242222",
                    height = int(0.3 * main_height),
                    width = int(0.7 * main_width),
                    corner_radius = 20
                )
            else:
                course_frame = Frame(
                    coursesList_frame,
                    border_width = 2,
                    border_color = "black",
                    fg_color = "#242222",
                    height = int(0.3 * main_height),
                    width = int(0.7 * main_width),
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
            
            course_name_size = int(window_width/48)
            
            courseName_label = Label(
                courseName_frame,
                font = ("Impact", course_name_size),
                text = str(course["name"]) + " (" + str(course["id"]) + ")"
            )
            courseName_label.pack()
            
            courseName_label.bind(
                "<Button-1>", 
                selectCourse_Handler(course)
            )
            
            courseNameButtonBorder_frame = Frame(
                courseName_frame,
                height = 3,
                fg_color = "black"
            )
            courseNameButtonBorder_frame.place(
                relx = 0.5,
                rely = 1,
                anchor = "s",
                relwidth = 1
            )
            
            courseNameButtonBorder_frame.bind(
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
            
            coursePerformance_centeringFrame.bind(
                "<Button-1>", 
                selectCourse_Handler(course)
            )
            
            def resize_course_frame(event, frame = course_frame):
                frame_height = self.winfo_height()
                frame_width = self.winfo_width()
                
                new_font_size = int(frame_width/48)

                frame.configure(
                    height = int(0.3 * frame_height),
                    width = int(0.7 * frame_width)
                )
                
                courseName_label.configure(
                    font = ("Impact", new_font_size)
                )

            self.bind(
                "<Configure>",
                resize_course_frame
            )
            
            for assignment in course["assignments"].values():
                
                assignment_frame = Frame(coursePerformance_centeringFrame)
                assignment_frame.pack(
                    side = "left"
                )
                
                def setSize(event, frame = assignment_frame):
                    frame_width = int(0.105 * self.winfo_width())
                    frame_height = int(0.168 * self.winfo_height())
                    
                    frame.configure(
                        width = frame_width,
                        height = frame_height
                    )
                
                assignment_frame.bind(
                    "<Configure>",
                    setSize
                )
                
                assignment_frame.bind(
                    "<Button-1>", 
                    selectCourse_Handler(course)
                )
                
                if selectedCourse and selectedCourse == course:
                    assignmentTitle_frame = Frame(assignment_frame)
                    assignmentTitle_frame.place(
                        relx = 0.05,
                        rely = 0.05,
                        relwidth = 0.9,
                        relheight = 0.25
                    )
                    
                    assignmentTitle_centeringFrame = Frame(assignmentTitle_frame)
                    assignmentTitle_centeringFrame.pack(expand = True)
                    
                    assessment_size = int(window_width/96)
                    content_size = int(window_width/106.667)
                    
                    assignment_title_Label = Label(
                        assignmentTitle_centeringFrame,
                        font = ("Impact", assessment_size),
                        text = str(assignment["name"])
                    )
                    assignment_title_Label.pack()
                
                    assignmentScore_frame = Frame(assignment_frame)
                    assignmentScore_frame.place(
                        relx = 0.05,
                        rely = 0.3,
                        relwidth = 0.9,
                        relheight = 0.65,
                    )
                    
                    score_label = Label(
                        assignmentScore_frame,
                        font = ("Impact", content_size),
                        text = str(
                            round(
                                ((assignment["score"]/assignment["weightage"])*100),
                                1
                            )
                        )+"%"
                    )
                    score_label.place(
                        relx = 0.5,
                        rely = 0.25,
                        anchor = "center"
                    )
                    
                    update_button = Button(
                        assignmentScore_frame, 
                        text = "Update",
                        font = ("Impact", content_size), 
                        command = lambda assignment = assignment: update_score(assignment)
                    )
                    update_button.place(
                        relx = 0.5,
                        rely = 0.5,
                        anchor = "center",
                        relwidth = 0.8,
                        relheight = 0.25
                    )
                    
                    reset_button = Button(
                        assignmentScore_frame,
                        text = "Reset",
                        font = ("Impact", content_size),
                        command = lambda assignment = assignment: reset_score(assignment)
                    )
                    reset_button.place(
                        relx = 0.5,
                        rely = 0.8,
                        anchor = "center",
                        relwidth = 0.8,
                        relheight = 0.25
                    )
                    
                    def resize_elements(event, title = assignment_title_Label, score = score_label, update = update_button, reset = reset_button):
                        new_width = self.controller.winfo_width()
                        title_size = int(new_width/96)
                        content_size = int(new_width/106.667)
                        
                        title.configure(
                            font = ("Impact", title_size)
                        )
                        
                        score.configure(
                            font = ("Impact", content_size)
                        )
                        
                        update.configure(
                            font = ("Impact", content_size)
                        )
                        
                        reset.configure(
                            font = ("Impact", content_size)
                        )
                        
                    self.bind(
                        "<Configure>",
                        resize_elements
                    )
                    
                else:
                    assignmentTitle_frame = Frame(assignment_frame)
                    assignmentTitle_frame.place(
                        relx = 0.05,
                        rely = 0.05,
                        relwidth = 0.9,
                        relheight = 0.25
                    )
                    
                    assignmentTitle_frame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    assignmentTitle_centeringFrame = Frame(assignmentTitle_frame)
                    assignmentTitle_centeringFrame.pack(expand = True)
                    
                    assignmentTitle_centeringFrame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    assessment_size = int(window_width/96)
                    content_size = int(window_width/106.667)
                    
                    assignment_title_Label = Label(
                        assignmentTitle_centeringFrame, 
                        text = str(assignment["name"]),
                        font = ("Impact", assessment_size)
                    )
                    assignment_title_Label.pack()
                
                    assignment_title_Label.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                
                    assignmentScore_frame = Frame(assignment_frame)
                    assignmentScore_frame.place(
                        relx = 0.05,
                        rely = 0.3,
                        relwidth = 0.9,
                        relheight = 0.65,
                    )
                    
                    assignmentScore_frame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    assignmentScore_centeringFrame = Frame(assignmentScore_frame)
                    assignmentScore_centeringFrame.pack(expand = True)
                    
                    assignmentScore_centeringFrame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                
                    score_label = Label(
                        assignmentScore_centeringFrame, 
                        text = str(
                            round(
                                ((assignment["score"]/assignment["weightage"])*100),
                                1
                            )
                        )+"%",
                        font = ("Impact", content_size)
                    )
                    score_label.pack()
                    
                    score_label.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
         
                    def resize_elements(event, title = assignment_title_Label, score = score_label):
                        new_width = self.controller.winfo_width()
                        title_size = int(new_width/96)
                        content_size = int(new_width/106.667)
                        
                        title.configure(
                            font = ("Impact", title_size)
                        )
                        
                        score.configure(
                            font = ("Impact", content_size)
                        )
                    
                    self.bind(
                        "<Configure>",
                        resize_elements
                    )
            
            for coursework in course["coursework_exams"].values():
                coursework_frame = Frame(coursePerformance_centeringFrame)
                coursework_frame.pack(
                    side = "left"
                )
                
                def setSize(event, frame = coursework_frame):
                    frame_width = int(0.105 * self.winfo_width())
                    frame_height = int(0.168 * self.winfo_height())
                    
                    frame.configure(
                        width = frame_width,
                        height = frame_height
                    )
                
                coursework_frame.bind(
                    "<Configure>",
                    setSize
                )
                
                coursework_frame.bind(
                    "<Button-1>", 
                    selectCourse_Handler(course)
                )
                
                if selectedCourse and selectedCourse == course:
                    courseworkTitle_frame = Frame(coursework_frame)
                    courseworkTitle_frame.place(
                        relx = 0.05,
                        rely = 0.05,
                        relwidth = 0.9,
                        relheight = 0.25
                    )
                    
                    courseworkTitle_centeringFrame = Frame(courseworkTitle_frame)
                    courseworkTitle_centeringFrame.pack(expand = True)
                    
                    assessment_size = int(window_width/96)
                    content_size = int(window_width/106.667)
                    
                    courseworkTitle_label = Label(
                        courseworkTitle_centeringFrame, 
                        text = str(coursework["name"]),
                        font = ("Impact", assessment_size),
                    )
                    courseworkTitle_label.pack()
                    
                    courseworkScore_frame = Frame(coursework_frame)
                    courseworkScore_frame.place(
                        relx = 0.05,
                        rely = 0.3,
                        relwidth = 0.9,
                        relheight = 0.65,
                    )
                
                    score_label = Label(
                        courseworkScore_frame, 
                        text = str(
                            round(
                                ((coursework["score"]/coursework["weightage"])*100),
                                1
                            )
                        )+"%",
                        font = ("Impact", content_size)
                    )
                    score_label.place(
                        relx = 0.5,
                        rely = 0.25,
                        anchor = "center"
                    )
                
                    update_button = Button(
                        courseworkScore_frame, 
                        text = "Update",
                        font = ("Impact", content_size),
                        command = lambda coursework = coursework: update_score(coursework)
                    )
                    update_button.place(
                        relx = 0.5,
                        rely = 0.5,
                        anchor = "center",
                        relwidth = 0.8,
                        relheight = 0.25
                    )
                
                    reset_button = Button(
                        courseworkScore_frame,
                        text = "Reset",
                        font = ("Impact", content_size),
                        command = lambda coursework = coursework: reset_score(coursework)
                    )
                    reset_button.place(
                        relx = 0.5,
                        rely = 0.8,
                        anchor = "center",
                        relwidth = 0.8,
                        relheight = 0.25
                    )
                    
                    def resize_elements(event, title = courseworkTitle_label, score = score_label, update = update_button, reset = reset_button):
                        new_width = self.controller.winfo_width()
                        title_size = int(new_width/96)
                        content_size = int(new_width/106.667)
                        
                        title.configure(
                            font = ("Impact", title_size)
                        )
                        
                        score.configure(
                            font = ("Impact", content_size)
                        )
                        
                        update.configure(
                            font = ("Impact", content_size)
                        )
                        
                        reset.configure(
                            font = ("Impact", content_size)
                        )
                        
                    self.bind(
                        "<Configure>",
                        resize_elements
                    )
                    
                else:
                    courseworkTitle_frame = Frame(coursework_frame)
                    courseworkTitle_frame.place(
                        relx = 0.05,
                        rely = 0.05,
                        relwidth = 0.9,
                        relheight = 0.25
                    )
                    
                    courseworkTitle_frame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    courseworkTitle_centeringFrame = Frame(courseworkTitle_frame)
                    courseworkTitle_centeringFrame.pack(expand = True)
                    
                    courseworkTitle_centeringFrame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    assessment_size = int(window_width/96)
                    content_size = int(window_width/106.667)
                    
                    courseworkTitle_label = Label(
                        courseworkTitle_centeringFrame, 
                        text = str(coursework["name"]),
                        font = ("Impact", assessment_size)
                    )
                    courseworkTitle_label.pack()
                    
                    courseworkTitle_label.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    courseworkScore_frame = Frame(coursework_frame)
                    courseworkScore_frame.place(
                        relx = 0.05,
                        rely = 0.3,
                        relwidth = 0.9,
                        relheight = 0.65,
                    )
                    
                    courseworkScore_frame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    courseworkScore_centeringFrame = Frame(courseworkScore_frame)
                    courseworkScore_centeringFrame.pack(expand = True)
                
                    courseworkScore_centeringFrame.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                
                    score_label = Label(
                        courseworkScore_centeringFrame, 
                        text = str(
                            round(
                                ((coursework["score"]/coursework["weightage"])*100),
                                1
                            )
                        )+"%",
                        font = ("Impact", content_size)
                    )
                    score_label.pack()
                    
                    score_label.bind(
                        "<Button-1>", 
                        selectCourse_Handler(course)
                    )
                    
                    def resize_elements(event, title = courseworkTitle_label, score = score_label):
                        new_width = self.controller.winfo_width()
                        title_size = int(new_width/96)
                        content_size = int(new_width/106.667)
                        
                        title.configure(
                            font = ("Impact", title_size)
                        )
                        
                        score.configure(
                            font = ("Impact", content_size)
                        )
                        
                    self.bind(
                        "<Configure>",
                        resize_elements
                    )

    def create_course_form_part1(self):
        #creating the CTkFrame form to enter the data for the new course
        form = TopLevel(self)
        form.title("Course Information")
        form.transient(self)
        if form.winfo_exists():
            form.grab_set()
            form.focus()
            form.attributes("-topmost", True)
            
        width = 400
        height = 380
            
        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate center position
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Set size and position
        form.geometry(f"{width}x{height}+{x}+{y}")
        
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
        
        input_div = Frame(form)
        input_div.pack()
        
        final_weightage = ctk.CTkEntry(input_div)
        final_weightage.pack(side = "left")
        
        percent_sign = Label(
            input_div,
            text = "%",
            font = ("Impact", 20)
        )
        percent_sign.pack(side = "left")
        
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
        ).pack(
            pady=10
        )
        
        Button(
            form, 
            text = "Cancel",
            font = ("Impact", 20),
            command = form.destroy
        ).pack()
        
    def create_course_form_part2(self, course_name, course_id, final_weightage, num_of_assignments, num_of_coursework_exams):
        #creating the form to enter the values and store them in variables
        form = TopLevel(self)
        form.title("Course Information")
        form.transient(self)
        if form.winfo_exists():
            form.grab_set()
            form.focus()
            form.attributes("-topmost", True)
            
        width = 600
        height = 380
            
        # Get the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate center position
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Set size and position
        form.geometry(f"{width}x{height}+{x}+{y}")
        
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
            
            input_div = Frame(scrollable_area)
            input_div.pack()
            
            weightage = ctk.CTkEntry(input_div)
            weightage.pack(side = "left")
            
            percent_sign = Label(
                input_div,
                text = "%",
                font = ("Impact", 20)
            )
            percent_sign.pack(side = "left")
            
            assignment_weightages.append(weightage)
        
        for i in range(1, num_of_coursework_exams+1):
            Label(
                scrollable_area, 
                text = "How much percent of your final grade is Coursework Exam "+ str(i) +" worth?",
                font = ("Impact", 20)
            ).pack()
            
            input_div = Frame(scrollable_area)
            input_div.pack()
            
            weightage = ctk.CTkEntry(input_div)
            weightage.pack(side = "left")
            
            percent_sign = Label(
                input_div,
                text = "%",
                font = ("Impact", 20)
            )
            percent_sign.pack(side = "left")
            
            coursework_exam_weightages.append(weightage)
            
        #populating all the assignments and coursework exams of the created course with their relevant weightage values 
        def submit_form():
            #initializing all the assignments dictionary for later updates
            def init_assignments(num_of_assignments):
                assignments = {}
            
                for i in range(1,num_of_assignments+1):
                    assignments["assignment_" + str(i)] = {
                        "name": "Assignment " + str(i),
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
                        "name": "Coursework Exam " + str(i),
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
        ).pack(
            pady = 10
        )
        
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

        main_height = self.controller.winfo_height()
        main_width = self.controller.winfo_width()
        
        
        
        new_size = int(main_width/4.8)
        new_font_size = int(main_width/96)
        title_font_size = int(main_width/38.4)
        assessment_size = int(main_width/48)
        
        def edit_goal():
            def update_goal_value():
                goal = int(input_field.get())
                self.course["goal"] = goal/100
                form.destroy()
                self.refresh_gui()
        
            form = TopLevel(self)
            form.title("Edit Goal")
            form.transient(self)
            if form.winfo_exists():
                form.grab_set()
                form.focus()
                form.attributes("-topmost", True)
                
            width = 700
            height = 150
                
            # Get the screen dimensions
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Calculate center position
            x = int((screen_width / 2) - (width / 2))
            y = int((screen_height / 2) - (height / 2))

            # Set size and position
            form.geometry(f"{width}x{height}+{x}+{y}")
            
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
            ).pack(
                pady = 10
            )
            
            Button(
                form,
                text = "Cancel",
                font = ("Impact", 20),
                command = form.destroy
            ).pack()
            
        navbar_frame = Frame(
            self,
            fg_color = "#242222"
        )
        navbar_frame.place(
            relx = 0,
            rely = 0,
            relwidth = 0.2,
            relheight = 1
        )
        
        logo_frame = Frame(navbar_frame)
        logo_frame.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 0.3
        )
        
        navButtons_frame = Frame(navbar_frame)
        navButtons_frame.place(
            relx = 0,
            rely = 0.3,
            relwidth = 1,
            relheight = 0.7
        )
        
        header_frame = Frame(
            self,
            border_width = 2,
            border_color = "black"
        )
        header_frame.place(
            relx = 0.2,
            rely = 0,
            relwidth = 0.8,
            relheight = 0.2
        )
        
        content_frame = ScrollableFrame(
            self,
            fg_color = "#18016b"
        )
        content_frame.place(
            relx = 0.2,
            rely = 0.2,
            relwidth = 0.8,
            relheight = 0.8
        )
        
        logo = ctk.CTkImage(
            light_image = Image.open("images/Logo.png"),
            dark_image = Image.open("images/Logo.png"),
            size = (new_size, new_size)
        )
        
        logoFrame_label = Label(
            logo_frame,
            text="",
            image = logo
        )
        logoFrame_label.pack(
            fill="both",
            expand="true"
        )
        
        Label(
            header_frame,
            text = str(self.course["name"])+" ("+str(self.course["id"])+")",
            font = ("Impact", title_font_size)
        ).place(
            relx = 0.5,
            rely = 0.5,
            anchor = "s"
        )
        
        Label(
            header_frame, 
            text = "Your goal is to attain "+str(self.course["goal"]*100)+"%",
            font = ("Impact", new_font_size)
        ).place(
            relx = 0.5,
            rely = 0.5,
            anchor = "n"
        )
        
        Button(
            navButtons_frame, 
            text = "EDIT GOAL",
            font = ("Impact", new_font_size),
            command = edit_goal
        ).place(
            relx = 0.5,
            rely = 0.1,
            anchor = "center",
            relwidth = 0.7,
            relheight = 0.08
        )
        
        Button(
            navButtons_frame, 
            text = "BACK",
            font = ("Impact", new_font_size),
            command = lambda:self.controller.open_page("MidtermPerformanceTracker")
        ).place(
            relx = 0.5,
            rely = 0.3,
            anchor = "center",
            relwidth = 0.7,
            relheight = 0.08
        )
        
        goal = self.course["goal"]*100
        score_sum = 0
        goal_remainder = goal
        
        total = 100
        weightage_sum = 0
        total_remainder = total
        
        required_score_sum = 0
        
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
            
            assessment_frame = Frame(
                content_frame,
                border_width = 2,
                border_color = "black",
                fg_color = "#242222",
                height = int(0.15 * main_height),
                width = int(0.7 * main_width),
                corner_radius = 10
            )
            assessment_frame.pack(
                pady = 20
            )
            
            def resize(event, frame = assessment_frame):
                frame_width = int(0.7 * self.controller.winfo_width())
                frame_height = int (0.14 * self.controller.winfo_height())
                    
                frame.configure(
                    height = frame_height,
                    width = frame_width
                )
            
            assessment_frame.bind(
                "<Configure>",
                resize
            )
            
            assessmentHeader_frame = Frame(assessment_frame)
            assessmentHeader_frame.place(
                relx = 0.01,
                rely = 0.1,
                relwidth = 0.3395,
                relheight = 0.8
            )
            
            assessementSeperator = Frame(
                assessment_frame,
                fg_color = "black",
                height = 146,
                width = 2
            )
            assessementSeperator.place(
                relx = 0.35,
                rely = 0.5,
                anchor = "center"
            )
            
            assessmentContent_frame = Frame(assessment_frame)
            assessmentContent_frame.place(
                relx = 0.355,
                rely = 0.1,
                relwidth = 0.6395,
                relheight = 0.8
            )
            
            if assignment["status"] == "WAITING":
                required_score = round(((weightage/total_remainder)*goal_remainder), 1)
                required_score_sum += required_score
                
                Label(
                    assessmentHeader_frame, 
                    text = assignment["name"],
                    font = ("Impact", assessment_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "center"
                )
                
                Label(
                    assessmentContent_frame, 
                    text = "You need to get at least",
                    font = ("Impact", new_font_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "s"
                )
                
                Label(
                    assessmentContent_frame, 
                    text = str(required_score)+"/"+str(weightage),
                    font = ("Impact", new_font_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "n"
                )
            
            else:
                required_score_sum += assignment["score"]*100
                
                Label(
                    assessmentHeader_frame, 
                    text = assignment["name"],
                    font = ("Impact", assessment_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "center"
                )
                
                Label(
                    assessmentContent_frame, 
                    text = "GRADED",
                    font = ("Impact", new_font_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "center"
                )
            
        for coursework_exam in self.course["coursework_exams"].values():
            score = coursework_exam["score"]*100
            weightage = round((coursework_exam["weightage"]*100), 1)
            
            assessment_frame = Frame(
                content_frame,
                border_width = 2,
                border_color = "black",
                fg_color = "#242222",
                height = int(0.15 * main_height),
                width = int(0.7 * main_width),
                corner_radius = 10
            )
            assessment_frame.pack(
                pady = 20
            )
            
            def resize(event, frame = assessment_frame):
                frame_width = int(0.7 * self.controller.winfo_width())
                frame_height = int (0.14 * self.controller.winfo_height())
                    
                frame.configure(
                    height = frame_height,
                    width = frame_width
                )
            
            assessment_frame.bind(
                "<Configure>",
                resize
            )
            
            assessmentHeader_frame = Frame(assessment_frame)
            assessmentHeader_frame.place(
                relx = 0.01,
                rely = 0.1,
                relwidth = 0.3395,
                relheight = 0.8
            )
            
            assessementSeperator = Frame(
                assessment_frame,
                fg_color = "black",
                height = 146,
                width = 2
            )
            assessementSeperator.place(
                relx = 0.35,
                rely = 0.5,
                anchor = "center"
            )
            
            assessmentContent_frame = Frame(assessment_frame)
            assessmentContent_frame.place(
                relx = 0.355,
                rely = 0.1,
                relwidth = 0.6395,
                relheight = 0.8
            )
            
            if coursework_exam["status"] == "WAITING":
                required_score = round(((weightage/total_remainder)*goal_remainder), 1)
                required_score_sum += required_score
        
                Label(
                    assessmentHeader_frame, 
                    text = coursework_exam["name"],
                    font = ("Impact", assessment_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "center"
                )
                
                Label(
                    assessmentContent_frame, 
                    text = "You need to get at least",
                    font = ("Impact", new_font_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "s"
                )
                
                Label(
                    assessmentContent_frame, 
                    text = str(required_score)+"/"+str(weightage),
                    font = ("Impact", new_font_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "n"
                )
            
            else:
                required_score_sum += coursework_exam["score"]*100
                
                Label(
                    assessmentHeader_frame, 
                    text = coursework_exam["name"],
                    font = ("Impact", assessment_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "center"
                )
                
                Label(
                    assessmentContent_frame, 
                    text = "GRADED",
                    font = ("Impact", new_font_size)
                ).place(
                    relx = 0.5,
                    rely = 0.5,
                    anchor = "center"
                )
                
        required_score = round((goal - required_score_sum), 1)
        
        final_frame = Frame(
            content_frame,
            border_width = 2,
            border_color = "black",
            fg_color = "#242222",
            height = int(0.15 * main_height),
            width = int(0.7 * main_width),
            corner_radius = 10
        )
        final_frame.pack(
            pady = 20
        )
        
        def resize(event):
            frame_width = int(0.7 * self.controller.winfo_width())
            frame_height = int (0.14 * self.controller.winfo_height())
                
            final_frame.configure(
                height = frame_height,
                width = frame_width
            )
        
        final_frame.bind(
            "<Configure>",
            resize
        )
        
        finalHeader_frame = Frame(final_frame)
        finalHeader_frame.place(
            relx = 0.01,
            rely = 0.1,
            relwidth = 0.3395,
            relheight = 0.8
        )
        
        finalSeparator = Frame(
            final_frame,
            fg_color = "black",
            height = 146,
            width = 2
        )
        finalSeparator.place(
            relx = 0.35,
            rely = 0.5,
            anchor = "center"
        )
        
        finalContent_frame = Frame(final_frame)
        finalContent_frame.place(
            relx = 0.355,
            rely = 0.1,
            relwidth = 0.6395,
            relheight = 0.8
        )
        
        Label(
            finalHeader_frame, 
            text = "Final Exam",
            font = ("Impact", assessment_size)
        ).place(
            relx = 0.5,
            rely = 0.5,
            anchor = "center"
        ) 
        
        Label(
            finalContent_frame, 
            text = "You need to get at least",
            font = ("Impact", new_font_size)
        ).place(
            relx = 0.5,
            rely = 0.5,
            anchor = "s"
        )  
        
        Label(
            finalContent_frame, 
            text = str(required_score)+"/"+str(self.course["final_weightage"]*100),
            font = ("Impact", new_font_size)
        ).place(
            relx = 0.5,
            rely = 0.5,
            anchor = "n"
        )             

# Tertiary GPA Tracker App
class TertiaryGPATracker(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        Label(
            self, 
            text = "Tertiary GPA Tracker",
            font = ("Impact", 20)
        ).pack()
        
        Label(
            self, 
            text = "Still Under Development",
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