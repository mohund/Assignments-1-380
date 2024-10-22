from jes4py import *
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor

# Global variable to hold the original image and modified image
original_image = None
modified_image = None

def load_image():
    global original_image, modified_image
    file_path = filedialog.askopenfilename()
    original_image = makePicture(file_path)
    modified_image = duplicatePicture(original_image)
    show(modified_image)

def save_image():
    global modified_image
    # يسمح بجميع أنواع الملفات الشائعة
    file_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",  # الافتراضي هو JPG
        filetypes=[
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        # التحقق من إضافة الامتداد إذا لم يكتب المستخدم امتداد
        if not (file_path.endswith(".jpg") or file_path.endswith(".png") or 
                file_path.endswith(".gif") or file_path.endswith(".bmp")):
            file_path += ".jpg"  # إضافة ".jpg" كامتداد افتراضي إذا لم يتم تحديد امتداد
        
        # حفظ الصورة في المسار المحدد
        writePictureTo(modified_image, file_path)


def reset_image():
    global modified_image
    modified_image = duplicatePicture(original_image)
    show(modified_image)

def change_color():
    global modified_image
    color = askcolor()[0]
    if color:
        for px in getPixels(modified_image):
            r, g, b = getRed(px), getGreen(px), getBlue(px)
            setColor(px, makeColor(min(255, int(r * color[0] / 255)),
                                   min(255, int(g * color[1] / 255)),
                                   min(255, int(b * color[2] / 255))))
        show(modified_image)

def rotate_image(angle):
    global modified_image
    width, height = getWidth(modified_image), getHeight(modified_image)
    rotated_pic = makeEmptyPicture(height, width)  # Empty picture for rotated image
    for x in range(width):
        for y in range(height):
            p = getPixel(modified_image, x, y)
            setColor(getPixel(rotated_pic, y, width - 1 - x), getColor(p))
    modified_image = rotated_pic
    show(modified_image)

def scale_image(scale_factor):
    global modified_image
    width, height = getWidth(modified_image), getHeight(modified_image)
    scaled_width, scaled_height = int(width * scale_factor), int(height * scale_factor)
    scaled_pic = makeEmptyPicture(scaled_width, scaled_height)
    
    for x in range(scaled_width):
        for y in range(scaled_height):
            orig_x, orig_y = int(x / scale_factor), int(y / scale_factor)
            p = getPixel(modified_image, orig_x, orig_y)
            setColor(getPixel(scaled_pic, x, y), getColor(p))  # Use setColor to set the color in the scaled image
    
    modified_image = scaled_pic
    show(modified_image)

def posterize_image(levels):
    global modified_image
    for p in getPixels(modified_image):
        r, g, b = getRed(p), getGreen(p), getBlue(p)
        r = int(r / (256 / levels)) * (256 // levels)
        g = int(g / (256 / levels)) * (256 // levels)
        b = int(b / (256 / levels)) * (256 // levels)
        setColor(p, makeColor(r, g, b))
    show(modified_image)

def apply_transformations():
    if rotate_var.get():
        angle = int(rotation_entry.get())
        rotate_image(angle)
    if scale_var.get():
        scale_factor = float(scale_entry.get())
        scale_image(scale_factor)
    if color_var.get():
        change_color()
    if posterize_var.get():
        levels = int(posterize_entry.get())
        posterize_image(levels)

# GUI
root = Tk()
root.title("Image Manipulation")

# Frame for the load, save, and reset buttons
top_frame = Frame(root)
top_frame.pack(pady=10)

Button(top_frame, text="Load Image", command=load_image).grid(row=0, column=0, padx=5)
Button(top_frame, text="Save Image", command=save_image).grid(row=0, column=1, padx=5)
Button(top_frame, text="Reset", command=reset_image).grid(row=0, column=2, padx=5)

# Frame for transformation options
options_frame = Frame(root)
options_frame.pack(pady=10)

rotate_var = BooleanVar()
scale_var = BooleanVar()
color_var = BooleanVar()
posterize_var = BooleanVar()

Checkbutton(options_frame, text="Rotate", variable=rotate_var).grid(row=0, column=0, sticky='w', padx=5)
rotation_entry = Entry(options_frame, width=10)
rotation_entry.grid(row=0, column=1, padx=5)

Checkbutton(options_frame, text="Scale", variable=scale_var).grid(row=1, column=0, sticky='w', padx=5)
scale_entry = Entry(options_frame, width=10)
scale_entry.grid(row=1, column=1, padx=5)

Checkbutton(options_frame, text="Change Color", variable=color_var).grid(row=2, column=0, sticky='w', padx=5)

Checkbutton(options_frame, text="Posterize", variable=posterize_var).grid(row=3, column=0, sticky='w', padx=5)
posterize_entry = Entry(options_frame, width=10)
posterize_entry.grid(row=3, column=1, padx=5)

# Frame for the action buttons
bottom_frame = Frame(root)
bottom_frame.pack(pady=10)

Button(bottom_frame, text="Apply Transformations", command=apply_transformations).grid(row=0, column=0, padx=5)
Button(bottom_frame, text="Save Image", command=save_image).grid(row=0, column=1, padx=5)

root.mainloop()
