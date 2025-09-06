[app]
# (str) Title of your application
title = CivataBot

# (str) Package name
package.name = civatabot

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]
# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
#android.activity_class_name = org.example.myapp.MyActivity

# (list) Pattern to whitelist for the whole project
#android.whitelist = 

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (list) Android application meta-data to set (key=value format)
#android.meta_data = 

# (list) Android library project to add (will be added in the libs dir)
#android.library_references = 

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# You can use the name "all" to build all available architectures.
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk).
android.debug_artifact = apk

# Python for android (p4a) specific
[buildozer:p4a]

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = 

# (str) Filename to the hook for p4a
#p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

# Control passing the --private and --add-source directories to p4a
# --private the main source of the app, used to contain the info about the app
# --add-source pass the extra source dirs to p4a build (if any)
# (list) additional source directories for p4a
# p4a.source_dirs = 

# (list) additional AAR files to add to the build process (supported in sdl2 bootstrap)
# p4a.aars = 

# (list) additional Java .jar files to add to the libs directory
# p4a.jars = 

# (str) XML file to include as an intent filter in your app
# p4a.intent_filters = 

# (str) launchMode to set for the main activity
# p4a.launchmode = standard

# (list) Android additional libraries to copy into libs/armeabi
#p4a.add_lib_armeabi = libs/android/*.so
#p4a.add_lib_armeabi_v7a = libs/android-v7/*.so
#p4a.add_lib_arm64_v8a = libs/android-v8/*.so
#p4a.add_lib_x86 = libs/android-x86/*.so
#p4a.add_lib_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#p4a.wakelock = False

# (list) Android application permissions to add (see Android documentation for complete list)
#android.permissions = INTERNET

# (str) Android SDK version to use
android.api = 34

# (str) Android NDK version to use
#android.ndk = 25b

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
android.ndk_dir = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_dir = 

# (str) python-for-android branch to use, defaults to master  
p4a.branch = master

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (str) If you need custom Java classes in your project, place them in a directory
# called java-classes and set this to the name of the directory
#android.java_src_dirs = java-classes

# (str) If you have gradle files in the android directory set this to the name of the directory
#android.gradle_dirs = gradle

# (str) Java version for javac. Default is 1.8
#android.java_version = 1.8

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK version to use
#android.ndk = 19b

# (str) Android minimum API to use
android.minapi = 26

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
#android.enable_androidx = False

# (bool) enable Android auto backup (Android API >= 23)
android.allow_backup = True

# (str) The format used to package the app for debug mode (apk or aab)
# android.debug_artifact = apk

# (str) The format used to package the app for release mode (apk or aab)
# android.release_artifact = apk

# (bool) Whether to build the debug version (True) or the release version (False)
android.debug = True

# (list) Gradle dependencies to add 
#android.gradle_dependencies = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
#android.enable_androidx = False

# (list) add java compile options
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# e.g. android.gradle_repositories = "google()", "jcenter()", "maven { url 'https://kotlin.bintray.com/ktor' }"
#android.gradle_repositories = 

# (list) packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# please enclose in double quotes 
# e.g. android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"
#android.add_packaging_options = 

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filter in your app
#android.intent_filters = 

# (list) Copy these files to src/main/res/xml/ (used for example with intent-filters)
#android.res_xml = 

# (str) launchMode to set for the main activity
#android.launchmode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_lib_armeabi = libs/android/*.so
#android.add_lib_armeabi_v7a = libs/android-v7/*.so
#android.add_lib_arm64_v8a = libs/android-v8/*.so
#android.add_lib_x86 = libs/android-x86/*.so
#android.add_lib_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android application permissions
# Check https://developer.android.com/guide/topics/permissions/overview
# for all available permissions
#android.permissions = INTERNET

# (bool) Android bootclasspath filtering
#android.bootclasspath_filtering = False

# (str) path to a custom gradle template
#android.gradle_template = 

# (str) path to a custom gradle build template (gradle.tmpl)
#android.gradle_build_template = 

# (bool) Whether to automatically accept the SDK license
# This is intended for automation only. If set to False (the default), the SDK
# license is not automatically accepted and you will be asked to accept it
# manually if it has not already been accepted before.
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64, all
android.archs = arm64-v8a
