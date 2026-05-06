import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.toast import toast

# Настройка для того, чтобы клавиатура не перекрывала поле ввода
Window.softinput_mode = "below_target"

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.bg_normal
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        MDTopAppBar:
            title: "Aviorum Architect"
            elevation: 4
            md_bg_color: self.theme_cls.primary_color

        MDTextField:
            id: ai_input
            hint_text: "Введите название проекта..."
            mode: "rectangle"
            multiline: True
            size_hint_y: None
            height: "120dp"
            font_size: "18sp"

        MDRaisedButton:
            text: "СОЗДАТЬ ПРОЕКТ"
            pos_hint: {"center_x": .5}
            size_hint_x: 1
            height: "50dp"
            on_release: app.create_project(ai_input)

        MDLabel:
            id: status_label
            text: "Готов к работе"
            halign: "center"
            theme_text_color: "Hint"
            font_style: "Caption"

        Widget:
'''

class AIAppArchitect(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def create_project(self, field):
        name = field.text.strip()
        if not name:
            toast("Поле пустое!")
            return
        
        # Очищаем название от лишних символов для папки
        folder_name = "".join([c for c in name if c.isalnum() or c in (' ', '_')]).strip()
        folder_name = folder_name.replace(" ", "_").lower()[:20]
        
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                self.root.ids.status_label.text = f"Папка создана: {folder_name}"
                toast("Успешно!")
                field.text = ""  # Полная очистка поля после создания
            else:
                self.root.ids.status_label.text = f"Уже есть: {folder_name}"
                toast("Папка уже существует")
        except Exception as e:
            toast("Ошибка доступа к памяти")
            self.root.ids.status_label.text = "Ошибка записи"

if __name__ == "__main__":
    AIAppArchitect().run()
