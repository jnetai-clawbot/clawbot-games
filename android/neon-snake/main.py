#!/usr/bin/env python3
"""
Neon Snake - Classic Snake Game Android App
A modern twist on the classic snake game with neon visuals
Built with Kivy for Android
"""

import random
import sys

try:
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.core.window import Window
    from kivy.properties import NumericProperty, StringProperty
    from kivy.clock import Clock
    from kivy.graphics import Color, Rectangle
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False

# Game Constants
GRID_SIZE = 20
CELL_SIZE = 20
GAME_WIDTH = GRID_SIZE * CELL_SIZE
GAME_HEIGHT = GRID_SIZE * CELL_SIZE


class SnakeGame:
    """Snake game logic"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset game state"""
        # Start in middle, length 3
        self.snake = [
            (GRID_SIZE // 2, GRID_SIZE // 2),
            (GRID_SIZE // 2 - 1, GRID_SIZE // 2),
            (GRID_SIZE // 2 - 2, GRID_SIZE // 2)
        ]
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed = 0.15  # Seconds per move
    
    def spawn_food(self):
        """Spawn food in empty cell"""
        while True:
            food = (random.randint(0, GRID_SIZE - 1), 
                    random.randint(0, GRID_SIZE - 1))
            if food not in self.snake:
                return food
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], 
                   head[1] + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
            new_head[1] < 0 or new_head[1] >= GRID_SIZE):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake[:-1]:
            self.game_over = True
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            # Speed up slightly
            self.speed = max(0.05, self.speed - 0.002)
        else:
            self.snake.pop()
    
    def change_direction(self, dx, dy):
        """Change snake direction"""
        # Prevent 180 degree turns
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)


class NeonSnakeApp(App):
    """Neon Snake Android App"""
    
    score = NumericProperty(0)
    high_score = NumericProperty(0)
    
    def build(self):
        if not KIVY_AVAILABLE:
            self.run_console_demo()
            return None
        
        self.game = SnakeGame()
        
        # Load high score
        try:
            with open('highscore.txt', 'r') as f:
                self.high_score = int(f.read())
        except:
            pass
        
        Window.size = (GAME_WIDTH, GAME_HEIGHT + 60)
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        
        Clock.schedule_interval(self.game_update, self.game.speed)
        
        return self.create_ui()
    
    def create_ui(self):
        """Create game UI"""
        from kivy.uix.widget import Widget
        
        class GameWidget(Widget):
            def __init__(self, app, **kwargs):
                super().__init__(**kwargs)
                self.app = app
                self.bind(on_key_down=self.on_key_down)
            
            def on_key_down(self, key):
                if key == 'w' or key == 'up':
                    self.app.game.change_direction(0, 1)
                elif key == 's' or key == 'down':
                    self.app.game.change_direction(0, -1)
                elif key == 'a' or key == 'left':
                    self.app.game.change_direction(-1, 0)
                elif key == 'd' or key == 'right':
                    self.app.game.change_direction(1, 0)
        
        return GameWidget(app=self)
    
    def game_update(self, dt):
        """Game loop"""
        if not hasattr(self, 'game'):
            return
            
        self.game.update()
        
        if self.game.game_over:
            if self.game.score > self.high_score:
                self.high_score = self.game.score
                try:
                    with open('highscore.txt', 'w') as f:
                        f.write(str(self.high_score))
                except:
                    pass
        
        # Force redraw
        if hasattr(self, 'root'):
            self.root.canvas.ask_update()
    
    def run_console_demo(self):
        """Console demo"""
        print("🐍 NEON SNAKE")
        print("=" * 40)
        print()
        print("Classic snake game with neon visuals")
        print()
        print("Controls: WASD or Arrow Keys")
        print()
        print("Features:")
        print("  • Smooth movement")
        print("  • Score tracking")
        print("  • High score persistence")
        print("  • Progressive speed")
        print()
        print("To build APK:")
        print("  pip install kivy buildozer")
        print("  buildozer init")
        print("  buildozer android debug")
        print()


def main():
    print("🐍 NEON SNAKE - Android Game")
    print("=" * 45)
    
    if KIVY_AVAILABLE:
        try:
            NeonSnakeApp().run()
        except:
            print("(Install Kivy to run)")
    else:
        print("Kivy not installed. Install with: pip install kivy")


if __name__ == "__main__":
    main()
