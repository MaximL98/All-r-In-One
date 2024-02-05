import tkinter as tk
from PIL import Image
from dotenv import dotenv_values

config = dotenv_values("config.env")
PATH_TO_VIDEOS = config['PATH_TO_VIDEOS']
sys.path.append(PATH_TO_VIDEOS)


class GifDisplay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gif Player")
        #self.attributes('-fullscreen', True)
        self.state("zoomed")
        self.configure(bg="#302f2f")
        self.create_widgets()

    def create_widgets(self):
        self.media_canvas = tk.Canvas(self, bg="black", width=700, height=350)
        self.media_canvas.pack(pady=10, fill=tk.BOTH, expand=True)

        self.control_buttons_frame = tk.Frame(self, bg="#302f2f")
        self.control_buttons_frame.pack(pady=5)

        self.gif_label = tk.Label(self.media_canvas, image="")
        self.gif_label.pack()

        '''self.start = tk.Button(self.control_buttons_frame, text="Start", command=lambda: self.animation(current_frame=0))
        self.start.pack()'''

        '''self.stop = tk.Button(self.control_buttons_frame, text="Stop", command=stop_animation)
        self.stop.pack()'''

    def display_gif(self, file_name):
        self.file = file_name
        self.info = Image.open(self.file)
        current_frame=0
        frames = self.info.n_frames  # number of frames

        photoimage_objects = []
        for i in range(frames):
            obj = tk.PhotoImage(file=self.file, format=f"gif -index {i}")
            photoimage_objects.append(obj)

        global loop
        self.image = photoimage_objects[current_frame]

        self.gif_label.configure(image=self.image)
        current_frame = current_frame + 1

        if current_frame == frames:
            current_frame = 0

        self.loop = self.media_canvas.after(50, lambda: display_gif(current_frame))


    def stop_animation(self):
        self.media_canvas.after_cancel(self.loop)


    
if __name__ == "__main__":
    root = GifDisplay()
    root.mainloop()
