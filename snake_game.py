
#Loja Snake ne Python duke perdorur modulin curses

# curses moduli i Python na jep mundesine te krijojme aplikacione ne terminal psh(input keyboar, screenviewer, mouse, etc)
import curses
# do ta perdorim per te gjeneruar pozicione te ndryshme te ushqimit ne fushen e lojes
import random
# 
import time

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score
    
    # Hide cursor
    curses.curs_set(0)
    
    # Game variables
    snake_color = curses.color_pair(1)
    food_color = curses.color_pair(2)
    score_color = curses.color_pair(3)
    
    # Get screen dimensions
    height, width = stdscr.getmaxyx()
    
    # Create game window that's smaller than full terminal
    win_height = min(30, height - 2)
    win_width = min(100, width - 2)
    
    # Center the window
    start_y = (height - win_height) // 2
    start_x = (width - win_width) // 2
    
    # Create game window
    win = curses.newwin(win_height, win_width, start_y, start_x)
    win.keypad(True)      # Enable arrow keys
    win.timeout(150)      # Refresh rate in ms
    
    def initialize_game():
        # Snake initial position (center of screen)
        snake_x = win_width // 4
        snake_y = win_height // 2
        
        # Initial snake body (3 segments)
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2]
        ]
        
        # Initial food position (random)
        food = place_food(snake)
        
        # Initial direction
        key = curses.KEY_RIGHT
        
        # Initial score
        score = 0
        
        return snake, food, key, score
    
    def place_food(snake):
        while True:
            food = [
                random.randint(1, win_height - 2),
                random.randint(1, win_width - 2)
            ]
            # Make sure food doesn't appear on snake
            if food not in snake:
                return food
    
    def display_game_over(score):
        win.clear()
        game_over_text = "GAME OVER"
        score_text = f"Final Score: {score}"
        restart_text = "Press 'R' to Restart or 'Q' to Quit"
        
        # Display game over message
        win.addstr(win_height // 2 - 2, (win_width - len(game_over_text)) // 2, 
                  game_over_text, curses.A_BOLD)
        
        # Display score
        win.addstr(win_height // 2, (win_width - len(score_text)) // 2, 
                  score_text, score_color)
        
        # Display restart instruction
        win.addstr(win_height // 2 + 2, (win_width - len(restart_text)) // 2, 
                  restart_text)
        
        win.refresh()
        
        # Wait for 'R' or 'Q' key
        while True:
            key = win.getch()
            if key in [ord('r'), ord('R')]:
                return True  # Restart
            elif key in [ord('q'), ord('Q')]:
                return False  # Quit
    
    def run_game():
        snake, food, key, score = initialize_game()
        
        while True:
            # Draw border
            win.border(0)
            
            # Display score
            score_text = f" Score: {score} "
            win.addstr(0, win_width - len(score_text) - 1, score_text, score_color)
            
            # Get next key press (non-blocking)
            next_key = win.getch()
            
            # If no key is pressed, continue with current direction
            if next_key == -1:
                pass
            # Quit game if 'q' is pressed
            elif next_key in [ord('q'), ord('Q')]:
                break
            # Otherwise set the key to the pressed key
            elif next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                key = next_key
            
            # Prevent snake from reversing direction
            if (key == curses.KEY_DOWN and next_key == curses.KEY_UP or
                key == curses.KEY_UP and next_key == curses.KEY_DOWN or
                key == curses.KEY_LEFT and next_key == curses.KEY_RIGHT or
                key == curses.KEY_RIGHT and next_key == curses.KEY_LEFT):
                key = key
            else:
                key = key if next_key == -1 else next_key
            
            # Calculate new head position based on direction
            new_head = [snake[0][0], snake[0][1]]
            
            if key == curses.KEY_DOWN:
                new_head[0] += 1
            elif key == curses.KEY_UP:
                new_head[0] -= 1
            elif key == curses.KEY_LEFT:
                new_head[1] -= 1
            elif key == curses.KEY_RIGHT:
                new_head[1] += 1
            
            # Insert new head
            snake.insert(0, new_head)
            
            # Check if snake hit the border
            if (snake[0][0] == 0 or snake[0][0] == win_height - 1 or
                snake[0][1] == 0 or snake[0][1] == win_width - 1):
                if display_game_over(score):
                    return True  # Restart game
                else:
                    return False  # Quit game
            
            # Check if snake hit itself
            if snake[0] in snake[1:]:
                if display_game_over(score):
                    return True  # Restart game
                else:
                    return False  # Quit game
            
            # Check if snake ate food
            if snake[0] == food:
                # Create new food
                food = place_food(snake)
                score += 10
                
                # Speed up the game slightly as score increases
                win.timeout(max(50, 100 - (score // 100) * 10))
            else:
                # Remove tail if didn't eat food
                tail = snake.pop()
                # Clear the tail position
                win.addch(tail[0], tail[1], ' ')
            
            # Draw food
            win.addch(food[0], food[1], '*', food_color)
            
            # Draw snake
            for i, segment in enumerate(snake):
                if i == 0:
                    win.addch(segment[0], segment[1], '@', snake_color)  # Head
                else:
                    win.addch(segment[0], segment[1], 'O', snake_color)  # Body
            
            # Refresh screen
            win.refresh()
    
    # Game loop
    while True:
        # Run the game, check if need to restart
        if not run_game():
            break

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Game terminated by Skendri Peza & Eriglen Mata")
    finally:
        print("Thanks for playing Snake Game!")

