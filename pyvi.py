from curses.wrapper import wrapper
import signal,curses,os,sys
import Editor
from Errors import *
from Events import *

def update(stdscr,ed):
  lines = ed.port()
  for y in range(len(lines)):
    stdscr.addstr(y,0,lines[y])
  stdscr.refresh()

def main(stdscr):
  (y,x) = stdscr.getmaxyx()
  ed = Editor.Editor(y-1,x)
  if len(sys.argv) > 1:
    filename = sys.argv[1]
    ed.buffer.load_from_file(filename)
  else:
    filename = ""
  curses.curs_set(0)
  update(stdscr,ed)
  event = -2
  while True:
    if ed.exit:
      break
    elif event == curses.KEY_RESIZE:
      (y,x) = stdscr.getmaxyx()
      ed.set_win(0,y-1,x)
      update(stdscr,ed)
    else:
      try:
        ed.handle_key(event2key(event))
      except KeyChainError, e:
        curses.flash()
      update(stdscr,ed)

    if not ed.exit:
      stdscr.addstr(y-2,x-15,"%d: %s" % (event,event2key(event)))
      stdscr.chgat(ed.cursor.y-ed.win.top,ed.cursor.x,1,curses.A_STANDOUT)
      stdscr.refresh()
      event = stdscr.getch()


wrapper(main)






