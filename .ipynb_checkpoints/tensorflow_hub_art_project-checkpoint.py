import os
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub
from tkinter import filedialog

hub_handle_1 = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1'
hub_handle_2 = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'


hub_module = hub.load(hub_handle_2)

hub_module = hub.load(hub_handle_2)

class App:

    def __init__(self, window, window_title, video_source=0):
        self.window=window
        self.window.title("Art Making Project - Tubo Lab, Tongmyong University")
        self.window.geometry("%dx%d" % (1300, 510))
        self.window.resizable(False, False)
        self.window.bind('<Escape>', lambda e: self.window.destroy())
        self.video_source=video_source

        self.vid= MyVideoCapture(self.video_source)
        self.canvas=tkinter.Canvas(window, width=self.vid.width*2, height=self.vid.height)
        self.canvas.pack()


        btn_frame=tkinter.Frame(window, background=self.from_rgb((211, 211, 211)))
        btn_frame.place(x=0,y=0, anchor="nw", width=1300)

        self.btn_snapshot=tkinter.Button(btn_frame, text="Capture Photo",width=15, command=self.snapshot, bg=self.from_rgb((52, 61, 70)), fg="white")
        self.btn_snapshot.pack(side="left", padx=10, pady=10)

        self.btn_about=tkinter.Button(btn_frame, text="Choose Art", width=10, command=self.choose_image, bg=self.from_rgb((52, 61, 70)), fg="white")
        self.btn_about.pack(side="left", padx=10, pady=10)
       
        self.btn_proses=tkinter.Button(btn_frame, text="Start Proses", width=15, command=self.process, bg=self.from_rgb((52, 61, 70)), fg="white")
        self.btn_proses.pack(side="left", padx=0, pady=10)

        self.art_image = None
       
        load = cv2.imread('tmp/missing.jpg')
        self.render = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(load))
        self.canvas.create_image(650,56, image=self.render, anchor=tkinter.NW)

        self.delay=15
        self.update()

        self.window.mainloop()

    def load_status(self, msg):
        statusbar = tkinter.Label(self.window, text = msg, bd = 1, relief = tkinter.SUNKEN, anchor = tkinter.W)
        statusbar.pack(side = tkinter.BOTTOM, fill = tkinter.X)
       
       
    def choose_image(self):
        self.load_status("Art Image Selected ....")
        self.art_image = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select BMP File", filetypes=[("BMP Files","*.jpg, *.jpg")])

    def snapshot(self):
        ret, frame=self.vid.get_frame()

        if ret:
            self.load_status("Image Captured ....")            
            cv2.imwrite("tmp/temp.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) )
           
    def process(self):
        self.makeArt()
        load = cv2.imread('art_is_ready.jpg', cv2.COLOR_RGB2BGR)
        self.render = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(load))
        self.canvas.create_image(650,56, image=self.render, anchor=tkinter.NW)
       
    def tensor_to_image(self, tensor):
        tensor = tensor*255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor)>3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
        return PIL.Image.fromarray(tensor)

    def load_img(self, path_to_img):
      max_dim = 640
      img = tf.io.read_file(path_to_img)
      img = tf.image.decode_image(img, channels=3)
      img = tf.image.convert_image_dtype(img, tf.float32)
   
      shape = tf.cast(tf.shape(img)[:-1], tf.float32)
      long_dim = max(shape)
      scale = max_dim / long_dim
   
      new_shape = tf.cast(shape * scale, tf.int32)
   
      img = tf.image.resize(img, new_shape)
      img = img[tf.newaxis, :]
      return img
   
   
    def makeArt(self):
        content_image = self.load_img('tmp/temp.jpg')
        style_image = self.load_img(self.art_image)

       
        stylized_image = hub_module(tf.constant(content_image), tf.constant(style_image))[0]
        self.tensor_to_image(stylized_image).save("final.jpg")
           

    def openFolder(self):       
        path=os.path.join(os.path.abspath(os.getcwd()), 'art_is_ready.jpg')
        command = 'explorer.exe ' + path
        os.system(command)
       
       
       
    def update(self):
        ret, frame=self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,56, image=self.photo, anchor=tkinter.NW)
            self.window.after(self.delay,self.update)

    def from_rgb(self,rgb):
        return "#%02x%02x%02x" % rgb
    

class  MyVideoCapture:
    def __init__(self, video_source=0): #0
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("unable open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH) #640
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) #480
       
       

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret,None)        
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()