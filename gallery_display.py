# importing the tkinter module and PIL
# that is pillow module
from tkinter import *
from PIL import ImageTk, Image

from dotenv import dotenv_values
import sys
import urllib.request
from urllib.error import HTTPError
import io

config = dotenv_values("config.env")
PATH_TO_REDDIT_API = config["PATH_TO_REDDIT_API"]
sys.path.append(PATH_TO_REDDIT_API)
from redditGallery import get_gallery


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



class GalleryDisplay(Toplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.title("Image Gallery")
        self.state("zoomed")
        self.configure(bg="#302f2f")
        self.List_images = []  # List to store image URLs
        self.x_size = []      # List to store original image widths
        self.y_size = []      # List to store original image heights
        self.img = None
        self.img_no = 0
        self.create_widgets()
        

    def create_widgets(self):
        window_width = 1920
        padx = window_width/4
        # List of the images so that we traverse the list
        self.media_canvas = Frame(self, bg="black", width=1000, height=500)
        self.media_canvas.pack(pady=10, fill=BOTH, expand=True)
        self.label = Label(self.media_canvas)
        self.label.pack()

        self.count_label = Label(
            self,
            text=f"",
            font=("Arial", 12, "bold"),
            fg="#555555",
            bg="#f0f0f0",
        )
        self.count_label.pack(pady=5)
        self.control_buttons_frame = Frame(self, bg="#302f2f")
        self.control_buttons_frame.pack(pady=5)


        # We will have three button back ,forward and exit
        self.button_back = Button(
                self.control_buttons_frame,
                text="Back",
                font=("Arial", 10, "bold"),
                bg="#2196F3",
                fg="white",
                command=self.back,
            )					
        self.button_forward = Button(
                self.control_buttons_frame,
                text="Forward",
                font=("Arial", 10, "bold"),
                bg="#2196F3",
                fg="white",
                command=self.forward,
            )

        # grid function is for placing the buttons in the frame
        self.button_back.pack(side=LEFT, padx=padx-20, pady=90)
        self.button_forward.pack(side=LEFT, padx=padx-50, pady=90)

        if self.img_no == 0:
            self.button_back['state'] = DISABLED
        else:
            self.button_back['state'] = NORMAL

    def display_gallery(self, post_id="18zrxvz"):
        self.List_images, self.x_size, self.y_size = get_gallery(post_id)
        self.update_image(self.img_no)

    def update_image(self, index):
        # Create the WebImage object and get the tk_image
        web_image = WebImage(url=self.List_images[index],
                                width=(self.x_size[index])//2 + 100, 
                                height=(self.y_size[index])//2 + 100)
        self.img = web_image.get()  # Store the tk_image reference in self.img

        self.count_label.configure(text=f"{index+1} out of {len(self.List_images)}")
        self.label.configure(image=self.img)
        self.label.image = self.img  # Maintain a reference to the image

    def forward(self):
        self.img_no+=1

        if self.img_no > 0:
            self.button_back['state'] = NORMAL
        
        if self.img_no + 1 == len(self.List_images):
            self.button_forward['state'] = DISABLED

        self.img = WebImage(url=self.List_images[self.img_no], width=(self.x_size[self.img_no])//2 + 100, height=(self.y_size[self.img_no])//2 + 100).get()
        self.label.configure(image=self.img)
        self.label.image=self.img
        self.count_label.configure(text=f"{self.img_no+1} out of {len(self.List_images)}")
            
    def back(self):
        self.img_no-=1    
        
        if self.img_no + 1 < len(self.List_images):
            self.button_forward['state'] = NORMAL

        if self.img_no - 1 == 0:
            self.button_back['state'] = DISABLED

        self.img = WebImage(url=self.List_images[self.img_no], width=(self.x_size[self.img_no])//2 + 100, height=(self.y_size[self.img_no])//2 + 100).get()
        self.label.configure(image=self.img)
        self.label.image=self.img
        self.count_label.configure(text=f"{self.img_no+1} out of {len(self.List_images)}")