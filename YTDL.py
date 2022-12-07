""""
    Author: @SeakMeng
    Date: 12/4/2022
    Github: https://github.com/SeakMengs
    Design inspired by customtkinter check them out :) https://github.com/TomSchimansky/CustomTkinter
"""
# Import the required modules for the program
from tkinter import *
import customtkinter as ctk
from PIL import Image
import os

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):

    def __init__(self):

        # inherit and run init of parent class
        super().__init__()

        # set app title and set the app to the middle 
        self.title("YatoDownloader")
        # set screen to middle
        screen_x = int(self.winfo_screenwidth() / 2 - self.winfo_width() / 2)
        screen_y = int(self.winfo_screenheight() / 2 - self.winfo_height() / 2)
        self.geometry("{}+{}".format(screen_x, screen_y))
        # self.iconbitmap("icon.ico")
        # self.config(bg="#000000")

        # give weight for responsive widgets
        self.rowconfigure((0), weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "Assets")
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "home_dark.png")), size=(20, 20))
        self.history_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "history_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "history_dark.png")), size=(20, 20))
        self.settings_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "settings_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "settings_dark.png")), size=(20, 20))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "download.png")), size=(50, 50))
        # create left-side navigation
        self.leftNavigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.leftNavigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.logo_label =ctk.CTkLabel(self.leftNavigation_frame, text=" YTDL", image=self.logo_image, text_color=("gray10", "gray90"), font=ctk.CTkFont(weight="bold", size=15), compound="left")
        self.logo_label.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.home_button = ctk.CTkButton(self.leftNavigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
        self.history_button = ctk.CTkButton(self.leftNavigation_frame, corner_radius=0, height=40, border_spacing=10, text="History",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.history_image, anchor="w", command=self.history_button_event)
        self.history_button.grid(row=2, column=0, sticky="ew")
        self.settings_button = ctk.CTkButton(self.leftNavigation_frame, corner_radius=0, height=40, border_spacing=10, text="settings",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.settings_image, anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")
        self.appearance_mode_label = ctk.CTkLabel(self.leftNavigation_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="s")
        self.leftNavigation_frame.rowconfigure(4, weight=1)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.leftNavigation_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0,fg_color="transparent", height=500, width=500)
        self.home_frame.grid_columnconfigure(0, weight=1)

        # self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        # self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # self.home_frame_button_1 = ctk.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        # self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.home_frame_button_2 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        # self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.home_frame_button_3 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        # self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.home_frame_button_4 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        # self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create history frame
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")
        self.appearance_mode_optionemenu.set("Dark")


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.history_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.history_frame.grid_forget()
        if name == "frame_3":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def history_button_event(self):
        self.select_frame_by_name("history")

    def settings_button_event(self):
        self.select_frame_by_name("settings")
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
