import tkinter as tk
from tkinter import ttk
from forumPage import ForumPage

class MainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("Main Page")
        self.pack(fill=tk.BOTH, expand=True)
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d" % (width, height))

        # Use ttk.Style for a modern look
        style = ttk.Style()
        style.configure('main.TButton', font=('Helvetica', 12), padding=10)
        style.configure('main.TFrame', background='#f0f0f0')

        # Create themed buttons for other pages
        button1 = ttk.Button(self, text="News", command=self.open_forum_page, style = "main.TButton")
        button2 = ttk.Button(self, text="Page 2", command=self.open_page2, style = "main.TButton")
        button3 = ttk.Button(self, text="Page 3", command=self.open_page3, style = "main.TButton")

        # Position the buttons in the middle
        button1.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        button2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button3.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Create "Add New Theme" themed button
        add_theme_button = ttk.Button(self, text="Add New Theme", command=self.add_new_theme)
        add_theme_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def open_forum_page(self):
        # Hide the main window
        # self.master.iconify()
        forum_page = ForumPage(self.master)

    def open_page2(self):
        # Add functionality to open Page 2
        print("Opening Page 2")

    def open_page3(self):
        # Add functionality to open Page 3
        print("Opening Page 3")

    def add_new_theme(self):
        # Add functionality for "Add New Theme" button
        print("Adding New Theme")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()
