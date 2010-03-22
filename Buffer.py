
class Buffer:
  def __init__(self):
    self.lines = [""]
  def __str__(self):
    return(self.get_contents())

  def set_contents(self,blob):
    if blob.endswith("\n"):
      blob = blob[:-1]
    self.lines = [ln + "\n" for ln in blob.split("\n")]
  def get_contents(self):
    return("".join(self.lines))

  def load_from_file(self,path):
    infile = open(path,"r")
    self.set_contents(infile.read())
    infile.close()
  def write_to_file(self,path):
    outfile = open(path,"w")
    outfile.write(self.get_contents())
    outfile.close()

  def line_count(self):
    return(len(self.lines))
  def size(self):
    return(len(self.get_contents()))

  def valid_position(self,row,col):
    if row < 0 or col < 0:
      return False
    try:
      char = self.lines[row][col]
    except IndexError:
      return False
    return True
  def valid_line(self,row):
    if row < 0:
      return False
    try:
      line = self.lines[row]
    except IndexError:
      return False
    return True
  
  def get_line(self,lnum):
    if not self.valid_line(lnum):
      raise IndexError, "Line %d is not within the buffer." % lnum
    return(self.lines[lnum])
  def insert_line(self,lnum,line):
    if not self.valid_line(lnum) and not self.valid_line(lnum-1):
      raise IndexError, "Line %d is not within the buffer." % lnum
    if "\n" in line[:-1]:
      raise Exception, "Lines cannot contain internal newline characters."
    if line[-1] != "\n":
      line = line + "\n" 
    self.lines.insert(lnum,line)
  def remove_line(self,lnum):
    if not self.valid_line(lnum):
      raise IndexError, "Line %d is not within the buffer." % lnum
    del(self.lines[lnum])
  def replace_line(self,lnum,line):
    if not self.valid_line(lnum):
      raise IndexError, "Line %d is not within the buffer." % lnum
    self.remove_line(lnum)
    self.insert_line(lnum,line)

  def get_char(self,lnum,col):
    if not self.valid_position(lnum,col):
      raise IndexError, "Position (%d,%d) is not within the buffer." % (lnum,col)
    return self.lines[lnum][col]
  def insert_char(self,lnum,col,char):
    if not self.valid_position(lnum,col):
      raise IndexError, "Position (%d,%d) is not within the buffer." % (lnum,col)
    line = self.get_line(lnum)
    left = line[:col]
    right = line[col:]
    self.replace_line(lnum,left + char + right)
  def remove_char(self,lnum,col):
    if not self.valid_position(lnum,col):
      raise IndexError, "Position (%d,%d) is not within the buffer." % (lnum,col)
    line = self.get_line(lnum)
    if col == len(line)-1 and lnum == self.line_count()-1:
      raise IndexError, "Cannot delete the final newline in the buffer."
    elif col == len(line)-1:
      nextline = self.get_line(lnum+1)
      self.remove_line(lnum)
      self.remove_line(lnum)
      self.insert_line(lnum,line[:-1] + nextline)
    else:
      ls = list(line)
      del(ls[col])
      self.replace_line(lnum,"".join(ls))
  def replace_char(self,lnum,col,char):
    self.remove_char(lnum,col)
    self.insert_char(lnum,col,char)

  #a blob includes both endpoints
  def valid_blob(self,startline,startcol,endline,endcol):
    if startline > endline:
      return False
    if startline == endline and startcol > endcol:
      return False
    if not self.valid_position(startline,startcol):
      return False
    if not self.valid_position(endline,endcol):
      return False
    return True
  def get_blob(self,startline,startcol,endline,endcol):
    if not self.valid_blob(startline,startcol,endline,endcol):
      raise Exception, "The blob (%d,%d)->(%d,%d) is not valid" % (startline,startcol,endline,endcol)
    #pick out the pieces
    lines = self.lines[startline:endline+1]
    lines[0] = lines[0][startcol:]
    lines[-1] = lines[-1][:endcol+1]
    return("".join(lines))
  def insert_blob(self,lnum,col,blob):
    if not self.valid_position(lnum,col):
      raise IndexError,"Position (%d,%d) is not within the buffer." % (lnum,col)
    if lnum < 0:
      lnum = self.line_count() + lnum
    line = self.get_line(lnum)
    left = line[:col]
    right = line[col:-1]
    lblob = left + blob + right
    blines = [ln+"\n" for ln in lblob.split("\n")]
    blines.reverse()
    for bline in blines:
      self.insert_line(lnum+1,bline)
    self.remove_line(lnum)
  def remove_blob(self,startline,startcol,endline,endcol):
    if not self.valid_blob(startline,startcol,endline,endcol):
      raise Exception, "The blob (%d,%d)->(%d,%d) is not valid" % (startline,startcol,endline,endcol)
    firstline = self.get_line(startline)
    left = firstline[:startcol]
    lastline = self.get_line(endline)
    right = lastline[endcol+1:]
    for i in range(endline,startline-1,-1):
      self.remove_line(i)
    self.insert_line(startline,left+right)
  def replace_blob(self,startline,startcol,endline,endcol,blob):
    self.remove_blob(startline,startcol,endline,endcol)
    self.insert_blob(startline,startcol,blob)



def testall():
  testline()
  testchar()
  testblob()
def testline():
  b = Buffer()
  b.set_contents("Test file\na line\nb line\n\nline line line\nlast line\n")
  if b.get_line(1) != "a line\n":
    print("Failed test 1")
  if b.get_line(4) != "line line line\n":
    print("Failed test 2\n")
  if b.line_count() != 6:
    print("Failed test 3")
  if b.get_contents() != "Test file\na line\nb line\n\nline line line\nlast line\n":
    print("Failed test 4")

  b.insert_line(2,"Inserted line")
  b.insert_line(4,"ins 2")
  b.insert_line(4,"ins 1\n")
  b.insert_line(7,"another line\n")
 
  if b.get_contents() != "Test file\na line\nInserted line\nb line\nins 1\nins 2\n\nanother line\nline line line\nlast line\n":
    print("Failed test 5")

  b.remove_line(1)
  b.remove_line(6)
  b.remove_line(4)

  if b.get_contents() != "Test file\nInserted line\nb line\nins 1\n\nline line line\nlast line\n":
    print("Failed test 6")

  b.replace_line(0,"A TEST FILE")
  b.replace_line(b.line_count()-1,"END OF FILE")

  if b.get_contents() != "A TEST FILE\nInserted line\nb line\nins 1\n\nline line line\nEND OF FILE\n":
    print("Failed test 7")

  print("Test(line) completed")
def testchar():
  b = Buffer()

  b.set_contents("Test file\na line\nb line\n\nline line line\nlast line\n")

  if b.valid_position(0,10) or not b.valid_position(2,4) or b.valid_position(-6,-9) or b.valid_position(-3,6):
    print("Failed test 0")

  if b.get_char(1,2) != "l":
    print("Failed test 1")
  if b.get_char(2,4) != "n":
    print("Failed test 2")
  
  b.insert_char(2,1,"Q")
  b.insert_char(5,5,"X")
  b.remove_char(1,4)
  b.replace_char(0,0,"t")
  b.remove_char(2,4)

  result = "test file\na lie\nbQ lne\n\nline line line\nlast Xline\n"
  if b.get_contents() != result:
    print("Failed test 3")

  b.remove_char(1,5)
  if b.get_contents() != "test file\na liebQ lne\n\nline line line\nlast Xline\n":
    print("Failed test 4")

  print("Test(char) completed")
def testblob():
  b = Buffer()
  b.set_contents("Test file\na line\nb line\n\nline line line\nlast line\n")

  if b.valid_blob(3,1,2,0) or not b.valid_blob(0,4,4,6):
    print("Failed test 0")

  if b.get_blob(1,3,4,5) != "ine\nb line\n\nline l":
    print("Failed test 1")

  b.insert_blob(2,3,"hello\nheres another\nline..")
  if b.get_contents() != "Test file\na line\nb lhello\nheres another\nline..ine\n\nline line line\nlast line\n":
    print("Failed test 2")
  
  b.remove_blob(1,4,6,0)
  if b.get_contents() != "Test file\na liine line line\nlast line\n":
    print("Failed test 3")

  b.replace_blob(1,3,2,2,"HOWDY\nPARDNER\n")
  if b.get_contents() != "Test file\na lHOWDY\nPARDNER\nt line\n":
    print("Failed test 4")

  print("Test(blob) completed")

