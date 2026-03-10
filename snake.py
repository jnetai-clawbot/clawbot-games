#!/usr/bin/env python3
"""
Snake Game - ClawBot Edition
Classic snake game with score tracking
"""

import curses
import random
import time

def main(stdscr):
    # Setup
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    # Game dimensions
    sh, sw = stdscr.getmaxyx()
    game_height = sh - 4
    game_width = sw - 4
    
    # Snake (list of y,x coordinates)
    snake = [(game_height // 2, game_width // 2)]
    direction = (0, 1)  # moving right
    score = 0
    speed = 100
    
    # Food
    food = (random.randint(1, game_height - 2), 
            random.randint(1, game_width - 2))
    
    # Border
    stdscr.border(0)
    score_win = curses.newwin(1, sw - 2, 0, 1)
    score_win.addstr(0, 0, f" ClawBot Snake | Score: {score} ", curses.color_pair(3))
    score_win.refresh()
    
    running = True
    while running:
        stdscr.border(0)
        
        # Display snake
        for i, (y, x) in enumerate(snake):
            if 0 < y < game_height and 0 < x < game_width:
                attr = curses.color_pair(1) if i == 0 else curses.color_pair(1)
                stdscr.addch(y, x, 'O', attr)
        
        # Display food
        if 0 < food[0] < game_height and 0 < food[1] < game_width:
            stdscr.addch(food[0], food[1], '*', curses.color_pair(2))
        
        stdscr.refresh()
        
        # Input
        key = stdscr.getch()
        
        if key == ord('q'):
            running = False
        elif key == curses.KEY_UP and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_DOWN and direction != (-1, 0):
            direction = (1, 0)
        elif key == curses.KEY_LEFT and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)
        
        # Move snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        
        # Check collision with walls
        if head[0] <= 0 or head[0] >= game_height - 1 or \
           head[1] <= 0 or head[1] >= game_width - 1:
            break
        
        # Check collision with self
        if head in snake:
            break
        
        snake.insert(0, head)
        
        # Eat food
        if head == food:
            score += 10
            score_win.clear()
            score_win.addstr(0, 0, f" ClawBot Snake | Score: {score} ", curses.color_pair(3))
            score_win.refresh()
            food = (random.randint(1, game_height - 2), 
                    random.randint(1, game_width - 2))
            # Speed up
            speed = max(50, speed - 2)
            stdscr.timeout(speed)
        else:
            snake.pop()
        
        time.sleep(0.01)
    
    # Game over
    stdscr.nodelay(0)
    msg = f"Game Over! Score: {score}"
    stdscr.addstr(game_height // 2, (game_width - len(msg)) // 2, msg, curses.color_pair(2))
    stdscr.addstr(game_height // 2 + 1, (game_width - 21) // 2, "Press any key to quit")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"Error: {e}")
        print("Run in terminal: python3 snake.py")
