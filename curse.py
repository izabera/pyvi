from curses.wrapper import wrapper
import signal
import curses
import Editor

def update(stdscr,ed):
  lines = ed.port()
  for y in range(len(lines)):
    stdscr.addstr(y,0,lines[y])
  stdscr.refresh()

def main(stdscr):
  (y,x) = stdscr.getmaxyx()
  ed = Editor.Editor(y-1,x)
  ed.buffer.load_from_file("test.txt")
  curses.curs_set(0)
  update(stdscr,ed)
  event = -1
  while True:
    if event == 4:
      break
    elif event == curses.KEY_RESIZE:
      (y,x) = stdscr.getmaxyx()
      ed.set_win(0,y,x)
      update(stdscr,ed)
    elif event == curses.KEY_UP:
      ed.move_cursor(row=ed.cursor.y-1,col=ed.cursor.x)
      update(stdscr,ed)
    elif event == curses.KEY_DOWN:
      ed.move_cursor(row=ed.cursor.y+1,col=ed.cursor.x)
      update(stdscr,ed)
    elif event == curses.KEY_LEFT:
      ed.move_cursor(row=ed.cursor.y,col=ed.cursor.x-1)
      update(stdscr,ed)
    elif event == curses.KEY_RIGHT:
      ed.move_cursor(row=ed.cursor.y,col=ed.cursor.x+1)
      update(stdscr,ed)
    elif event == 5:
      ed.move_window(ed.win.top+1)
      update(stdscr,ed)
    elif event == 25:
      ed.move_window(ed.win.top-1)
      update(stdscr,ed)
    stdscr.addstr(y-1,min(20,x-15),str(event)+"   ")
    stdscr.chgat(ed.cursor.y-ed.win.top,ed.cursor.x,1,curses.A_STANDOUT)
    stdscr.refresh()
    event = stdscr.getch()


wrapper(main)






