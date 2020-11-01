import math

class VEB:
	def c_(self, x):
		return int(math.floor(x / math.sqrt(self.u)))

	def i_(self, x):
		return int((x % math.ceil(math.sqrt(self.u))))

	def x_(self, c, i):
		return int((c * math.floor(math.sqrt(self.u))) + i)
  
	def get_pair(self, x):
		return self.c_(x), self.i_(x)
  
	def __init__(self, w=64):
		self.w = w
		self.w_2 = math.floor(w/2)
		self.u = 2**w
		self.sqrt_u = self.c_(self.u)
  
		if self.u < 0:
			raise Exception ("U não pode ser menor que 0")
		
		self.min = None
		self.max = None

		if (self.u > 2): # não são folhas
			self.resumo = None
			self.clusters = [ None for i in range(self.c_(self.u)+1)] 

		self.log_operations = [] # lista de tuplas que guardará o log das operações

	def search(self, x):
		if x == self.min or x == self.max:
			return True
		elif self.u <=2: # chegamos nas folhas e não encontramos
			return False
		else:
			c, i = self.get_pair(x)
			cluster = self.clusters[c]
			if cluster is not None:
				return cluster.search(i)
			else: 
				return False
		
	def empty_insert(self, x):
		self.min = x
		self.max = x

	def insert(self, x):
		if self.search(x):
			print("Elemento repetido = ", x)
			return False
		if self.min is None:
			self.empty_insert(x)
		else:
			if x < self.min:
				aux = self.min
				self.min = x
				x = aux
			if x > self.max:
				self.max = x
			if self.u > 2:
				c, i = self.get_pair(x)
				if self.clusters[c] is None:
					self.clusters[c] = VEB(self.w_2)
				if self.resumo is None:
					self.resumo = VEB(self.w_2)
				if self.clusters[c].min is None:
					self.resumo.insert(c)
				self.clusters[c].insert(i)
			print("Inseri ", x)
	
	def sucessor(self, x):
		if self.u <= 2:
			if x == 0 and self.max == 1:
				return 1
			else:
				return None
		elif (self.min != None and x < self.min):
			return self.min
		else:
			c, i = self.get_pair(x)
			maxlow = None
			cluster = self.clusters[c]

			if cluster is not None:
				maxlow = cluster.max
			if maxlow is not None and i < maxlow:
				offset = cluster.sucessor(i)
				return self.x_(c, offset)
			else:
				c_linha = None
				if self.resumo is not None:
					c_linha = self.resumo.sucessor(c)
				if c_linha is None:
					return None
				else:
					cluster2 = self.clusters[c_linha]
					offset = 0
					if cluster2 is not None:
						offset = cluster2.min
						return self.x_(c_linha, offset)
		return -1

	def predecessor(self, x):
		if self.u <= 2:
			if x == 0 and self.min == 1:
				return 1
			else:
				return None
		elif (self.max != None and x > self.max):
			return self.max
		else:
			c, i = self.get_pair(x)
			minlow = None
			cluster = self.clusters[c]

			if cluster is not None:
				minlow = cluster.min
			if minlow is not None and i > minlow:
				offset = cluster.predecessor(i)
				if offset == None:
					offset = 0
				return self.x_(c, offset)
			else:
				c_linha = None
				if self.resumo is not None:
					c_linha = self.resumo.predecessor(c)
				if c_linha is None:
					if self.min is not None and x > self.min:
						return self.min
					else:
						return None
				else:
					cluster2 = self.clusters[c_linha]
					offset = 0
					if cluster2 is not None:
						offset = cluster2.max
					return self.x_(c_linha, offset)
		return 0
	
	def remove(self, x):
		if self.search(x):
			if 1:
				if x == self.min:
					if self.u <=2 or (self.u > 2 and self.resumo is None):
						c = None
					else:
						c = self.resumo.min
					if c is None:
						if self.min == self.max:
							self.max = None
						self.min = None
						return True
					self.min = self.x_(self.c_(x), self.clusters[c].min)
					x = self.min
				c = self.c_(x)
				self.clusters[c].remove(self.i_(x))
				if self.clusters[c].min is None:
					self.resumo.remove(c)
				if self.resumo.min is None:
					self.max = self.min
				else:
					c_linha = self.resumo.max
					self.max = self.x_(c_linha, self.clusters[c_linha].max)
				return True
		else:
			return False

	def load_file(self, filename):
		"""
            Load file with list operations in this hash table
            Params: filename
            Return: 1, if operation was successful
                    -1, c.c.
		""" 
		try:
			file = open(filename, "r")
			for line in file:
				operation, value = line.split(":")
				if operation == "INC":
					self.insert(int(value))
					self.log_operations.append("\nINC:{}\n".format(value))
				elif operation == "REM":
					retorno = self.remove(int(value))
					self.log_operations.append("\nREM:{}\n{}\n".format(value, retorno))
				elif operation == "BUS":
					retorno = self.search(int(value))
					self.log_operations.append("\nBUS:{}\n{}\n".format(value, retorno))
				elif operation == "SUC":
					retorno = self.sucessor(int(value))
					self.log_operations.append("\nSUC:{}\n{}\n".format(value, retorno))
				elif operation == "PRE":
					retorno = self.predecessor(int(value))
					self.log_operations.append("\nPRE:{}\n{}\n".format(value, retorno)) 
			file.close()
			return 1
		except:
			return -1
            
    
	def write_file(self, filename):
		"""
            Write file with log operations in this hash table
            Params: filename
            Return: 1, if operation was successful
                    -1, c.c.
        """ 
		try:
			file = open(filename, 'w')
			file.writelines(self.log_operations)
			file.close()
			return 1
		except:
			return -1
