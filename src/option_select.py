import curses
from pathlib import Path


def print_menu(stdscr, selected_indices, options):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(options):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(options) // 2 + idx
        if y < 0 or x < 0:
            continue  # Skip if position is out of bounds
        if idx in selected_indices:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def print_menu(stdscr, selected_indices, options, current_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(options):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(options) // 2 + idx
        if y < 0 or x < 0:
            continue  # Skip if position is out of bounds
        if idx == current_row_idx:
            stdscr.attron(curses.color_pair(2))  # Highlight color
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(2))
        elif idx in selected_indices:
            stdscr.attron(curses.color_pair(1))  # Selected color
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def main(stdscr, options):
    curses.curs_set(0)
    stdscr.keypad(True)  # Enable keypad input
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected color
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight color
    current_row_idx = 0
    selected_indices = []
    print_menu(stdscr, selected_indices, options, current_row_idx)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(options) - 1:
            current_row_idx += 1
        elif key == ord(" "):  # Space bar to select/unselect
            if current_row_idx in selected_indices:
                selected_indices.remove(current_row_idx)
            else:
                selected_indices.append(current_row_idx)
        elif key == ord("\n"):  # Enter to confirm selection
            stdscr.addstr(
                len(options) + 5,
                0,
                f"You selected: {[options[i] for i in selected_indices]}",
            )
            stdscr.refresh()
            stdscr.getch()
            return [options[i] for i in selected_indices]
        print_menu(stdscr, selected_indices, options, current_row_idx)


def select(options):
    # Ensure options are strings
    options = [str(option) for option in options]
    return curses.wrapper(lambda stdscr: main(stdscr, options))
