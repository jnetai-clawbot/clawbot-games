#!/usr/bin/env python3
"""
DJ Mixer V7 - Android WebView App
Loads the DJ Mixer V7 HTML5 application in a native Android WebView
With error handling and debug logging
"""

import os
import sys
import traceback

# Debug flag - set to True for verbose logging
DEBUG = True

def log(msg, error=False):
    """Debug logging function"""
    if DEBUG or error:
        prefix = "❌ ERROR: " if error else "📱 "
        print(f"{prefix}{msg}")

# Try to import Kivy - will run in demo mode if not available
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.textinput import TextInput
    from kivy.core.window import Window
    from kivy.properties import StringProperty
    from kivy.clock import Clock
    
    # Android-specific imports for WebView
    try:
        from jnius import autoclass, cast
        from android.runnable import run_on_ui_thread
        ANDROID_AVAILABLE = True
        log("Android modules loaded successfully")
    except ImportError:
        ANDROID_AVAILABLE = False
        log("Android modules not available (running in demo mode)")
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    ANDROID_AVAILABLE = False
    log("Kivy not available")

# URLs for DJ Mixer V7
# Method 1: Local HTML (if bundled with app)
LOCAL_HTML = "file:///android_asset/dj-mixer-V7.html"

# Method 2: Remote URL (fallback)
REMOTE_URL = "https://raw.githubusercontent.com/jnetai-clawbot/clawbot-games/main/dj-mixer-V7.html"

# Method 3: Alternative - Music Assistant (as requested fallback)
FALLBACK_URL = "https://jnetai.com/apps/music_assistant/"

class DJMixerV7App(App if KIVY_AVAILABLE else object):
    """Main application class"""
    
    # Properties for KV bindings
    status_text = StringProperty("Initializing...")
    debug_text = StringProperty("")
    current_url = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.webview = None
        self.error_count = 0
        self.max_retries = 3
        log("DJ Mixer V7 App initializing...")
    
    def build(self):
        """Build the app UI"""
        log("Building UI...")
        
        if not KIVY_AVAILABLE:
            return self.build_demo()
        
        # Set window properties
        Window.clearcolor = (0.02, 0.02, 0.05, 1)
        
        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=None, height=50)
        header.add_widget(Label(
            text="🎧 DJ Mixer V7",
            font_size=20,
            color=(0, 1, 0.53, 1),  # #00ff88
            size_hint_x=0.7
        ))
        header.add_widget(Button(
            text="↻ Reload",
            size_hint_x=0.3,
            on_press=lambda x: self.reload()
        ))
        layout.add_widget(header)
        
        # Status bar
        self.status_label = Label(
            text=self.status_text,
            font_size=12,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.status_label)
        
        # Debug info (scrollable)
        self.debug_label = Label(
            text=self.debug_text,
            font_size=10,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=80,
            text_size=(360, None)
        )
        layout.add_widget(self.debug_label)
        
        # Try to create WebView
        if ANDROID_AVAILABLE:
            try:
                self.create_android_webview(layout)
            except Exception as e:
                log(f"WebView creation failed: {e}", error=True)
                self.show_error(layout, e)
        else:
            # Demo mode - show info
            self.show_demo_info(layout)
        
        return layout
    
    def create_android_webview(self, layout):
        """Create Android WebView"""
        log("Creating Android WebView...")
        
        try:
            # Import Android WebView
            from jnius import autoclass
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            Activity = autoclass('org.kivy.android.PythonActivity')
            
            # Create WebView
            self.webview = WebView(Activity.getInstance())
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.getSettings().setDomStorageEnabled(True)
            self.webview.getSettings().setAllowFileAccess(True)
            self.webview.getSettings().setAllowContentAccess(True)
            
            # Set WebViewClient
            webview_client = WebViewClient()
            self.webview.setWebViewClient(webview_client)
            
            # Load URL
            self.load_url(layout)
            
        except Exception as e:
            log(f"Android WebView error: {e}", error=True)
            traceback.print_exc()
            self.show_error(layout, e)
    
    def load_url(self, layout, url=None, retry_count=0):
        """Load URL with retry logic"""
        if url is None:
            # Try local first, then remote
            url = LOCAL_HTML
            log(f"Attempting to load: {url}")
        
        self.status_text = f"Loading: {url[:50]}..."
        self.current_url = url
        
        try:
            if self.webview:
                self.webview.loadUrl(url)
                self.status_text = f"✅ Loaded: {url[:40]}..."
                log(f"Successfully loaded: {url}")
        except Exception as e:
            log(f"Load error ({retry_count + 1}/{self.max_retries}): {e}", error=True)
            
            if retry_count < self.max_retries - 1:
                # Retry with fallback URLs
                if url == LOCAL_HTML:
                    self.load_url(layout, REMOTE_URL, retry_count + 1)
                elif url == REMOTE_URL:
                    self.load_url(layout, FALLBACK_URL, retry_count + 1)
            else:
                self.error_count += 1
                self.status_text = f"❌ Error after {self.max_retries} attempts"
                self.debug_text = f"Failed to load:\n{url}\n\nError: {str(e)[:100]}"
                log(f"Max retries exceeded. Error: {e}", error=True)
    
    def reload(self):
        """Reload the current page"""
        log("Reload requested")
        if self.webview:
            try:
                self.webview.reload()
                self.status_text = "🔄 Reloading..."
            except Exception as e:
                log(f"Reload error: {e}", error=True)
                self.status_text = f"❌ Reload failed: {str(e)[:30]}"
    
    def show_demo_info(self, layout):
        """Show demo information when not on Android"""
        info = Label(
            text="📱 DJ Mixer V7 - Android App\n\n"
                 "This app loads the DJ Mixer V7\n"
                 "in a native Android WebView.\n\n"
                 "🔗 URLs:\n"
                 f"• Local: {LOCAL_HTML}\n"
                 f"• Remote: {REMOTE_URL[:50]}...\n\n"
                 "Build APK with:\n"
                 "buildozer android debug\n\n"
                 "Error Count: 0\n"
                 "Debug Mode: " + ("ON" if DEBUG else "OFF"),
            font_size=14,
            color=(1, 1, 1, 1),
            text_size=(340, None),
            valign='top'
        )
        layout.add_widget(info)
        
        # Add buttons to test URLs
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
        btn_layout.add_widget(Button(
            text="Load Remote",
            on_press=lambda x: self.test_url(REMOTE_URL)
        ))
        btn_layout.add_widget(Button(
            text="Load Fallback",
            on_press=lambda x: self.test_url(FALLBACK_URL)
        ))
        layout.add_widget(btn_layout)
    
    def show_error(self, layout, error):
        """Show error information"""
        error_msg = f"❌ Error Details:\n\n{str(error)[:200]}\n\n"
        error_msg += f"Error count: {self.error_count}\n\n"
        error_msg += "Fallback URL:\n" + FALLBACK_URL
        
        error_label = Label(
            text=error_msg,
            font_size=12,
            color=(1, 0.3, 0.3, 1),
            text_size=(340, None)
        )
        layout.add_widget(error_label)
        
        # Add reload button
        layout.add_widget(Button(
            text="🔄 Try Fallback URL",
            size_hint_y=None,
            height=50,
            on_press=lambda x: self.load_url(layout, FALLBACK_URL)
        ))
    
    def test_url(self, url):
        """Test loading a specific URL"""
        log(f"Testing URL: {url}")
        self.debug_text = f"Testing: {url[:60]}...\n\n"
        self.status_text = f"Testing: {url[:30]}..."
    
    def on_pause(self):
        """Handle app pause"""
        log("App paused")
        return True
    
    def on_resume(self):
        """Handle app resume"""
        log("App resumed")
        return True
    
    def on_stop(self):
        """Handle app stop"""
        log("App stopped")
        if self.webview:
            try:
                self.webview.destroy()
            except:
                pass


def main():
    """Main entry point with error handling"""
    print("=" * 50)
    print("🎧 DJ Mixer V7 - Android WebView App")
    print("=" * 50)
    print()
    print("📋 Configuration:")
    print(f"  DEBUG: {DEBUG}")
    print(f"  Local HTML: {LOCAL_HTML}")
    print(f"  Remote URL: {REMOTE_URL[:60]}...")
    print(f"  Fallback URL: {FALLBACK_URL}")
    print()
    print("🔧 Build Instructions:")
    print("  1. pip install kivy buildozer")
    print("  2. Copy dj-mixer-V7.html to android/dj-mixer-v7/")
    print("  3. buildozer init")
    print("  4. buildozer android debug")
    print()
    
    if KIVY_AVAILABLE:
        try:
            app = DJMixerV7App()
            app.run()
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            traceback.print_exc()
            print("\n📋 Running in demo mode...")
            print("Install Kivy/Buildozer to build APK:")
            print("  pip install kivy buildozer")
    else:
        print("Install Kivy to run: pip install kivy")


if __name__ == "__main__":
    main()