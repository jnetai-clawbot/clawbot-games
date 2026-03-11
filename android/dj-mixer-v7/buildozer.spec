[app]

title = DJ Mixer V7
package.name = djmixerv7
package.domain = com.clawbot

version = 1.0.0

requirements = python3,kivy,pyjnius

orientation = portrait

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# API settings
android.api = 31
android.minapi = 21
android.accept_sdk_license = True

# Include HTML file and assets
source.include_exts = py,png,jpg,kv,atlas,html,js,css

# Fullscreen mode
fullscreen = 1

# Enable WebView features
android.enable_webview = True

# iOS settings (for potential iOS build)
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0