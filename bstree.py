import pickle

class BSTNode:
  def __init__(self, token_list):
    #token list is a nonempty, sorted list of token strings
    mid = len(token_list)
    self.l = self.r = None
    self.val = token_list[mid]
    if mid!=0:
      self.l = BSTNode(token_list[:mid])
    if mid!=len(token_list):
      self.r = BSTNode(token_list[mid+1:])

  def search(self, string):
    if self.val == string:
      return self
    if self.val >string:
      if not self.l:
        return self
      return self.l.search(string)
    else:
      if not self.r:
        return None
      return self.r.search(string)

class BST:
  def __init__(self, token_list):
    self.root = BSTNode(token_list)

  def search(self, string):
    
