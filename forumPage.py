import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from ttkthemes import ThemedTk
from paths import PATH_TO_SQLITE, PATH_TO_REDDIT_API, PATH_TO_VIDEOS
import sys

import urllib.request
from urllib.error import HTTPError
import io
from PIL import ImageTk, Image

import os
import re
import subprocess
os.add_dll_directory('C:\\Program Files\\VideoLAN\\VLC')

# importing vlc module 
import vlc 

import requests
import cv2
from io import BytesIO

from moviepy.editor import VideoFileClip, AudioFileClip
import tkvlc

import pyaudio
import wave
import threading
import time

import datetime
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo

#from tkVideoPlayer import TkinterVideo

sys.path.append(PATH_TO_SQLITE)
sys.path.append(PATH_TO_REDDIT_API)
sys.path.append(PATH_TO_VIDEOS)

from redditVideos import get_video
from selectData import get_data
from database import refresh_data, insert_theme, remove_subreddit, remove_themes
from selectComments import get_comments
from selectTheme import get_themes

import webbrowser 
import subprocess

def callback(url):
    # Open website 
    webbrowser.open(url) 

class AudioPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.chunk = 1024
        self.paused = False
        self.play_thread = None

        # Open the audio file
        self.wf = wave.open(self.file_path, 'rb')

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()

        # Open stream
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)

    def play(self):
        data = self.wf.readframes(self.chunk)
        while data:
            while self.paused:
                time.sleep(0.1)
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def start(self):
        self.play_thread = threading.Thread(target=self.play)
        self.play_thread.start()

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def stop(self):
        if self.play_thread:
            self.play_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class WebImage:
    def __init__(self, url, width=None, height=None):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))

        # Resize the image if width and/or height are specified
        if width and height:
            image = image.resize((width, height), Image.LANCZOS)
        elif width:
            w_percent = width / float(image.size[0])
            h_size = int(float(image.size[1]) * float(w_percent))
            image = image.resize((width, h_size), Image.LANCZOS)
        elif height:
            h_percent = height / float(image.size[1])
            w_size = int(float(image.size[0]) * float(h_percent))
            image = image.resize((w_size, height), Image.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(image)

    def get(self):
        return self.tk_image


class Post:
    def __init__(self, title, content, subreddit, id, theme):
        self.id = id
        self.title = title
        self.content = content
        self.subreddit = subreddit
        self.theme = theme
        self.comments = []


class ScrollableFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


class Subreddits:
    def __init__(self, theme, subreddits):
        self.theme = theme
        self.subreddits = subreddits




          
class ForumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALL r/ In One")
        self.root.geometry("800x600")  # Set the initial window size

        # Dark mode theme configuration
        style = ttk.Style()
        style.theme_use("clam")  # Use the clam theme as a base

        root.configure(bg="#1c1c1c")  # Set the background color

        style.configure("TButton",
                        font=("Helvetica", 10),  # Set the font size for buttons
                        padding=(5, 5),  # Set padding for buttons
                        relief="flat",
                        background="#2b0945",  # Default background color for buttons
                        foreground="white",  # Default text color for buttons
                        hoverbackground="#4c246b",  # Background color for buttons on hover
                        )

        style.map("TButton",
                  background=[("active", "#4c246b")]  # Background color for buttons when clicked
                  )

        style.configure("TLabel",
                        font=("Helvetica", 12),  # Set the font size for labels
                        background="#1c1c1c",  # Dark background color for labels
                        foreground="white")  # White text for labels

        global THEME
        THEME = 'News'

        def toggle_menu():

            def collapse_toggle_menu():
                toggle_menu_frame.destroy()
                toggle_btn.config(text='☰')
                toggle_btn.config(command=toggle_menu)

            def home_page(theme):
                self.posts = []

                self.scrollable_frame = ScrollableFrame(self.scrollable_frame, bg="#2E2E2E")
                self.scrollable_frame.pack(fill="both", expand=True)

                selected_data = get_data(theme)
                for data in selected_data:
                    self.posts.append(Post(data[3], data[4], data[2], data[0], theme))

                # Change the title_label text
                page_title = theme
                app.title_label.config(text=f'/r ALL {page_title}')
                THEME = theme

                self.add_post_buttons()

            def delete_pages():
                for frame in self.scrollable_frame.winfo_children():
                    frame.destroy()

            def hide_indicators():
                home_indicate.config(bg='#2b0945')

            def indicate(lb, page, theme):
                global THEME
                THEME = theme
                hide_indicators()
                lb.config(bg='white')
                delete_pages()
                home_page(theme)
                #page()

            def edit_themes():
                def add_subreddits():
                    subreddits = simpledialog.askstring("Add Subreddits", "Enter Subreddits (comma-separated):")

                    if subreddits is not None:
                        temp = subreddits.split(',')
                        subreddit_list = [x.strip(' ') for x in temp]
                        insert_theme(theme, subreddit_list)
                    else:
                        print("User canceled the input.")
                       

                def remove_subreddits():
                    subreddits = simpledialog.askstring("Add Subreddits", "Enter Subreddits (comma-separated):")
                    if subreddits is not None:
                        temp = subreddits.split(',')
                        subreddit_list = [x.strip(' ') for x in temp]
                        remove_subreddit(theme, subreddit_list)
                    else:
                        print("User canceled the input.")

                def remove_theme():
                        remove_themes(theme)
                    


                theme = simpledialog.askstring("Edit Theme", "Which Theme You Want To Edit?")

                if theme is not None:
                    box = tk.Toplevel(root)

                    btn1 = tk.Button(box, text="Add Subreddits", command=add_subreddits)
                    btn1.pack(side="left", padx=5)

                    btn2 = tk.Button(box, text="Remove Subreddits", command=remove_subreddits)
                    btn2.pack(side="left", padx=5)

                    btn3 = tk.Button(box, text="Remove Theme", command=remove_theme)
                    btn3.pack(side="left", padx=5)

                    close_button = tk.Button(box, text="Close", command=box.destroy)
                    close_button.pack(pady=10)
                    
                    

                if flag == 1:
                    subreddits = simpledialog.askstring("Edit Theme", "Enter Subreddits (comma-separated):")

                    # Check if the user clicked Cancel
                    if theme is not None and subreddits is not None:
                        print(f"Theme: {theme}, Subreddits: {subreddits}")

                    else:
                        print("User canceled the input.")
                

            toggle_menu_frame = tk.Frame(root, bg='#2b0945')
            
            # Just an example for later, will need to add 60 to y in placement for each new button
        
            obj = get_themes()
            y = 20
            for key, value in obj.items():
                home_btn = tk.Button(toggle_menu_frame, text=key, font=('Bold', 15), bd=0, bg='#2b0945', fg='white',
                                    activebackground='#2b0945', activeforeground='white', command=lambda key=key: indicate(home_indicate, home_btn, key))
                home_btn.place(x=20, y=y)

                home_indicate = tk.Label(toggle_menu_frame, text='', bg='#2b0945')
                #home_indicate.place(x=3, y=y, width=5, height=40)

                y+=60


            window_height = root.winfo_height()

            edit_btn = tk.Button(toggle_menu_frame, text="Edit Themes", font=('Bold', 12), bd=0, bg='#2b0945', fg='white',
                                    activebackground='#2b0945', activeforeground='white', command=edit_themes)

            edit_btn.place(x=20, y=window_height-100)


            toggle_menu_frame.place(x=0, y=50, height=window_height, width=200)

            toggle_btn.config(text='X')
            toggle_btn.config(command=collapse_toggle_menu)


        
        head_frame = tk.Frame(root, bg='#2b0945', highlightbackground='white', highlightthickness=1)

        toggle_btn = tk.Button(head_frame, text='☰', bg='#2b0945', fg='white', font=('Bold', 20),
                                bd=0,activebackground='#2b0945', activeforeground='white', command=toggle_menu)
 
        toggle_btn.pack(side=tk.LEFT, anchor=tk.W)

        head_frame.pack(side=tk.TOP, fill=tk.X)
        head_frame.pack_propagate(False)
        head_frame.configure(height=50)

        
        


        self.posts = []
        page_title = '/r ALL'
        self.title_label = ttk.Label(root, text=page_title, font=("Helvetica", 18, "bold"), style="TLabel")
        self.title_label.pack(pady=10)

        self.scrollable_frame = ScrollableFrame(root, bg="#2E2E2E")
        self.scrollable_frame.pack(pady=10, fill="both", expand=True)

        themes = get_themes()
        if themes != None:
            for key in themes.keys():
                selected_data = get_data(key)
                for data in selected_data:
                    self.posts.append(Post(data[3], data[4], data[2], data[0], key))
            self.add_post_buttons()

        # Bind the mouse wheel event to the main window
        root.bind("<MouseWheel>", self.on_mousewheel)

        # Refresh button
        refresh_button = ttk.Button(root, text="Refresh", command= self.refresh_posts)
        refresh_button.pack(side="right", anchor="e", padx=10, pady=10)

        # Add theme button
        self.add_theme_button = tk.Button(root, text="Add Theme", command=self.show_theme_popup)
        self.add_theme_button.pack(side="left", anchor="e", padx=10, pady=10)

    def show_theme_popup(self):
        theme = simpledialog.askstring("Add Theme", "Enter Theme:")
        subreddits = simpledialog.askstring("Add Theme", "Enter Subreddits (comma-separated):")

        # Check if the user clicked Cancel
        if theme is not None and subreddits is not None:
            temp = subreddits.split(',')
            subreddit_list = [x.strip(' ') for x in temp]
            insert_theme(theme, subreddit_list)
        else:
            print("User canceled the input.")

        

    def add_post_buttons(self):
        global THEME
        for i, post in enumerate(self.posts):
            if post.theme == THEME:
                post_frame = tk.Frame(self.scrollable_frame.scrollable_frame, bg="#1c1c1c")
                post_frame.pack(pady=5, padx=75, fill='both')

                post_text = tk.Text(post_frame, wrap="word", bg="#1c1c1c", fg="white", padx=4, pady=1)

                if post.theme == "News":
                    post_text.tag_bind("content", "<Button-1>", lambda event, url=post.content: callback(url))
                    post_text.tag_configure("content", foreground="#5dade2", underline=True, font=("Helvetica", 12))
                    post_text.tag_bind("content", "<Enter>", lambda event: post_text.config(cursor="hand2"))
                    post_text.tag_bind("content", "<Leave>", lambda event: post_text.config(cursor=""))
                else:
                    post_text.tag_configure("content", font=("Helvetica", 12))


                post_text.tag_configure("title", font=("Helvetica", 16, "bold"), justify="center")
                post_text.tag_configure("subreddit", font=("Helvetica", 11))

                
                post_text.insert("1.0", f"r/{post.subreddit}", "subreddit")


                post_text.insert("1.0", f"{post.content}\n\n", "content")

                
                post_text.insert("1.0", f"{post.title}\n\n", "title")

                
                
                post_text.config(state=tk.DISABLED)  # Make the Text widget read-only

                post_text.grid(row=0, column=0, sticky="nsew")

                # Display image if the content ends with "png" or "jpg"
                if post.content.endswith(("png", "jpg", "jpeg")):
                    try:
                        post_text.config(height=10)
                        img = WebImage(url=post.content, width=640, height=640).get()
                        imagelab = tk.Label(post_frame, image=img)
                        imagelab.image = img  # Keep a reference to the image to prevent it from being garbage collected
                        imagelab.grid(row=1, column=0, sticky="nsew")
                    except HTTPError as e:
                        if e.code == 404:
                            print("Image not found. It may have been deleted.")
                            # Handle the situation accordingly, e.g., provide a default image or log the event
                        else:
                            print(f"HTTP Error {e.code}: {e.reason}")
                            # Handle other HTTP errors as needed

                ### TRYING TO ADD VIDEO PLAYER
                if post.content.startswith(("https://v.redd.it")):
                    button = ttk.Button(post_frame, text="View video", command=lambda p=post: self.view_video(p))
                    button.grid(row=3, column=0, sticky="w")
                    '''try:
                       
                        
                        

                    except HTTPError as e:
                        if e.code == 404:
                            print("Video not found. It may have been deleted.")
                            # Handle the situation accordingly, e.g., provide a default image or log the event
                        else:
                            print(f"HTTP Error {e.code}: {e.reason}")
                            # Handle other HTTP errors as needed'''
                
                

            
                button = ttk.Button(post_frame, text="View Comments", command=lambda p=post: self.view_comments(p))
                button.grid(row=2, column=0, sticky="w")


                # Set cursor on hover
                button.bind("<Enter>", lambda event, button=button: button.configure(cursor="hand2"))
                button.bind("<Leave>", lambda event, button=button: button.configure(cursor=""))


    def view_video(self, post):
        # Replace 'your_video_url' with the actual URL of the video you want to download
        video_url = get_video(post.id)

        # Download the video using requests
        response = requests.get(video_url)

        # Download the audio for the video
        
        pattern = re.compile(r'_(\d+)')

        # Insert "_AUDIO_128" before the last part of the URL
        audio_url = pattern.sub('', video_url)
        # Split the URL based on "/"
        url_parts = audio_url.split('/')
        audio_url = '/'.join(url_parts[:-1] + [url_parts[-1].replace('DASH', 'DASH_AUDIO_128')])
        response_audio = requests.get(audio_url)

        print(audio_url)

        if response.status_code == 200 and response_audio.status_code == 200:
            file_name = os.path.join(PATH_TO_VIDEOS, f"video_{post.id}.mp4")
            print(f"fileName = {file_name}")
            file_name_video = os.path.join(PATH_TO_VIDEOS, f"video_only_{post.id}.mp4")
            with open(file_name_video, 'wb') as video_file:
                video_file.write(response.content)
            print(f"Video downloaded successfully: {file_name_video}")

            file_name_audio = os.path.join(PATH_TO_VIDEOS, f"audio_{post.id}.mp4")
            with open(file_name_audio, 'wb') as audio_file:
                audio_file.write(response_audio.content)
            print(f"Video downloaded successfully: {file_name_audio}")


            def merge_audio_video(video_path, audio_path, output_path):
                # Load video and audio clips
                video_clip = VideoFileClip(video_path)
                audio_clip = AudioFileClip(audio_path)

                # Set video clip's audio to the loaded audio clip
                video_clip = video_clip.set_audio(audio_clip)

                # Write the result to a file
                video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                # Close the clips
                video_clip.close()
                audio_clip.close()

            if not os.path.exists(file_name):
                merge_audio_video(file_name_video, file_name_audio, file_name)

        
            def on_close():
                # Stop and release the media player before closing the window
                videoplayer.stop()
                videoplayer.release()
                root.destroy()

            def update_duration(event):
                """ updates the duration after finding the duration """
                duration = vid_player.video_info()["duration"]
                end_time["text"] = str(datetime.timedelta(seconds=duration))
                progress_slider["to"] = duration


            def update_scale(event):
                """ updates the scale value """
                progress_value.set(vid_player.current_duration())


            
            def display_and_play_video(file_name):
                """ displays and plays the video from the given file name """
                if file_name:
                    print(f"Now playing: {file_name}")
                    vid_player.load(file_name)
                    vid_player.play()  # Auto-play the video
                    audio_player.start()

                    progress_slider.config(to=0, from_=0)
                    play_pause_btn["text"] = "Pause"
                    progress_value.set(0)


            def seek(value):
                """ used to seek a specific timeframe """
                vid_player.seek(int(value))


            def skip(value: int):
                """ skip seconds """
                vid_player.seek(int(progress_slider.get())+value)
                progress_value.set(progress_slider.get() + value)


            def play_pause():
                """ pauses and plays """
                if vid_player.is_paused():
                    vid_player.play()
                    play_pause_btn["text"] = "Pause"
                    audio_player.pause()

                else:
                    vid_player.pause()
                    play_pause_btn["text"] = "Play"
                    audio_player.unpause()


            def video_ended(event):
                """ handle video ended """
                progress_slider.set(progress_slider["to"])
                play_pause_btn["text"] = "Play"
                progress_slider.set(0)
                audio_player.stop()


            root=tk.Toplevel(self.root)
    
            
            root.title(post.title)

            load_btn = tk.Button(root, text="Display Video", command=lambda: display_and_play_video(file_name))
            load_btn.pack()

            vid_player = TkinterVideo(scaled=True, master=root)
            vid_player.pack(expand=True, fill="both")
            audio_player = AudioPlayer(file_name_audio)

            play_pause_btn = tk.Button(root, text="Play", command=play_pause)
            play_pause_btn.pack()

            skip_plus_5sec = tk.Button(root, text="Skip -5 sec", command=lambda: skip(-5))
            skip_plus_5sec.pack(side="left")

            start_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
            start_time.pack(side="left")

            progress_value = tk.IntVar(root)

            progress_slider = tk.Scale(root, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
            # progress_slider.bind("<ButtonRelease-1>", seek)
            progress_slider.pack(side="left", fill="x", expand=True)

            end_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
            end_time.pack(side="left")

            vid_player.bind("<<Duration>>", update_duration)
            vid_player.bind("<<SecondChanged>>", update_scale)
            vid_player.bind("<<Ended>>", video_ended )

            skip_plus_5sec = tk.Button(root, text="Skip +5 sec", command=lambda: skip(5))
            skip_plus_5sec.pack(side="left")

            root.mainloop()
            
            
            
            '''root.protocol("WM_DELETE_WINDOW", on_close)

            videoplayer = TkinterVideo(master=root, scaled=True)
            videoplayer.load(file_name)
            videoplayer.pack(expand=True, fill="both")

            videoplayer.play() # play the video

            root.mainloop()'''


            ### TODO ###
            '''I need to download the audio file separately hen combine them, either manually or using a tool like ffmpeg.
             Also i need to add controlers to the VLC instance.'''

        else:
            print(f"Failed to download video. Status code: {response.status_code}")

    def view_comments(self, post):
        comment_window = tk.Toplevel(self.root)
        comment_window.title(f"Comments for {post.title}")

        comment_list = tk.Text(
            comment_window, wrap="word", width=50, height=10, bg="#1c1c1c", fg="white", padx=4, pady=2
        )
        comment_list.pack(pady=10)

        all_comments = get_comments(post.id)
        for comment in all_comments:
            post.comments.append(comment[0])

        comment_list.insert("1.0", "\n".join(f"Comment: {comment}\n" for comment in post.comments))
        comment_list.config(state=tk.DISABLED)  # Make the Text widget read-only

        close_button = ttk.Button(comment_window, text="Close", command=comment_window.destroy)
        close_button.pack(pady=10)

    def on_mousewheel(self, event):
        # Adjust the scrolling speed as needed
        self.scrollable_frame.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def refresh_posts(self):
        global THEME
        # Add logic here to refresh or update the posts
        print("Refreshing posts...")
        # For demonstration purposes, you can clear the existing posts and add new ones
        refresh_data(THEME)
        self.posts.clear()
        
        themes = get_themes()
        if themes != None:
            for key in themes.keys():
                selected_data = get_data(key)
                for data in selected_data:
                    self.posts.append(Post(data[3], data[4], data[2], data[0], key))


        # Clear existing widgets in the scrollable frame
        for widget in self.scrollable_frame.scrollable_frame.winfo_children():
            widget.destroy()

        # Add updated posts
        self.add_post_buttons()

    

# Example usage with different themes
themes = ['arc', 'black', 'blue', 'clearlooks', 'elegance', 'equilux', 'itft1', 'keramik', 'kroc', 'plastik',
          'radiance', 'scidthemes', 'smog', 'ubuntu', 'winxpblue', 'winnative']
if __name__ == "__main__":
    root = ThemedTk(theme="black")
    app = ForumApp(root)
    root.mainloop()
