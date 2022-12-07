""""
    Author: @SeakMeng
    Date: 12/4/2022
    Github: https://github.com/SeakMengs
    Design inspired by customtkinter check them out :) https://github.com/TomSchimansky/CustomTkinter
"""
# Import the required modules for the program
from tkinter import *
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
from pytube import YouTube
from pytube import Playlist
import os
import sys
import subprocess
import requests
import io

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):

    def __init__(self):

        # inherit and run init of parent class
        super().__init__()

        # set app title and set the app to the middle 
        self.title("YatoDownloader")
        # self.iconbitmap("icon.ico")
        # self.config(bg="#000000")

        # set default thumbnail size
        self.thumbnail_size_x = 50
        self.thumbnail_size_y = 50

        # give weight for responsive widgets
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

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
        
        self.logo_label =ctk.CTkLabel(self.leftNavigation_frame, text="  YTDL", image=self.logo_image, text_color=("gray10", "gray90"), font=ctk.CTkFont(weight="bold", size=15), compound="left")
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
        self.leftNavigation_frame.grid_rowconfigure(4, weight=1)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.leftNavigation_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event, text_color=("gray10", "gray90"))
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.version_label = ctk.CTkLabel(self.leftNavigation_frame, text="Version 0.0.1", text_color=("gray10", "gray90"))
        self.version_label.grid(row=6, column=0, padx=20, pady=(0,5))

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        self.home_frame.grid_columnconfigure(0, weight=2)
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        # create mid frame inside home
        self.inside_home_mid_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent", corner_radius=0)
        self.inside_home_mid_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.inside_home_mid_frame.grid_columnconfigure(0, weight=1)
        self.inside_home_mid_frame.grid_rowconfigure(0, weight=1)
        self.video_thumbnail_label = ctk.CTkLabel(self.inside_home_mid_frame, text_color=("gray10", "gray90"),
                                                text="Youtube Thumbnail", font=ctk.CTkFont(weight="bold", size=15), compound="left")
        self.video_thumbnail_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")
        self.choose_path_entry = ctk.CTkEntry(self.inside_home_mid_frame, placeholder_text="Save path")
        self.choose_path_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.choose_path_button = ctk.CTkButton(self.inside_home_mid_frame, text="Choose path", text_color=("gray10", "gray90"), command=self.save_path_button_event)
        self.choose_path_button.grid(row=1, column=2,padx=(0,20), pady=10, sticky="nsew")
        self.paste_url_entry = ctk.CTkEntry(self.inside_home_mid_frame, placeholder_text="Youtube url")
        self.paste_url_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.download_button = ctk.CTkButton(self.inside_home_mid_frame, text="Download", text_color=("gray10", "gray90"))
        self.download_button.grid(row=2, column=2,padx=(0,20), pady=10, sticky="nsew")
        self.quality_optionemenu = ctk.CTkOptionMenu(self.inside_home_mid_frame, values=["Quality"], text_color=("gray10", "gray90"))
        self.quality_optionemenu.grid(row=3, column=0,columnspan=3 ,padx=20, pady=10, sticky="nsew")


        # create right-side frame inside home
        self.inside_home_right_frame = ctk.CTkFrame(self.home_frame, corner_radius=0)
        self.inside_home_right_frame.grid(row=0, column=1, sticky="nsew")

        # create history frame
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")
        self.appearance_mode_optionemenu.set("Dark")

        # set screen to middle every time the app start
        screen_x = int(self.winfo_screenwidth() / 2 - self.winfo_width() / 2)
        screen_y = int(self.winfo_screenheight() / 2 - self.winfo_height() / 2)
        self.geometry("{}+{}".format(screen_x, screen_y))

        # # * Temp delete later
        # temp_ur_img = YouTube("https://www.youtube.com/watch?v=k7gFWkew_zo&ab_channel=%E1%9E%9C%E1%9E%8E%E1%9F%92%E1%9E%8E%E1%9E%8A%E1%9E%B6-VannDaOfficial").thumbnail_url
        # self.read_image_from_url(temp_ur_img, self.video_thumbnail_label, 500, 500)
        # # *

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

    def read_image_from_url(self, url, widget, size_x, size_y):
        response = requests.get(url)
        img_data = response.content
        img = ctk.CTkImage(Image.open(io.BytesIO(img_data)), size=(size_x, size_y))
        # img = ctk.CTkImage(Image.open(io.BytesIO(img_data)).crop((0, 0, 1280, 720)), size=(size_x, size_y))
        
        widget.configure(image=img)

    def save_path_button_event(self):
        self.choose_path_entry.insert(0, (filedialog.askdirectory()))

    # self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text=" video", compound="left")
    # self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
    # self.read_image_from_url(YouTube("https://www.youtube.com/watch?v=_NURmDlK0OE&ab_channel=AirRemix").thumbnail_url, self.home_frame_large_image_label)

    # playlist = Playlist("https://www.youtube.com/playlist?list=PL2rTmCt6YI5VuZt0-CevRpQdeSim_j-BE")
    # for urls in playlist.video_urls:
    #     # check widget in home_frame
    #     temp_grid = len(self.home_frame.winfo_children())
    #     temp_widget = ctk.CTkLabel(self.home_frame, text="video", compound="left")
    #     temp_widget.grid(row=temp_grid, column=0, padx=20, pady=10)
    #     YouTube(urls).thumbnail_url
    #     self.read_image_from_url(YouTube(urls).thumbnail_url, temp_widget)

if __name__ == "__main__":
    app = App()
    app.mainloop()
