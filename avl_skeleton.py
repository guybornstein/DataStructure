#username - complete info
#id1      - 215061631
#name1    - Guy Bornstein
#id2      - 328491402
#name2    - Ori Dudai 



"""A class represnting a node in an AVL tree"""



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
		self.size = -1
		

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
		if self.height == -1:
			self.height = 0

	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node
		if self.height == -1:
			self.height = 0
			
	def setSize(self, node):
		self.size = node


	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		self.parent = node
		if self.height == -1:
			self.height = 0

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
		return (not self.left.isRealNode()) and (not self.right.isRealNode)



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
		return self.root == None


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		if i+1 >= self.len:
			return None
		return self.retrieveRec(self.root, i+1).getValue()
  
	def retrieveNode(self, i):
		if i >= self.len:
			return None
		return self.retrieveRec(self.root, i+1)
	
 
	def retrieveRec(self, node, i):
		r = node.getLeft().getSize() + 1
		if i == r:
			return node
		elif i < r:
			return self.retrieveRec(node.getLeft(), i)
		else:
			return self.retrieveRec(node.getRight(), i - r)
			


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
		NewNode.setValue(val)
		NewNode.setLeft(AVLNode("Rami pastuz"))
		NewNode.setRight(AVLNode("Rami pastuz"))
  
  
		CurrentNode = self.root

		"List is empty"
		if self.empty():
			self.root = NewNode
			self.lastItem = NewNode
			self.firstItem = NewNode
			return 0
		
		if i == self.len:
			CurrentNode = self.last()
			CurrentNode.setRight(NewNode)
			NewNode.setParent(CurrentNode)
		else:
			CurrentNode = self.retrieveNode(i+1)
   
			if not CurrentNode.getLeft().isRealNode():
				CurrentNode = self.last()
				CurrentNode.setLeft(NewNode)
				NewNode.setParent(CurrentNode)

			else:
				pre = self.getPredecessor(CurrentNode)
				pre.setRight(NewNode)
				NewNode.setParent(pre)
    
		CurrentNode = NewNode.getParent()
		self.changeHeight(CurrentNode)
		self.changeSize(CurrentNode)
    
		while CurrentNode != None:
			prevHeight = CurrentNode.getHeight()
			self.changeHeight(CurrentNode)
			self.changeSize(CurrentNode)
   
			bf = self.getBalanceFactor(CurrentNode)

			if -2 < bf and bf < 2:
				if prevHeight == CurrentNode.getHeight():
					break
				else:
					rebalancingOperationCounter += 1
			
			else: 	
				#Left Left
				if bf == 2 and self.getBalanceFactor(CurrentNode.getLeft()) == 1:
					self.rightRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Right
				elif bf == -2 and self.getBalanceFactor(CurrentNode.getRight()) == -1:
					self.leftRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Left
				elif bf == -2 and self.getBalanceFactor(CurrentNode.getRight()) == 1:
					self.rightLeftRotation(CurrentNode)
					rebalancingOperationCounter += 2
		
				#Left Right
				elif bf == 2 and self.getBalanceFactor(CurrentNode.getLeft()) == -1:
					self.leftRightRotation(CurrentNode)
					rebalancingOperationCounter += 2
				break
			CurrentNode = CurrentNode.getParent()
		
				
		if NewNode.parent == self.firstItem:
			self.firstItem = NewNode
		if NewNode.parent == self.lastItem:
			self.lastItem = NewNode
  
		self.len += 1
		return rebalancingOperationCounter



	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		
		rebalancingOperationCounter = 0
     
		if i >= self.len:
			return -1
		node = self.retrieveNode(i)
  
		  
		# case 1: No children
		if node.isLeaf():
      	# case 1.1: only item
			if self.len == 1:
				self.root = None
				self.len = 0
				return 0
			if node.getParent().getLeft == node:
				node.getParent().setLeft(AVLNode())
			else:
				node.getParent().setRight(AVLNode())
			
    
		# case 2: one child
		elif node.getLeft().isRealNode() and not node.getRight().isRealNode:
			if node.getParent().getRight() == node:
				node.getParent().setRight(node.getLeft())
			else:
				node.getParent().setLeft(node.getLeft())
			node.getLeft.setParent(node.getParent())

		elif not node.getLeft().isRealNode() and node.getRight().isRealNode:
			if node.getParent().getRight() == node:
				node.getParent().setRight(node.getRight())
			else:
				node.getParent().setLeft(node.getRight())
			node.getRight.setParent(node.getParent())
		
		# case 3: 2 children
		else:
			succ = self.getSuccessor(node)
   
			# delete succ
			if succ.isLeaf():
				if succ.getParent().getLeft == succ:
					succ.getParent().setLeft(AVLNode())
				else:
					succ.getParent().setRight(AVLNode())
			else: 
				if succ.getParent().getRight() == succ:
					succ.getParent().setRight(succ.getRight())
				else:
					succ.getParent().setLeft(succ.getRight())
					succ.getRight.setParent(succ.getParent())

			#replace node by succ
			succ.setParent(node.getParent)
			succ.setRight(node.getRight)
			succ.setLeft(node.getLeft)
			node.getRight().setParent(succ)
			node.getLeft().setParent(succ)
			if node.getParent().getRight() == node:
				node.getParent().setRight(succ)
			else:
				node.getParent().setLeft(succ)
    
    
		#avl
		CurrentNode = node.getParent()
		self.changeHeight(CurrentNode)
		self.changeSize(CurrentNode)
    
		while CurrentNode != None:
			prevHeight = CurrentNode.getHeight()
			self.changeHeight(CurrentNode)
			self.changeSize(CurrentNode)
   
			bf = self.getBalanceFactor(CurrentNode)

			if -2 < bf and bf < 2:
				if prevHeight == CurrentNode.getHeight():
					break
				else:
					rebalancingOperationCounter += 1
			
			else: 	
				#Left Left
				if bf == 2 and self.getBalanceFactor(CurrentNode.getLeft()) == 1:
					self.rightRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Right
				elif bf == -2 and self.getBalanceFactor(CurrentNode.getRight()) == -1:
					self.leftRotation(CurrentNode)
					rebalancingOperationCounter += 1
		
				#Right Left
				elif bf == -2 and self.getBalanceFactor(CurrentNode.getRight()) == 1:
					self.rightLeftRotation(CurrentNode)
					rebalancingOperationCounter += 2
		
				#Left Right
				elif bf == 2 and self.getBalanceFactor(CurrentNode.getLeft()) == -1:
					self.leftRightRotation(CurrentNode)
					rebalancingOperationCounter += 2
			CurrentNode = CurrentNode.getParent()
   
		if node == self.firstItem:
			self.firstItem = node.getParent
		if node == self.lastItem:
			self.lastItem = node.getParent
   
		self.len -= 1
		return rebalancingOperationCounter


		

		
		


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		return self.firstItem
		"""
		if self.empty():
			return None
		node = self.root
		while self.root.left.isRealNode():
				node = node.getLeft()
			
		return node.getValue()
		"""

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		return self.lastItem
		"""
		if self.empty():
			return None
		node = self.root
		while node.isRealNode():
			node = node.getLeft()
		return node.getValue()
  		"""

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		lst = []
		if self.root != None:
			self.inOrder(self.root.getLeft(), lst)
			lst.append(self.root.getValue)
			self.inOrder(self.root.getRight(), lst)
		return lst

	def inOrder(self, node, lst):
		if node.isRealNode():
			self.inOrder(node.getLeft(), lst)
			lst.append(node.getValue)
			self.inOrder(node.getRight(), lst)

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
		return None

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		return None

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		if not self.root.isRealNode():
			return -1		
		i = self.search_rec(self.root.getLeft(), val)
		if i != -1:
			return i
		if self.root.getValue == val:
			return self.getRank(self.root)
		return self.search_rec(self.root.getRight(), val)

	def search_rec(self, node, val):
		if not node.isRealNode():
			return -1		
		i = self.search_rec(node.getLeft(), val)
		if i != -1:
			return i
		if node.getValue == val:
			return self.getRank(node)
		return self.search_rec(node.getRight(), val) 
		



	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return self.root


	def getPredecessor(self, node):
		if node.getLeft().isRealNode():
			node = node.getLeft()
			while node.getRight().isRealNode():
				node = node.getRight()
			return node
		else:
			prevNode = node
			node = node.getParent()
			while node.getRight() == prevNode:
				prevNode = node()
				node = node.getParent()
			return node

	def getSuccessor(self, node):
		if node.getRight().isRealNode():
			node = node.getRight()
			while node.getLeft().isRealNode():
				node = node.getLeft()
			return node
		else:
			prevNode = node
			node = node.getParent()
			while node.getLeft() == prevNode:
				prevNode = node()
				node = node.getParent()
			return node

	#Updates the height of node by the heights of his children
	def changeHeight(self, node):
		node.setHeight(max(node.getLeft().getHeight(), node.getRight().getHeight()) + 1)
	
	#Updates the size of node by the sizes of his children
	def changeSize(self, node):
		node.setSize(node.getLeft().getSize()+ node.getRight().getSize() + 1)
  
  
	#Give the upper, returns the upper
	def rightRotation(self, a):
     
		b = a.getLeft()
		t = b.getRight()
		b.setRight(a)
		a.setParent(b)
		a.setLeft(t)
		t.setParent(a)
		
		self.changeHeight(a)
		self.changeHeight(b)
		self.changeSize(a)
		self.changeSize(b)
		return b
		
	def leftRotation(self, a):
		b = a.getRight
		t = b.getLeft()
		b.setLeft(a)
		a.setRight(t)
		a.setParent(b)
		
		self.changeHeight(a)
		self.changeHeight(b)
		self.changeSize(a)
		self.changeSize(b)
		return b

	def rightLeftRotation(self, node):
		node.setLeft(self.leftRotation(node.left))
		return self.RightRotation(node)
     
	def leftRightRotation(self, node):
		node.setRight(self.rightRotation(node.right))
		return self.leftRotation(node)
		
	def getBalanceFactor(self, node):
		if not node.isRealNode():
			return 0
		x,y = node.getLeft().getHeight(), node.getRight().getHeight()
		if not node.getLeft().isRealNode():
			x=0
		if not node.getRight().isRealNode():
			y=0
		return x - y

	def getRank(self, node):
		tmp = node
		parent = node.getParent()
		a = node.getLeft().getSize()
		while tmp !=None:
			if parent.getRight==node:
				a=a+parent.getSize()+1
				tmp = tmp.get_parent()
				parent = tmp.get_parent()
		return a



#for tests

	def append(self, val):
		n = self.len
		self.insert(n, val)
  
	def getTreeHeight(self):
		return self.root.getHeight()


	def printt(self):
		out = ""
		for row in self.printree(self.root):  # need printree.py file
			out = out + row + "\n"
		print(out)

	def printree(self, t, bykey=True):
		# for row in trepr(t, bykey):
		#        print(row)
		return self.trepr(t, False)

	def trepr(self, t, bykey=False):
		if t == None:
			return ["#"]

		thistr = str(t.key) if bykey else str(t.getValue())

		return self.conc(self.trepr(t.left, bykey), thistr, self.trepr(t.right, bykey))

	def conc(self, left, root, right):

		lwid = len(left[-1])
		rwid = len(right[-1])
		rootwid = len(root)

		result = [(lwid+1)*" " + root + (rwid+1)*" "]

		ls = self.leftspace(left[0])
		rs = self.rightspace(right[0])
		result.append(ls*" " + (lwid-ls)*"_" + "/" + rootwid *
						" " + "\\" + rs*"_" + (rwid-rs)*" ")

		for i in range(max(len(left), len(right))):
			row = ""
			if i < len(left):
				row += left[i]
			else:
				row += lwid*" "

			row += (rootwid+2)*" "

			if i < len(right):
				row += right[i]
			else:
				row += rwid*" "

			result.append(row)

		return result

	def leftspace(self, row):
		# row is the first row of a left node
		# returns the index of where the second whitespace starts
		i = len(row)-1
		while row[i] == " ":
			i -= 1
		return i+1

	def rightspace(self, row):
		# row is the first row of a right node
		# returns the index of where the first whitespace ends
		i = 0
		while row[i] == " ":
			i += 1
		return i

