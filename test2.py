#!/usr/bin/pytohn3

import curses
# import logging
# import logging.handlers


# logger = logging.getLogger('test2.py')
# logger.setLevel(logging.DEBUG)
# handler = logging.handlers.SysLogHandler(address = '/var/log')
# logger.addHandler(handler)


screen = curses.initscr()

# Update the buffer, adding text at different locations
row = 10
col = 20

## Positioning game platform
for r in range (0, row):
    trueCol = col * 2       # Considering the white space
    for c in range (0, trueCol):
        if c % 2 == 0:
            screen.addstr(r,c , "_")
        else:
            screen.addstr(r, c, " ")



# Changes go in to the screen buffer and only get
# displayed after calling `refresh()` to update
screen.refresh()

curses.napms(3000)
curses.endwin()
