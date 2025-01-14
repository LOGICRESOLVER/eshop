import sys
import os 
import pickle 
import re
import multiprocessing
from cache import external_storage, acumulator, cache
import uuid
from flask import render_template, make_response, request
from flask import request, make_response, redirect, url_for
from web_apps import page_wrapper, forum, market
from flask import session as _sess_
import datetime
import json
from flask import session as sess
from TRANSACTIONS import TRANSACTIONS
"""
class template():


	def __init__(self,name,path,temp,storage):
		self.name = name
		self.temp = temp
		self.path = path
		self.storage = storage
	

	def __call__(self):
		data = self.export()
		if not data == None:
			temp = self.temp
			for item in data.keys():
					temp = temp.replace("{{"+str(item)+"}}", str(data[item]))					
			return temp
		else:
			return self.temp
			
	def export(self):
		ex = dict()
		vars_ = self.find_vars(self.temp)
		for var in vars_:
			try:
				ex.update({var:self.storage[var]})
			except:
				pass 
		return(ex)



	def find_vars(self,temp):
		return self.find_between(temp, "{{", "}}")
		
	
	def find_between(self,s, first, last):		
		try:
			regex = rf'{first}(.*?){last}'
			return re.findall(regex, s)
		except ValueError:
			return -1
"""
from tools import template


#WARNING!!!: CONTAINET BLOCKS TRY FOR CORECTION ERROR IN APACHE MOD_WSGI
class menu_bar():
	def __init__(self,storage): 
		try:
			self.category_dict = storage["category_dict"]
			for cat in self.category_dict.keys(): 		
				setattr(self,cat,menu_button(cat,self.category_dict[cat],storage))
			#------------
			self.map = dict()
			for key in self.category_dict.keys():
				for item in self.category_dict[key]:
					self.map.update({item:key})
			for key in self.category_dict.keys():
				self.map.update({key:key})
			#----------------------
			self.storage = storage
			#path = os.getcwd()+"/"
			#self.storage.load_data(path+"data/storage.pickle")
		except:
			pass


	def __call__(self):
		cont = self.get_complet()
		return str(self.make_menu(cont))

	def click_to_menu(self,name):
		cat = self.map[name] 
		return (getattr(self,cat)).click(name)

	def get_complet(self):
		try:
			temp = ""
			for item in self.category_dict.keys(): 
				it = (getattr(self,item))()
				#tp = template("menu_part","",self.storage["temp_sub_button"],dict())
				#tp.storage = dict({"X":it})
				#temp = temp + tp()
				temp = temp + it
			return temp
		except:
			pass



	
	def make_menu(self,X):
		templ = self.storage["temp_out_menu"]
		temp = template("menu","",templ,dict())
		temp.storage = dict({"X":X})
		return temp()
		


class menu_button():	

	def __init__(self,cat_name,category_list,storage):
		self.cat_name = cat_name 
		self.category_list = category_list 
		self.switch = False
		#__closed_menu_template__
		cat = template(cat_name,"",storage["temp_button"],dict())
		cat.storage = dict({"X":str(cat_name)})
		self.closed_cat_temp = str(cat())
		#__open_menu_template__
		parc = ""
		for item in category_list:
			cat_item = template(item,"",storage["temp_sub_button"],dict())
			cat_item.storage = dict({"X":str(item)})
			parc = parc + cat_item()
		#print(parc)
		cat_open = template(cat_name,"",storage["temp_menu_cat"],dict())
		cat_open.storage = dict({"CONTENT":parc,"name":self.closed_cat_temp})
		self.open_cat_temp = str(cat_open()) 
		#---------------------
		self.content = self.closed_cat_temp


	def __call__(self):
		return self.content

	def click(self,name):
		if name == self.cat_name:
			self.switch = not self.switch
			if self.switch == False:
				self.content = self.closed_cat_temp
			else:
				self.content = self.open_cat_temp
		return self.content


class web_ads:

	def __init__(self,img):
		self.img = img  

	def __call__(self):
		return "<center><img src=static/{0}></center>".format(str(self.img))



class nav_bar:

	def __init__(self,storage,basket_status = int(0)):
		self.tamp_nav_bar = storage["temp_nav_bar"]
		self.path_img_basket = storage["path_img_basket"]
		self.path_img_banner = storage["path_img_banner"]
		self.basket_status = basket_status
		self.storage = storage	


	def __call__(self):
		return str(self.storage["temp_nav_bar"])


class footer:
	def __init__(self):
		pass

	def __call__(self):
		stri = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
		stri = stri + "NOOTROPICMARKET_CZ (R) 2024. &nbsp;&nbsp; Info: info@nootropicsmarket.com"
		stri = stri + "<br>_"	
		return stri



from web_apps import basket




class home:

	def __init__(self,storage):
		self.index = storage["temp_index"]

	def __call__(self):
		return self.index



class about_us:

	def __init__(self):
		pass

	def __call__(self):
		return "This is page ABOUT_US."



class account:

	def __init__(self):
		pass

	def __call__(self):
		return "This is page ACCOUNT."


class empty:
	def __ini__(self,var):
		pass
	def __call__(self):
		return ""


class smalll:
	def __ini__(self,var):
		self.var
	def __call__(self):
		return str(self.var)


class empty_page:
	def __ini__(self):
		pass
	def __call__(self):
		return ""

class content_page:
	
	def __init__(self,uid,path,storage,active_pages=["basket"]):
		self.storage = storage
		self.path = path
		self.uid = uid
		
		__content = list((self.storage["category_dict"]).keys())
		self.map = dict()		
		for cat in self.storage["category_dict"].keys():		
			for item in self.storage["category_dict"][cat]:
				__content.append(item)
				self.map.update({str(item): page_wrapper(item,self.path,self.storage)})			
		self.content = set(__content)
		self.__page = None
		self.name = ""
		self.view = ""
		self.active_pages = active_pages
		self.empty = empty_page()



	def __call__(self):
		if self.name in self.map.keys():
			self.__page = self.map[self.name]
			self.view = self.__page()
			return self.view
		else:
			#print("ssssssssss")
			try:
				return "<div class=\"item_cont\">" + self.storage["temp_"+str(self.name)] + "</div>"
				#return self.storage["temp_"+str(self.name)]
			except: 
				return "" 

			#try:
				#__page = getattr(self,self.name)
			#	self.view = storage["temp_"+str(self.name)]
				#self.view = __page()
			#	return self.view
			#except:
			#	return("")	


	def page(self,name=""):
		if name == "":
			pass
		else:
			self.name = name
		if not(self.name in self.map.keys()):
			if self.name == "":
				print("   --> content_page.page(): Name not set.!")
				return self.empty
			
			if self.name in self.active_pages:
				return self.empty
			else:
				temp = template(self.name,"",self.storage["temp_"+str(self.name)],dict())
				vars_ = list(temp.find_vars(temp()))
				data = dict()
				for var in vars_:
					data.update({str(var):self.storage[str(var)]})
				temp.storage = data
				self.__page == temp
				return self.__page
		
		

		else:
			pass
		self.__page = self.map[str(self.name)]

		#print("===========================")
		#print(self.__page)


		return self.__page


	
	def __get__(self, name):
		return self.page(self.name)


	def __set__(self, name, value):
		(self.__dict__)[self.name] = value
	



class session:

	def __init__(self,uid,config,storage):
		self.config = config
		self.uid = uid 
		self.path = config["path"]  #!!!!!!!!!ERROR in mode_wsgi. wrong path...
		#self.path = os.getcwd()+"/" #config["path"]  #!!!!!!!!!ERROR in mode_wsgi. wrong path...
		self.storage = storage 		
		self.menu = menu_bar(self.storage)
		self.context = content_page(self.uid,self.path,self.storage,{"basket"})

		#self.page = self.context()
		self.context.page("index")
		#self.page = self.context.page("index")
		#self.context.render_page()
		#self.context.get_page()
		#sself.page = self.context
		
		self.main = template("main","",storage["temp_main"],dict())
		self.main.storage = dict({"menu":"","page":""})
		
		self.nav_bar = nav_bar(storage)
		
		#try:
		#	self.style = self.config["style"]	
		#except:	
		self.style = self.storage["style"]

		self.ads = web_ads("ads.jpg")
		self.footer = footer()
		self.account = account()
		self.home = home(self.storage)
		self.about_us = about_us()
		self.cookies = dict()
		self.page = ""
		self.__page = ""
		self.active = {"basket"}
		self.storage.update({"path":self.path})

		self.storage.update({"currency":"EUR"})
		self.storage.update({"hostname":"nootropic.noiz.cz"})
		self.storage.update({"lang":"EN"})

		config = dict({"path":self.path,"hostname":self.storage["hostname"],"lang":self.storage["lang"],"currency":self.storage["hostname"]})	
		#self.trans = TRANSACTIONS(self.path,self.storage,config)
		self.basket = basket(self.path,uid,storage)

		#__GENERATE_MARKET_PAGE__
		market_wrapper = market(self.path,self.storage)
		market_wrapper.make_data()
		market_wrapper.wrapper()		

		self.user_cache = dict()



	def url(self):
		return "http://"+self.config["localhost"] + ":" + str(self.config["port"]) + "/"


	
	def refresh(self):
		#self.page.get_page()
		#try:
		#	page = self.page()
		#exec:
		#	page = ""		
		#try:
		#self.page = self.context.page()
		#print(self.page.name)
		#print(self.page)
		#print("=======")
		#print(self.__page)		

		if self.page == "":
			self.context.page()	
			self.page = self.context()
		else:
			pass			
		#print(self.context())
		#except:
		#	page = self.page		
		page = self.page
		menu = self.menu()
		nav_bar = self.nav_bar()
		ads = self.ads()
		aside = ads
		footer = self.footer()
		self.main.storage = dict({"menu":menu,"page":page, "style":self.style, "nav_bar":nav_bar, "aside":aside, "footer":footer})		
		#resp = make_response(self.main())
		#return resp
		self.__page = ""
		self.page = ""		
		return make_response(self.main())		
		#return render_template("main.html", menu = menu, page = page)


	def click(self,name):
		#if name in ["basket","home","about_us","account"]:
		#	self.page = (getattr(self,str(name)))()
		#print("-==============")
		#print(name)	
		#self.__page = ""
		if name in self.active:
			if name == "basket": 
				self.page = self.basket() 
		else:
			
			if name in ["home","about_us","account"]:
				#self.context.page(name)
				#self.page = self.context()
				#print(self.page)
				self.context.page(name)
				self.page = self.context()
				#self.page = self.storage["temp_"+name]
				

			else:
				#self.page = self.context.page(name)
				self.menu.click_to_menu(name)
				#wrapper = self.context.page(name)
				#if name == "parno":
				#	print(wrapper.forum.data)
				#else:
				#	pass

				#print(self.context.get_page())
							
				self.page = self.context.page(name)
				
			#print(name)
			return self.refresh()		
				#print(self.context.name)
				#print("click to name "+str(name))
				#return(self.page)
				#ref = self.refresh()
				#messages = json.dumps({"page":page,"url":name})
				#_sess_["messages"] = messages
				#return redirect(url_for("runtime"))#,messages = messages))
	#			return None

	def trans_task(self):
		_type = "BTC"
		_items = self.basket.data
		ID = 34523			
		address = dict({"street":"OLSINKY","city":"UnL","ZIP_CODE":"40322","residence_number":529})
		metadata = dict({"address":address})
		#------------------------------------
		res = self.__trans.set_transaction("BTC",dict({"2FMA":3,"selegiline":2}),34523,metadata)
		KEY = int(res[4:])
		vector = self.__trans.data[KEY]	
		vector.update({"STATUS":True})
		res = self.__trans.get_transaction(KEY,vector)		
		self.basket.switch = 3
		self.basket.view = str(res)
		#print(self.storage["num_2FMA"])
		return self.refresh()


	def __redirect__(self,url = "https://www.google.com/",wait = 0):
		if wait == 0:
			return redirect(url)
		else:
			return "<html><head><meta http-equiv=\"refresh\" content=\"{0}; URL={1}\"></head><body>Redirecting...</body><html>".format(str(wait),url) 




	"""
	def GET_DATA_OUT(self,endpoint_url=None,data=None):
		#endpoint = endpoint_url
		endpoint = "http://localhost:8082/register/create?id=12345"
		#data = 	data
		data = dict({'key_1': "val_1",'key_2': 'val_2'})
		if type(dict()) == type(data) and type(endpoint) == type(""):
			res = str(requests.get(url=endpoint, cookies = data))
		else:
			res = ""
		return res




	def GET_DATA_IN(self):
		pass
	"""



from flask import session as sess



class sessions():



	def __new__(cls,config,storage = None):
		cls.config = config
		if storage == None:
			path = config["path"]  #!!!!!!!!!ERROR in mode_wsgi. wrong path...
			cls.path = path
			storage = cache()		
			storage.load_data(path+"data/storage.pickle")
			#cls.storage = storage 
		sessions.Transactions = TRANSACTIONS(storage,config)
		return super().__new__(cls)




	#ok
	def __init__(self,config,storage = None):
		self.config = config
		self.path = config["path"]
		self.colector = set()
		from tools import operator
		self.op = operator()
		self.__ses = dict()
		
		#self.url = "http://"+config["hostname"] + ":" + str(config["port"]) + "/"
		self.url = "http://"+ "127.0.0.1:5001" + "/"
		storage = cache()		
		storage.load_data(self.path+"data/storage.pickle")
		self.storage = storage
		#print(self.path)
		#print(self.storage["category_dict"])

		#print(self.storage)
		#self.storage = cache()
		#self.storage.load_data(self.path+"data/storage.pickle")



		"""
		from multiprocessing import shared_memory
		mem = shared_memory.SharedMemory("mem",create=True, size=10)
		cache = mem.buf

		cache[1]=66
		#cache.append(3)
		print(cache[1])
		mem.close()
		mem.unlink()
		"""
	
	def ses(self):
		S = self.check()
		self.__ses.update({S.uid:S})	
		
		print("   --> SESSION (SERVER): "+str(S.uid))
		print("   --> SESSION (USER): "+str(sess["id"]))
		return self.__ses[S.uid]			
	
	#Special function for server without cookies
	def get_ses(self,uid):
		return self.__ses[uid]

	#Special function for server without cookies
	def set_ses(self,uid,ses):
		return self.__ses.update({uid:ses}) 





	#ok
	def load_static_cookies(self,uid):
		try:
			cookies = self.config["cookies"]
		except:
			cookies = self.storage["cookies"]
		cookies.update({"id":uid})
		return cookies
	
	#ok
	def get_new_ses(self):
		uid = self.gen_uid()
		ses = session(uid,self.config,self.storage)
		self.colector.add(uid)
		ses.cookies = self.load_static_cookies(uid)
		self.set_ses(uid,ses)
		self.save_ses(uid)
		return ses


	#ok
	def load_ses(self,uid):
		ses = session(uid,self.config,self.storage)
		self.colector.add(uid)
		try:
			ses.user_cache = self.op.load_pickle(self.path+"data/sessions/"+str(uid)+".pickle",ses)
			for key in (ses.user_cache).keys():
				setattr(ses,str(key),ses.user_cache[key])	
		except:
			pass		
		self.set_ses(uid,ses)
		return ses



	def save_ses(self,uid):
		key_map = ["basket","uid"]
		try:
			ses = self.get_ses(uid)
			basket = ses.basket
			uid = ses.uid
			ses.user_cache.update({"basket":basket})
			self.set_ses(uid,ses)
			#for key in key_map:
				#(self.__ses[uid]).user_cache.update({key,getattr((self.__ses[uid]),key)})
				#ses.user_cache.update({key,getattr((self.__ses[uid]),key)})
			self.op.save_pickle(self.path+"data/sessions/"+str(uid)+".pickle",(self.__ses[uid]).user_cache)
		except:
			print("   -->Error: Not posibble save session "+str(uid)+".")
	
		return None


	#NOT
	def delete_session(self,uid):	
		self.colector.pop(uid)
		return None

	#ok
	def gen_uid(self):
		while True:
			uid = str(uuid.uuid4())
			if not uid in self.colector:
				break
			else:
				pass
		uid = "UID"+uid
		return uid



	#ok
	def check(self):
		status = False 		
		uid = "UID_DISSABLE"
		try:		
			uid = sess["id"]
			if uid in self.__ses.keys():
				ses = self.__ses[uid]
				return ses
			else:
				ses = self.load_ses(uid)
				return ses
		except:		
			ses = self.get_new_ses()
			sess["id"] = ses.uid
			return ses



	def __redirect__(self,url = "https://www.google.com/",wait = 0):
		if wait == 0:
			return redirect(url)
		else:
			return "<html><head><meta http-equiv=\"refresh\" content=\"{0}; URL={1}\"></head><body>Redirecting...</body><html>".format(str(wait),url) 
			#return "<html><head></head><body>redirecting...<script>setTimeout(function () {window.location.href = {0};}, {1});</script></body></html>".format(url,str(wait))




	def OUT(self,url,data):
		KEY = str(data["KEY"]) 
		ENDPOINT = url + KEY       
		res = requests.get(url=ENDPOINT, cookies = data)
		return(res)
		                                                                                                                                                                                                                                               

	def IN(self,request):		
		data = dict()
		for key in (request.cookies).keys():
			data.update({str(key):str(request.cookies.get(str(key)))})
		return data



		"""
		if url[-1] == "/":
			url = url[:len(url)-1]
		rev_url = url[::-1]
		try:
			KEY = url[len(url)-rev_url.index("/"):]
		except:
			KEY = url
		"""
		#INTERFACE = url[0:len(url)-len(KEY)]
		#if INTERFACE[-1] == "/":
		#	INTERFACE = INTERFACE[:len(INTERFACE)-1]
		#INTERFACE = INTERFACE[len(INTERFACE)-((INTERFACE[::-1]).index("/"))-1:]	
		#INTERFACE = "CARD"
		



	#ok
	def getcookie(self,key_): 	
		key = str(key_)
		try:
			VAL = request.cookies.get(key) 
			return(VAL)
		except:
			return(None)
	

	#ok
	def setcookies(self,cookies,resp):  
		resp_ = make_response(resp)  
		for key in cookies.keys():	
			resp_.set_cookie(key,str(cookies[key])) 
		return resp_ 

	
	def setcookie(self,key,val):  
		resp_ = make_response("<html><head></head></html>")  
		resp_.set_cookie(str(key),str(val)) 



	#ok
	def getcookies(self,keys_): 
		keys = list(keys_)
		out = dict()
		for key in keys:
			try:
				VAL = request.cookies.get(str(key)) 
				out.update({str(key):str(VAL)})
			except:
				pass
		return out




"""

class sessions():

	def __init__(self,config):
		self.config = config
		self.colector = dict()

	
	def init_cache(self,ses):
		ses.cache = id_cache()
		return ses
	

	def get_session(self):
		uid = self.gen_uid()
		ses = session(uid,self.config)
		setattr(ses,cache,id_cache())
		self.init_cache()
		self.colector.update({uid:ses})
		return ses

	def delete_session(self,uid):	
		self.colector.pop(uid)
		return None

	def gen_uid(self):
		while True:
			uid = str(uuid.uuid4())
			if not uid in self.colector.keys():
				break
			else:
				pass
		uid = "UID"+uid
		return uid

	 
	def getcookie(self,key_): 
		key = str(key_)
		try:
			VAL = request.cookies.get(key) 
			return(VAL)
		except:
			return(None)

	def setcookies(self,cookies,resp):  
		resp_ = make_response(resp)  
		for key in cookies.keys():	
			resp_.set_cookie(key,str(cookies[key])) 
		return resp_ 

	def getcookies(self,keys_): 
		keys = list(keys_)
		out = dict()
		for key in keys:
			try:
				VAL = request.cookies.get(str(key)) 
				out.update({str(key):str(VAL)})
			except:
				pass
		return out


	def check(self):
		status = False
		try: 		
			uid = self.getcookie("uid"):	
			ses = self.colector[uid]			
			status = True
		except:
			pass
		if status == False:
			ses = self.get_session()
			uid = ses.uid
			self.setcookies(ses.cookies,"loading_cookies...")
		return None
		

"""




#__TESTS_____________________________________________________
#============================================================
#ses = session(int(1))
#print(ses.menu.click_to_menu("stimulanty"))
#print(ses.menu.click_to_menu("stimulanty"))
#print(ses.menu.click_to_menu("stimulanty"))
#path = os.getcwd()+"/"
#storage = cache()
#storage.load_data(path+"storage.pickle")
#page = content_page(storage,storage["temp_index"],"index")
#page.get_page("stimulanty")
#page.render_page()
#print(page())
#print(storage["temp_out_menu"])






