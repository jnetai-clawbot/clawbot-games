# 🤖 ClawBot Android Games

A collection of Android games built with Python/Kivy - automatically builds to APK via GitHub Actions!

## 📱 Games Included

| Game | Genre | Description |
|------|-------|-------------|
| **Neon Void** | 3D Maze | First-person maze runner with procedural mazes |
| **Quantum Assault** | Space Shooter | Retro shooter with waves & powerups |
| **Neon Snake** | Arcade | Classic snake game with high scores |
| **Color Fall** | Puzzle | Match-3 color puzzle game |

## 📦 Download APKs

**Latest APKs (automatically built):**
- [Neon Void APK](https://github.com/jnetai-clawbot/clawbot-games/releases)
- [Quantum Assault APK](https://github.com/jnetai-clawbot/clawbot-games/releases)
- [Neon Snake APK](https://github.com/jnetai-clawbot/clawbot-games/releases)
- [Color Fall APK](https://github.com/jnetai-clawbot/clawbot-games/releases)

## 🔄 Automatic Builds

APKs are automatically built when you push to the `android` folder!

1. Push changes to `android/` folder
2. GitHub Actions builds all 4 games
3. Downloads available in Actions artifacts
4. Release created automatically with all APKs

## 🛠️ Build Manually

```bash
# Install buildozer
pip install buildozer cython

# Build a specific game
cd android/neon-void
buildozer android debug

# APK location: bin/*.apk
```

## 🎮 Buildozer Config

Each game folder contains:
- `main.py` - Game source code
- `buildozer.spec` - Build configuration
- `game.json` - Game metadata

## 🌐 Web Versions

HTML5 versions available at:
- [github.com/jnetai-clawbot/clawbot-games](https://github.com/jnetai-clawbot/clawbot-games)

## 🤖 Built with Kivy

[Kivy](https://kivy.org) - Open source Python library for rapid development of applications
that make use of innovative user interfaces, such as multi-touch apps.
