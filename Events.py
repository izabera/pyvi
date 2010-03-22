import curses




def event2key(event):
  eventhash = {
    27: "<ESC>",
    4 : "<BREAK>",
    curses.KEY_UP: "<UP>",
    curses.KEY_DOWN: "<DOWN>",
    curses.KEY_RIGHT:"<RIGHT>",
    curses.KEY_LEFT: "<LEFT>",
    5: "<C-e>",
    25: "<C-y>",
    8: "<C-h>",
    12: "<C-l>",
    32: "<space>",
    40: "<lparen>",
    41: "<rparen>",
    33: "<bang>",
    96: "<backtick>",
    39: "<squote>",
    34: "<dquote>",
    45: "<dash>",
    95: "<uscore>",
    -2: "<INIT>"
  }
  for e in range(65,91):
    eventhash[e] = chr(e)
  for e in range(97,123):
    eventhash[e] = chr(e)
  return eventhash.get(event,"<UNKNOWN>")

