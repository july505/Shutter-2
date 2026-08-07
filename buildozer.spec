[app]

title = Shutter PR
package.name = shutterpr
package.domain = com.shutterpr
source.dir = .
source.include_exts = py,json,kv
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a

android.permissions =

[buildozer]

log_level = 2
warn_on_root = 1
