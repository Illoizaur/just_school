import tkinter as tk
import random
from tkinter import font

# Список відповідей Magic 8-Ball
ANSWERS = [
    # Позитивні відповіді
    "Так, точно",
    "Усе добре",
    "Без сумніву",
    "Це так",
    "Найімовірніше",
    
    # Нейтральні відповіді
    "Можливо",
    "Не впевнено",
    "Питай пізніше",
    "Краще не говорити",
    "Зараз не можу сказати",
    
    # Негативні відповіді
    "Ні",
    "Не думаю",
    "Дуже сумніваюсь",
    "Не сподівайся",
    "Категорично ні",
]

class MagicEightBall:
    def __init__(self, root):
        self.root = root
        self.root.title("Magic 8-Ball")
        self.root.geometry("600x750")
        self.root.configure(bg="#1a1a1a")
        
        # Заголовок
        title_font = font.Font(family="Arial", size=36, weight="bold")
        title_label = tk.Label(
            self.root, 
            text="Magic 8-Ball", 
            font=title_font,
            fg="#FFD700",
            bg="#1a1a1a"
        )
        title_label.pack(pady=30)
        
        # Кулька (чорний круг з відповіддю)
        self.ball_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.ball_frame.pack(pady=30)
        
        self.canvas = tk.Canvas(
            self.ball_frame,
            width=350,
            height=350,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Рисуємо кульку
        self.canvas.create_oval(15, 15, 335, 335, fill="#000000", outline="#FFD700", width=4)
        
        # Вікно для відповіді в центрі кульки
        self.canvas.create_oval(100, 100, 250, 250, fill="#1a1a1a", outline="#666666", width=2)
        
        self.answer_text = self.canvas.create_text(
            175, 175,
            text="?",
            font=("Arial", 32, "bold"),
            fill="#FFD700"
        )
        
        # Інструкція
        instruction_font = font.Font(family="Arial", size=14)
        instruction = tk.Label(
            self.root,
            text="Задай запитання і натисни кнопку",
            font=instruction_font,
            fg="#CCCCCC",
            bg="#1a1a1a"
        )
        instruction.pack(pady=10)
        
        # Кнопка для тремтіння кульки
        button_font = font.Font(family="Arial", size=16, weight="bold")
        self.shake_button = tk.Button(
            self.root,
            text="Тремтіти кульку 🎱",
            font=button_font,
            command=self.shake_ball,
            bg="#FFD700",
            fg="#000000",
            padx=30,
            pady=15,
            cursor="hand2"
        )
        self.shake_button.pack(pady=40)
        
        self.is_shaking = False
    
    def shake_ball(self):
        if self.is_shaking:
            return
        
        self.is_shaking = True
        self.shake_button.config(state="disabled")
        
        # Анімація тремтіння
        self.animate_shake(0)
    
    def animate_shake(self, count):
        if count < 20:
            # Змінюємо текст під час тремтіння
            texts = ["?", "8", ".", "..", "..."]
            self.canvas.itemconfig(self.answer_text, text=random.choice(texts))
            self.root.after(50, self.animate_shake, count + 1)
        else:
            # Показуємо випадкову відповідь
            answer = random.choice(ANSWERS)
            self.canvas.itemconfig(self.answer_text, text=answer)
            
            self.is_shaking = False
            self.shake_button.config(state="normal")

# Створюємо вікно
root = tk.Tk()
app = MagicEightBall(root)
root.mainloop()

