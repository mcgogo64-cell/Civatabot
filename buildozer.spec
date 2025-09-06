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
# HATA ÇIKARMAMASI İÇİN SABİT DEĞERLER
android.api = 34
android.minapi = 26
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# Tek mimari (modern cihazlar için 64-bit). Cihazın 32-bit ise bunu "armeabi-v7a" yap.
android.arch = arm64-v8a

# ÖNEMLİ: Aşağıdakiler OLMAYACAK!
# android.sdk = ...
# android.ndk = ...
