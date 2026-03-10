[app]

title = Color fall
package.name = colorfall
package.domain = com.clawbot

version = 1.0.0

requirements = python3,kivy

orientation = portrait

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.accept_sdk_license = True

source.include_exts = py,png,jpg,kv,atlas

fullscreen = 1

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
