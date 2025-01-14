

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
	


	def generate_key(self,vector):
		ID = vector["ID"]
		KEY = ""
		for i in range(0,len(ID)):
			KEY = KEY + str(random.randint(0,9))
		vector.update({"KEY":KEY})
		return vector





	def init_trans(self,vector):
		vector.update({"ID":vector["uid"]})
		vector = self.generate_key(vector)
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
		if "KEY" in vector.keys():
			pass
		else:
			vector = self.init_trans(vector)
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
		

	def check_trans(self,ID,KEY,vector):
		print("Not implemented...")
		return True

	#======================================

	#__SUPPORT_PART__

	def format_output(self,vector):
		return vector



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
		curr = currency(self.config["currency"])
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
		vector.update({"KEY":"78612225"})
		vector.update({"PRICE":"0.08590986615191307"})
		#----------------------
		res = requests.get(url = ENDPOINT, cookies = vector)
		return(res)



	def MAKE(self,__vector):
		#try:
		if True:
			vector = __vector
			vector = self.init_trans(vector)
			vector = self.create_trans(vector)
			res = self.send(vector)	
			try:
				KEY = res["KEY"]
				__vector = res
				for key in __vector.keys():
					if not(key == "KEY"):
						vector.update({key,__vector[key]})
			except:
				pass
			vector.update({"PAYGATE_STATUS":"True"})
			print("   --> Paygate_BTC: successs send transaction.")		
			print(vector)
		"""
		except Exception as err:
			vector = __vector
			vector.update({"PAYGATE_STATUS":"False"})
			print("   --> Paygate_BTC.senf(vector): Error: "+str(err))
			print("      --> vector: "+str(vector))

		return vector
		"""


def TEST_PAYGATE_BTC():
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
	vector = {**items,**metadata,"uid":"UID12345"}
	vector = PAYGATE.MAKE(vector)
	#print(vector)

