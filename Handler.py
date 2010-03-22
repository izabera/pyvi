
syms = {
  "<space>"    : " ",
  "<lparen>"   : "(",
  "<rparen>"   : ")",
  "<bang>"     : "!",
  "<backtick>" : "`",
  "<squote>"   : "'",
  "<dquote>"   : '"',
  "<dash>"     : "-",
  "<uscore>"   : "_",
}

class Handler:
  """
  handler functions have take the parameters:
  1) Editor ed
  2) string mode (the mode it was called *from*)
  3) string keychain (the string of keys that called the handler)
  """

  def __init__(self):
    self.mode = {}
    self.add_default_handlers()

  def register_mode(self,modename):
    if not self.mode.has_key(modename):
      self.mode[modename] = {}
  def register_handler(self,mode,keychain,handler):
    self.register_mode(mode)
    for kc in self.mode[mode].keys():
      if kc.startswith(keychain) or keychain.startswith(kc):
        raise KeyError, "Cannot register '%s', there is a conflicting key in %s" % (keychain,mode)
    self.mode[mode][keychain] = handler
  def call_handler(self,ed,mode,keychain):
    if self.mode.has_key(mode) and self.mode[mode].has_key(keychain):
      func = self.mode[mode][keychain]
      func(ed,mode,keychain)
    else:
      raise KeyError, "No handler is registered for '%s.%s'" % (mode,keychain)


  def add_default_handlers(self):
    self.register_mode("normal")
    self.register_mode("insert")
    self.register_handler("normal","i",to_insert_mode)
    self.register_handler("insert","<ESC>",to_normal_mode)
    self.register_handler("normal","<BREAK>",set_exit)
    self.register_handler("insert","<BREAK>",set_exit)
    self.register_handler("normal","<INIT>",do_nothing)
    self.register_handler("normal","ZZ",save_and_quit)

    self.register_handler("normal","h",cursor_left)
    self.register_handler("normal","j",cursor_down)
    self.register_handler("normal","k",cursor_up)
    self.register_handler("normal","l",cursor_right)
    self.register_handler("normal","<LEFT>",cursor_left)
    self.register_handler("normal","<DOWN>",cursor_down)
    self.register_handler("normal","<UP>",cursor_up)
    self.register_handler("normal","<RIGHT>",cursor_right)
    self.register_handler("insert","<LEFT>",cursor_left)
    self.register_handler("insert","<DOWN>",cursor_down)
    self.register_handler("insert","<UP>",cursor_up)
    self.register_handler("insert","<RIGHT>",cursor_right)
    self.register_handler("normal","<C-h>",cursor_far_left)
    self.register_handler("normal","<C-l>",cursor_far_right)

    self.register_handler("normal","<C-e>",window_down)
    self.register_handler("normal","<C-y>",window_up)
    self.register_handler("insert","<C-e>",window_down)
    self.register_handler("insert","<C-y>",window_up)

    self.register_handler("normal","dd",delete_line)
    self.register_handler("normal","o",insert_line)
    self.register_handler("normal","x",remove_char)
    self.register_handler("normal","A",append_to_line)

    for c in "abcdefghijklmnopqrstuvwxyz":
      self.register_handler("insert",c,insert_character)
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
      self.register_handler("insert",c,insert_character)
    for c in "1234567890":
      self.register_handler("insert",c,insert_character)
    for s in syms:
      self.register_handler("insert",s,insert_symbol)

def to_insert_mode(ed,mode,kc):
  ed.mode = "insert"
def to_normal_mode(ed,mode,kc):
  ed.mode = "normal"
def do_nothing(ed,mode,kc):
  pass

def reload_from_file(ed,mode,kc):
  ed.buffer.read_from_file(ed.filename)
def save_and_quit(ed,mode,kc):
  ed.buffer.write_to_file("test.txt.bak")
  ed.exit = True
def set_exit(ed,mode,kc):
  ed.exit = True

def cursor_up(ed,mode,kc):
  ed.move_cursor(row=ed.cursor.y-1)
def cursor_down(ed,mode,kc):
  ed.move_cursor(row=ed.cursor.y+1)
def cursor_right(ed,mode,kc):
  ed.move_cursor(col=ed.cursor.x+1)
def cursor_left(ed,mode,kc):
  ed.move_cursor(col=ed.cursor.x-1)
def cursor_far_left(ed,mode,kc):
  ed.move_cursor(col=0)
def cursor_far_right(ed,mode,kc):
  ed.move_cursor(col=10000)
def window_up(ed,mode,kc):
  ed.move_window(ed.win.top-1)
def window_down(ed,mode,kc):
  ed.move_window(ed.win.top+1)

def delete_line(ed,mode,kc):
  ed.buffer.remove_line(ed.cursor.y)
  ed.move_cursor()
def insert_line(ed,mode,kc):
  ed.buffer.insert_line(ed.cursor.y+1,"")
  ed.move_cursor(row=ed.cursor.y+1)
  ed.mode="insert"
def append_to_line(ed,mode,kc):
  cursor_far_right(ed,mode,kc)
  to_insert_mode(ed,mode,kc)
def remove_char(ed,mode,kc):
  ed.buffer.remove_char(ed.cursor.y,ed.cursor.x)
  ed.move_cursor()

def insert_character(ed,mode,kc):
  char = kc[-1]
  ed.buffer.insert_char(ed.cursor.y,ed.cursor.x,char)
  ed.move_cursor(col=ed.cursor.x+1)
 
def insert_symbol(ed,mode,kc):
  symbolname = kc[kc.rfind("<"):]
  symbol = syms[symbolname]
  ed.buffer.insert_char(ed.cursor.y,ed.cursor.x,symbol)
  ed.move_cursor(col=ed.cursor.x+1)

