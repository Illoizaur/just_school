import mouse  
import keyboard
import tkinter as tk
from tkinter import messagebox

running = False   
delay = 0 

def start_clicker():
    global running, delay     
    
    try:
        clicks_per_second = int(вап.get())
        if clicks_per_second <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть ціле число більше 0!")
        return

    delay = int(1000 / clicks_per_second) 
    
    messagebox.showinfo("Auto Clicker", "Auto Clicker розпочинає роботу.")
    running = True
    schedule_click()

def schedule_click():
    if running:
        mouse.click()
        фіва.after(delay, schedule_click)

def exit_app():
    global running    
    running = False
    фіва.destroy()

def show_info(event):
    messagebox.showinfo("Інформація", "Це автоклікер, він буде клікати мишкою зі швидкістю, яку ти вкажеш!")

фіва = tk.Tk()
фіва.title("авто клікер (фіва)")

авіф = tk.Label(фіва, text="авто клікер (фіва) версія 1.0", font=("Roboto", 25))
авіф.pack()

вап = tk.Entry(фіва, font=("Roboto", 20))
вап.pack()

keyboard.add_hotkey('esc', exit_app)  
keyboard.add_hotkey('F1', start_clicker)

пав = tk.Button(фіва, text="старт", font=("Roboto", 15), command=start_clicker)
пав.pack()

віф = tk.Button(фіва, text="фініш", font=("Roboto", 15), command=exit_app)
віф.pack()

фіва.mainloop()