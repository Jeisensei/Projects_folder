import tkinter as tk



root = tk.Tk()
root.title("Hello, World!")
window_width = 300
window_height = 200
screen_width = root.winfo_screenmmwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
message = tk.Label(root, text="Hello, World!")
message.pack()
root.mainloop()
