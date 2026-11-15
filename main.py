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

        self.title = "BASHNET CORE 17"

        self.adapter = BluetoothAdapter.getDefaultAdapter()

        self.devices = {}

        self.receiver = None

        main = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        self.status = Label(
            text="BASHNET CORE 17\nREADY",
            font_size=20,
            size_hint_y=None,
            height=80
        )

        self.bluetooth_status = Label(
            text="BLUETOOTH: NOT CHECKED",
            font_size=17,
            size_hint_y=None,
            height=55
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
            height=60
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

        main.add_widget(self.status)
        main.add_widget(self.bluetooth_status)
        main.add_widget(check_button)
        main.add_widget(scan_button)
        main.add_widget(scroll)

        return main

    def update_label_size(self, instance, size):

        instance.height = size[1]
        instance.text_size = (instance.width, None)

    # CHECK BLUETOOTH

    def check_bluetooth(self, instance):

        try:

            if self.adapter is None:

                self.bluetooth_status.text = (
                    "BLUETOOTH NOT AVAILABLE"
                )

                return

            if self.adapter.isEnabled():

                self.bluetooth_status.text = (
                    "BLUETOOTH: ON\nREADY"
                )

            else:

                self.bluetooth_status.text = (
                    "BLUETOOTH: OFF"
                )

        except Exception as error:

            self.bluetooth_status.text = (
                "ERROR:\n" + str(error)
            )

    # START SCAN

    def start_scan(self, instance):

        if self.adapter is None:

            self.status.text = (
                "BLUETOOTH NOT AVAILABLE"
            )

            return

        try:

            if not self.adapter.isEnabled():

                self.status.text = (
                    "PLEASE TURN ON BLUETOOTH"
                )

                return

            permissions = [
                "android.permission.BLUETOOTH_SCAN",
                "android.permission.BLUETOOTH_CONNECT"
            ]

            if int(BuildVersion.SDK_INT) < 31:

                permissions.append(
                    "android.permission.ACCESS_FINE_LOCATION"
                )

            missing = []

            for permission in permissions:

                if not check_permission(permission):

                    missing.append(permission)

            if missing:

                self.status.text = (
                    "REQUESTING PERMISSIONS..."
                )

                request_permissions(
                    missing,
                    self.permission_result
                )

                return

            self.begin_discovery()

        except Exception as error:

            self.status.text = (
                "SCAN ERROR:\n" + str(error)
            )

    # PERMISSION RESULT

    def permission_result(self, permissions, grants):

        if all(grants):

            Clock.schedule_once(
                lambda dt: self.begin_discovery(),
                1
            )

        else:

            self.status.text = (
                "PERMISSION DENIED\n"
                "ALLOW NEARBY DEVICES"
            )

    # BEGIN DISCOVERY

    def begin_discovery(self, *args):

        try:

            self.devices = {}

            self.device_list.text = (
                "PREPARING BLUETOOTH..."
            )

            self.status.text = (
                "CHECKING BLUETOOTH..."
            )

            if self.adapter.isDiscovering():

                self.adapter.cancelDiscovery()

            # REGISTER RECEIVER

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

            # START DISCOVERY

            self.status.text = (
                "STARTING DISCOVERY..."
            )

            result = self.adapter.startDiscovery()

            if result:

                self.status.text = (
                    "DISCOVERY STARTED!\n"
                    "WAITING FOR DEVICES..."
                )

                Clock.schedule_once(
                    self.check_scan_status,
                    4
                )

            else:

                self.status.text = (
                    "DISCOVERY RESULT: FALSE\n"
                    "ANDROID REFUSED TO START"
                )

                self.show_permission_status()

        except Exception as error:

            self.status.text = (
                "DISCOVERY ERROR:\n" + str(error)
            )

    # CHECK DISCOVERY

    def check_scan_status(self, dt):

        try:

            scanning = self.adapter.isDiscovering()

            if scanning:

                self.status.text = (
                    "IS DISCOVERING: TRUE\n"
                    "SEARCHING FOR DEVICES..."
                )

            else:

                self.status.text = (
                    "IS DISCOVERING: FALSE\n"
                    "SCAN NOT ACTIVE"
                )

                self.show_permission_status()

        except Exception as error:

            self.status.text = (
                "STATUS ERROR:\n" + str(error)
            )

    # SHOW PERMISSIONS

    def show_permission_status(self):

        try:

            scan = check_permission(
                "android.permission.BLUETOOTH_SCAN"
            )

            connect = check_permission(
                "android.permission.BLUETOOTH_CONNECT"
            )

            self.status.text += (
                "\nSCAN PERMISSION: " + str(scan) +
                "\nCONNECT PERMISSION: " + str(connect)
            )

        except Exception as error:

            self.status.text += (
                "\nPERMISSION ERROR: " + str(error)
            )

    # RECEIVE BLUETOOTH DEVICES

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

    # ADD DEVICE

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

    # DISCOVERY FINISHED

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

    # STOP APP

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