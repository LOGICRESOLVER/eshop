import pickle


class external_storage():
	__slots__ = ("attr")
	__storage = dict()

	def __init__(self, attr):
		self.attr = attr

	def __set__(self, instance, value):
		self.__storage[self.attr] = value

	def __get__(self, instance, owner=None):
		return self.__storage[self.attr]


class acumulator:
	__slots__=("attr","val")
	
	def __new__(cls,attr,val):
		setattr(cls,attr,external_storage(attr))
		cls.val = val
		return super().__new__(cls)
				

	def __init__(self,attr, val):
		setattr(self, attr, val)


class cache(dict):
	#__TEST_#1__
		#atr = ("A","B")
		#val = (3333,5)
		#test = cache()
		#test.import_data(atr,val)
		#test.load_data("/home/debian/Desktop/CACHE/data.pickle")
		#print(test["A"])
		#test["A"]=10
		#test.A = test.A - 5
		#print(test["A"])
	#__TEST_#2__
		#class TEST():
		#	def __init__(self,x,y):
		#		operator = cache()		
		#		self = cache.get_class_constructor(TEST,self,("x","y"),(x,y))
		#		self.x=x
		#		self.y=y
		#test_2 = TEST(*val)
		#print(test_2.x)
	def __new__(cls):
		temp = ""
		cache_=external_storage
		for attr in cache_._external_storage__storage.keys():
			
			temp = temp + str(attr) +","#+"data"
			
		temp = temp + ",__dict__"	
		sl = "("+temp+")"
		sl = sl 
		setattr(cls,"__slots__",sl)
		return super().__new__(cls)

	def __init__(self):
		cache_=external_storage._external_storage__storage
		self.__dict__ = cache_
	
	
	def __set__(self, attr, value):
		(self.__dict__)[self.attr] = value
	
	
	def __get__(self, attr):
		return (self.__dict__).attr

	#----------------------------------------------

	@staticmethod
	def import_data(attributes,values):
		data_dict = dict(zip(attributes,values))
		for item in data_dict:
			acu = acumulator(item,data_dict[item])
		return None


	def export_data(self):
		return self.__dict__



	def save_data(self,file_):
		try:		
			with open(str(file_), 'wb') as handle:
				pickle.dump(self.__dict__, handle, protocol=pickle.HIGHEST_PROTOCOL)
		except Exception as ex:
			print("   -->ERROR: save cache data to pickle, error_var: "+str(ex))
		return None


	def load_data(self,file_):
		try:
			with open(str(file_), 'rb') as handle:
				self.__dict__ = pickle.load(handle)
		except Exception as ex:
			print("   -->ERROR: load cache data to pickle, error_var: "+str(ex))
		return None

	def __setitem__(self, key, item):
		self.__dict__[key] = item

	def __getitem__(self, key):
		return self.__dict__[key]

	def update(self, *args, **kwargs):
		return self.__dict__.update(*args, **kwargs)

	def keys(self):
		return self.__dict__.keys()

	def values(self):
		return self.__dict__.values()

	def items(self):
		return self.__dict__.items()

	@staticmethod
	def get_class_constructor(instance,self_,attributes,values):
		data_dict = dict(zip(attributes,values))
		for attr in attributes:    
			setattr(instance, attr, external_storage(attr))
			exec("{0}={1}".format(attr,data_dict[attr]))		
			setattr(self_, str(attr), attr)
		return self_




class id_external_storage():
	__slots__ = ("attr")
	__storage = dict()

	def __init__(self, attr):
		self.attr = attr

	def __set__(self, instance, value):
		self.__storage[id(instance), self.attr] = value

	def __get__(self, instance, owner=None):
		return self.__storage[id(instance), self.attr]


class id_cache(dict):
	def __new__(cls):
		temp = ""
		cache_=id_external_storage
		for attr in cache_._id_external_storage__storage.keys():
			
			temp = temp + str(attr) +","#+"data"
			
		temp = temp + ",__dict__"	
		sl = "("+temp+")"
		sl = sl 
		setattr(cls,"__slots__",sl)
		return super().__new__(cls)

	def __init__(self):
		cache_=external_storage._external_storage__storage
		self.__dict__ = dict()
		for key in dict(cache_).keys():
			self.__dict__dict(cache_)[key]
	
	
	def __set__(self, attr, value):
		(self.__dict__)[id(instance) ,self.attr] = value
	
	
	def __get__(self, attr):
		return (self.__dict__)[id(instance) ,attr]



	@staticmethod
	def get_class_constructor(instance,self_,attributes,values):
		data_dict = dict(zip(attributes,values))
		for attr in attributes:    
			setattr(instance, attr, external_storage(attr))
			exec("{0}={1}".format(attr,data_dict[attr]))		
			setattr(self_, str(attr), attr)
		return self_

