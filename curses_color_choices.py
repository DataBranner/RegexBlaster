#!/usr/bin/python

import curses

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    breaks = {
            17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95, 101, 
            107, 113, 119, 125, 131, 137, 143, 149, 155, 161, 167, 173, 
            179, 185, 191, 197, 203, 209, 215, 221, 227, 233}
    try:
        for i in range(0, curses.COLORS):
            if i in breaks:
                stdscr.addstr('\n')
            stdscr.addstr(str(i) + ' ', curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

curses.wrapper(main)
