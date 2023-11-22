import tkinter as tk
from tkinter import ttk
from paths import PATH_TO_SQLITE
import sys

sys.path.append(PATH_TO_SQLITE)
from selectData import get_data
from database import refresh_data
from selectComments import get_comments

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

class ForumPage(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.title("Forum Page")
        self.geometry("800x600")
        self.forum_app = ForumApp(self)

        

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

        

        self.posts = []

        self.title_label = ttk.Label(root, text="Forum Posts", font=("Helvetica", 16), style="TLabel")
        self.title_label.pack(pady=10)

        self.scrollable_frame = ScrollableFrame(root, bg="#2E2E2E")
        self.scrollable_frame.pack(pady=10, fill="both", expand=True)

        selected_data = get_data()
        for data in selected_data:
            self.posts.append(Post(data[3], data[4], data[2], data[0]))

        self.add_post_buttons()

        # Bind the mouse wheel event to the main window
        root.bind("<MouseWheel>", self.on_mousewheel)

        # Add a refresh button
        refresh_button = ttk.Button(root, text="Refresh", command=self.refresh_posts)
        refresh_button.pack(side="right", anchor="e", padx=10, pady=10)



   


        

    def add_post_buttons(self):
        for i, post in enumerate(self.posts):
            post_frame = tk.Frame(self.scrollable_frame.scrollable_frame, bg="#2E2E2E")
            post_frame.pack(pady=5, padx=10, anchor="w")

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
        
        selected_data = get_data()
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
