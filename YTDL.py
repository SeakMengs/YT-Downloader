""""
    Author: @SeakMeng
    Date: 12/4/2022
    Github: https://github.com/SeakMengs
    Design inspired by customtkinter check them out :) https://github.com/TomSchimansky/CustomTkinter
"""
# Import the required modules for the program
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from pytube import YouTube
from pytube import Playlist
import os
import sys
import subprocess
import requests
import io
import threading

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):

    def __init__(self):

        # inherit and run init of parent class
        super().__init__()


        # set default thumbnail size
        self.thumbnail_size_x = 50
        self.thumbnail_size_y = 50

        # give weight for responsive widgets
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  "Assets")
        self.logo_ico = os.path.join(image_path, "download.ico")
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "home_dark.png")), size=(20, 20))
        self.history_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "history_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "history_dark.png")), size=(20, 20))
        self.settings_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "settings_light.png")),
                                       dark_image=Image.open(os.path.join(image_path, "settings_dark.png")), size=(20, 20))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "download.png")), size=(50, 50))
        
        # set app title and set the app to the middle 
        self.title("YatoDownloader")
        self.iconbitmap(True, self.logo_ico)
        # self.config(bg="#000000")

        # create left-side navigation
        self.leftNavigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.leftNavigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.logo_label =ctk.CTkLabel(self.leftNavigation_frame, text="  YTDL", image=self.logo_image, text_color=("gray10", "gray90"),
                                     font=ctk.CTkFont(weight="bold", size=15), compound="left")
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
        self.home_frame.grid_columnconfigure(0, weight=1)
        #* future plan frame -------------------------------
        # self.home_frame.grid_columnconfigure(1, weight=1)
        #*--------------------------------------------------
        self.home_frame.grid_rowconfigure(0, weight=1)

        # create mid frame inside home
        self.inside_home_mid_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent", corner_radius=0)
        self.inside_home_mid_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.inside_home_mid_frame.grid_columnconfigure(0, weight=1)
        self.inside_home_mid_frame.grid_rowconfigure(0, weight=1)
        # * testing
        self.video_thumbnail_label = ctk.CTkLabel(self.inside_home_mid_frame, text_color=("gray10", "gray90"),
                                                text="", font=ctk.CTkFont(weight="bold", size=15), compound="left", fg_color="transparent", anchor="center")
        self.video_thumbnail_label.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky="nsew")
        self.choose_path_entry = ctk.CTkEntry(self.inside_home_mid_frame, placeholder_text="Save path")
        self.choose_path_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.choose_path_entry.bind("<KeyRelease>", self.choose_path_entry_event)
        self.choose_path_button = ctk.CTkButton(self.inside_home_mid_frame, text="Choose path", text_color=("gray10", "gray90"), command=self.save_path_button_event)
        self.choose_path_button.grid(row=1, column=2,padx=(0,20), pady=10, sticky="nsew")
        self.paste_url_entry = ctk.CTkEntry(self.inside_home_mid_frame, placeholder_text="Paste youtube url (Choose the existing path to save first)")
        self.paste_url_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.paste_url_entry.bind("<KeyRelease>", self.paste_url_entry_event)
        self.download_button = ctk.CTkButton(self.inside_home_mid_frame, text="Download", text_color=("gray10", "gray90"), command=self.video_download_event)
        self.download_button.grid(row=2, column=2,padx=(0,20), pady=10, sticky="nsew")
        self.quality_optionemenu = ctk.CTkOptionMenu(self.inside_home_mid_frame, values=["Quality"], text_color=("gray10", "gray90"), command=self.option_menu_choose_quality)
        self.quality_optionemenu.grid(row=3, column=0,columnspan=3 ,padx=20, pady=10, sticky="nsew")
        self.status_label = ctk.CTkLabel(self.inside_home_mid_frame, text="Status: waiting for your save path :)", text_color=("gray10", "gray90"), anchor="w")
        self.status_label.grid(row=4, column=0, padx=20, sticky="nsew")
        self.progress_bar = ctk.CTkProgressBar(self.inside_home_mid_frame, orientation="horizontal", mode="indeterminate")
        self.progress_bar.grid(row=5, column=0, columnspan=3, padx=20, pady= (10,20) , sticky="nsew")
        self.progress_bar.start()
        
        #* For now these frames are not part of the plan, they're part of the future plan :)
        # create right-side frame inside home
        self.inside_home_right_frame = ctk.CTkFrame(self.home_frame, corner_radius=0)
        # self.inside_home_right_frame.grid(row=0, column=1, sticky="nsew")

        # create history frame
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # * Temp delete later
        temp_ur_img = YouTube("https://www.youtube.com/watch?v=b9naukf9yes&ab_channel=8KTUBEPlanet").thumbnail_url
        self.read_image_from_url(temp_ur_img, self.video_thumbnail_label)
        # *--------------------------------------------------------------------------------------------------------

        # select default frame
        self.select_frame_by_name("home")
        self.appearance_mode_optionemenu.set("Dark")
        self.download_button.configure(state="disabled")
        self.quality_optionemenu.configure(state="disabled")
        self.paste_url_entry.configure(state="disabled")

#* Front-end functions ------------------------------------------------------------------------------------------------------------------------------------------------------------


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.history_button.configure(fg_color=("gray75", "gray25") if name == "history" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "history":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.history_frame.grid_forget()
        if name == "settings":
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

#* Back-end ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def read_image_from_url(self, url, widget, size_x=640, size_y=360):
        url = self.get_max_res_thumbnail(url)
        response = requests.get(url)
        img_data = response.content
        img = ctk.CTkImage(Image.open(io.BytesIO(img_data)), size=(size_x, size_y))
        widget.configure(image=img)


    def get_max_res_thumbnail(self, url):
        # pytube return low res thumbnail, i modify the last part to maxresdefault.jpg so that i will receive the highest resolution available
        return url.replace("sddefault.jpg", "maxresdefault.jpg")
    

    def save_path_button_event(self):
        self.choose_path_entry.insert(0, (filedialog.askdirectory()))
        self.choose_path_entry_event(None)


    def choose_path_entry_event(self, event):
        self.save_to_path = self.choose_path_entry.get()
        # check if path exist
        if os.path.exists(self.save_to_path):
            self.save_to_path = os.path.abspath(self.save_to_path)
            print(self.save_to_path)
            self.paste_url_entry.configure(state="normal")
            self.status_label.configure(text="Status: waiting for Youtube url :)")
        else:
            self.download_button.configure(state="disabled")
            self.paste_url_entry.configure(state="disabled")
            self.quality_optionemenu.configure(state="disabled")


    def paste_url_entry_event(self, event):
        try:
            self.yt_url_string = self.paste_url_entry.get()
            yt_url_list = ["youtube.com/watch", "youtube.com/playlist", "youtu.be/"]
            if not any(x in self.yt_url_string for x in yt_url_list):
                self.status_label.configure(text="Status: Youtube url is not valid :(")
                self.quality_optionemenu.configure(values=["Quality"])
                self.paste_url_entry.configure(border_color=("red", "red"))
                return None

            """ check if the url is a playlist url or a video url by checking "youtube.com/playlist" in url
                find() function return -1 if not found
            """
            self.paste_url_entry.configure(border_color=("#979DA2", "#565B5E"))
            self.quality_optionemenu.configure(state="normal")
            if self.yt_url_string.find("youtube.com/playlist?") != -1:
                self.status_label.configure(text="Status: playlist detected :) Click download to start")
                # if url is a playlist url go to playlist function
                self.playlist_event(self.yt_url_string)
            else:
                self.status_label.configure(text="Status: video detected, choose your preferred quality :)")
                # else if url is a video url go to video function
                self.start_anti_freeze(self.video_event(self.yt_url_string))
                # self.video_event(self.yt_url_string)
        except Exception as err:
            self.error_handler(err)


    def video_event(self, url):
        try:
            self.yt_video = YouTube(url, on_progress_callback=self.progress_Check)
            # replace image
            self.read_image_from_url(self.yt_video.thumbnail_url, self.video_thumbnail_label)
        except Exception as err:
            self.error_handler(err)
        self.available_download_options = []
        self.list_of_download_options = []
        # check all available download and sort by highest stream size and abr
        for stream in self.yt_video.streams.filter(file_extension="mp4").order_by("filesize").desc():
            # convert file size to MB precisely by dividing 1024*1024

            # because we receive the mine_type as audio/mp4, we modify it to audio/mp3 to avoid confusion
            showMp3 = stream.mime_type
            if stream.mime_type == "audio/mp4":
                showMp3 = "audio/mp3"
            
            if showMp3 == "audio/mp3":
                self.list_of_download_options.append([stream.abr, showMp3, str(round(stream.filesize / 1048576, 2)) + " MB"])
                self.available_download_options.append("Bitrate: {},  Format: {},  Filesize: {}".format(stream.abr, showMp3, str(round(stream.filesize / 1048576, 2)) + " MB"))
            else:
                self.list_of_download_options.append([stream.resolution, showMp3,"Fps {}".format(stream.fps) , str(round(stream.filesize / 1048576, 2)) + " MB"])
                self.available_download_options.append("Quality: {},  Format: {},  Fps: {},  Filesize: {}".format(stream.resolution, showMp3, stream.fps , str(round(stream.filesize / 1048576, 2)) + " MB"))

        # self.quality_optionemenu.configure(values=self.available_download_options)
        # use multi-processing to avoid freezing the gui
        self.quality_optionemenu.configure(values=self.available_download_options)


    def option_menu_choose_quality(self, select):
        # find the index of the selected quality self.availableDownloadOptions[?] = index, where string is it value
        try:
            self.selected_quality = self.available_download_options.index(select)
            self.download_button.configure(state="normal")
            self.status_label.configure(text="Status: waiting for you to click download :)")
        except Exception as err:
            self.error_handler(err)


    #* When user click download it start here ------------------------------------------------------------------------------------------------------------------------------------
    def video_download_event(self):
        try:
            self.status_label.configure(text="Status: downloading {}".format(self.yt_video.title))
            self.video_file_name = self.valid_output_file_name(self.yt_video.title)
            # check if the download is a video or audio, if video download video and download highest audio and then combine it together to a mp4, if audio download audio
            if self.list_of_download_options[self.selected_quality][1].split("/")[0] == "video":

                self.yt_video.streams.filter(file_extension="mp4").order_by("filesize").desc()[self.selected_quality].download(self.save_to_path, self.video_file_name)
                self.video_fps_int = self.yt_video.streams.filter(file_extension="mp4").order_by("filesize").desc()[self.selected_quality].fps

                # download highest audio and combine it with video for me
                self.yt_video.streams.filter(mime_type="audio/mp4").order_by("abr").desc().first().download(self.save_to_path, self.video_file_name.replace(".mp4", ".mp3"))
                
                # combine audio and video using ffmpeg python library
                # self.combine_audio_video(self.save_to_path, self.video_file_name, self.video_file_name.replace(".mp4", ".mp3"))

            else:
                # get file extension by spliting mime_type by '/'
                file_extension_type = self.list_of_download_options[self.selected_quality][1].split("/")[1]
                
                # Since we receive the mine_type as audio/mp4, we need to split it by '/' and get the second part if it is audio/mp4 set file_extension_type to mp3
                if file_extension_type == "mp4":
                    file_extension_type = "mp3"

                # validate file existence
                self.audio_file_name = self.valid_output_file_name(self.audio_file_name.replace(".mp4", ".{}".format(file_extension_type)))

                self.yt_video.streams.filter(file_extension="mp4").order_by("filesize").desc()[self.selected_quality].download(self.save_to_path, self.audio_file_name.replace(".mp4", file_extension_type))
        except Exception as err:
            self.error_handler(err)


    def combine_audio_video(self, save_path, video, audio):

        # using ffmpeg to combine audio and video method using subprocess to overwrite the video file
        try:
            video_name_string = video
            video = self.valid_output_file_name(video)
            os.rename(os.path.join(self.save_to_path, video_name_string), os.path.join(self.save_to_path, video))

            # check if the file already exist or not if exist add 1 to the file name
            video_name_string = self.valid_output_file_name(video_name_string)

            """ 
                command explanation:
                # -i input file, -c copy copy the stream from input file to output file, -map 0:v map the video stream from input file 0 to output file, -map 1:a map the audio stream from input file 1 to output file
                # -0:v:0 set the output video stream to 0, -0:a:0 set the output audio stream to 0
                # -r set the frame rate of the output file to the frame rate of the input file
            """
            # normally we get the fps, but just for validation in case we get NoneType
            if self.video_fps_int > 0 and self.video_fps_int < 300:
                # subprocess with fps 
                subprocess.call(["ffmpeg", "-i", os.path.join(self.save_to_path, video), "-i", os.path.join(self.save_to_path, audio), "-c", "copy", "-map", "0:v", "-map", "1:a", "-r", str(self.video_fps_int), os.path.join(self.save_to_path, video_name_string)])
            else:
                # subprocess without fps 
                subprocess.call(["ffmpeg", "-i", os.path.join(self.save_to_path, video), "-i", os.path.join(self.save_to_path, audio), "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", os.path.join(self.save_to_path, video_name_string)])
                
            
            os.remove(os.path.join(self.save_to_path, video))
            os.remove(os.path.join(self.save_to_path, audio))

        except Exception as err:
            self.error_handler(err)


    def playlist_event(self, url):
        print("playlist")


    def valid_output_file_name(self, filename):
        # check if downloadFileName contain any special character of file name and replace with '-'
        for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            filename = filename.replace(char, "-")

        return filename


    def valid_exist_folder_name(self, filename):
        # check if folder name exist in current save path
        if os.path.isfile(os.path.join(self.save_to_path, filename)):
            count = 1

            while os.path.isfile(os.path.join(self.save_to_path, filename)):
                filename = filename.replace(".{}".format(filename.split(".")[-1]), "({}).{}".format(count, filename.split(".")[-1]))
                count += 1 

        return filename


    def progress_Check(self, stream, chunk, bytes_remaining):
        self.curr = stream.filesize - bytes_remaining
        self.done = int(50 * self.curr / stream.filesize)
        # sys.stdout.write("\r[{}{}]{}% {}/{}Mbs".format('=' * self.done, ' ' * (50-self.done),
        #                 int(self.curr/stream.filesize*100), round(self.curr/1048576, 2), round(stream.filesize/1048576, 2)))
        # sys.stdout.flush()
        
#* Functions to protect the application ------------------------------------------------------------------------------------------------------------------------------------------

    def set_app_middle_screen(self):
        # set screen to middle every time the app start
        self.screenX = (int(self.winfo_screenwidth()) / 2 - int(self.winfo_reqwidth()) / 2)
        self.screenY = (int(self.winfo_screenheight()) / 2 - int(self.winfo_reqheight()) / 2)
        self.geometry("+{}+{}".format(int(self.screenX), int(self.screenY)))


    def error_handler(self, error):
        messagebox.showerror(title = "YatoDownloader", message = "Error {}".format(error))


    # https://stackoverflow.com/questions/42422139/how-to-easily-avoid-tkinter-freezing
    def anti_freeze(self):
        self.update()
        self.after(1000,self.anti_freeze)
    

    def start_anti_freeze(self, function):
        self.anti_freeze()
        threading.Thread(target=function).start()

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
