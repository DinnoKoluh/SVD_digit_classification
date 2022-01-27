import cv2 as cv
import matplotlib.pyplot as plt
from tkinter import *
from PIL import ImageGrab

def process_img(name):
    img = plt.imread(name)
    img = cv.resize(img[:,:,1],(16,16)) # has 3 for RGB coloring
    #img = np.float64(img[:,:,1])/255
    y_img = img.reshape(256,)
    plt.imshow(img.reshape(16,16), cmap='gray')
    return y_img

# https://pythonprogramming.altervista.org/draw-in-tkinters-canvas/?doing_wp_cron=1642695015.1103270053863525390625
def draw_digit():
    def paint(event):
        thickness = 10
        # get x1, y1, x2, y2 co-ordinates
        x1, y1 = (event.x-thickness), (event.y-thickness)
        x2, y2 = (event.x+thickness), (event.y+thickness)
        color = "white"
        # display the mouse movement inside canvas
        wn.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def save(event):
        x=root.winfo_rootx()+wn.winfo_x()
        y=root.winfo_rooty()+wn.winfo_y()
        x1=x+wn.winfo_width()
        y1=y+wn.winfo_height()
        im = ImageGrab.grab((x, y, x1, y1))
        im.save("digit.png")
    
    # create canvas
    #name = "./my_digits/digit.png"
    name = "digit.png"
    root = Tk()
    root.title("Paint Application")
    size = 200
    root.geometry(str(size)+"x"+str(size))

    wn=Canvas(root, width=size, height=size, bg='black')
    # bind mouse event with canvas(wn)
    wn.bind('<B1-Motion>', paint)
    # bind saving the canvas with ctrl+s
    root.bind("<Control-s>", save)
    wn.pack(expand=YES, fill=BOTH)
    root.mainloop()
    return name