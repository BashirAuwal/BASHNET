from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from jnius import autoclass

from android.permissions import (
    check_permission,
    request_permissions
)

from android.broadcast import BroadcastReceiver


BluetoothAdapter = autoclass(
    "android.bluetooth.BluetoothAdapter"
)

BluetoothDevice = autoclass(
    "android.bluetooth.BluetoothDevice"
)

BuildVersion = autoclass(
    "android.os.Build$VERSION"
)


class BashnetApp(App):

    def build(self):

        self.title = "BASHNET CORE 16"

        self.adapter = BluetoothAdapter.getDefaultAdapter()

        self.devices = {}

        self.receiver = None

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        self.status = Label(
            text="BASHNET CORE 16\nREADY",
            font_size=22,
            size_hint_y=None,
            height=70
        )

        self.bluetooth_status = Label(
            text="BLUETOOTH: NOT CHECKED",
            font_size=18,
            size_hint_y=None,
            height=50
        )

        check_button = Button(
            text="CHECK BLUETOOTH",
            size_hint_y=None,
            height=55
        )

        check_button.bind(
            on_press=self.check_bluetooth
        )

        scan_button = Button(
            text="SEARCH NEARBY DEVICES",
            size_hint_y=None,
            height=55
        )

        scan_button.bind(
            on_press=self.start_scan
        )

        self.device_list = Label(
            text="NO DEVICES FOUND",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.device_list.bind(
            texture_size=self.update_label_size
        )

        scroll = ScrollView()

        scroll.add_widget(self.device_list)

        layout.add_widget(self.status)
        layout.add_widget(self.bluetooth_status)
        layout.add_widget(check_button)
        layout.add_widget(scan_button)
        layout.add_widget(scroll)

        return layout

    def update_label_size(self, instance, size):

        instance.height = size[1]
        instance.text_size = (instance.width, None)

    def check_bluetooth(self, instance):

        try:

            if self.adapter is None:

                self.bluetooth_status.text = (
                    "BLUETOOTH NOT AVAILABLE"
                )

            elif self.adapter.isEnabled():

                self.bluetooth_status.text = (
                    "BLUETOOTH: ON\n"
                    "BASHNET READY"
                )

            else:

                self.bluetooth_status.text = (
                    "BLUETOOTH: OFF"
                )

        except Exception as error:

            self.bluetooth_status.text = str(error)

    def start_scan(self, instance):

        if self.adapter is None:

            self.status.text = "BLUETOOTH NOT AVAILABLE"
            return

        if not self.adapter.isEnabled():

            self.status.text = "PLEASE TURN ON BLUETOOTH"
            return

        permissions = [
            "android.permission.BLUETOOTH_SCAN",
            "android.permission.BLUETOOTH_CONNECT"
        ]

        if int(BuildVersion.SDK_INT) < 31:

            permissions.append(
                "android.permission.ACCESS_FINE_LOCATION"
            )

        missing = [
            permission
            for permission in permissions
            if not check_permission(permission)
        ]

        if missing:

            self.status.text = "REQUESTING PERMISSIONS..."

            request_permissions(
                missing,
                self.permission_result
            )

            return

        self.begin_discovery()

    def permission_result(self, permissions, grants):

        if all(grants):

            Clock.schedule_once(
                lambda dt: self.begin_discovery(),
                0.5
            )

        else:

            self.status.text = (
                "PERMISSION DENIED\n"
                "Allow Nearby Devices"
            )

   def begin_discovery(self):

        try:

            if self.adapter.isDiscovering():
                self.adapter.cancelDiscovery()

            self.devices = {}

            self.device_list.text = (
                "SEARCHING FOR DEVICES..."
            )

            self.status.text = (
                "BASHNET DISCOVERY ACTIVE"
            )

            if self.receiver is None:

                actions = [
                    BluetoothDevice.ACTION_FOUND,
                    BluetoothAdapter.ACTION_DISCOVERY_FINISHED
                ]

                self.receiver = BroadcastReceiver(
                    self.on_bluetooth_broadcast,
                    actions=actions
                )

                self.receiver.start()

            result = self.adapter.startDiscovery()

            if not result:

                scan_permission = check_permission(
                    "android.permission.BLUETOOTH_SCAN"
                )

                connect_permission = check_permission(
                    "android.permission.BLUETOOTH_CONNECT"
                )

                self.status.text = (
                    "DISCOVERY FAILED\n"
                    "Bluetooth State: " + str(self.adapter.getState()) +
                    "\nScan Permission: " + str(scan_permission) +
                    "\nConnect Permission: " + str(connect_permission)
                )

            else:

                self.status.text = (
                    "DISCOVERY STARTED SUCCESSFULLY"
                )

        except Exception as e:

            self.status.text = (
                "BLUETOOTH ERROR:\n" + str(e)
            ) 

        except Exception as error:

            self.status.text = (
                "SCAN ERROR:\n" + str(error)
            )

    def on_bluetooth_broadcast(self, context, intent):

        action = intent.getAction()

        if action == BluetoothDevice.ACTION_FOUND:

            try:

                device = intent.getParcelableExtra(
                    BluetoothDevice.EXTRA_DEVICE
                )

                name = device.getName()

                address = device.getAddress()

                if not name:
                    name = "UNKNOWN DEVICE"

                Clock.schedule_once(
                    lambda dt: self.add_device(
                        name,
                        address
                    )
                )

            except Exception as error:

                print("DEVICE ERROR:", error)

        elif action == BluetoothAdapter.ACTION_DISCOVERY_FINISHED:

            Clock.schedule_once(
                self.discovery_finished
            )

    def add_device(self, name, address):

        if address in self.devices:
            return

        self.devices[address] = name

        result = "\n\n".join(
            [
                "NAME: " + device_name +
                "\nADDRESS: " + device_address

                for device_address, device_name
                in self.devices.items()
            ]
        )

        self.device_list.text = result

        self.status.text = (
            "DEVICES FOUND: " +
            str(len(self.devices))
        )

    def discovery_finished(self, dt):

        if self.devices:

            self.status.text = (
                "DISCOVERY FINISHED\n"
                "DEVICES FOUND: " +
                str(len(self.devices))
            )

        else:

            self.status.text = (
                "DISCOVERY FINISHED\n"
                "NO DEVICES FOUND"
            )

    def on_stop(self):

        try:

            if self.adapter and self.adapter.isDiscovering():

                self.adapter.cancelDiscovery()

            if self.receiver:

                self.receiver.stop()

                self.receiver = None

        except Exception as error:

            print("STOP ERROR:", error)


if __name__ == "__main__":

    BashnetApp().run()