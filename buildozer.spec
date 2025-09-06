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

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 23b
android.arch = armeabi-v7a
