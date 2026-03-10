# 🤖 ClawBot Android Games

A collection of Android games built with Python/Kivy, ready to compile to APK!

## 📱 Games Included

### 🎮 Neon Void
- **Genre:** 3D Maze Runner
- **Description:** First-person maze exploration game with procedurally generated mazes
- **Features:**
  - Procedural maze generation
  - Collect glowing orbs
  - Avoid enemies
  - Multiple levels
  - Combo scoring system

### 🚀 Quantum Assault  
- **Genre:** Space Shooter
- **Description:** Retro-style space shooter with waves and powerups
- **Features:**
  - 3 enemy types (basic, fast, tank)
  - Shield & double-shot powerups
  - Progressive difficulty waves
  - Starfield background

### 🐍 Neon Snake
- **Genre:** Classic Arcade
- **Description:** Modern twist on classic snake game
- **Features:**
  - Smooth movement
  - Score & high score tracking
  - Progressive speed increase

### 🎨 Color Fall
- **Genre:** Puzzle
- **Description:** Color-matching puzzle game
- **Features:**
  - Match 3+ colored blocks
  - Chain reactions
  - Progressive difficulty

## 🛠️ Building APKs

### Prerequisites
```bash
# Install Python dependencies
pip install kivy buildozer

# For Android SDK, see: https://kivy.org/doc/stable/guide/android.html
```

### Build Steps
```bash
# Navigate to game folder
cd neon-void  # or any other game

# Initialize buildozer (first time only)
buildozer init

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release
```

The APK will be in `bin/` folder.

## 🎯 Project Structure
```
clawbot-android/
├── neon-void/
│   ├── game.json       # Game metadata
│   └── main.py         # Game source
├── quantum-assault/
│   ├── game.json
│   └── main.py
├── neon-snake/
│   ├── game.json
│   └── main.py
└── color-fall/
    ├── game.json
    └── main.py
```

## 🌐 Web Versions

These games also have HTML5 versions at:
- [github.com/jnetai-clawbot/clawbot-games](https://github.com/jnetai-clawbot/clawbot-games)

## 🤖 Built with Kivy

[Kivy](https://kivy.org) - Open source Python library for rapid development of applications
that make use of innovative user interfaces, such as multi-touch apps.
