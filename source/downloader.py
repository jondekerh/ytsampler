# importing packages
from pytube import YouTube
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys

# this is the function that trims audio
def theSnipper(tsStart, tsEnd, newFile):
    # if timestamps are filled do stuff
    if tsStart or tsEnd:
        #error check for both start and End
        if not tsStart or not tsEnd:
            messagebox.showerror("error!", "you need to fill out both fields")
            root.deiconify()
            return

        song = AudioSegment.from_file(newFile)
        snipList = []
        snipList.append(tsStart)
        snipList.append(tsEnd)

        # timestamp conversion
        msTimestamps = []
        for i in snipList:
            try:
                # i am so good at math :) (i copied most this off stack overflow :)))
                msTimestamps.append(sum(int(x) * 60 ** i * 1000 for i, x in enumerate(reversed(i.split(':')))))
            except Exception:
                messagebox.showerror("error!", "something went wrong, make sure there aren't any letters or spaces in the timestamp fields pls <3")
                root.deiconify()
                return

        # error checking - first one is for start times greater than end times, second is for start times greater than video duration
        if msTimestamps[0] >= msTimestamps[1]:
            messagebox.askquestion("error!", "start time greater than end time, cannot cut. run again and do math")
            root.deiconify()
            return
        if msTimestamps[0] >= (song.duration_seconds * 1000):
            messagebox.showerror("error!", "your start time is longer than the video. double check the videos length and run again :)")
            root.deiconify()
            return
        # this stops users from entering something stupid like 55 hours as the end cut and then getting all
        # surprised_pikachu.FLAC when pydub actually treats the mp3 as being 55 hours long
        elif msTimestamps[1] > (song.duration_seconds * 1000):
            msTimestamps[1] = (song.duration_seconds * 1000)

        # the song is then saved over the original with the same title
        newSong = song[msTimestamps[0]:msTimestamps[1]]
        newSong.export(newFile, format="mp3")
        messagebox.showinfo("", "done :)\n" + snipList[0] + " to " + snipList[1] + " saved as " + os.path.basename(newFile))
        sys.exit()

    # if no, exit
    else:
        messagebox.showinfo("", "done :)\n saved as " + os.path.basename(newFile))
        sys.exit()

# click handler for dl button
def download_clicked():
    url = url_entry.get()
    save_directory = save_directory_var.get()
    timestamp_start = timestamp_start_var.get()
    timestamp_end = timestamp_end_var.get()

    root.withdraw()

    # check that the url is valid and start the process
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    except Exception:
        messagebox.showerror("error!", "that might not have been a valid URL, double check the link and try again")
        root.deiconify()
        return

    # extract only audio
    video = yt.streams.get_audio_only()

    # download the file
    out_file = video.download(output_path=save_directory)

    # save the file (this needs to be done so pydub can use the actual mp3 file or ffmpeg gets big mad)
    base, ext = os.path.splitext(out_file)
    newFile = base + '.mp3'
    os.rename(out_file, newFile)

    # snipsnip :)
    theSnipper(timestamp_start, timestamp_end, newFile)

# handles file browsing
def browse_directory():
    directory = filedialog.askdirectory()
    save_directory_var.set(directory)

# GUI, made mostly in chagtp
root = tk.Tk()
root.title("youtube sampler")

# Left Frame for URL and Save Directory
left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=10, pady=10)

#url entry field
url_label = tk.Label(left_frame, text="URL")
url_label.pack()
url_entry = tk.Entry(left_frame)
url_entry.pack()

#blank frame for a e s t h e t i c s
tk.Label(left_frame).pack()

#save directory input
browse_button = tk.Button(left_frame, text="File Destination", command=browse_directory)
browse_button.pack()

save_directory_var = tk.StringVar()
save_directory_entry = tk.Entry(left_frame, textvariable=save_directory_var)
save_directory_entry.pack()

# Right Frame for Timestamps and Download Button
right_frame = tk.Frame(root)
right_frame.pack(side="right", padx=10, pady=10)

#timestamps
timestamps_label = tk.Label(right_frame, text="Timestamps (HH:MM:SS)")
timestamps_label.pack()

timestamp_frame = tk.Frame(right_frame)
timestamp_frame.pack()

timestamp_start_var = tk.StringVar()
timestamp_start_entry = tk.Entry(timestamp_frame, textvariable=timestamp_start_var, width=10)
timestamp_start_entry.pack(side="left")

timestamp_end_var = tk.StringVar()
timestamp_end_entry = tk.Entry(timestamp_frame, textvariable=timestamp_end_var, width=10)
timestamp_end_entry.pack(side="left")

# a e s t h e t i c s
tk.Label(right_frame, text="").pack()

#dl button
download_button = tk.Button(right_frame, text="Download!", command=download_clicked)
download_button.pack()
root.bind('<Return>', download_clicked)

root.mainloop()


# ignore this, its for testing
# https://www.youtube.com/watch?v=HLQ1cK9Edhc
