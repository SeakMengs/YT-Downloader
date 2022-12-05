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
import time
import subprocess

class YTDLConsole():

    # Constructor
    def __init__(self):
        self.description()

    # function to describe about the program
    def description(self):
        # clear console
        print("\033c")
        print("This is a program to download Youtube video and audio written by @SeakMengs")
        print("Press Ctrl+C to exit the program".center(76, '-'), end="\n\n")

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
        self.availableDownloadOptions = []

        # clear console
        print("\033c")
        # Format center the text and fill with '-' (it fill 40 characters)
        print("Available Download".center(150, "-"))

        count = 0
        # check all available download and sort by highest stream size and abr
        for stream in self.ytVideo.streams.filter(file_extension="mp4").order_by("filesize").desc():
            # convert file size to MB precisely by dividing 1024*1024

            # because we receive the mine_type as audio/mp4, we modify it to audio/mp3 to avoid confusion
            showMp3 = stream.mime_type
            if stream.mime_type == "audio/mp4":
                showMp3 = "audio/mp3"

            self.availableDownloadOptions.append([stream.resolution, showMp3, str(round(stream.filesize / 1048576, 2)) + " MB"])
            print("{}. {}".format(count, self.availableDownloadOptions[count]))
            count += 1

        self.downloadType = int(input("\nEnter the number: "))

        # set downloadFileName
        self.downloadFileName = self.ytVideo.title + "." + \
        self.availableDownloadOptions[self.downloadType][1].split("/")[1]

        # validate file name
        self.downloadFileName = self.validFileName(self.downloadFileName)
        self.downloadFileName = self.validExistedFileName(self.downloadFileName)

        # start download
        self.startDownload(self.downloadType, self.savePath_string, self.downloadFileName)

    # function to deal with playlist if we recognize youtube url as a playlist url
    def playlist(self):
        pass

    def startDownload(self, downloadOptions, savePath, filename):
        try:

            print("\nDownloading {}".format(self.ytVideo.title))

            # check if the download is a video or audio, if video download video and download highest audio and then combine it together to a mp4, if audio download audio
            if self.availableDownloadOptions[downloadOptions][1].split("/")[0] == "video":

                self.ytVideo.streams.filter(file_extension="mp4").order_by("filesize").desc()[downloadOptions].download(savePath, filename)

                # download highest audio and combine it with video for me
                self.ytVideo.streams.filter(mime_type="audio/mp4").order_by("abr").desc().first().download(savePath, filename.replace(".mp4", ".mp3"))
                
                # combine audio and video using ffmpeg python library
                self.combineAudioVideo(savePath, filename, filename.replace(".mp4", ".mp3"))

            else:
                # get file extension by spliting mime_type by '/'
                fileExtension = self.availableDownloadOptions[downloadOptions][1].split("/")[1]
                
                # Since we receive the mine_type as audio/mp4, we need to split it by '/' and get the second part if it is audio/mp4 set fileExtension to mp3
                if fileExtension == "mp4":
                    fileExtension = "mp3"

                # validate file existence
                filename = self.validExistedFileName(filename.replace(".mp4", ".{}".format(fileExtension)))

                self.ytVideo.streams.filter(file_extension="mp4").order_by("filesize").desc()[downloadOptions].download(savePath, filename.replace(".mp4", fileExtension))

            # pause the program to wait for user to read the message
            time.sleep(2)
        
            # after download is complete, prompt user to download another video or exit
            print("\033c")
            print("Download complete!".center(150, "-"))
            print("File saved at {}".format(savePath))
            print("File name: {}".format(filename))
            print("1. Download another video or audio")
            print("2. Exit")

            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.description()
            else:
                sys.exit()

        except Exception as err:

            print("\nError: ", err)
            # if error occurs, ask user to input everything again

    def validFileName(self, filename):
        # check if downloadFileName contain any special character of file name and replace with '-'
        for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            filename = filename.replace(char, "-")

        return filename

    def validExistedFileName(self, filename):
        # check if downloadFileName exist in savePath
        if os.path.isfile(os.path.join(self.savePath_string, filename)):
            count = 1

        while os.path.isfile(os.path.join(self.savePath_string, filename)):
            filename = filename.replace(".{}".format(filename.split(".")[-1]), "({}).{}".format(count, filename.split(".")[-1]))
            count += 1 

        return filename

    def combineAudioVideo(self, savePath, video, audio):

        # using ffmpeg to combine audio and video method using subprocess to overwrite the video file
        try:
            videoName = video
            video = self.validExistedFileName(video)
            os.rename(os.path.join(savePath, videoName), os.path.join(savePath, video))

            # check if the file already exist or not if exist add 1 to the file name
            videoName = self.validExistedFileName(videoName)

            subprocess.call(["ffmpeg", "-i", os.path.join(savePath, video), "-i", os.path.join(savePath, audio), "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", os.path.join(savePath, videoName)])
            
            os.remove(os.path.join(savePath, video))
            os.remove(os.path.join(savePath, audio))

        except Exception as err:
            print("Error: ", err)
            sys.exit()


    # function to check print progress when downloading the video or audio
    def progress_Check(self, stream, chunk, bytes_remaining):
        self.curr = stream.filesize - bytes_remaining
        self.done = int(50 * self.curr / stream.filesize)
        
        sys.stdout.write("\r[{}{}]{}%".format('=' * self.done, ' ' * (50-self.done), int(self.curr/stream.filesize*100)))
        sys.stdout.flush()


if __name__ == "__main__":
    YTDLConsole()
