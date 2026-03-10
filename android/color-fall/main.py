#!/usr/bin/env python3
"""
Color Fall - Color Matching Puzzle Game
Match falling colors to clear blocks
Built with Kivy for Android
"""

import random
import sys

try:
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.core.window import Window
    from kivy.properties import NumericProperty, ListProperty, StringProperty
    from kivy.clock import Clock
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False

# Game Constants
COLS = 6
ROWS = 12
CELL_SIZE = 40
COLORS = [
    (1, 0.2, 0.2, 1),  # Red
    (0.2, 1, 0.2, 1),  # Green
    (0.2, 0.2, 1, 1),  # Blue
    (1, 1, 0.2, 1),    # Yellow
    (1, 0.2, 1, 1),    # Magenta
    (0.2, 1, 1, 1),    # Cyan
]


class ColorFallGame:
    """Color Fall puzzle game logic"""
    
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.drop_timer = 0
        self.drop_speed = 1.0  # Seconds between drops
        self.current_color = random.randint(0, len(COLORS) - 1)
        self.current_col = COLS // 2
        self.falling_row = 0
    
    def new_piece(self):
        """Create new falling piece"""
        self.current_color = random.randint(0, len(COLORS) - 1)
        self.current_col = COLS // 2
        self.falling_row = 0
    
    def move_piece(self, dx):
        """Move piece horizontally"""
        new_col = self.current_col + dx
        if 0 <= new_col < COLS:
            # Check if column is full at top
            if self.grid[0][new_col] is None:
                self.current_col = new_col
    
    def drop_piece(self):
        """Drop piece one row"""
        if self.grid[self.falling_row + 1][self.current_col] is not None:
            # Lock piece in place
            self.lock_piece()
            return
        
        self.falling_row += 1
        
        if self.falling_row >= ROWS - 1:
            self.lock_piece()
    
    def lock_piece(self):
        """Lock piece into grid"""
        if self.falling_row >= 0:
            self.grid[self.falling_row][self.current_col] = self.current_color
        
        # Check for matches
        self.check_matches()
        
        # Check game over
        if self.grid[0][COLS // 2] is not None:
            self.game_over = True
            return
        
        self.new_piece()
    
    def check_matches(self):
        """Check for matching colors"""
        matched = set()
        
        # Check horizontal matches
        for row in range(ROWS):
            for col in range(COLS - 2):
                if (self.grid[row][col] is not None and
                    self.grid[row][col] == self.grid[row][col + 1] == self.grid[row][col + 2]):
                    matched.add((row, col))
                    matched.add((row, col + 1))
                    matched.add((row, col + 2))
        
        # Check vertical matches
        for row in range(ROWS - 2):
            for col in range(COLS):
                if (self.grid[row][col] is not None and
                    self.grid[row][col] == self.grid[row + 1][col] == self.grid[row + 2][col]):
                    matched.add((row, col))
                    matched.add((row + 1, col))
                    matched.add((row + 2, col))
        
        # Remove matches
        if matched:
            for row, col in matched:
                self.grid[row][col] = None
            
            # Score
            points = len(matched) * 10 * (1 + len(matched) // 5)
            self.score += points
            self.lines_cleared += len(matched) // 3
            
            # Level up
            if self.lines_cleared >= self.level * 10:
                self.level += 1
                self.drop_speed = max(0.2, self.drop_speed - 0.1)
            
            # Apply gravity
            self.apply_gravity()
            
            # Check for chain reactions
            self.check_matches()
    
    def apply_gravity(self):
        """Apply gravity to floating blocks"""
        for col in range(COLS):
            # Move blocks down
            for row in range(ROWS - 1, 0, -1):
                if self.grid[row][col] is None:
                    # Find nearest block above
                    for above in range(row - 1, -1, -1):
                        if self.grid[above][col] is not None:
                            self.grid[row][col] = self.grid[above][col]
                            self.grid[above][col] = None
                            break
    
    def update(self, dt):
        """Update game state"""
        if self.game_over:
            return
        
        self.drop_timer += dt
        
        if self.drop_timer >= self.drop_speed:
            self.drop_timer = 0
            self.drop_piece()


class ColorFallApp(App):
    """Color Fall Android App"""
    
    score = NumericProperty(0)
    level = NumericProperty(1)
    
    def build(self):
        if not KIVY_AVAILABLE:
            self.run_console_demo()
            return None
        
        self.game = ColorFallGame()
        
        Window.size = (COLS * CELL_SIZE, ROWS * CELL_SIZE + 80)
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        Clock.schedule_interval(self.game_update, 1/60)
        
        return self.create_ui()
    
    def create_ui(self):
        """Create game UI"""
        from kivy.uix.widget import Widget
        
        class GameWidget(Widget):
            pass
        
        return GameWidget(app=self)
    
    def game_update(self, dt):
        """Game loop"""
        if not hasattr(self, 'game'):
            return
            
        self.game.update(dt)
        self.score = self.game.score
        self.level = self.game.level
    
    def run_console_demo(self):
        """Console demo"""
        print("🎨 COLOR FALL")
        print("=" * 40)
        print()
        print("Color-matching puzzle game")
        print()
        print("Match 3+ same-colored blocks")
        print("Chain reactions for bonus points!")
        print()
        print("To build APK:")
        print("  pip install kivy buildozer")
        print("  buildozer init")
        print("  buildozer android debug")


def main():
    print("🎨 COLOR FALL - Android Puzzle Game")
    print("=" * 45)
    
    if KIVY_AVAILABLE:
        try:
            ColorFallApp().run()
        except:
            print("(Install Kivy to run)")
    else:
        print("Kivy not installed. Install with: pip install kivy")


if __name__ == "__main__":
    main()
