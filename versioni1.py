import random
# curses Controls the terminal screen layout.
import curses

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(150)

    sh, sw = stdscr.getmaxyx()
    snk_x = sw // 4
    snk_y = sh // 2
    snake = [[snk_y, snk_x], [snk_y, snk_x - 1], [snk_y, snk_x - 2]]

    food = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
    stdscr.addch(food[0], food[1], '*')

    key = curses.KEY_RIGHT
    score = 0

    while True:
        stdscr.clear()
        stdscr.border()

        # Show score
        stdscr.addstr(0, 2, f'Score: {score}')

        # Draw food
        stdscr.addch(food[0], food[1], '*')

        # Get user input
        next_key = stdscr.getch()
        key = key if next_key == -1 else next_key

        # Calculate new head position
        head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_DOWN:
            head[0] += 1
        if key == curses.KEY_UP:
            head[0] -= 1
        if key == curses.KEY_LEFT:
            head[1] -= 1
        if key == curses.KEY_RIGHT:
            head[1] += 1

        snake.insert(0, head)

        # Game over check
        if head[0] in [0, sh - 1] or head[1] in [0, sw - 1] or head in snake[1:]:
            stdscr.addstr(sh // 2, sw // 2 - 5, "GAME OVER")
            stdscr.nodelay(0)
            stdscr.getch()
            break

        # Eating food
        if head == food:
            score += 10
            food = None
            while food is None:
                nf = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
                food = nf if nf not in snake else None
        else:
            tail = snake.pop()

        # Draw snake
        for y, x in snake:
            stdscr.addch(y, x, '#')

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
