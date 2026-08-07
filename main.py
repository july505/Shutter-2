from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.storage.jsonstore import JsonStore

KV = r"""
#:import dp kivy.metrics.dp

<MainScreen>:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(10)

    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "SHUTTER PR"
        font_size: dp(30)
        bold: True
        size_hint_y: None
        height: dp(55)
        color: 0.08, 0.08, 0.08, 1

    Label:
        text: "Control de cargadores y recaudación"
        font_size: dp(15)
        size_hint_y: None
        height: dp(30)
        color: 0.25, 0.25, 0.25, 1

    BoxLayout:
        spacing: dp(10)

        Button:
            text: "PISTOLA\\nGRANDE"
            font_size: dp(20)
            bold: True
            background_normal: ""
            background_color: 0.18, 0.48, 0.80, 1
            on_release: root.add_large()

        Button:
            text: "PISTOLA\\nPEQUEÑA"
            font_size: dp(20)
            bold: True
            background_normal: ""
            background_color: 0.20, 0.65, 0.38, 1
            on_release: root.add_small()

    GridLayout:
        cols: 2
        spacing: dp(8)
        size_hint_y: None
        height: dp(120)

        Label:
            text: "GRANDES"
            bold: True
            font_size: dp(17)
            color: 0.08, 0.08, 0.08, 1
        Label:
            text: "PEQUEÑAS"
            bold: True
            font_size: dp(17)
            color: 0.08, 0.08, 0.08, 1

        Label:
            text: "Cargadores: " + str(root.large_count) + "\\nRecaudado: " + str(root.large_money) + " CUP"
            font_size: dp(17)
            color: 0.08, 0.08, 0.08, 1
        Label:
            text: "Cargadores: " + str(root.small_count) + "\\nRecaudado: " + str(root.small_money) + " CUP"
            font_size: dp(17)
            color: 0.08, 0.08, 0.08, 1

    BoxLayout:
        size_hint_y: None
        height: dp(48)
        spacing: dp(8)

        Button:
            text: "Deshacer grande"
            font_size: dp(14)
            on_release: root.undo_large()

        Button:
            text: "Deshacer pequeña"
            font_size: dp(14)
            on_release: root.undo_small()

    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        size_hint_y: None
        height: dp(150)

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(12)]

        Label:
            text: "TOTAL"
            bold: True
            font_size: dp(24)
            color: 0.08, 0.08, 0.08, 1

        Label:
            text: "Cargadores: " + str(root.total_count) + "\\nDinero: " + str(root.total_money) + " CUP"
            font_size: dp(22)
            bold: True
            color: 0.08, 0.08, 0.08, 1

    Button:
        text: "REINICIAR CONTROL"
        size_hint_y: None
        height: dp(52)
        font_size: dp(17)
        bold: True
        background_normal: ""
        background_color: 0.80, 0.18, 0.18, 1
        on_release: root.reset_confirm()
"""

class MainScreen(__import__("kivy.uix.boxlayout", fromlist=["BoxLayout"]).BoxLayout):
    large_count = NumericProperty(0)
    small_count = NumericProperty(0)
    large_money = NumericProperty(0)
    small_money = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore("shutter_pr.json")
        self.load_data()

    @property
    def total_count(self):
        return self.large_count + self.small_count

    @property
    def total_money(self):
        return self.large_money + self.small_money

    def save_data(self):
        self.store.put(
            "sales",
            large_count=self.large_count,
            small_count=self.small_count,
            large_money=self.large_money,
            small_money=self.small_money,
        )

    def load_data(self):
        if self.store.exists("sales"):
            data = self.store.get("sales")
            self.large_count = data.get("large_count", 0)
            self.small_count = data.get("small_count", 0)
            self.large_money = data.get("large_money", 0)
            self.small_money = data.get("small_money", 0)

    def add_large(self):
        self.large_count += 1
        self.large_money += 800 if self.large_count == 1 else 700
        self.save_data()

    def add_small(self):
        self.small_count += 1
        self.small_money += 500 if self.small_count == 1 else 400
        self.save_data()

    def undo_large(self):
        if self.large_count > 0:
            self.large_money -= 800 if self.large_count == 1 else 700
            self.large_count -= 1
            self.save_data()

    def undo_small(self):
        if self.small_count > 0:
            self.small_money -= 500 if self.small_count == 1 else 400
            self.small_count -= 1
            self.save_data()

    def reset_confirm(self):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label

        box = BoxLayout(orientation="vertical", padding=12, spacing=10)
        box.add_widget(Label(text="¿Seguro que quieres reiniciar el control?"))
        buttons = BoxLayout(spacing=8)
        yes = Button(text="Sí, reiniciar")
        no = Button(text="Cancelar")
        buttons.add_widget(yes)
        buttons.add_widget(no)
        box.add_widget(buttons)

        popup = Popup(
            title="Confirmar reinicio",
            content=box,
            size_hint=(0.85, 0.35),
            auto_dismiss=False,
        )

        no.bind(on_release=popup.dismiss)
        yes.bind(on_release=lambda *_: self.reset(popup))
        popup.open()

    def reset(self, popup):
        self.large_count = 0
        self.small_count = 0
        self.large_money = 0
        self.small_money = 0
        self.save_data()
        popup.dismiss()


class ShutterPRApp(App):
    title = "Shutter PR"

    def build(self):
        Builder.load_string(KV)
        return MainScreen()


if __name__ == "__main__":
    ShutterPRApp().run()
