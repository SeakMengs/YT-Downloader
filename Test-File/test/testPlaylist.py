from pytube import Playlist
import os
import sys

# def progress_Check(stream, chunk, bytes_remaining):
#     contentSize = stream.filesize
#     size = contentSize - bytes_remaining
#     print(f"{int(size/contentSize*100)}% done...")

def progress_Check(stream, chunk, bytes_remaining):
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    sys.stdout.write("\r[{}{}]{}%".format('=' * done, ' ' * (50-done), int(curr/stream.filesize*100)) )
    sys.stdout.flush()

downloadType = "mp4"
savePath_string = "D:\Meng\Projects\YT-Downloader"
playlist = Playlist("https://www.youtube.com/playlist?list=PL2rTmCt6YI5WYjsqSTCJfQs5KEC7crSsB")
folderName = playlist.title
# create a folder in the savePath_string with the playlist title and download all videos to that folder
# if the folder already exists add a number to the end of the folder name
if not os.path.exists(savePath_string + "\\" + folderName):
    os.mkdir(savePath_string + "\\" + folderName)
else:
    i = 1
    os.rmdir(savePath_string + "\\" + folderName)
    while os.path.exists(savePath_string + "\\" + folderName + str(i)):
        i += 1
    os.mkdir(savePath_string + "\\" + folderName + str(i))
    folderName += str(i)

for video in playlist.videos:
    # show progress each video
    print("Downloading: " + video.title)
    video.register_on_progress_callback(progress_Check)
    video.streams.filter(progressive=True, file_extension=downloadType, ).first().download(savePath_string + "\\" + playlist.title)

print("Download Complete")