import tkinter as tk


root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200, bg="light grey")
canvas.pack()

image = "Flag.gif"

image = tk.PhotoImage(file=image)
print(image.width(), image.height())
image = image.zoom(1)
print(image.width(), image.height())
image = image.subsample(2)
print(image.width(), image.height())

canvas.create_image(10, 10, image=image, anchor='nw')

root.mainloop()