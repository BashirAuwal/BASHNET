[app]

title = BASHNET

package.name = bashnet

package.domain = org.bashnet

source.dir = .

source.include_exts = py,kv,png,jpg,atlas

version = 1.0.0

requirements = python3,kivy,pyjnius

orientation = portrait

fullscreen = 0

android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,BLUETOOTH_ADVERTISE,ACCESS_FINE_LOCATION

android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]

log_level = 2