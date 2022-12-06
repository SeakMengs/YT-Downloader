# YT-Downloader

# Requirement
cd to project folder and paste the line below to your terminal <br>
pip install -r requirements.txt <br>

If you are not a linux user skip the line below<br>
For Linux users run this command after install the requirements (remove ffmpeg.exe which is for window os)<br>

rm ffmpeg.exe <br>
sudo apt install ffmpeg


# How to convert python file to exe for console version
pip install pyinstaller <br>
<br>
cd to project folder <br>
pyinstaller --console -–add-binary ffmpeg.exe;. --onefile -i logo.ico YTDLConsole.py