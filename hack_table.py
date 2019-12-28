class HashTable():
	def __init__(self,size):
		self.size_now = 0;
		# получение размера словаря
		prime_generator = self.get_prime() 
		prime_size = next(prime_generator)
		while size >= prime_size:
			prime_size = next(prime_generator)
		self.size = prime_size
		self.dict = [None] * self.size
		self.collisions = 0

	def insert_quadratic_collision(self,value):
		# обнуляем количество коллизий
		self.collisions = 0
		# квадратичный метод разрешения коллизий
		key = self.PJWHash(value) % self.size
		value_in_table = self.dict[key]
		counter = 0
		# все точно также,только вместо прохода по массиву мы идем по key + 1,key + 4,key + 9,key + 16
		if value_in_table is None:
			self.size_now += 1
			self.dict[key] = { value:1 }
			counter += 1
		elif value not in value_in_table.keys():
			self.collisions += 1
			counter += 2
			trying = 0
			while self.dict[key] is not None and value not in self.dict[key].keys():
				self.collisions += 1
				counter += 2
				trying += 1
				key += trying * trying
				if key >= self.size:
					key = key % self.size
			if self.dict[key] is None:
				counter += 1
				self.dict[key] = { value:1 }
				self.size_now += 1
			else:
				counter += 1
				self.dict[key][value] += 1
		else:
			counter += 2
			self.dict[key][value] += 1
		return counter

	def insert_linear_collision(self,value):
		# обнуляем количество коллизий
		self.collisions = 0
		# линейный метод разрешения коллизий
		key = self.PJWHash(value) % self.size
		value_in_table = self.dict[key]
		counter = 0
		# если нет коллизии - просто вносим
		if value_in_table is None:
			self.dict[key] = { value:1 }
			counter += 1
			self.size_now += 1
		# если коллизия - просто проходим дальше по массиву и ищем пустое место,либо значение,которое уже внесли
		elif value not in value_in_table.keys():
			self.collisions += 1
			counter += 2
			while self.dict[key] is not None and value not in self.dict[key].keys():
				self.collisions += 1
				counter += 2
				key += 1
				if key == self.size:
					key = 0
			if self.dict[key] is None:
				counter += 1
				self.dict[key] = { value:1 }
				self.size_now += 1
			else:
				counter += 1
				self.dict[key][value] += 1
		# просто обновляем значение,если нет коллизий 
		else:
			counter += 2
			self.dict[key][value] += 1
		return counter

	def get_prime(self):
		# Решето Эратосфена
		D = {}
		q = 2
		while True:
			if q not in D:
				yield q
				D[q * q] = [q]
			else:
				for p in D[q]:
					D.setdefault(p + q, []).append(p)
				del D[q]
			q += 1

	def PJWHash(self,key):
		BitsInUnsignedInt = 4 * 8
		ThreeQuarters = int((BitsInUnsignedInt * 3) / 4)
		OneEighth = int(BitsInUnsignedInt / 8)
		HighBits = (0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth)
		hash = 0

		for i in range(len(key)):
			hash = (hash << OneEighth) + ord(key[i])
			test = hash & HighBits
			if test != 0:
				hash = ((hash ^ (test >> ThreeQuarters)) & (~HighBits))
		return hash & 0x7FFFFFFF