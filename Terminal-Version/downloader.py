""""
    Author: @SeakMengs
    Date: 12/5/2022
    Github: https://github.com/SeakMengs
    This is a console version
"""

# Import necessary libraries to use in our program
from pytube import YouTube
import os
import sys

class App():

    # Constructor
    def __init__(self):
        self.description();

    # function to describe about the program
    def description(self):
        # clear console
        print("\033c")
        print("This is a program to download Youtube video and audio written by @SeakMengs\n")

        self.savePath_string = input("Enter save path: ")
        # check savePath existence and create if not exist input again
        while not os.path.exists(self.savePath_string):
            print("\nSave path does not not exist!")
            self.savePath_string = input("Enter save path: ")

        self.ytUrl_string = input("Enter url: ")
        # check url is valid or not by checking "youtube.com" in url
        while self.ytUrl_string.find("youtube.com/watch") == -1:
            print("\nUrl is not valid!")
            self.ytUrl_string = input("Enter url: ")

        """ check if the url is a playlist url or a video url by checking "youtube.com/playlist" in url
            find function return -1 if not found
        """
        if self.ytUrl_string.find("youtube.com/playlist?") != -1:
            # if url is a playlist url go to playlist function
            self.playlist()
        else:
            # else if url is a video url go to video function
            self.video()
    
    # function to deal with video if we recognize youtube url as a video url
    def video(self):
        # object creation using YouTube pass url, and enable progress checktry: 
        try:
            self.ytVideo = YouTube(self.ytUrl_string, on_progress_callback=self.progress_Check)
        except Exception as err:
            print("Error: ", err)
            # if error occurs, ask user to input everything again
            self.description()
        
        # always reset this list to an empty list in order to prevent error when running this function
        availableDownloadOptions = []


        # clear console
        print("\033c")
        print("Available Download")
        
        count = 0
        # check all available stream and push to availableDownloadOptions
        for stream in self.ytVideo.streams:
            availableDownloadOptions.append([stream.resolution, stream.mime_type, str(round(stream.filesize/1000000, 2)) + " MB"])
            print("{}. {}".format(count, availableDownloadOptions[count]))
            count += 1


        
    # function to deal with playlist if we recognize youtube url as a playlist url
    def playlist(self):
        pass

    def Start_download(self):
        pass





    # function to check print progress when downloading the video or audio
    def progress_Check(self,stream, chunk, bytes_remaining):
        self.curr = stream.filesize - bytes_remaining
        self.done = int(50 * self.curr / stream.filesize)
        sys.stdout.write("\r[{}{}]{}%".format('=' * self.done, ' ' * (50-self.done), int(self.curr/stream.filesize*100)) )
        sys.stdout.flush()




if __name__ == "__main__":
    App()