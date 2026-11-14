from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class BashnetApp(App):

    def build(self):
        self.title = "BASHNET"

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        self.status = Label(
            text="BASHNET CORE 14\n\nSYSTEM ACTIVE",
            font_size=23,
            size_hint_y=None,
            height=120
        )

        self.device_status = Label(
            text="BLUETOOTH: NOT SCANNING",
            font_size=16,
            size_hint_y=None,
            height=50
        )

        self.device_list = Label(
            text="NO DEVICES FOUND",
            font_size=17,
            size_hint_y=None,
            height=100
        )

        scan_button = Button(
            text="START SCANNING",
            font_size=20,
            size_hint_y=None,
            height=60
        )

        stop_button = Button(
            text="STOP SCANNING",
            font_size=20,
            size_hint_y=None,
            height=60
        )

        check_button = Button(
            text="CHECK BASHNET",
            font_size=18,
            size_hint_y=None,
            height=55
        )

        scan_button.bind(
            on_press=self.start_scanning
        )

        stop_button.bind(
            on_press=self.stop_scanning
        )

        check_button.bind(
            on_press=self.check_system
        )

        layout.add_widget(self.status)
        layout.add_widget(self.device_status)
        layout.add_widget(self.device_list)
        layout.add_widget(scan_button)
        layout.add_widget(stop_button)
        layout.add_widget(check_button)

        return layout

    def start_scanning(self, instance):
        self.device_status.text = (
            "BLUETOOTH: SCANNING REQUESTED"
        )

        self.device_list.text = (
            "BLUETOOTH DISCOVERY MODULE\n"
            "PREPARING..."
        )

    def stop_scanning(self, instance):
        self.device_status.text = (
            "BLUETOOTH: STOPPED"
        )

        self.device_list.text = (
            "SCANNING STOPPED"
        )

    def check_system(self, instance):
        self.status.text = (
            "BASHNET CORE 14 ACTIVE\n\n"
            "ANDROID APP RUNNING"
        )


if __name__ == "__main__":
    BashnetApp().run()