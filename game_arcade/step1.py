"""
Шпаргалочка:
1. arcade.View — клас для створення окремих сцен (меню, гра, пауза). Кожен View має свої методи:
   - on_show_view: виконується 1 раз при відкритті сцени (зміна фону, завантаження ресурсів).
   - on_draw: виконується ~60 разів на секунду для малювання графіки.
   - on_key_press: обробка натискань клавіш.

2. arcade.gui.UIManager — головний менеджер інтерфейсу. Він "слухає" події мишки та кнопок.
   - .enable(): обов'язково вмикає відстеження подій.
   - .draw(): малює всі додані кнопки та віджети.

3. Контейнери (Layouts):
   - UIAnchorLayout: дозволяє "прикріпити" елементи до центру або країв екрана (anchor_x/y).
   - UIBoxLayout: автоматично розставляє елементи в стовпчик (вертикально) або в рядок.

4. arcade.Text — об'єкт тексту. Створюється в __init__, щоб не витрачати ресурси на 
   створення тексту кожного кадру в on_draw.
"""

import arcade
import arcade.gui

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Terraria Clone 0.1.0"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.anchor_layout = arcade.gui.UIAnchorLayout()

        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="ГРАТИ", width=200)
        self.v_box.add(start_button.with_padding(bottom=20))

        exit_button = arcade.gui.UIFlatButton(text="ВИХІД", width=200)
        self.v_box.add(exit_button)

        start_button.on_click = self.on_click_start
        exit_button.on_click = self.on_click_exit

        self.anchor_layout.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.manager.add(self.anchor_layout)

        self.title_text = arcade.Text(
            "CRAFT-CLONE 2D",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 100,
            arcade.color.GOLDENROD,
            font_size=50,
            anchor_x="center"
        )

    def on_click_start(self, event):
        self.window.show_view(GameView())

    def on_click_exit(self, event):
        arcade.exit()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        self.manager.draw()

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.info_text = arcade.Text(
            "ЕКРАН ГРИ\nТут почнеться генерація світу.\nНатисніть ESC для повернення",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
            multiline=True,
            width=400
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()
        self.info_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(MenuView())
    arcade.run()

if __name__ == "__main__":
    main()