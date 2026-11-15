from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from jnius import autoclass
from android.permissions import check_permission


class BashnetApp(App):

    def build(self):
        self.title = "BASHNET CORE 15"

        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=20
        )

        self.status = Label(
            text="BASHNET CORE 15\n\nREADY",
            font_size=22
        )

        self.bluetooth_status = Label(
            text="BLUETOOTH: NOT CHECKED",
            font_size=18
        )

        check_button = Button(
            text="CHECK BLUETOOTH",
            font_size=20
        )

        check_button.bind(
            on_press=self.check_bluetooth
        )

        layout.add_widget(self.status)
        layout.add_widget(self.bluetooth_status)
        layout.add_widget(check_button)

        return layout

    def check_bluetooth(self, instance):

        self.bluetooth_status.text = "CHECKING..."

        try:
            permission = check_permission(
                "android.permission.BLUETOOTH_CONNECT"
            )

            if not permission:
                self.bluetooth_status.text = (
                    "PERMISSION NOT GRANTED\n"
                    "Open App Settings\n"
                    "Allow Nearby Devices"
                )
                return

            BluetoothAdapter = autoclass(
                "android.bluetooth.BluetoothAdapter"
            )

            adapter = BluetoothAdapter.getDefaultAdapter()

            if adapter is None:
                self.bluetooth_status.text = (
                    "BLUETOOTH NOT AVAILABLE"
                )

            elif adapter.isEnabled():
                self.bluetooth_status.text = (
                    "BLUETOOTH: ON\n"
                    "BASHNET READY"
                )

            else:
                self.bluetooth_status.text = (
                    "BLUETOOTH: OFF\n"
                    "TURN ON BLUETOOTH"
                )

        except Exception as error:
            self.bluetooth_status.text = (
                "BLUETOOTH ERROR:\n" + str(error)
            )


if __name__ == "__main__":
    BashnetApp().run()