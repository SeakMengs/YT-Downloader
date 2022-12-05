""""
    Author: @SeakMengs
    Date: 12/4/2022
    Github: https://github.com/SeakMengs
    This file is a test file for me to understand how to use the pytube library (a little bit messy because I'm still learning) 
"""

from pytube import YouTube
import sys
import os

# def progress_Check(stream, chunk, bytes_remaining):
#     contentSize = stream.filesize
#     size = contentSize - bytes_remaining
#     print(f"{int(size/contentSize*100)}% done...")

def progress_Check(stream, chunk, bytes_remaining):
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    sys.stdout.write("\r[{}{}]{}%".format('=' * done, ' ' * (50-done), int(curr/stream.filesize*100)) )
    sys.stdout.flush()

ytUrl_string = input("Paste the url: ")
savePath_string = "D:\Meng\Projects\YT-Downloader"
yt = YouTube(ytUrl_string)


try: 
    # object creation using YouTube
    # which was imported in the beginning 
    yt = YouTube(ytUrl_string, on_progress_callback=progress_Check)
except: 
    print("Connection Error") #to handle exception 

availableDownloadOptions = []
# show all the streams available mp4 and mp3, mp4 must contain audio, otherwise don't show it
# i = 0
mp4WithAudio = 0
for stream in yt.streams.filter(progressive=True):
    if stream.mime_type.split('/')[0] == "video" and stream.includes_audio_track:
        availableDownloadOptions.append([stream.resolution, stream.mime_type, str(round(stream.filesize/1000000, 2)) + " MB"])
        mp4WithAudio += 1
    # print(i, availableDownloadOptions)
    # i += 1

# get all mp3 streams
for stream in yt.streams.filter(only_audio=True):
    availableDownloadOptions.append([stream.abr, stream.mime_type, str(round(stream.filesize/1000000, 2)) + " MB"])
    # print(i, availableDownloadOptions)
    # i += 1
# reverse the list so that the highest quality is at the top

# modify all none video to audio in availableDownloadOptions[1]
for i in range(len(availableDownloadOptions)):
    if availableDownloadOptions[i][1] == "audio/mp4":
        availableDownloadOptions[i][1] = "audio/mp3"



for j in range(len(availableDownloadOptions)):
    print(j, availableDownloadOptions[j])

# clear console
print("\033c")
print("Choose the resolution you want to download: ")
# show the list of available resolutions print availableDownloadOptions
# ask user to choose type by number 
for i in range(len(availableDownloadOptions)):
    print(str(i) + ": " + str(availableDownloadOptions[i]))

downloadType = int(input("Enter the number: "))

downloadFileName = yt.title + "." + availableDownloadOptions[downloadType][1].split("/")[1]  
# check if file already exists in that path
# if it does, add a number to the end of the file name
if os.path.isfile(savePath_string + "\\" + downloadFileName):
    i = 1
    while os.path.isfile(savePath_string + "\\" + downloadFileName):
        downloadFileName = yt.title + "(" + str(i) + ")." + availableDownloadOptions[downloadType][1].split("/")[1]
        i += 1 


    # yt.streams[downloadType].download(savePath_string, filename=yt.title)
try: 
    # download video with downloadType chosen by user and set file type to downloadType[1] and set title to yt.title (file type can be mp3, mp4, webm, etc)
    # combine video with sound
    if availableDownloadOptions[downloadType][1] == "video":
        yt.streams.filter(progressive=True)[downloadType].download(savePath_string, filename= downloadFileName)
        # yt.streams.filter(only_audio=True).first().download(savePath_string, filename=yt.title)
    else:
        # minus mp4WithAudio we push mp4 first then mp3
        yt.streams.filter(only_audio=True)[downloadType - mp4WithAudio].download(savePath_string, filename= downloadFileName)
    # yt.streams[downloadType].download(savePath_string, filename=yt.title + "." + availableDownloadOptions[downloadType][1].split("/")[1])
    print('Task Completed!') 
except Exception as e: 
    print("An Error Occured: ", e)