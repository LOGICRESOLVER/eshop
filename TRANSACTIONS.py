import random 
import os
from cache import id_cache
import datetime
from bitcoin_value import currency
import random
import requests



class admin_pannel:
	
	def __init__(self):
		pass



class email:
	
	def __init__(self):
		pass




class TRANSACTIONS:

	def __init__(self,storage,config):
		#-------------------------
		self.storage = storage
		self.config = config
		self.path = config["path"]
		#-------------------------
		self.path = self.config["path"]
		self.key_log = dict()
		#-------------------------
		self.PAYGATE_CARD = Paygate_CARD(config,storage)
		self.PAYGATE_BTC = Paygate_BTC(config,storage)
		#-------------------------
		self.email = email()
		self.admin = admin_pannel()#self.storage,self.path,self.keylog)
		#-------------------------
		self.data = dict()
		self.log = dict()
		self.private_storage = id_cache()
		self.expire_time_periode = 50 #min
		#-------------------------
		self.IN_URL = self.config["IN_URL"]		
		self.OUT_URL = self.config["OUT_URL"]
		self.url = self.config["url"]


	def pointer(self,_type):
		if _type == "BTC":
			return self.PAYGATE_BTC
		if _type == "CARD":
			return self.PAYGATE_CARD
		else:
			print("   -->Error: self.pointer()")
			return None


	def token(self,uid = ""):
		default_len = 10
		#-----------------
		if uid == "": 
			len_ = default_len
		else:
			len_ = len(str(uid))
		KEY = ""
		for i in range(0,len_):
			KEY = KEY + str(random.randint(0,9))
		return KEY
			
		#return vector


	def make_config_vector(self,_type):
		__vector = dict()
		__vector.update({"lang":self.config["lang"]})
		__vector.update({"currency":self.config["currency"]})
		__vector.update({"hostname":self.config["hostname"]})
		__vector.update({"IN_URL":self.config["IN_URL"]})
		__vector.update({"OUT_URL":self.config["OUT_URL"]})
		__vector.update({"type":str(_type)})
		__vector.update({"STATUS":False})
		return __vector


	def manage_ID(self,ID):
		return str(ID)



	    
	def init_transaction(self,vector):
		ID = self.manage_ID(vector["uid"]) 
		KEY = self.token(ID)
		vector.update({"KEY":KEY})
		vector.update({"ID":ID})
		vector_conf = self.make_config_vector(vector["TYPE"])
		for key in vector_conf.keys():
			vector.update({key:vector_conf[key]})
		if vector["TYPE"] == "BTC":
			vector_2 = (self.pointer(vector["TYPE"])).init_trans(vector) 	
			vector = {**vector,**vector_2}
		if vector["TYPE"] == "CARD":
			KEY = self.token(vector["ID"])
			vector.update({"KEY":str(KEY)})
		vector.update({"TIME":self.get_date(stri = True)})
		return vector


	def keyloger(self,vector):
		return vector



	def check_keylog(self,vector):
		#print(vector)
		if vector["KEY"] in self.data.keys():
			return True
		else:
			return False


	def key_decorator(self,vector):
		#if "ID" in vector.keys():
		#	vector.pop("ID")
		#if "uid" in vector.keys():
		#	vector.pop("uid")
		return vector


	def time_diference(self,START_TIME,EXP_TIME):
		for sign in START_TIME:
			if sign == EXP_TIME[START_TIME.index(sign)]:
				pass	
			else:
				diff_factor = START_TIME.index(sign)
				break
		TOT_TIME = 0
		TOT_TIME_EXP = 0
		for j in range(diff_factor,len(START_TIME)):
			TOT_TIME = TOT_TIME + int(START_TIME[j])
			TOT_TIME_EXP = TOT_TIME_EXP + int(EXP_TIME[j])
		if TOT_TIME_EXP > TOT_TIME + (self.expire_time_periode * 60 * 60 * 1000000):
			return True
		else: 
			return False



	def check_transaction(self,vector):
		#print(vector)
		answ = self.check_keylog(vector)
		if answ == False:
			return False
		else:
			pass
		return True
		#START_TIME = self.data[vector["KEY"]]["TIME"]
		#EXP_TIME = self.get_date(False)	
		#if self.time_diference(START_TIME,EXP_TIME) == False:
		#	return False
		#else:
		#	return True
			

	def SET(self,vector):
		base_vector = self.init_transaction(vector)
		vector = {**vector,**base_vector}
		vector = self.keyloger(vector)
		self.data.update({str(vector["KEY"]):vector})
		vector = self.key_decorator(vector)
		print("!!!!!!!!!!!!!!")
		print(vector["KEY"])
		print("!!!!!!!!!!!!!!")
		if vector["TYPE"] == "BTC":
			OUT_vector = (self.pointer(vector["TYPE"])).MAKE(vector)
		if vector["TYPE"] == "CARD":
			OUT_vector = (self.pointer(vector["TYPE"])).MAKE(vector)
		print("!!!!!!!!!!!!!!")
		print(OUT_vector["KEY"])
		print("!!!!!!!!!!!!!!")

		#print(OUT_vector)
		return OUT_vector



	def GET(self,url,vector):

		print("??????????????")
		#self.data
		print("??????????????")
		print("??????????????")

		print("??????????????")

		print("??????????????")


		
		vector_orig_unconfrimed = vector
		"""	
		vector_orig_unconfrimed.update({"STATUS":"UNCONFRIMED"})		
		if not(self.IN_URL[-1] == "/"):
			self.IN_URL = self.IN_URL + "/" 
	
		INTERFACE = self.IN_URL[self.IN_URL.rindex(self.url)+len(self.url):]			
		if not(INTERFACE in url):
			return dict()#vector_orig_unconfrimed
		else:
			pass
		print(url)
		URL_KEY = url[url.rindex(INTERFACE)+len(INTERFACE):]	
		"""
		URL_KEY = str(url)
		if not(str(URL_KEY) == str(vector["KEY"])):
			return dict() #vector_orig_unconfrimed
		else:
			KEY = str(URL_KEY)
		if self.check_transaction(vector)==False:
			return dict()#vector_orig_unconfrimed
		else:
			vector = self.data[vector["KEY"]]
		__vector = {**vector,**(self.data[KEY])}
		print("??????????????")
		print(__vector)
		print("??????????????")
		__vector.update({"STATUS":"CONFRIMED"})
		self.buy_rutina(__vector)
		self.write_transaction(__vector)
		return __vector


	def buy_rutina(self,vector):
		try:
			EMAIL = self.EMAIL_template(vector)
			self.email.send(EMAIL)
			self.admin.set_request(vector)
			return None
		except:
			pass
			return None


	def write_transaction(self,vector):
		items_keys = []
		for key in vector.keys():
			if "item_" in str(key):
				items_keys.append(key[5:])
		for key in items_keys:
			num = self.storage["num_"+key] - vector["item_"+key]
			print("num: "+str(num))
			print("num_storage: "+str(self.storage["num_"+key]))
			self.storage.update({"num_"+key:int(num)})
			print("num_updated_storage: "+str(self.storage["num_"+key]))
		self.storage.save_data(self.path + "data/storage.pickle")
		self.data.pop(vector["KEY"])
		return None


	#OK.
	def get_date(self, stri = False):
		date = datetime.datetime.today()
		if stri == True:
			return str(date)
		else:		
			return [date.year,date.month,date.day,date.hour,date.minute,date.second,date.microsecond]


	#OK
	def date(self):
		date = datetime.datetime.today()
		return [date.year,date.month,date.day,date.hour,date.minute,date.second,date.microsecond]



class Paygate_BTC:

	#__MANDATORY_PART__

	def __init__(self,config,storage):
		self.config = config
		self.storage = storage
		self.key_collector = []
		#---------------------
		self.deep_factor = 3	
		self.factor_len = 3	
		self.OUT_URL = config["OUT_URL"]
		self.IN_URL = config["IN_URL"]
		self.expiret_time = 45 #[min]
		self.adress_url = ""#config["BTC_ADDRESS"] 
	

	"""
	def generate_key(self,vector):
		ID = vector["ID"]
		KEY = ""
		for i in range(0,len(ID)):
			KEY = KEY + str(random.randint(0,9))
		vector.update({"KEY":KEY})
		return vector
	"""




	def init_trans(self,vector):
		#vector.update({"ID":vector["uid"]})
		#print(vector)
		#vector = self.generate_key(vector)
		#try:	
		#	self.IN_URL = vector["IN_URL"]
		#except:
		#	self.IN_URL = self.config["IN_URL"]
		vector.update({"IN_URL":self.IN_URL})
		vector.update({"IN_URL":self.IN_URL})
		vector = self.generate_PRICE(vector)
		
		#vector.update({"PAYGATE_STATUS":"False"})
		
		return(vector)


	def create_trans(self,vector = None):
		"""
		if "KEY" in vector.keys():
			pass
		else:
			vector = self.init_trans(vector)
		"""
		for key in self.config.keys():
			if type(self.config[key])==type("..."):
				vector.update({key:self.config[key]})
		vector.update({"STATUS":"UNCONFRIMED"})
		vector.update({"GW_URL":self.config["GW_URL"]+vector["KEY"]})
		#vector.update({"GW":vector["IN_URL"]})
		vector.update({"TIME":self.get_date()})
		vector.update({"ADDRESS":self.get_btc_address()})
		new_vector = self.str_corrector(vector)
		return new_vector
		

	#def check_trans(self,ID,KEY,vector):
	#	print("Not implemented...")
	#	return True

	#======================================

	#__SUPPORT_PART__

	#def format_output(self,vector):
	#	return vector



	def get_btc_address(self):
		ind = random.randint(0,len(self.config["address"])-1)		
		return (self.config["address"])[ind]



	def calc_price(self,vector):
		__sum = float(0)
		for __item in vector.keys():
			if "item_" in __item:
				item = __item[5:]
				#print(vector[__item])
				#print(self.storage["price_"+item])
				__sum = __sum + float(self.storage["price_"+item])*float(vector[__item])
				#print("..."+str(__sum))
		#print("...wwww"+str(__sum))
		curr = 58235.46
		#curr = currency(self.config["currency"])
		#print("====>>>")
		bitcoin_value = float(curr)
		price_bitcoin = (1/bitcoin_value) * __sum 
		#print(price_bitcoin)
		return(price_bitcoin,__sum,curr)


	def generate_PRICE(self,vector):
		deep_factor = 3	
		factor_len = 3	
		OUT = self.calc_price(vector)	
		price_bitcoin = OUT[0]
		price_base = OUT[1]
		curr = OUT[2]
		vector.update({"base_price":str(price_base)})
		vector.update({"base_price_BTC":str(price_bitcoin)})
		vector.update({"BTC_currency":str(curr)})
		start_index = len(str(price_bitcoin)) - factor_len
		symb = ""
		for i in range(0,len(str(price_bitcoin))):
			#print(symb)
			if i < start_index:
				if i == 1:
					symb = symb + "."
				else:
					symb = symb + "0"
			else:		
				symb = symb + str(random.randint(0,9))
		rand_factor = float(symb)
		PRICE = str(price_bitcoin - rand_factor) 
		vector.update({"PRICE":PRICE})
		#vector.update({"KEY":KEY})
		return vector
		
	def str_corrector(self,vector):
		new_vector = dict()
		for key in vector.keys():
			try:
				new_vector.update({str(key):str(vector[key])})			
			except:
				pass
		return new_vector



	def get_date(self):
		date = datetime.datetime.today()
		time = str(date.year) + "_" + str(date.month) + "_" + str(date.day) + "_" + str(date.hour) + "_" + str(date.minute) + "_" + str(date.second) + "_" + str(date.microsecond)                      
		#expired_time = str(date.year) + str(date.month) + "_" + str(date.day) + "_" + str(date.hour) + "_" + str(date.minute) + "_" + str(date.second) + "_" + str(date.microsecond)                      
		return time


	def send(self,vector):
		KEY = str(vector["KEY"])
		URL = self.OUT_URL
		ENDPOINT = URL + KEY     
		#print("ENDPOINT")  

		#CUSTOME_TEST	
		#----------------------		
		#vector.update({"KEY":"78612225"})
		#vector.update({"PRICE":"0.08590986615191307"})
		#----------------------
		res = requests.get(url = ENDPOINT, cookies = vector)
		return(res)



	def MAKE(self,vector):
		#try:
		#if True:
		#vector = __vector
		vector = self.init_trans(vector)
		vector = self.create_trans(vector)
		#print(vector)
		res = self.send(vector)	
		#	try:
		#		pass
				#KEY = res["KEY"]
				#__vector = res
				#for key in __vector.keys():
				#	if not(key == "KEY"):
				#		vector.update({key,__vector[key]})
		#	except:
				#pass
		#	vector.update({"PAYGATE_STATUS":"True"})
		#	print("   --> Paygate_BTC: successs send transaction.")		
			#print(vector)
		
		#except Exception as err:
		#	vector = dict()#__vector
		#	vector.update({"PAYGATE_STATUS":"False"})
		#	print("   --> Paygate_BTC.senf(vector): Error: "+str(err))
		#	#print("      --> vector: "+str(vector))

		return vector
	

class Paygate_CARD:
	
	def __init__(self,config,storage):
		pass



def TEST_PAYGATE_BTC():
	"""
	import os
	path = os.getcwd()+"/"
	from cache import cache 
	storage = cache()
	storage.load_data(path+"data/storage.pickle")
	config = dict({"currency":"EUR"})
	config.update({"IN_URL":"http://127.0.0.1:5001/interface/"})	
	config.update({"GW_URL":"http://127.0.0.1:5001/user_return_call/"})
	config.update({"OUT_URL":"http://localhost:8080/register/create?id="})	
	#------------------------------
	address=["1Lbcfr7sAHTD9CgdQo3HTMTkV8LK4ZnX71",
		"a89sd09as8d0as08das90f8as09df8sd09",
		"as89d8as0d98as90d8a9s0d8as90d8asff",
		"as7d98as79a8sd7as89HTMTkV8LK4ZnX71"]
	config.update({"address":address})	
	PAYGATE = Paygate_BTC(config,storage)
	items = dict({"item_2FMA":4,"item_selegiline":1})
	metadata = dict({"city":"ul","street":"olsinky"})
	vector = {**items,**metadata,"uid":"UID12345","TYPE":"BTC"}
	vector = PAYGATE.MAKE(vector)
	#print(vector)
	"""

def TEST_TRANSACTIONS():

	#__CLASS_INIT__
	import os
	__path = os.getcwd()+"/"
	from cache import cache 
	storage = cache()
	storage.load_data(__path+"data/storage.pickle")	
	config = dict({"currency":"EUR"})
	config.update({"path":str(__path)})
	config.update({"url":"http://127.0.0.1:5001/"})
	config.update({"IN_URL":"http://127.0.0.1:5001/interface/"})	
	config.update({"GW_URL":"http://127.0.0.1:5001/user_return_call/"})
	config.update({"OUT_URL":"http://localhost:8080/register/create?id="})	
	#------------------------------
	address=["1Lbcfr7sAHTD9CgdQo3HTMTkV8LK4ZnX71",
		"a89sd09as8d0as08das90f8as09df8sd09",
		"as89d8as0d98as90d8a9s0d8as90d8asff",
		"as7d98as79a8sd7as89HTMTkV8LK4ZnX71"]
	config.update({"address":address})	
	#-----------------------------------------
	config.update({"lang":"EN"})
	config.update({"currency":"EUR"})
	config.update({"hostname":"127.0.0.1"})
	config.update({"port":"5001"})

	#-----------------------------------------


	trans = TRANSACTIONS(storage,config)


	#__TRANS__
	#-----------------------------------------
	items = dict({"item_2FMA":4,"item_selegiline":1})
	metadata = dict({"city":"ul","street":"olsinky"})
	vector = {**items,**metadata,"uid":"UID12345","TYPE":"BTC"}
	vector.update({"uid":"UID32948"})
	#print("INPUT-vector: ")
	#print(vector)
	#print("=======================")
	_vector = trans.SET(vector)
	#print("OUTPUT-vector: ")
	#print(_vector)
	
	url = _vector["IN_URL"] + _vector["KEY"] 
	#print(url)
	_vector.update({"KEY":_vector["KEY"]})
	res = trans.GET(url,_vector)
	print(res)




class paygate_TEMPLATE:

	def __init__(self,config,storage):
		self.config = config
		

	def init_trans(self,ID = "",KEY = ""):
		ID = ID
		if KEY == "":
			KEY = 12345
		return(KEY)


	def create_trans(self,vector = dict()):
		KEY = vector["KEY"]
		__vector = dict()
		__vector = {**vector,**__vector}
		return vector




	def check_trans(self,ID,KEY,vector):
		#--------------

		
		return None


	def check_trans(self,KEY,vector=None):
		if vector == None:
			vector = call_to_check(KEY)
		if "STATUS" in vector.keys():
			if vector["STATUS"] == True:
				res = True
		return res


	def format_output(self,vector):
		return vector




#if __name__ == "__main__":
	#TEST_TRANSACTIONS()
	#pass




