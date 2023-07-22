####Take Watermark-Image without any background
import time
import tkinter
from tkinter import *
from tkinter import ttk, Checkbutton
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np

from image import FinalImage, Watermark

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to fill the screen
root.geometry(f"{screen_width}x{screen_height-80}")



photo_folder = []
watermark_folder = []


def selected_img(event):
    global photo
    entry["state"] = "disabled"
    selected_file = photo_box.get(photo_box.curselection())
    photo = next(photo_selected for photo_selected in photo_folder if photo_selected.name==selected_file)

    watermark = photo.watermark_obj
    if watermark.watermark_type == "Label":
        watermark_text = watermark.watermark_content
        print("this is the watermark text: ", watermark_text)
        entry["state"]="normal"
        #text.set(watermark_text)

    else:
        entry["state"]="disabled"
    resize_canvas(event)
    print(photo)
    #resize_canvas(event)

def selected_watermark(event):
    selected_watermark_name = watermark_box.get(watermark_box.curselection())
    selected_watermark = next(watermark for watermark in watermark_folder if watermark.name==selected_watermark_name)
    photo.watermark_obj = selected_watermark
    photo.format_img()
    resize_canvas(None)
def change_watermark_size(event):
    print(photo.watermark_obj.watermark_content)
    photo.size_factor = slider.get()/100
    photo.format_img()
    print(photo.size_factor)
    resize_canvas(event)

def show_img(cur_photo):

    photo_displayed = ImageTk.PhotoImage(cur_photo)
    canvas.create_image(0, 0, image=photo_displayed, anchor="nw")
    canvas.image = photo_displayed
def resize_canvas(event):
    global resized_photo
    canvas_height = canvas.winfo_height()
    canvas_width = canvas.winfo_width()

    if photo != None:
        print(photo.height, photo.width)
        ratio = min(photo.height/canvas_height, photo.width/canvas_width )
        print(photo.height, photo.width, canvas_height, canvas_width)
        x = min(canvas_width, canvas_height/photo.ratio)
        y = x*photo.ratio

        resized_photo = photo.final_img.resize((int(x),int(y)))

        print(resized_photo)
        show_img(resized_photo)

def save():
    folder_path = filedialog.askdirectory()
    for to_save_photo in photo_folder:

        if folder_path:
            name_without_format = to_save_photo.name.split(".")[0]
            # Save the image using the PIL library
            file_path = f"{folder_path}/{name_without_format}_watermarked.png"
            to_save_photo.final_img.save(file_path)

def browse_img(button_id):
    filenames = filedialog.askopenfilenames(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Photo files",
                                                      "*.png*"),
                                                     ("all files",
                                                      "*.*")))
    if button_id == 2:
        new_watermark = Watermark(watermark_content=filenames[0], watermark_type="Image")
        watermark_folder.append(new_watermark)
        watermark_box.insert(END, new_watermark.name)
        upload_button["state"]="normal"


    elif button_id == 1:

        for item in filenames:
            new_image = FinalImage(item)
            new_image.add_watermark(watermark_folder[0])
            new_image.format_img()
            photo_folder.append(new_image)
            print(item)
            #print(new_image.watermark.height)
            photo_box.insert(END, new_image.name)
            photo_box.select_set(0)
            photo_box.event_generate("<<ListboxSelect>>")

    #if len(watermark_folder)!=0 and len(photo_folder)!=0:

def change_color(color_selected):
    colors_to_select = {
        "white":(255,255,255,255),
        "red": (255, 0, 0, 50),
        "original": {"Image": {"colored_img":photo.watermark_obj.img},
                     "Label": {"cur_color": photo.watermark_obj.original_color}
                     }
    }
    watermark_type = photo.watermark_obj.watermark_type
    print(watermark_type)
    if color_selected=="original":
        print(colors_to_select[color_selected][watermark_type])
        photo.watermark_obj.update_attributes(**colors_to_select[color_selected][watermark_type])

    else:
        photo.watermark_obj.cur_color = colors_to_select[color_selected]
        if watermark_type == "Image":
            photo.watermark_obj.color_image()

    photo.format_img()
    resize_canvas(None)


def apply_to_all():
    attributes = {
        "watermark_pos": photo.watermark_pos,
        "size_factor": photo.size_factor,
        "watermark_obj": photo.watermark_obj
    }
    for photo_selected in photo_folder:
        photo_selected.update_attributes(**attributes)
        photo_selected.format_img()

def change_pos(button_id):
    position = {
        "top left": (0, 0),
        "top right": (0, 1),
        "bottom left": (1, 0),
        "bottom right": (1, 1)
    }
    photo.watermark_pos = position[button_id]
    photo.format_img()
    resize_canvas(None)


def label_watermark():
    new_watermark = Watermark(watermark_type="Label")
    watermark_folder.append(new_watermark)
    watermark_box.insert(END, new_watermark.name)
    upload_button["state"]="normal"
    #browse_img(1)
    print("button was clicked")

def update_watermark_text(text):

    updated_text = text.get()
    print("----updated_text",updated_text)
    photo.watermark_obj.watermark_content = updated_text
    photo.format_img()
    resize_canvas(None)

def create_update_function(text_var):
    def update_watermark(*args, text_var=text_var):
        update_watermark_text(text_var)

    return update_watermark
#### Create two frames
frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root, padding=10)
root.grid_columnconfigure(0, weight=6, uniform="group1")
root.grid_columnconfigure(1, weight=4, uniform="group1")
root.grid_rowconfigure(0, weight=1)

frame1.grid(column=0, row=0, sticky='nsew',padx=10, pady=10)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_rowconfigure(0, weight=1)

# Set the width of frame2
frame2.grid(column=1, row=0, sticky='nsew',padx=10, pady=10)
frame2.grid_columnconfigure(0, weight=1)

###Frame1--The Preview of Final Image / Left Side
canvas = Canvas(frame1)
canvas.grid(column=0,row=0,sticky="nsew")
canvas.bind("<Configure>", resize_canvas)
print(frame1.winfo_width())
print(frame1.winfo_height())


###Frame2--All the different features / Right Side

#Selected Photos
upload_button = ttk.Button(frame2, text="Upload Photo",state="disabled", command=lambda: browse_img(1))
upload_button.grid(column=0, row=0)

photo_box = Listbox(frame2, height=5, exportselection=False)
photo_box.bind("<<ListboxSelect>>", selected_img)
photo_box.grid(columnspan=2, column=0, row=1)

#Select what kind of Watermark you want to have
#watermark_image_button = ttk.Button(frame2, text="Image", command=lambda: browse_img(2))
menu_button = ttk.Menubutton(frame2, text="Watermark")
menu_button.grid(column=1, row=0)

dropdown_menu = Menu(menu_button, tearoff=0)
dropdown_menu.add_command(label="Image", command=lambda: browse_img(2))
dropdown_menu.add_command(label="Label", command=label_watermark)

menu_button['menu'] = dropdown_menu

text = StringVar()
text.trace("w", create_update_function(text))
entry = Entry(frame2,name="entry", textvariable=text)
entry.grid(column=0, row=8)

watermark_box = Listbox(frame2, height=5)
watermark_box.bind("<<ListboxSelect>>", selected_watermark)
watermark_box.grid(columnspan=2, column=1, row=1)



#Size Slider
slider = Scale(frame2, from_=0, to=100, orient='horizontal', command=change_watermark_size)
slider.set(50)
slider.grid(column=0, row=2, columnspan=2, padx=10, pady=5)
colors = {
    1:[]
}



#Position Buttons
top_right_btn = ttk.Button(frame2, text="Top Left", command=lambda: change_pos("top left"))
top_right_btn.grid(column=0, row=4)

top_right_btn = ttk.Button(frame2, text="Top Right", command=lambda: change_pos("top right"))
top_right_btn.grid(column=1, row=4)

top_right_btn = ttk.Button(frame2, text="Bottom Left", command=lambda: change_pos("bottom left"))
top_right_btn.grid(column=0, row=5)

top_right_btn = ttk.Button(frame2, text="Bottom Right", command=lambda: change_pos("bottom right"))
top_right_btn.grid(column=1, row=5)

#Color Buttons
white_color_btn = ttk.Button(frame2,text="White", command=lambda :change_color("white"))
white_color_btn.grid(column=0,row=6)

red_color_btn = ttk.Button(frame2, text="Red", command=lambda : change_color("red"))
red_color_btn.grid(column=1, row=7)

original_color_btn = ttk.Button(frame2, text="Original Color", command=lambda: change_color("original"))
original_color_btn.grid(column=1, row=6)

#Apply and Save Button
apply_to_all_btn = ttk.Button(frame2, text="Apply to all", command=apply_to_all)
apply_to_all_btn.grid(column=0, row=9)

save_btn = ttk.Button(frame2, text="Save", command=save)
save_btn.grid(column=1, row=9)


root.mainloop()
