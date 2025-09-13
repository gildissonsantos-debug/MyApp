[app]
title = My Application
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,kv,json
source.exclude_dirs = tests, bin, venv
version = 0.1
requirements = python3,kivy,kivymd,telethon
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET
android.sdk_path = /opt/android-sdk
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.extra_args = --sdk_dir=/opt/android-sdk

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1
