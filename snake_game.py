import curses
import random
# import time

# funksioni kryesor i lojes 
def main(stdscr):
    # Initialize colors
    curses.start_color() # Aktivizon modalitetin e ngjyrave.
     #curses.init_pair(index, fg, bg) percakton ngjyrat — jeshile me background te zi (snake), e kuqe (ushqimi), e verdhe (piket) 
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Ushqimi
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK) # Piket
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK) # ngjyra e titullit te lojes

    height, width = stdscr.getmaxyx() # Marrim dimensionet e terminalit

    # Përcaktojme madhësinë dhe pozicionin e dritares
    win_height = min(30, height - 2) # Siguron që dritarja e lojës të përshtatet brenda terminalit.
    win_width = min(100, width - 2)
    start_y = (height - win_height) // 2 # Llogarit këndet per tu shfaqur loja ne qender.
    start_x = (width - win_width) // 2

    win = curses.newwin(win_height, win_width, start_y, start_x) # krijojme nje dritare per lojen qe te sfaqet
    win.keypad(True) # Aktivizon tastierën e paisjes per pergjigjie.
    win.timeout(120) # vendos shpejtesine e lojes

    win.addstr(0, 2, "SNAKE GAME", curses.A_BOLD) # Shtojme titullin e lojes
    # win.addstr(0, win_width - 12, "Score: 0", curses.A_BOLD) # Shtojme titullin e lojes

    # Hide cursor
    curses.curs_set(0)

    # hapim variabla per secilin objekt per ti dhene vleren e ngjyrave qe kemi percaktuar me lart 
    snake_color = curses.color_pair(1)
    food_color = curses.color_pair(2)
    score_color = curses.color_pair(3)
    title_color = curses.color_pair(4)

    # funksioni per inicializimin e lojes psh(si do te levizi snake, ku do te dali ushqimi, etj) 
    def initialize_game():
        snake_x = win_width // 4 # Pjestoni win_width me 4 = (të plotë) dhe ruajm ne variabel atë rezultat në snake_x
        snake_y = win_height // 2
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2],
            # [snake_y, snake_x - 3],
            # [snake_y, snake_x - 4],
            # [snake_y, snake_x - 5],
            # [snake_y, snake_x - 6],
            # [snake_y, snake_x - 7],
            # [snake_y, snake_x - 8],
        ] # Kjo krijon trupin fillestar të snake si një listë koordinatash
        food = place_food(snake)
        key = curses.KEY_RIGHT
        score = 0
        return snake, food, key, score

    # funksioni per vendosjen e ushqimit ne pozicione te rastit 
    def place_food(snake):
        while True:
            food = [
                random.randint(1, win_height - 2),
                random.randint(1, win_width - 2)
            ]
            if food not in snake:
                return food

    # funksioni per te nxjerr tabelen e lojes game over si dhe te jep mundesine ta rinisesh lojen ose ta dalesh nga loja
    def display_game_over(score):
        win.clear()
        game_over_text = "GAME OVER"
        score_text = f"Final Score: {score}"
        restart_text = "Press 'R' to Restart or 'Q' to Quit"
        game_creators_text = "This Game is Created by Skendri Peza & Eriglen Mata. Falemniderit!"

        win.addstr(win_height // 2 - 2, (win_width - len(game_over_text)) // 2, 
                   game_over_text, curses.A_BOLD)
        win.addstr(win_height // 2, (win_width - len(score_text)) // 2, 
                   score_text, score_color)
        win.addstr(win_height // 2 + 2, (win_width - len(restart_text)) // 2, 
                   restart_text)
        win.addstr(win_height // 5, (win_width - len(game_creators_text)) // 2, game_creators_text, curses.A_BOLD)
        win.refresh()

        while True:
            key = win.getch()
            if key in [ord('r'), ord('R')]:
                return True
            elif key in [ord('q'), ord('Q')]:
                return False

    # funksioni per te treguar si do te funksionoi loja
    def run_game():
        snake, food, key, score = initialize_game()
        while True: # while loop 
            win.border(0) # percakton borderin e dritares se lojes
            score_text = f" Score: {score} || " # piket e lojes
            win.addstr(0, win_width - len(score_text) - 1, score_text, score_color)
            win.addstr(0, 40, "SNAKE GAME", title_color) # Shtojme ngjyren e titullit

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
    # i jep mundesein perdoruesit te rinis lojen
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