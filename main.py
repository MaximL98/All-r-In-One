import tkinter as tk
from tkinter import ttk, scrolledtext
from redditAPI.redditAPI import DATA

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content
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

class ForumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Forum")
        self.root.geometry("800x600")  # Set the initial window size

        # Dark mode theme configuration
        style = ttk.Style()
        style.theme_use("clam")  # Use the clam theme as a base

        root.configure(bg="#2E2E2E")  # Set the background color

        style.configure("TButton",
                        font=("Helvetica", 10),   # Set the font size for buttons
                        padding=(5, 5),            # Set padding for buttons
                        relief="flat",
                        background="#4CAF50",      # Default background color for buttons
                        foreground="white",        # Default text color for buttons
                        hoverbackground="#45a049", # Background color for buttons on hover
                        )

        style.map("TButton",
                  background=[("active", "#45a049")]  # Background color for buttons when clicked
                  )

        style.configure("TLabel",
                        font=("Helvetica", 12),  # Set the font size for labels
                        background="#2E2E2E",    # Dark background color for labels
                        foreground="white")       # White text for labels

        self.posts = []

        self.title_label = ttk.Label(root, text="Forum Posts", font=("Helvetica", 16), style="TLabel")
        self.title_label.pack(pady=10)

        self.scrollable_frame = ScrollableFrame(root, bg="#2E2E2E")
        self.scrollable_frame.pack(pady=10, fill="both", expand=True)

        for i in range(len(DATA)):
            self.posts.append(Post(DATA['title'], DATA['secure_media']))

        self.add_post_buttons()

    def add_post_buttons(self):
        for i, post in enumerate(self.posts):
            post_frame = tk.Frame(self.scrollable_frame.scrollable_frame, bg="#2E2E2E")
            post_frame.pack(pady=5, padx=10, anchor="w")

            post_label = ttk.Label(post_frame, text=f"Title: {post.title}\nContent: {post.content}", style="TLabel")
            post_label.pack()

            button = ttk.Button(post_frame, text="View Comments", command=lambda p=post: self.view_comments(p))
            button.pack(side="left")

            # Set cursor on hover
            button.bind("<Enter>", lambda event, button=button: button.configure(cursor="hand2"))
            button.bind("<Leave>", lambda event, button=button: button.configure(cursor=""))

    def view_comments(self, post):
        comment_window = tk.Toplevel(self.root)
        comment_window.title(f"Comments for {post.title}")

        comment_list = scrolledtext.ScrolledText(comment_window, width=50, height=10, wrap=tk.WORD, bg="#2E2E2E", fg="white")
        comment_list.pack(pady=10)

        for comment in post.comments:
            comment_list.insert(tk.END, f"Comment: {comment}\n\n")

        close_button = ttk.Button(comment_window, text="Close", command=comment_window.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ForumApp(root)
    root.mainloop()








