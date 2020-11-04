import pickle

class BSTNode:
  def __init__(self, token_list):
    #token list is a nonempty, sorted list of token strings
    mid = len(token_list)//2
    self.l = self.r = None
    self.val = token_list[mid]
    if mid!=0:
      self.l = BSTNode(token_list[:mid])
    if len(token_list)>1 and mid !=len(token_list)-1:
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

def minValue(node):
    current = node
    # loop down to find the leftmost leaf 
    while(current is not None):
        if current.left is None:
            break
        current = current.left
    return current

def inOrderSuccessor(root, n):
    # Step 1 of the above algorithm 
    if n.r is not None:
        return minValue(n.right)
    # Step 2 of the above algorithm 
    succ=None
    while(root):
        if(root.data<n.data):
            root=root.r
        elif(root.data>n.data):
            succ=root
            root=root.l
        else:
            break
    return succ
