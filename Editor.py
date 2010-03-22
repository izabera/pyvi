from Buffer import Buffer
from Handler import Handler
import curses
from Errors import KeyChainError

class Cursor:
  def __init__(self,x=0,y=0):
    self.x = x
    self.y = y
  def __str__(self):
    return str((self.x,self.y))
class Window:
  def __init__(self,top=0,x=0,y=0):
    self.top = top
    self.x = x
    self.y = y
  def __str__(self):
    return str((self.top,self.x,self.y))

def linepad(line,width):
  if line.endswith("\n"):
    line = line[:-1]
  if len(line) > width:
    return line[:width]
  elif len(line) < width:
    return line + (width - len(line)) * " " 
  else:
    return line

class Editor:
  def __init__(self,h,w):
    self.win = Window(top=0,x=w,y=h)
    self.buffer = Buffer()
    self.filename = ""
    self.cursor = Cursor()
    self.mode = "normal"
    self.exit = False
    self.handlers = Handler()
    self.command = ""
    self.message = ""
  def __str__(self):
    return "An Editor"


  def port(self):
    lines = self.textport()
    lines.append(self.statline())
    return lines
  def textport(self):
    if not self.buffer.valid_line(self.win.top):
      raise IndexError, "Line %d is not within the buffer." % self.win.top
    if self.win.top+ self.win.y >= self.buffer.line_count():
      slines = self.buffer.lines[self.win.top:]
      extracount = self.win.y - len(slines)
      for i in range(extracount):
        slines.append("")
    else:
      slines = self.buffer.lines[self.win.top:self.win.top+self.win.y]
    vlines = [linepad(line,self.win.x) for line in slines]
    return vlines
  def statline(self):
    if self.command:
      left = self.command
    else:
      left = self.message
    right = "%s  %s " % (self.mode,self.cursor)
    line = left + " " * (self.win.x - len(left) - len(right) - 1) + right
    return line
  def set_win(self,firstline,height,width):
    if height < 2 or width < 10 or firstline < 0:
      raise Exception, "Can't set a window to (%d,%d,%d)." % (firstline,height,width)
    self.win.y = height
    self.win.x = width
    self.win.top = firstline
    #adjust cursor to still be in the window..
    if self.cursor.y >= self.win.top + self.win.y:
      self.cursor.y = self.win.top+ self.win.y - 1
    elif self.cursor.y < self.win.top:
      self.cursor.y = self.win.top
    if self.cursor.x >= self.win.x:
      self.cursor.x = self.win.x - 1

  def move_cursor(self,row=-1,col=-1):
    if row == -1: row = self.cursor.y
    if col == -1: col = self.cursor.x
    nc = Cursor(y=self.cursor.y,x=self.cursor.x)
    #find a good y value
    if row >= self.buffer.line_count():
      nc.y = self.buffer.line_count()-1
    elif row < 0:
      nc.y = 0
    else:
      nc.y = row
    #find a good x value on that line
    if col >= len(self.buffer.get_line(nc.y)):
      nc.x = len(self.buffer.get_line(nc.y)) - 1
    elif col < 0:
      nc.x = 0
    else:
      nc.x = col
    if nc.x > self.win.x-1:
      nc.x = self.win.x-1
    self.cursor = nc
    #adjust the window to include the cursor
    if self.cursor.y < self.win.top:
      self.win.top = self.cursor.y
    elif self.cursor.y >= self.win.top + self.win.y:
      self.win.top = self.cursor.y - self.win.y + 1

  def move_window(self,top):
    newtop = self.win.top
    #figure out where the window will now sit
    if top < 0:
      newtop = 0
    elif top >= self.buffer.line_count() - self.win.y:
      newtop = max(0,self.buffer.line_count()-self.win.y)
    else:
      newtop = top
    self.win.top = newtop
    #figure out a new cursor location that's within that window.
    if self.cursor.y < self.win.top:
      self.move_cursor(row=self.win.top)
    elif self.cursor.y >= self.win.top + self.win.y:
      self.move_cursor(row=self.win.top + self.win.y - 1)


  def handle_key(self,key):
    self.message = ""
    self.command = self.command + key
    if self.handlers.mode[self.mode].has_key(self.command):
      self.handlers.call_handler(self,self.mode,self.command)
      self.command = ""
    else:
      keys = self.handlers.mode[self.mode].keys()
      for key in keys:
        if key.startswith(self.command):
          return
      attempted = self.command
      self.command = ""
      raise KeyChainError, "The keychain '%s' doesn't belong to any existing maps." % attempted





    
