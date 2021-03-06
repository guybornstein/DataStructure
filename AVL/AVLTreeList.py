#username - complete info
#id1      - 215061631
#name1    - Guy Bornstein
#id2      - 328491402
#name2    - Ori Dudai 



"""A class represnting a node in an AVL tree"""




import copy
from email.errors import FirstHeaderLineIsContinuationDefect
import sys


class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type value: str
	@param value: data of your node
	"""
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0
		

	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""
	def getLeft(self):
		if self.height==-1:
			return None
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""
	def getRight(self):
		if self.height == -1:
			return None
		return self.right

	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def getParent(self):
		return self.parent

	"""return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	"""
	def getValue(self):
		if self.height==-1:
			return None
		return self.value

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def getHeight(self):
		return self.height

	"""
 	returns the size
 
	@rtype: int
	@returns: the size of self, -1 if the node is virtual
	"""
	def getSize(self):
		return self.size

	"""
	sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def setLeft(self, node):
		self.left = node


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node

			
	def setSize(self, node):
		self.size = node


	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		self.parent = node

	"""sets value

	@type value: str
	@param value: data
	"""
	def setValue(self, value):
		self.value = value
		

	"""sets the balance factor of the node

	@type h: int
	@param h: the height
	"""
	def setHeight(self, h):
		self.height = h
  
	

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def isRealNode(self):
		return not (self.height == -1)


	def isLeaf(self):
		return ((not self.left.isRealNode()) or self.left == None) and ((not self.right.isRealNode()) or self.right == None)



"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		self.firstItem = None
		self.lastItem = None
		self.len = 0

	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.len == 0

	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		if i >= self.length() or i<0:
			return None
		a =  self.retrieveRec(self.root, i+1)
		return a.getValue()
  
	def retrieveNode(self, i):
		if i >= self.length() or i<0:
			return None
		if i==0:
			return self.firstItem
		return self.retrieveRec(self.root, i+1)
	
 
	def retrieveRec(self, node, i):
		if not node.left.isRealNode():
			r = 1
		else:
			r = node.left.getSize()+1
   
		if i == r:
			return node
		elif i < r:
			return self.retrieveRec(node.left, i)
		else:
			return self.retrieveRec(node.right, i - r)
			


	"""
 	inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, i, val):

		rebalancingOperationCounter = 0
  
		NewNode = AVLNode(val)
		NewNode.setLeft(AVLNode("fake"))
		NewNode.setRight(AVLNode("fake"))
		NewNode.right.parent = NewNode
		NewNode.left.parent = NewNode


		CurrentNode = self.root

		#List is empty
		if self.empty():
			self.root = NewNode
			self.lastItem = NewNode
			self.firstItem = NewNode
			self.len = 1
			AVLTreeList.changeHeight(NewNode)
			AVLTreeList.changeSize(NewNode)
			return 0, NewNode
		
		if i == self.len:
			CurrentNode = self.retrieveNode(self.len -1)
			CurrentNode.setRight(NewNode)
			NewNode.setParent(CurrentNode)
		else:
			CurrentNode = self.retrieveNode(i)
   
			if not CurrentNode.left.isRealNode():
				CurrentNode.setLeft(NewNode)
				NewNode.setParent(CurrentNode)

			else:
				CurrentNode = self.getPredecessor(CurrentNode)
				CurrentNode.setRight(NewNode)
				NewNode.setParent(CurrentNode)
    
		CurrentNode = NewNode.getParent()
		AVLTreeList.changeHeight(NewNode)
		AVLTreeList.changeSize(NewNode)

    
    
		while CurrentNode != None:
			prevHeight = CurrentNode.getHeight()
			AVLTreeList.changeHeight(CurrentNode)
			AVLTreeList.changeSize(CurrentNode)
   
			bf = AVLTreeList.getBalanceFactor(CurrentNode)

			if -2 < bf and bf < 2:
				if prevHeight == CurrentNode.getHeight():
					break
				else:
					rebalancingOperationCounter += 1
			
			else: 	
				#Left Left
				if bf == 2 and AVLTreeList.getBalanceFactor(CurrentNode.left) == 1:
					CurrentNode = AVLTreeList.rightRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Right
				elif bf == -2 and AVLTreeList.getBalanceFactor(CurrentNode.right) == -1:
					CurrentNode = AVLTreeList.leftRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Left
				elif bf == -2 and AVLTreeList.getBalanceFactor(CurrentNode.right) == 1:
					CurrentNode = AVLTreeList.leftRightRotation(CurrentNode)
					rebalancingOperationCounter += 2
		
				#Left Right
				elif bf == 2 and AVLTreeList.getBalanceFactor(CurrentNode.left) == -1:
					CurrentNode = AVLTreeList.rightLeftRotation(CurrentNode)
					rebalancingOperationCounter += 2
				break
			CurrentNode = CurrentNode.getParent()
   
		sizenode = CurrentNode
		if CurrentNode !=None:
			sizenode = CurrentNode.getParent()
   
		while sizenode != None:
			AVLTreeList.changeSize(sizenode)
			sizenode = sizenode.getParent()
		
		if NewNode.parent == self.firstItem:
			if NewNode.getParent().left == NewNode:
				self.firstItem = NewNode
		if NewNode.getParent() == self.lastItem:
				if NewNode.getParent().right == NewNode:
					self.lastItem = NewNode
     
		while self.root.getParent() != None:
			self.root = self.root.getParent()
  
		self.len += 1
		return rebalancingOperationCounter, NewNode


	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		
		rebalancingOperationCounter = 0
     
		if i >= self.len or i<0 or self.empty():
			return -1
		node = self.retrieveNode(i)
		nodeCopy = node
  

		# case 1: No children
		if node.isLeaf():
      		# case 1.1: only item
			if self.len == 1:
				self.root = None
				self.len = 0
				self.firstItem = None
				self.lastItem = None
				return 0
			elif node.getParent().getLeft() == node:
				node.getParent().setLeft(AVLNode("fake"))
				node.parent.left.parent = node.parent
			else:
				node.getParent().setRight(AVLNode("fake"))
				node.parent.right.parent = node.parent

		
    
		# case 2: one child
		elif node.left.isRealNode() and not node.right.isRealNode():
			if node.getParent() == None:
				self.root = node.left
				node.left.parent = None
			elif node.getParent().right == node:
				node.getParent().setRight(node.left)
			else:
				node.getParent().setLeft(node.left)
			node.left.setParent(node.getParent())
			node = node.left

		elif not node.left.isRealNode() and node.right.isRealNode:
			if node.getParent() == None:
				self.root = node.right
				node.right.parent = None
			elif node.getParent().right == node:
				node.getParent().setRight(node.right)
			else:
				node.getParent().setLeft(node.right)
			node.right.setParent(node.getParent())
			node = node.right

		
		# case 3: 2 children
		else:
			succ = self.getSuccessor(node)
			succCopy = copy.copy(succ)
   
			# delete succ
			if succ.isLeaf():
				if succ.getParent().getLeft() == succ:
					succ.getParent().setLeft(AVLNode("fake"))
					succ.parent.left.parent = succ.parent
				else:
					succ.getParent().setRight(AVLNode("fake"))
					succ.parent.right.parent = succ.parent

			else: 
				if succ.getParent().right == succ:
					succ.getParent().setRight(succ.right)

				else:
					succ.getParent().setLeft(succ.right)
					succ.getRight().setParent(succ.getParent())

			#replace node by succ
			succ.setParent(node.parent)
			succ.setRight(node.right)
			succ.setLeft(node.left)
			node.right.setParent(succ)
			node.left.setParent(succ)
			if node == self.root:
				self.root = succ
			else:
				if node.getParent().right == node:
					node.getParent().setRight(succ)
				else:
					node.getParent().setLeft(succ)
	
			if succCopy.parent == node:
				node = succ.right
			else:
				node = succCopy
    
    
		#avl
		CurrentNode = node.getParent()

    
		while CurrentNode != None:
			prevHeight = CurrentNode.getHeight()
			AVLTreeList.changeHeight(CurrentNode)
			AVLTreeList.changeSize(CurrentNode)
   
			bf = AVLTreeList.getBalanceFactor(CurrentNode)

			if -2 < bf and bf < 2:
				if prevHeight != CurrentNode.getHeight():
					rebalancingOperationCounter += 1
					#break

			
			else: 	
				#Left Left
				if bf == 2 and ((AVLTreeList.getBalanceFactor(CurrentNode.left) == 1) or (AVLTreeList.getBalanceFactor(CurrentNode.left) == 0)):
					CurrentNode = AVLTreeList.rightRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Right
				elif bf == -2 and (AVLTreeList.getBalanceFactor(CurrentNode.right) == -1 or AVLTreeList.getBalanceFactor(CurrentNode.right) == 0):
					CurrentNode = AVLTreeList.leftRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Left
				elif bf == -2 and AVLTreeList.getBalanceFactor(CurrentNode.right) == 1:
					CurrentNode = AVLTreeList.leftRightRotation(CurrentNode)
					rebalancingOperationCounter += 2
		
				#Left Right
				elif bf == 2 and AVLTreeList.getBalanceFactor(CurrentNode.left) == -1:
					CurrentNode = AVLTreeList.rightLeftRotation(CurrentNode)
					rebalancingOperationCounter += 2
				
			CurrentNode = CurrentNode.getParent()
   
   
		sizenode = CurrentNode
		if CurrentNode !=None:
			sizenode = CurrentNode.getParent()
   
		while sizenode != None:
			AVLTreeList.changeSize(sizenode)
			sizenode = sizenode.getParent()
   
		nodeSafe = nodeCopy
		if nodeSafe == self.firstItem:
			if nodeSafe.right.isRealNode():     		
				while nodeSafe.right.isRealNode():
					nodeSafe = nodeSafe.right
				self.firstItem = nodeSafe
			else:	
				self.firstItem = nodeSafe.getParent()
    
    
		if nodeCopy == self.lastItem:
			if nodeCopy.left.isRealNode():     		
				while nodeCopy.left.isRealNode():
					nodeCopy = nodeCopy.left
				self.lastItem = nodeCopy
			else:
				self.lastItem = nodeCopy.getParent()
   
		while self.root.getParent() != None:
			self.root = self.root.getParent()
   
		try:
			AVLTreeList.changeHeight(succ)
		except:
			1==1
   
   
		self.len -= 1
		return rebalancingOperationCounter


		

		
		


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.firstItem==None:
			return None
		return self.firstItem.getValue()
		

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.lastItem==None:
			return None
		return self.lastItem.getValue()
		

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		lst = []
		if self.root != None:
			self.inOrder(self.root.left, lst)
			lst.append(self.root.getValue())
			self.inOrder(self.root.right, lst)
		return lst

	def inOrder(self, node, lst):
		if node.isRealNode():
			self.inOrder(node.left, lst)
			lst.append(node.getValue())
			self.inOrder(node.right, lst)

	def aaa(node, lst):
		if node.isRealNode():
			AVLTreeList.aaa(node.left, lst)
			lst.append(node.getValue())
			AVLTreeList.aaa(node.right, lst)
	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return  self.len

	"""splits the list at the i'th index

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list according to whom we split
	@rtype: list
	@returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
	right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
	"""
	def split(self, i):
     
		node = self.retrieveNode(i)
     
		left = AVLTreeList()
		right = AVLTreeList()
     
		if node.left!=None and node.left.isRealNode():
			left.root = node.left
			left.len = node.left.getSize()
			tmp = node.left
			while tmp.left.isRealNode():
				tmp = tmp.left
			left.firstItem = tmp
			tmp = node.left
			while tmp.right.isRealNode():
				tmp = tmp.right
			left.lastItem = tmp
			left.root.parent = None
   
		if node.right!=None and node.right.isRealNode():
			right.root = node.right
			right.len = node.right.getSize()
			tmp = node.right
			while tmp.left.isRealNode():
				tmp = tmp.left
			right.firstItem = tmp
			tmp = node.right
			while tmp.right.isRealNode():
				tmp = tmp.right
			right.lastItem = tmp
			right.root.parent = None

		
		x = node.getParent()
		prev = node
		while x != None:
			next = x.getParent()
			if x.left == prev:
       
				if prev == node:
					x.left = AVLNode("fake")
					x.left.parent = x
					tmp = x
				x.right.setParent(None)
				if right.root!=None:
					right.root.setParent(None)
				right.len += x.right.getSize() + 1
				right.root = AVLTreeList.join(right.root, x, x.right)	
				if right.firstItem == None or not right.firstItem.isRealNode():
					right.firstItem = x
				tmp = right.getRoot()
				while tmp.right.isRealNode():
					tmp = tmp.right
				right.lastItem = tmp
			else:
				if prev == node:
					x.right = AVLNode("fake")
					x.right.parent = x
				x.left.setParent(None)
				if left.root!=None:
					left.root.setParent(None)
				left.len += x.left.getSize() + 1
				left.root = AVLTreeList.join(x.left, x, left.root)
				if left.lastItem == None or not left.lastItem.isRealNode():
					left.lastItem = x
				tmp = left.getRoot()
				while tmp.left.isRealNode():
					tmp = tmp.left
				left.firstItem = tmp

			prev = x
			x = next
			

  
		return [left, node.getValue(), right]

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):

		if lst.empty():
			if self.empty():
				return 0
			return self.root.getHeight()+1
		if self.empty():
			self.root = lst.root
			self.len = lst.len
			self.firstItem = lst.firstItem
			self.lastItem = lst.lastItem
			return lst.root.getHeight()+1
		if lst.length() == 1:
			self.insert(self.length(),lst.firstItem.getValue())
			return self.root.getHeight()-1
		if self.length() == 1:
			v = self.firstItem.getValue()
			self.root = lst.root
			self.len = lst.len
			self.firstItem = lst.firstItem
			self.lastItem = lst.lastItem
			self.insert(0,v)
			return lst.root.getHeight()-1

		diff = self.root.getHeight() - lst.root.getHeight()
  
		node = self.lastItem
	
		self.delete(self.len - 1)
		self.root = AVLTreeList.join(self.root, node, lst.root)
		self.len += lst.len+1
		self.lastItem = lst.lastItem
		return abs(diff)


	def join(left, node, right):
     
		if (left == None or not left.isRealNode()) and (right == None or not right.isRealNode()):
			node.Right = AVLNode("fake")
			node.Left = AVLNode("fake")
			node.right.parent = node
			node.left.parent = node
			AVLTreeList.changeHeight(node)
			AVLTreeList.changeSize(node)
			return node
			

       
		elif left == None or not left.isRealNode():
			tmp = AVLTreeList()
			tmp.root = right
			tmp.len = right.getSize()
			tmp.insert(0, node.getValue())
			return tmp.root

		elif right == None or not right.isRealNode():
			tmp = AVLTreeList()
			tmp.root = left
			tmp.len = left.getSize()
			tmp.insert(tmp.len, node.getValue())
			return tmp.root


		diff = left.getHeight() - right.getHeight()
		
		if diff <= 0:
      
			subtree = right
      
			while subtree.getHeight() > left.getHeight():
				subtree = subtree.left

			c = subtree.getParent()
			node.setRight(subtree)
			node.setLeft(left)
			left.setParent(node)
			subtree.setParent(node)
			node.setParent(c)
			if c == None:
				c = AVLNode(node.value)
				c.setLeft(left)
				left.setParent(c)
				c.setRight(subtree)
				subtree.setParent(c)
				AVLTreeList.changeHeight(c)
				AVLTreeList.changeSize(c)
				return c
			else:
				c.setLeft(node)
   
			#rebalncing
  
  
  
			CurrentNode = node
    
			while CurrentNode != None:
				AVLTreeList.changeHeight(CurrentNode)
				AVLTreeList.changeSize(CurrentNode)
   
				bf = AVLTreeList.getBalanceFactor(CurrentNode)		
			
				if -2 == bf or bf == 2:
					#Left Left
					if bf == 2 and ((AVLTreeList.getBalanceFactor(CurrentNode.left) == 1) or (AVLTreeList.getBalanceFactor(CurrentNode.left) == 0)):
						CurrentNode = AVLTreeList.rightRotation(CurrentNode)

					#Right Right
					elif bf == -2 and (AVLTreeList.getBalanceFactor(CurrentNode.right) == -1 or AVLTreeList.getBalanceFactor(CurrentNode.right) == 0):
						CurrentNode = AVLTreeList.leftRotation(CurrentNode)
		
					#Right Left
					elif bf == -2 and AVLTreeList.getBalanceFactor(CurrentNode.right) == 1:
						CurrentNode = AVLTreeList.leftRightRotation(CurrentNode)
		
					#Left Right
					elif bf == 2 and AVLTreeList.getBalanceFactor(CurrentNode.left) == -1:
						CurrentNode = AVLTreeList.rightLeftRotation(CurrentNode)

				if CurrentNode.parent == None:
					ro = CurrentNode
				
				CurrentNode = CurrentNode.getParent()
   
   
			return ro
   
		else: 
			subtree = left
      
			while subtree.getHeight() > right.getHeight():
				subtree = subtree.right

			c = subtree.getParent()

			node.setLeft(subtree)
			node.setRight(right)
			right.setParent(node)
			subtree.setParent(node)
			node.setParent(c)
			if c == None:
				c = AVLNode(node.value)
				c.setRight(right)
				left.setParent(c)
				c.setLeft(subtree)
				subtree.setParent(c)
				AVLTreeList.changeHeight(c)
				AVLTreeList.changeSize(c)
				return c
			c.setRight(node)
  
			CurrentNode = node
    
			while CurrentNode != None:

				AVLTreeList.changeHeight(CurrentNode)
				AVLTreeList.changeSize(CurrentNode)
   
				bf = AVLTreeList.getBalanceFactor(CurrentNode)		
			
				if -2 == bf or bf == 2:
					#Left Left
					if bf == 2 and ((AVLTreeList.getBalanceFactor(CurrentNode.right) == 1) or (AVLTreeList.getBalanceFactor(CurrentNode.right) == 0)):
						CurrentNode = AVLTreeList.rightRotation(CurrentNode)

					#Right Right
					elif bf == -2 and (AVLTreeList.getBalanceFactor(CurrentNode.left) == -1 or AVLTreeList.getBalanceFactor(CurrentNode.left) == 0):
						CurrentNode = AVLTreeList.leftRotation(CurrentNode)
		
					#Right Left
					elif bf == -2 and AVLTreeList.getBalanceFactor(CurrentNode.left) == 1:
						CurrentNode = AVLTreeList.leftRightRotation(CurrentNode)
		
					#Left Right
					elif bf == 2 and AVLTreeList.getBalanceFactor(CurrentNode.right) == -1:
						CurrentNode = AVLTreeList.rightLeftRotation(CurrentNode)
				if CurrentNode.parent == None:
					ro = CurrentNode
				
				CurrentNode = CurrentNode.getParent()
    

   
			return ro

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		if self.root == None or not self.root.isRealNode():
			return -1		
		i = self.search_rec(self.root.left, val)
		if i != -1:
			return i
		if self.root.value == val:
			return self.getRank(self.root) - 1
		return self.search_rec(self.root.right, val)

	def search_rec(self, node, val):
		if not node.isRealNode():
			return -1		
		i = self.search_rec(node.left, val)
		if i != -1:
			return i
		if node.value == val:
			return self.getRank(node) - 1
		return self.search_rec(node.right, val) 
		



	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return self.root


	def getPredecessor(self, node):
		if node.left.isRealNode():
			node = node.left
			while node.right.isRealNode():
				node = node.right
			return node
		else:
			prevNode = node
			node = node.getParent()
			while node.right == prevNode:
				prevNode = node()
				node = node.getParent()
			return node

	def getSuccessor(self, node):
		if node.right.isRealNode():
			node = node.right
			while node.left.isRealNode():
				node = node.left
			return node
		else:
			prevNode = node
			node = node.getParent()
			while node.left == prevNode:
				prevNode = node()
				node = node.getParent()
			return node

	#Updates the height of node by the heights of his children
	def changeHeight(node):
		if node.value == "fake":
			return
		if (not node.left.isRealNode()) and (not node.right.isRealNode()):
			node.setHeight(0)
			return
		leftheight, rightheight = 0, 0
		if node.left.isRealNode():
			leftheight= node.left.getHeight()
		if node.right.isRealNode():
			rightheight= node.right.getHeight()
		node.setHeight(max(leftheight, rightheight) +1)
	
	#Updates the size of node by the sizes of his children
	def changeSize(node):
		if node.value == "fake":
			return
		leftsize, rightsize = 0, 0
		if node.left.isRealNode():
			leftsize= node.left.getSize()
		if node.right.isRealNode():
			rightsize= node.right.getSize()
		node.setSize(leftsize + rightsize + 1)
  
  
	#Give the upper, returns the upper
	def rightRotation(a):
     
		b = a.left
		t = b.right
		if a.parent != None:
			if a.parent.right == a:
				a.parent.setRight(b)
			else:
				a.parent.setLeft(b)
		b.setRight(a)
		b.setParent(a.getParent())
		a.setParent(b)
		a.setLeft(t)
		t.setParent(a)

		
		AVLTreeList.changeHeight(a)
		AVLTreeList.changeHeight(b)
		
		AVLTreeList.changeSize(a)
		AVLTreeList.changeSize(b)
		if b.parent != None:
			AVLTreeList.changeHeight(b.parent)
			AVLTreeList.changeSize(b.parent)
		return b
		
	def leftRotation(a):
		b = a.right
		t = b.left
		if a.parent != None:
			if a.parent.right == a:
				a.parent.setRight(b)
			else:
				a.parent.setLeft(b)
		b.setLeft(a)
		a.setRight(t)
		b.setParent(a.getParent())
		a.setParent(b)
		t.setParent(a)
		
		AVLTreeList.changeHeight(a)
		AVLTreeList.changeHeight(b)
		AVLTreeList.changeSize(a)
		AVLTreeList.changeSize(b)
		if b.parent != None:
			AVLTreeList.changeHeight(b.parent)
			AVLTreeList.changeSize(b.parent)
		return b

	def rightLeftRotation(node):
		node.setLeft(AVLTreeList.leftRotation(node.left))
		return AVLTreeList.rightRotation(node)
     
	def leftRightRotation(node):
		node.setRight(AVLTreeList.rightRotation(node.right))
		return AVLTreeList.leftRotation(node)
		
	def getBalanceFactor(node):
		if not node.isRealNode():
			return 0
		x,y = node.left.getHeight(), node.right.getHeight()

		return x - y

	def getRank(self, node):
		tmp = node
		a = node.left.getSize() + 1
		while tmp.parent != None:
			if tmp.parent.getRight()==tmp:
				a = a+ tmp.parent.left.getSize()+1
			tmp = tmp.parent

		return a




	def insertTest(self, i, val):

		rebalancingOperationCounter = 0
  
		NewNode = AVLNode(val)
		NewNode.setLeft(AVLNode("fake"))
		NewNode.setRight(AVLNode("fake"))
		NewNode.right.parent = NewNode
		NewNode.left.parent = NewNode


		CurrentNode = self.root

		#List is empty
		if self.empty():
			self.root = NewNode
			self.lastItem = NewNode
			self.firstItem = NewNode
			self.len = 1
			AVLTreeList.changeHeight(NewNode)
			AVLTreeList.changeSize(NewNode)
			return 0, NewNode
		
		if i == self.len:
			CurrentNode = self.lastItem
			CurrentNode.setRight(NewNode)
			NewNode.setParent(CurrentNode)
		else:
			CurrentNode = self.retrieveNode(i)
   
			if not CurrentNode.left.isRealNode():
				CurrentNode.setLeft(NewNode)
				NewNode.setParent(CurrentNode)

			else:
				CurrentNode = self.getPredecessor(CurrentNode)
				CurrentNode.setRight(NewNode)
				NewNode.setParent(CurrentNode)
    
		CurrentNode = NewNode.getParent()
		AVLTreeList.changeHeight(NewNode)
		AVLTreeList.changeSize(NewNode)

    
    
		while CurrentNode != None:
			prevHeight = CurrentNode.getHeight()
			AVLTreeList.changeHeight(CurrentNode)
			AVLTreeList.changeSize(CurrentNode)
   
			bf = AVLTreeList.getBalanceFactor(CurrentNode)

			if prevHeight != CurrentNode.getHeight():
				rebalancingOperationCounter += 1
			
			
			CurrentNode = CurrentNode.getParent()
   
		
		
		if NewNode.parent == self.firstItem:
			if NewNode.getParent().left == NewNode:
				self.firstItem = NewNode
		if NewNode.getParent() == self.lastItem:
				if NewNode.getParent().right == NewNode:
					self.lastItem = NewNode
     
		while self.root.getParent() != None:
			self.root = self.root.getParent()
  
		self.len += 1
		return rebalancingOperationCounter, NewNode

	def getDepth(self, node):
		i = 0
		while node.parent != None:
			i+=1
			node = node.parent
		return i


fromStartBalanced = AVLTreeList()
fromStartNotBalanced = AVLTreeList()

sumRebalanceBalanced = [0,0,0,0,0,0,0,0,0,0]
sumRebalanceNotBalanced = [0,0,0,0,0,0,0,0,0,0]
sumDepthBalanced = [0,0,0,0,0,0,0,0,0,0]
sumDepthNotBalanced = [0,0,0,0,0,0,0,0,0,0]

sys.setrecursionlimit(10000)

print(sys.getrecursionlimit())

for i in range(1, 11):
	for j in range(1000*i):
		x = fromStartBalanced.insert(0, j)
		sumRebalanceBalanced[i-1] += x[0]
		sumDepthBalanced[i-1] += fromStartBalanced.getDepth(x[1])
		x = fromStartNotBalanced.insertTest(0, j)
		sumRebalanceNotBalanced[i-1] += x[0]
		sumDepthNotBalanced[i-1] += fromStartNotBalanced.getDepth(x[1])
	print("passed " + str(i))
	print(i)
	print("Balanced Tree avg of rebalancing opr: " + str(sumRebalanceBalanced[i-1]/((i)*1000)))
	print("UnBalanced Tree avg of rebalancing opr: " + str(sumRebalanceNotBalanced[i-1]/((i)*1000)))
	print("Balanced Tree avg depth: " + str(sumDepthBalanced[i-1]/((i)*1000)))
	print("UnBalanced Tree avg depth: " + str(sumDepthNotBalanced[i-1]/((i)*1000)))
        

for i in range(0, 9):
	print(i+1)
	print("Balanced Tree avg of rebalancing opr: " + str(sumRebalanceBalanced[i]/((i+1)*1000)))
	print("UnBalanced Tree avg of rebalancing opr: " + str(sumRebalanceNotBalanced[i]/((i+1)*1000)))
	print("Balanced Tree avg depth: " + str(sumDepthBalanced[i]/((i+1)*1000)))
	print("UnBalanced Tree avg depth: " + str(sumDepthNotBalanced[i]/((i+1)*1000)))
        