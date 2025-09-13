[app]

# (str) Title of your application
title = My Application

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,kivymd,telethon

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

#
# OSX Specific
#
osx.python_version = 3
osx.kivy_version = 1.9.1

#
# Android specific
#
fullscreen = 0
android.permissions = INTERNET
#android.api = 31
#android.minapi = 21
#android.sdk = 20
#android.ndk = 23b
#android.ndk_api = 21
#android.private_storage = True
#android.ndk_path =
android.sdk_path = ./android-sdk
#android.ant_path =
#android.skip_update = False
#android.accept_sdk_license = False
#android.entrypoint = org.kivy.android.PythonActivity
#android.activity_class_name = org.kivy.android.PythonActivity
#android.extra_manifest_xml = ./src/android/extra_manifest.xml
#android.extra_manifest_application_arguments = ./src/android/extra_manifest_application_arguments.xml
#android.service_class_name = org.kivy.android.PythonService
#android.apptheme = "@android:style/Theme.NoTitleBar"
#android.whitelist =
#android.whitelist_src =
#android.blacklist_src =
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar
#android.add_src =
#android.add_aars =
#android.add_assets =
#android.add_resources =
#android.gradle_dependencies =
#android.enable_androidx = True
#android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"
#android.add_gradle_repositories =
#android.add_packaging_options =
#android.add_activities = com.example.ExampleActivity
#android.ouya.category = GAME
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png
#android.manifest.intent_filters =
#android.res_xml = PATH_TO_FILE,
#android.manifest.launch_mode = standard
#android.manifest.orientation = fullSensor
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so
#android.wakelock = False
#android.meta_data =
#android.library_references =
#android.uses_library =
#android.logcat_filters = *:S python:D
#android.logcat_pid_only = False
#android.adb_args = -H host.docker.internal
#android.copy_libs = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
#android.no-byte-compile-python = False

#
# Python for android (p4a) specific
#
#p4a.url =
#p4a.fork = kivy
#p4a.branch = master
#p4a.commit = HEAD
#p4a.source_dir =
#p4a.local_recipes =
#p4a.hook =
#p4a.bootstrap = sdl2
#p4a.port =
#p4a.setup_py = false
#p4a.extra_args =

#
# iOS specific
#
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1
# build_dir = ./.buildozer
# bin_dir = ./bin
