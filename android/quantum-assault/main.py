#!/usr/bin/env python3
"""
Quantum Assault - Space Shooter Android Game
A retro-style space shooter with powerups and waves
Built with Kivy for Android
"""

import random
import math
import sys

try:
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.core.window import Window
    from kivy.properties import NumericProperty, ListProperty
    from kivy.clock import Clock
    from kivy.graphics import Color, Rectangle, Ellipse, Triangle
    from kivy.uix.widget import Widget
    
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
POWERUP_SPEED = 2

COLORS = {
    'player': (0, 1, 1, 1),      # Cyan
    'enemy': (1, 0.3, 0.3, 1),    # Red
    'bullet': (1, 1, 0, 1),       # Yellow
    'powerup_shield': (0, 1, 0, 1),   # Green
    'powerup_double': (1, 0, 1, 1),    # Magenta
    'star': (1, 1, 1, 1)          # White
}


class GameObject:
    """Base class for game objects"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.alive = True
        self.color = (1, 1, 1, 1)
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
    
    def collides_with(self, other):
        return (abs(self.x - other.x) < (self.width + other.width) / 2 and
                abs(self.y - other.y) < (self.height + other.height) / 2)


class Player(GameObject):
    """Player ship"""
    
    def __init__(self):
        super().__init__(WINDOW_WIDTH // 2, 80, 40, 40)
        self.speed = PLAYER_SPEED
        self.shoot_delay = 0
        self.shoot_cooldown = 0.15
        self.lives = 3
        self.shield = False
        self.double_shot = False
        self.score = 0
        self.color = COLORS['player']
        self.direction = 0  # 0=up, 1=right, 2=down, 3=left
        self.moving = False
    
    def move_direction(self, dx, dy):
        self.direction = {(-1, 0): 3, (1, 0): 1, (0, 1): 2, (0, -1): 0}.get((dx, dy), self.direction)
        self.vx = dx * self.speed
        self.vy = dy * self.speed
        self.moving = dx != 0 or dy != 0
    
    def stop(self):
        self.vx = 0
        self.vy = 0
        self.moving = False
    
    def can_shoot(self):
        if self.shoot_delay <= 0:
            self.shoot_delay = self.shoot_cooldown
            return True
        return False
    
    def update(self, dt):
        self.shoot_delay -= dt
        
        # Boundary check
        self.x = max(self.width//2, min(WINDOW_WIDTH - self.width//2, self.x))
        self.y = max(self.height//2, min(WINDOW_HEIGHT - self.height//2, self.y))


class Bullet(GameObject):
    """Bullet fired by player"""
    
    def __init__(self, x, y, vy=-BULLET_SPEED):
        super().__init__(x, y, 6, 15)
        self.vy = vy
        self.color = COLORS['bullet']


class Enemy(GameObject):
    """Enemy ship"""
    
    def __init__(self, x, y, enemy_type='basic'):
        super().__init__(x, y, 35, 35)
        self.vy = -ENEMY_SPEED
        self.vx = random.choice([-1, 1]) * 1.5
        self.type = enemy_type
        self.health = 1
        self.color = COLORS['enemy']
        
        if enemy_type == 'fast':
            self.health = 1
            self.vy = -ENEMY_SPEED * 1.5
            self.width = 25
            self.height = 25
        elif enemy_type == 'tank':
            self.health = 3
            self.vy = -ENEMY_SPEED * 0.5
            self.width = 50
            self.height = 50


class Powerup(GameObject):
    """Powerup item"""
    
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, 25, 25)
        self.vy = -POWERUP_SPEED
        self.type = powerup_type
        
        if powerup_type == 'shield':
            self.color = COLORS['powerup_shield']
        elif powerup_type == 'double':
            self.color = COLORS['powerup_double']


class Star:
    """Background star"""
    
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)
        self.color = COLORS['star']
        self.color = (self.color[0], self.color[1], self.color[2], random.uniform(0.3, 0.8))
    
    def move(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = WINDOW_HEIGHT
            self.x = random.randint(0, WINDOW_WIDTH)


class QuantumAssaultGame(Widget):
    """Main game widget"""
    
    score = NumericProperty(0)
    lives = NumericProperty(3)
    wave = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.powerups = []
        self.stars = [Star() for _ in range(50)]
        self.keys = {'left': False, 'right': False, 'up': False, 'down': False, 'space': False}
        self.game_over = False
        self.spawn_timer = 0
        self.enemies_to_spawn = 5
        self.enemies_spawned = 0
        
        # Bind keyboard
        if KIVY_AVAILABLE:
            Window.bind(on_key_down=self.on_key_down)
            Window.bind(on_key_up=self.on_key_up)
            Clock.schedule_interval(self.update, 1/60)
    
    def on_key_down(self, window, key, *args):
        if key == 275:  # right
            self.keys['right'] = True
        elif key == 276:  # left
            self.keys['left'] = True
        elif key == 273:  # up
            self.keys['up'] = True
        elif key == 274:  # down
            self.keys['down'] = True
        elif key == 32:  # space
            self.keys['space'] = True
    
    def on_key_up(self, window, key, *args):
        if key == 275:
            self.keys['right'] = False
        elif key == 276:
            self.keys['left'] = False
        elif key == 273:
            self.keys['up'] = False
        elif key == 274:
            self.keys['down'] = False
        elif key == 32:
            self.keys['space'] = False
    
    def update(self, dt):
        if self.game_over:
            return
        
        # Move player
        dx, dy = 0, 0
        if self.keys.get('right'):
            dx = 1
        elif self.keys.get('left'):
            dx = -1
        if self.keys.get('up'):
            dy = 1
        elif self.keys.get('down'):
            dy = -1
        
        if dx != 0 or dy != 0:
            self.player.move_direction(dx, dy)
        else:
            self.player.stop()
        
        self.player.update(dt)
        
        # Shooting
        if self.keys.get('space') and self.player.can_shoot():
            if self.player.double_shot:
                self.bullets.append(Bullet(self.player.x - 10, self.player.y + 20))
                self.bullets.append(Bullet(self.player.x + 10, self.player.y + 20))
            else:
                self.bullets.append(Bullet(self.player.x, self.player.y + 20))
        
        # Move bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0 or bullet.y > WINDOW_HEIGHT:
                bullet.alive = False
        
        # Spawn enemies
        self.spawn_timer += dt
        if self.spawn_timer > 1 and self.enemies_spawned < self.enemies_to_spawn:
            self.spawn_timer = 0
            self.spawn_enemy()
            self.enemies_spawned += 1
        
        # Check if wave complete
        if (self.enemies_spawned >= self.enemies_to_spawn and 
            len(self.enemies) == 0):
            self.wave += 1
            self.enemies_to_spawn = 5 + self.wave * 2
            self.enemies_spawned = 0
            self.player.double_shot = self.wave >= 3
        
        # Move enemies
        for enemy in self.enemies[:]:
            enemy.move()
            # Bounce off walls
            if enemy.x < enemy.width//2 or enemy.x > WINDOW_WIDTH - enemy.width//2:
                enemy.vx *= -1
            
            # Check collision with player
            if enemy.collides_with(self.player):
                if self.player.shield:
                    enemy.alive = False
                    self.player.shield = False
                else:
                    self.player.lives -= 1
                    self.lives = self.player.lives
                    if self.player.lives <= 0:
                        self.game_over = True
                    else:
                        # Reset player position
                        self.player.x = WINDOW_WIDTH // 2
                        self.player.y = 80
            
            # Remove if off screen
            if enemy.y < -50:
                enemy.alive = False
        
        # Move powerups
        for powerup in self.powerups[:]:
            powerup.move()
            
            if powerup.collides_with(self.player):
                if powerup.type == 'shield':
                    self.player.shield = True
                elif powerup.type == 'double':
                    self.player.double_shot = True
                self.score += 50
                powerup.alive = False
            
            if powerup.y < -50:
                powerup.alive = False
        
        # Bullet-enemy collisions
        for bullet in self.bullets[:]:
            if not bullet.alive:
                continue
            for enemy in self.enemies[:]:
                if not enemy.alive:
                    continue
                if bullet.collides_with(enemy):
                    bullet.alive = False
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.alive = False
                        self.score += 100 * enemy.health
                    
                    # Chance to drop powerup
                    if random.random() < 0.1:
                        ptype = random.choice(['shield', 'double'])
                        self.powerups.append(Powerup(enemy.x, enemy.y, ptype))
                    break
        
        # Move stars
        for star in self.stars:
            star.move()
        
        # Clean up
        self.bullets = [b for b in self.bullets if b.alive]
        self.enemies = [e for e in self.enemies if e.alive]
        self.powerups = [p for p in self.powerups if p.alive]
        
        # Update score
        self.score = self.player.score
    
    def spawn_enemy(self):
        x = random.randint(50, WINDOW_WIDTH - 50)
        y = WINDOW_HEIGHT + 30
        
        # Enemy types based on wave
        if self.wave >= 5 and random.random() < 0.2:
            etype = 'tank'
        elif self.wave >= 3 and random.random() < 0.3:
            etype = 'fast'
        else:
            etype = 'basic'
        
        self.enemies.append(Enemy(x, y, etype))


class QuantumAssaultApp(App):
    """Android App"""
    
    def build(self):
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        Window.clearcolor = (0, 0, 0, 1)
        return QuantumAssaultGame()
    
    def on_pause(self):
        return True


def main():
    """Main entry"""
    print("🚀 QUANTUM ASSAULT - Space Shooter")
    print("=" * 45)
    print()
    print("Game: Retro space shooter")
    print("Platform: Android (via Kivy/Buildozer)")
    print()
    print("Controls:")
    print("  ⬅️ ➡️ ⬆️ ⬇️  - Move ship")
    print("  ␣ Space   - Fire")
    print()
    print("Features:")
    print("  🚀 3 enemy types (basic, fast, tank)")
    print("  🛡️  Shield powerup")
    print("  ⚡ Double shot powerup")
    print("  🌊 Progressive waves")
    print("  ⭐ Starfield background")
    print()
    print("To build APK:")
    print("  pip install kivy buildozer")
    print("  buildozer init")
    print("  buildozer android debug")
    print()
    
    if KIVY_AVAILABLE:
        try:
            QuantumAssaultApp().run()
        except:
            print("(Running in console mode)")


if __name__ == "__main__":
    main()
