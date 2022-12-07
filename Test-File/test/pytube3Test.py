from pytube import YouTube
import os 

yt = YouTube('https://www.youtube.com/watch?v=G9BFbGqOqKk&ab_channel=8KHDRWORLD')
print(yt.streams)

print("\n\n\n")

# for stream in yt.streams:
#     print(stream.resolution)



# count = 0
# availableDownloadOptions = []
# # check all available download and sort by highest stream size and abr
# for stream in yt.streams.filter(file_extension="mp4").order_by("filesize").desc():
#     # convert file size to MB precisely by dividing 1024*1024

#     # because we receive the mine_type as audio/mp4, we modify it to audio/mp3 to avoid confusion
#     showMp3 = stream.mime_type
#     if stream.mime_type == "audio/mp4":
#         showMp3 = "audio/mp3"

#     availableDownloadOptions.append([stream.resolution, showMp3, stream.fps , str(round(stream.filesize / 1048576, 2)) + " MB"])
#     print("{}. {}".format(count, availableDownloadOptions[count]))
#     count += 1
# print(os.name)

# https://stackoverflow.com/questions/63533960/how-to-cancel-and-pause-a-download-using-pytube