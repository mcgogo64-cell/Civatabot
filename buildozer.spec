[app]
title = CivataBot
package.name = civatabot
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Güvenli API/minAPI; build-tools sabitlemeye gerek yok (aksiyon hallediyor)
android.api = 34
android.minapi = 26
android.accept_sdk_license = True

# Tek mimari (modern cihazlar). 32-bit cihazsa: armeabi-v7a yap.
android.arch = arm64-v8a
