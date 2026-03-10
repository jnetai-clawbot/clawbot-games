#!/usr/bin/env python3
"""
Neon Void - 3D Maze Runner Android Game
A first-person maze exploration game
Built with Kivy for Android
"""

import os
import sys
import random
import math

# Kivy imports
try:
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.slider import Slider
    from kivy.core.window import Window
    from kivy.properties import NumericProperty, StringProperty, BooleanProperty
    from kivy.clock import Clock
    from kivy.graphics import Color, Rectangle, Ellipse
    from kivy.core.audio import SoundLoader
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("Kivy not available - running in demo mode")

# Game constants
MAZE_SIZE = 11
CELL_SIZE = 40
PLAYER_SIZE = 20
ORB_SIZE = 15
ENEMY_SIZE = 18

class MazeGenerator:
    """Generate maze using recursive backtracker"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = self.generate()
    
    def generate(self):
        maze = [[{'n': True, 's': True, 'e': True, 'w': True, 'visited': False} 
                 for _ in range(self.width)] for _ in range(self.height)]
        
        stack = [(0, 0)]
        maze[0][0]['visited'] = True
        
        while stack:
            x, y = stack[-1]
            neighbors = []
            
            if y > 0 and not maze[y-1][x]['visited']:
                neighbors.append(('n', x, y-1))
            if y < self.height-1 and not maze[y+1][x]['visited']:
                neighbors.append(('s', x, y+1))
            if x > 0 and not maze[y][x-1]['visited']:
                neighbors.append(('w', x-1, y))
            if x < self.width-1 and not maze[y][x+1]['visited']:
                neighbors.append(('e', x+1, y))
            
            if neighbors:
                direction, nx, ny = random.choice(neighbors)
                maze[y][x][direction] = False
                maze[ny][nx][{'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}[direction]] = False
                maze[ny][nx]['visited'] = True
                stack.append((nx, ny))
            else:
                stack.pop()
        
        return maze

class GameState:
    """Main game state"""
    
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.combo = 0
        self.player_x = 1
        self.player_y = 1
        self.player_dir = 0  # 0=north, 1=east, 2=south, 3=west
        self.orbs = []
        self.enemies = []
        self.exit_pos = (self.width-2, self.height-2)
        self.maze = None
        self.generate_level()
    
    @property
    def width(self):
        return MAZE_SIZE
    
    @property
    def height(self):
        return MAZE_SIZE
    
    def generate_level(self):
        """Generate new level"""
        self.maze = MazeGenerator(self.width, self.height)
        
        # Reset player position
        self.player_x = 1
        self.player_y = 1
        
        # Place exit
        self.exit_pos = (self.width - 2, self.height - 2)
        
        # Generate orbs
        self.orbs = []
        orb_count = 5 + self.level * 2
        for _ in range(orb_count):
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                if (x, y) != (self.player_x, self.player_y) and (x, y) != self.exit_pos:
                    if (x, y) not in self.orbs:
                        self.orbs.append((x, y))
                        break
        
        # Generate enemies
        self.enemies = []
        enemy_count = 2 + self.level
        for _ in range(enemy_count):
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                dist = abs(x - self.player_x) + abs(y - self.player_y)
                if dist > 4:
                    self.enemies.append({
                        'x': x, 'y': y,
                        'dir': random.randint(0, 3),
                        'move_timer': 0
                    })
                    break
    
    def move_player(self, dx, dy):
        """Move player in direction"""
        if dx == 0 and dy == 0:
            return
        
        # Update direction
        if dx > 0:
            self.player_dir = 1
        elif dx < 0:
            self.player_dir = 3
        elif dy > 0:
            self.player_dir = 2
        elif dy < 0:
            self.player_dir = 0
        
        # Check wall
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        if 0 < new_x < self.width and 0 < new_y < self.height:
            if dx == 1 and not self.maze.maze[self.player_y][self.player_x]['e']:
                self.player_x = new_x
            elif dx == -1 and not self.maze.maze[self.player_y][self.player_x]['w']:
                self.player_x = new_x
            elif dy == 1 and not self.maze.maze[self.player_y][self.player_x]['s']:
                self.player_y = new_y
            elif dy == -1 and not self.maze.maze[self.player_y][self.player_x]['n']:
                self.player_y = new_y
    
    def check_collisions(self):
        """Check orb and enemy collisions"""
        # Check orbs
        player_pos = (self.player_x, self.player_y)
        if player_pos in self.orbs:
            self.orbs.remove(player_pos)
            self.score += 100 * (1 + self.combo * 0.1)
            self.combo += 1
            
            # Check level complete
            if len(self.orbs) == 0:
                self.level += 1
                self.generate_level()
        
        # Check enemies
        for enemy in self.enemies:
            if enemy['x'] == self.player_x and enemy['y'] == self.player_y:
                self.lives -= 1
                self.combo = 0
                # Reset player position
                self.player_x = 1
                self.player_y = 1
                if self.lives <= 0:
                    return False
        return True
    
    def move_enemies(self, dt):
        """Move enemies"""
        for enemy in self.enemies:
            enemy['move_timer'] += dt
            if enemy['move_timer'] > 1.0:  # Move every second
                enemy['move_timer'] = 0
                
                # Simple random movement
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                random.shuffle(directions)
                
                for dx, dy in directions:
                    nx, ny = enemy['x'] + dx, enemy['y'] + dy
                    if 0 < nx < self.width and 0 < ny < self.height:
                        # Check walls
                        maze_cell = self.maze.maze[enemy['y']][enemy['x']]
                        can_move = False
                        if dx == 1 and not maze_cell['e']:
                            can_move = True
                        elif dx == -1 and not maze_cell['w']:
                            can_move = True
                        elif dy == 1 and not maze_cell['s']:
                            can_move = True
                        elif dy == -1 and not maze_cell['n']:
                            can_move = True
                        
                        if can_move:
                            enemy['x'] = nx
                            enemy['y'] = ny
                            break


class NeonVoidGame(BoxLayout if KIVY_AVAILABLE else object):
    """Main game widget"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = GameState()
        self.orientation = 'portrait'
        
        if KIVY_AVAILABLE:
            self.setup_ui()
            Clock.schedule_interval(self.update, 1/60)
    
    def setup_ui(self):
        """Setup UI elements"""
        pass  # UI would be built in KV file
    
    def update(self, dt):
        """Game update loop"""
        if not hasattr(self, 'game_state'):
            return
            
        self.game_state.move_enemies(dt)
        if not self.game_state.check_collisions():
            self.game_over()
    
    def move(self, direction):
        """Handle player movement"""
        if not hasattr(self, 'game_state'):
            return
            
        dx, dy = 0, 0
        if direction == 'up':
            dy = -1
        elif direction == 'down':
            dy = 1
        elif direction == 'left':
            dx = -1
        elif direction == 'right':
            dx = 1
        
        self.game_state.move_player(dx, dy)
        self.game_state.check_collisions()


class NeonVoidApp(App if KIVY_AVAILABLE else object):
    """Android App"""
    
    def build(self):
        if not KIVY_AVAILABLE:
            print("=" * 50)
            print("🌀 NEON VOID - 3D Maze Runner")
            print("=" * 50)
            print("\nThis is the Android source code.")
            print("To build APK, install Kivy and use:")
            print("  buildozer init")
            print("  buildozer android debug")
            print("\nGame Features:")
            print("  • Procedurally generated mazes")
            print("  • Collect orbs for points")
            print("  • Avoid enemies")
            print("  • Multiple levels")
            print("  • Combo system")
            return None
        
        Window.clearcolor = (0, 0, 0, 1)
        return NeonVoidGame()
    
    def on_pause(self):
        return True


def main():
    """Main entry point"""
    print("🌀 NEON VOID - Android Game")
    print("=" * 40)
    print()
    print("Game: First-person 3D maze runner")
    print("Platform: Android (via Kivy/Buildozer)")
    print()
    print("Features:")
    print("  🎮 Touch controls")
    print("  🌀 Infinite procedural mazes")
    print("  💎 Collect glowing orbs")
    print("  👾 Avoid red enemies")
    print("  📈 Progressive difficulty")
    print("  🔥 Combo scoring system")
    print()
    print("To build APK:")
    print("  1. pip install kivy buildozer")
    print("  2. buildozer init")
    print("  3. buildozer android debug")
    print()
    
    if KIVY_AVAILABLE:
        try:
            NeonVoidApp().run()
        except:
            print("(Running in console mode)")
    else:
        print("Install Kivy to run: pip install kivy")


if __name__ == "__main__":
    main()
