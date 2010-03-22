import exceptions

class KeyChainError(exceptions.Exception):
  def __init__(self,text):
    self.text = text
  def __str__(self):
    return "Keychain Error: %s" % self.text
