import curses
import random
import time

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score

    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    # Define window size and position
    win_height = min(30, height - 2)
    win_width = min(100, width - 2)
    start_y = (height - win_height) // 2
    start_x = (width - win_width) // 2

    # Create game window
    win = curses.newwin(win_height, win_width, start_y, start_x)
    win.keypad(True)      # Enable arrow keys
    win.timeout(150)      # Refresh rate in ms
    win.nodelay(True)     # Non-blocking input

    # Hide cursor
    curses.curs_set(0)

    snake_color = curses.color_pair(1)
    food_color = curses.color_pair(2)
    score_color = curses.color_pair(3)

    def initialize_game():
        snake_x = win_width // 4
        snake_y = win_height // 2
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2]
        ]
        food = place_food(snake)
        key = curses.KEY_RIGHT
        score = 0
        return snake, food, key, score

    def place_food(snake):
        while True:
            food = [
                random.randint(1, win_height - 2),
                random.randint(1, win_width - 2)
            ]
            if food not in snake:
                return food

    def display_game_over(score):
        win.clear()
        game_over_text = "GAME OVER"
        score_text = f"Final Score: {score}"
        restart_text = "Press 'R' to Restart or 'Q' to Quit"

        win.addstr(win_height // 2 - 2, (win_width - len(game_over_text)) // 2, 
                   game_over_text, curses.A_BOLD)
        win.addstr(win_height // 2, (win_width - len(score_text)) // 2, 
                   score_text, score_color)
        win.addstr(win_height // 2 + 2, (win_width - len(restart_text)) // 2, 
                   restart_text)
        win.refresh()

        while True:
            key = win.getch()
            if key in [ord('r'), ord('R')]:
                return True
            elif key in [ord('q'), ord('Q')]:
                return False

    def run_game():
        snake, food, key, score = initialize_game()
        while True:
            win.border(0)
            score_text = f" Score: {score} "
            win.addstr(0, win_width - len(score_text) - 1, score_text, score_color)

            next_key = win.getch()
            if next_key == -1:
                pass
            elif next_key in [ord('q'), ord('Q')]:
                break
            elif next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                key = next_key

            if (key == curses.KEY_DOWN and next_key == curses.KEY_UP or
                key == curses.KEY_UP and next_key == curses.KEY_DOWN or
                key == curses.KEY_LEFT and next_key == curses.KEY_RIGHT or
                key == curses.KEY_RIGHT and next_key == curses.KEY_LEFT):
                key = key
            else:
                key = key if next_key == -1 else next_key

            new_head = [snake[0][0], snake[0][1]]

            if key == curses.KEY_DOWN:
                new_head[0] += 1
            elif key == curses.KEY_UP:
                new_head[0] -= 1
            elif key == curses.KEY_LEFT:
                new_head[1] -= 1
            elif key == curses.KEY_RIGHT:
                new_head[1] += 1

            snake.insert(0, new_head)

            # Collision with border
            if (snake[0][0] == 0 or snake[0][0] == win_height - 1 or
                snake[0][1] == 0 or snake[0][1] == win_width - 1):
                if display_game_over(score):
                    return True
                else:
                    return False

            # Collision with self
            if snake[0] in snake[1:]:
                if display_game_over(score):
                    return True
                else:
                    return False

            # Eat food
            if snake[0] == food:
                food = place_food(snake)
                score += 10
                win.timeout(max(50, 100 - (score // 100) * 10))
            else:
                tail = snake.pop()
                win.addch(tail[0], tail[1], ' ')

            win.addch(food[0], food[1], '*', food_color)

            for i, segment in enumerate(snake):
                if i == 0:
                    win.addch(segment[0], segment[1], '@', snake_color)
                else:
                    win.addch(segment[0], segment[1], 'O', snake_color)

            win.refresh()

    while True:
        if not run_game():
            break

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Game terminated by Skendri Peza & Eriglen Mata")
    finally:
        print("Thanks for playing Snake Game!")