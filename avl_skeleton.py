#username - complete info
#id1      - 215061631
#name1    - Guy Bornstein
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

from selectors import EpollSelector


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



"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		# add your fields here
		self.length = 0

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
		return self.retrieveRec(self.root, i)
  
	
	def retrieveRec(self, node, i):
		r = AVLNode.getSize() + 1
		if i == r:
			return node
		elif i<r:
			return self.retriveRec(node.left, i)
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
		NewNode.setValue(val)
		NewNode.setLeft(AVLNode())
		NewNode.setRight(AVLNode())
  
  
		CurrentNode = self.root

		"List is empty"
		if CurrentNode == None:
			self.root = NewNode
			return 0
		
		if i == self.length:
			CurrentNode = self.last()
			CurrentNode.setRight(NewNode)
			NewNode.setParent(CurrentNode)
		else:
			CurrentNode = self.retrieve(i+1)
   
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
		while CurrentNode!=self.root:
			CurrentNode = NewNode.getParent()
			self.changeHeight(CurrentNode)
			self.changeSize(CurrentNode)
   
			bf = self.getBalanceFactor(CurrentNode)

			#Left Left
			if bf == 2 and self.getBalanceFactor(CurrentNode.getLeft()) == 1:
				self.rightRotation(CurrentNode)
				rebalancingOperationCounter += 1
    
			#Right Right
			elif bf == -2 and self.getBalanceFactor(CurrentNode.getLeft()) == -1:
				self.leftRotation(CurrentNode)
				rebalancingOperationCounter += 1
    
			#Left Right
			elif bf == 2 and self.getBalanceFactor(CurrentNode.getLeft()) == -1:
				self.rightLeftRotation(CurrentNode)
				rebalancingOperationCounter += 1
    
			#Right left
			elif bf == -2 and self.getBalanceFactor(CurrentNode.getLeft()) == -1:
				self.leftRightRotation(CurrentNode)
				rebalancingOperationCounter += 1
    
				
				
		return rebalancingOperationCounter



	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		return -1


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.empty():
			return None
		node = self.root
		while self.root.left.isRealNode():
				node = node.getLeft()
			
		return node.getValue()

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.empty():
			return None
		node = self.root
		while node.isRealNode():
			node = node.getLeft()
		return node.getValue()

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
		self.length

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
		return None



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

	#Updates the height of node by the heights of his children
	def changeHeight(self, node):
		node.setHeight(max(node.getLeft().getHeight(), node.getHeight().getHeight()) + 1)
	
	#Updates the size of node by the sizes of his children
	def changeSize(self, node):
		node.setSize(node.getLeft().getSize(), node.getRight().getSize() + 1)
  
  
	#Give the upper, returns the upper
	def rightRotation(self, a):
     
		b = a.getLeft()
		T = b.getRight()
		b.setRight(a)
		a.setParent(b)
		a.setLeft(T)
		T.setParent(a)
		
		self.changeHeight(a)
		self.changeHeight(b)
		self.changeSize(a)
		self.changeSize(b)
		return b
		
	def leftRotation(self, a):
		b = a.getRight
		T = b.getLeft()
		b.setLeft(a)
		a.setRight(T)
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
		return node.getLeft().getHeight() - node.getRight().getHeight()

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

