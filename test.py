import tkinter as tk

root = tk.Tk()
root.title("Just School")
root.geometry("400x300")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

label_width = tk.Label(root, text=f"Screen Width: {screen_width}", font=("Arial", 26))
label_width.pack(pady=20)

label_height = tk.Label(root, text=f"Screen Height: {screen_height}", font=("Arial", 26))
label_height.pack(pady=20)

root.mainloop()