import threading
import tkinter as tk
import youtube_dl

def download():
    # Get the values entered in the URL, destination, start, and end entry fields
    url = url_entry.get()
    destination = destination_entry.get()
    start = start_entry.get()
    end = end_entry.get()

    # Create labels to display number of bytes downloaded and total bytes
    bytes_downloaded_label = tk.Label(text="Bytes downloaded: ")
    bytes_downloaded_label.pack()

    total_bytes_label = tk.Label(text="Total bytes: ")
    total_bytes_label.pack()

    def progress_callback(download_progress):
        bytes_downloaded_label.config(text="Bytes downloaded: {}".format(download_progress["downloaded_bytes"]))
        total_bytes_label.config(text="Total bytes: {}".format(download_progress["total_bytes"]))

    # Use youtube_dl to download the video in a separate thread
    def download_thread():
        ydl_opts = {
            'outtmpl': destination + '/%(title)s.%(ext)s',
            'format': 'best[height<=480]',
            'keepvideo': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'start': start,
            'end': end,
            'progress_hooks': [progress_callback]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        download_button.config(state='normal')
    download_thread = threading.Thread(target=download_thread)
    download_thread.start()
    download_button.config(state='normal')
# Create the main window
window = tk.Tk()
window.title("FM")
window.geometry("200x225")

# Create a label and text entry field for the URL
url_label = tk.Label(text="URL:")
url_label.pack()
url_entry = tk.Entry(width=30)
url_entry.pack()

# Create a label and text entry field for the destination folder
destination_label = tk.Label(text="Destination Folder: *OPTIONAL*")
destination_label.pack()
destination_entry = tk.Entry()
destination_entry.pack()

# Create a label and text entry field for the start time
start_label = tk.Label(text="Start Time (hh:mm:ss): *OPTIONAL*")
start_label.pack()
start_entry = tk.Entry()
start_entry.pack()

# Create a label and text entry field for the end time
end_label = tk.Label(text="End Time (hh:mm:ss): *OPTIONAL*")
end_label.pack()
end_entry = tk.Entry()
end_entry.pack()

# Create a button to initiate the download
download_button = tk.Button(text="Download", command=download)
download_button.pack()

# Run the Tkinter event loop
window.mainloop()
