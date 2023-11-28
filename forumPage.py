import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from paths import PATH_TO_SQLITE
import sys

sys.path.append(PATH_TO_SQLITE)
from selectData import get_data
from database import refresh_data, insert_theme
from selectComments import get_comments
from selectTheme import get_themes

class Post:
    def __init__(self, title, content, subreddit, id):
        self.id = id
        self.title = title
        self.content = content
        self.subreddit = subreddit
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

        root.configure(bg="#2E2E2E")  # Set the background color

        style.configure("TButton",
                        font=("Helvetica", 10),  # Set the font size for buttons
                        padding=(5, 5),  # Set padding for buttons
                        relief="flat",
                        background="#4CAF50",  # Default background color for buttons
                        foreground="white",  # Default text color for buttons
                        hoverbackground="#45a049",  # Background color for buttons on hover
                        )

        style.map("TButton",
                  background=[("active", "#45a049")]  # Background color for buttons when clicked
                  )

        style.configure("TLabel",
                        font=("Helvetica", 12),  # Set the font size for labels
                        background="#2E2E2E",  # Dark background color for labels
                        foreground="white")  # White text for labels

        style.configure("Red.TButton",
                background="red",  # Change background color to red
                hoverbackground="#CC0000"  # Hover background color for red
                )
        style.map("Red.TButton",
                  background=[("active", "#CC0000")]  # Background color for buttons when clicked
                  )

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
                    self.posts.append(Post(data[3], data[4], data[2], data[0]))

                

                self.add_post_buttons()

            def delete_pages():
                for frame in self.scrollable_frame.winfo_children():
                    frame.destroy()

            def hide_indicators():
                home_indicate.config(bg='grey')

            def indicate(lb, page, theme):
                print(theme)
                hide_indicators()
                lb.config(bg='white')
                delete_pages()
                home_page(theme)
                page()

            toggle_menu_frame = tk.Frame(root, bg='grey')
            
            # Just an example for later, will need to add 60 to y in placement for each new button
        
            obj = get_themes()
            y = 20
            for key, value in obj.items():
                print(f"key={key} value={value}")  
                home_btn = tk.Button(toggle_menu_frame, text=key, font=('Bold', 15), bd=0, bg='grey', fg='white',
                                    activebackground='grey', activeforeground='white', command=lambda key=key: indicate(home_indicate, home_btn, key))
                home_btn.place(x=20, y=y)

                home_indicate = tk.Label(toggle_menu_frame, text='', bg='grey')
                #home_indicate.place(x=3, y=y, width=5, height=40)

                y+=60


            window_height = root.winfo_height()
            toggle_menu_frame.place(x=0, y=50, height=window_height, width=200)

            toggle_btn.config(text='X')
            toggle_btn.config(command=collapse_toggle_menu)


        


        head_frame = tk.Frame(root, bg='grey', highlightbackground='white', highlightthickness=1)

        toggle_btn = tk.Button(head_frame, text='☰', bg='grey', fg='white', font=('Bold', 20),
                                bd=0,activebackground='grey', activeforeground='white', command=toggle_menu)
 
        toggle_btn.pack(side=tk.LEFT, anchor=tk.W)

        head_frame.pack(side=tk.TOP, fill=tk.X)
        head_frame.pack_propagate(False)
        head_frame.configure(height=50)

        
        


        self.posts = []

        self.title_label = ttk.Label(root, text="Forum Posts", font=("Helvetica", 16), style="TLabel")
        self.title_label.pack(pady=10)

        self.scrollable_frame = ScrollableFrame(root, bg="#2E2E2E")
        self.scrollable_frame.pack(pady=10, fill="both", expand=True)

        themes = get_themes()
        if themes != None:
            for key in themes.keys():
                print(key)
                selected_data = get_data(key)
                for data in selected_data:
                    self.posts.append(Post(data[3], data[4], data[2], data[0]))
            self.add_post_buttons()

        # Bind the mouse wheel event to the main window
        root.bind("<MouseWheel>", self.on_mousewheel)

        # Refresh button
        refresh_button = ttk.Button(root, text="Refresh", command=self.refresh_posts)
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
        for i, post in enumerate(self.posts):
            post_frame = tk.Frame(self.scrollable_frame.scrollable_frame, bg="#2E2E2E")
            post_frame.pack(pady=5, padx=75)

            post_text = tk.Text(post_frame, wrap="word", bg="#2E2E2E", fg="white", padx=4, pady=2)

            post_text.tag_configure("title", font=("Helvetica", 14, "bold"), justify="center")
            post_text.tag_configure("content", font=("Helvetica", 12))
            post_text.tag_configure("subreddit", font=("Helvetica", 11))

            post_text.insert("1.0", f"r/{post.subreddit}", "subreddit")
            post_text.insert("1.0", f"{post.content}\n\n", "content")
            post_text.insert("1.0", f"{post.title}\n\n", "title")
            
            post_text.config(state=tk.DISABLED)  # Make the Text widget read-only

            post_text.pack(expand=True, fill="both")

            button = ttk.Button(post_frame, text="View Comments", command=lambda p=post: self.view_comments(p))
            button.pack(side="left")

            # Set cursor on hover
            button.bind("<Enter>", lambda event, button=button: button.configure(cursor="hand2"))
            button.bind("<Leave>", lambda event, button=button: button.configure(cursor=""))

    def view_comments(self, post):
        comment_window = tk.Toplevel(self.root)
        comment_window.title(f"Comments for {post.title}")

        comment_list = tk.Text(
            comment_window, wrap="word", width=50, height=10, bg="#2E2E2E", fg="white", padx=4, pady=2
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
        # Add logic here to refresh or update the posts
        print("Refreshing posts...")

        # For demonstration purposes, you can clear the existing posts and add new ones
        refresh_data()
        self.posts.clear()
        
        themes = get_themes()
        if themes != None:
            for key in themes.keys():
                print(key)
                selected_data = get_data(key)
                for data in selected_data:
                    self.posts.append(Post(data[3], data[4], data[2], data[0]))


        # Clear existing widgets in the scrollable frame
        for widget in self.scrollable_frame.scrollable_frame.winfo_children():
            widget.destroy()

        # Add updated posts
        self.add_post_buttons()

    


if __name__ == "__main__":
    root = tk.Tk()
    app = ForumApp(root)
    root.mainloop()
