# YT-Downloader
a Python-based YouTube video downloader with a GUI and command-line interface that makes use of Pytube3 and FFMPEG. capable of downloading mp3s, playlists, and high definition videos.
# Requirement
cd to project folder and paste the line below to your terminal <br>
pip install -r requirements.txt <br>

If you are not a linux user skip the line below<br>
For Linux users run this command after install the requirements (remove ffmpeg.exe which is for window os)<br>

rm ffmpeg.exe <br>
sudo apt install ffmpeg

# How to get?
cd to folder project and compile YTDL.py for GUI version or YTDLConsole.py for command-line version (command-lnie is not updated)

# How to convert python file to exe for console version
pip install pyinstaller <br>
<br>
cd to project folder <br><br>
for console version <br>
<!-- pyinstaller --console -–add-binary ffmpeg.exe;. --onefile -i logo.ico YTDLConsole.py -->
pyinstaller --console --onefile -i logo.ico YTDLConsole.py
<br><br>
for gui version <br>
https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging <br>
pyinstaller --noconfirm --onedir --windowed --noconsole --add-data "CustomTkinter Location/customtkinter;customtkinter/" -i download.ico "ytdl.py"

then add "Assets folder and ffmpeg to the folder that has exe" <br>

# Preview with light and dark mode
![image](https://user-images.githubusercontent.com/54373229/207796577-504f1356-0310-4880-a137-0aa29659dd12.png)
<br>
![image](https://user-images.githubusercontent.com/54373229/207796631-1ad9b2a7-fbb5-4097-8ea1-57b11911987a.png)

