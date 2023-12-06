import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from ttkthemes import ThemedTk
from paths import PATH_TO_SQLITE
import sys

import urllib.request
from urllib.error import HTTPError
import io
from PIL import ImageTk, Image

sys.path.append(PATH_TO_SQLITE)
from selectData import get_data
from database import refresh_data, insert_theme
from selectComments import get_comments
from selectTheme import get_themes

import webbrowser 

def callback(url):
    # Open website 
    webbrowser.open(url) 

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
            print(f"Theme: {theme}, Subreddits: {subreddits}")
            insert_theme(theme,subreddits.split(','))
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

            
                button = ttk.Button(post_frame, text="View Comments", command=lambda p=post: self.view_comments(p))
                button.grid(row=2, column=0, sticky="w")


                # Set cursor on hover
                button.bind("<Enter>", lambda event, button=button: button.configure(cursor="hand2"))
                button.bind("<Leave>", lambda event, button=button: button.configure(cursor=""))

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
