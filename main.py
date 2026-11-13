from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class BashnetApp(App):

    def build(self):
        self.title = "BASHNET"

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        self.status = Label(
            text="BASHNET CORE 13\n\nANDROID APK TEST",
            font_size=24
        )

        button = Button(
            text="CHECK BASHNET",
            font_size=20
        )

        button.bind(on_press=self.check_system)

        layout.add_widget(self.status)
        layout.add_widget(button)

        return layout

    def check_system(self, instance):
        self.status.text = (
            "BASHNET CORE ACTIVE\n\n"
            "ANDROID APP RUNNING\n"
            "NEXT: BLUETOOTH CONNECTION"
        )


if __name__ == "__main__":
    BashnetApp().run()