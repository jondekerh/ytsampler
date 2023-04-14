# importing packages
from pytube import YouTube
from pydub import AudioSegment
import easygui
from easygui import *
import os
import sys

# url input from user
yt = YouTube(str(easygui.enterbox("ENTER URL")))

# extract only audio
video = yt.streams.filter(only_audio=True).first()

# select save destination
destination = str(easygui.diropenbox("SELECT DESTINATION"))

# download the file
out_file = video.download(output_path=destination)

# save the file (this needs to be done so pydub can use the actual mp3 file or ffmpeg gets big mad)
base, ext = os.path.splitext(out_file)
newFile = base + '.mp3'
os.rename(out_file, newFile)

# prompt user to trim the file
snipsnip = easygui.ynbox("Would you like to trim audio?", "DOWNLOAD COMPLETE!")

def theSnipper():
    # if yes, user enters timestamps which are converted into ms for ffmpeg
    if snipsnip:
        song = AudioSegment.from_file(newFile)
        snipBox = multenterbox("", "Enter the timestamps in HH:MM:SS format", ["Start", "End"])
        msTimestamps = []

        #error check for both start and End
        if not snipBox[0] or not snipBox[1]:
            easygui.msgbox("please try again and fill out all fields :)))")
            theSnipper()

        # timestamp conversion
        for i in snipBox:
            try:
                # i am so good at math :) (i copied most this off stack overflow :)))
                msTimestamps.append(sum(int(x) * 60 ** i * 1000 for i, x in enumerate(reversed(i.split(':')))))
            except Exception:
                easygui.msgbox("something went wrong - you probably entered a letter or space. try agian :)")
                theSnipper()



        # error checking - first one is for start times greater than end times, second is for start times greater than video duration
        if msTimestamps[0] >= msTimestamps[1]:
            easygui.msgbox("start time greater than end time, cannot cut. run again and do math")
            theSnipper()
        if msTimestamps[0] >= (song.duration_seconds * 1000):
            easygui.msgbox("your start time is longer than the video. double check the videos length and run again")
            theSnipper()
        # this stops users from entering something stupid like 55 hours as the end cut and then getting all
        # surprised_pikachu.FLAC when pydub actually treats the mp3 as being 55 hours long
        elif msTimestamps[1] >= (song.duration_seconds * 1000):
            msTimestamps[1] = (song.duration_seconds * 1000)

        # the song is then saved over the original with the same title
        newSong = song[msTimestamps[0]:msTimestamps[1]]
        newSong.export(newFile, format="mp3")
        print("done :) " + snipBox[0] + " to " + snipBox[1] + " saved")
        sys.exit()

    # if no, exit
    else:
        print("done :)")
        sys.exit()

theSnipper()

# ignore this, its for testing
# https://www.youtube.com/watch?v=HLQ1cK9Edhc
