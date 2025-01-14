from tools import operator, template
import datetime
from flask import url_for
import datetime
import re
import os
from tools import template
from TRANSACTIONS import TRANSACTIONS



class forum:
	#__USAGE:__
	#app = Flask(__name__)
	#dis = forum(app,[],5)
	#
	#@app.route("/")
	#def index():
	#	return redirect(url_for("forum_run_time"))
	#
	#@app.route("/forum_run_time", methods=["GET", ])
	#def forum_run_time():
	#	return dis.forum_run_time(request)	
	#
	#@app.route("/forum_button", methods=["POST"])
	#def forum_button():
	#	return dis.forum_button(request)
	
	#__forum_data_structure__
	#class for discuse forum.
	#data = [[user,date,text],[user,date,text],...]

	def __init__(self,storage,name,data=[],size = 100):
	#def __init__(self,app,data=[],size = 100):
		#setattr(forum,"app",app)
		self.storage = storage
		self.name = name
		interface = ""
		interface = interface + "<div class=\"col\">"
		interface = interface + "	<div class=\"form-group\">"
		interface = interface + "		<label>Enter user name, and your post text.</label>"
		interface = interface + "		<form method=\"POST\" action=\"/call_from_page\">"
		interface = interface + "			<input name=\"user\", id=\"forum\", placeholder=\"User\" >"
		interface = interface + "			<input name=\"text\", id=\"forum\", placeholder=\"Text\" >"
		interface = interface + "			<input type=\"submit\" >"
		interface = interface + "		</form>"
		interface = interface + "	</div>"
		interface = interface + "</div>"
		self.interface = interface
		#self.name = name
		self.data = data
		self.size = size	
		self.templ = "<forum><h3> Discuse Forum. </h3>" + self.interface + " <hr> {{X}}</forum>"
		self.temp = template("templ","",self.templ,dict())
		self.templ_ansv = "<forum_row><b> - User: {{user}}.</b>________<b>[ Date: {{date}} ].</b></forum_row><p>{{text}}</p><center>_______________________________</center>"
		self.temp_ansv = template("templ_ansv","",self.templ_ansv,dict())		
		#self.temp_ansv = template("templ_ansv","",templ_ansv,dict({"user":user,"date":date,"text":text}))
		self.view = ""
		self.update_status = False 
		self.worker = operator()
		#self.storage = storage 

		self.__temp_forum = self.storage["temp_forum"]
		self.__temp_forum_post = self.storage["temp_forum_post"]
		self.temp_forum = template("temp_forum","",self.__temp_forum,dict())
		self.temp_forum_post = template("temp_forum_post","",self.__temp_forum_post,dict())

		self.temp = self.temp_forum
		self.temp_ansv = self.temp_forum_post


	def get_str_date(self,date):
		return str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])


	def rutina(self):
		self.view = ""		
		#print(type(self.data))
		if self.size > len(self.data): 
			acu = self.data	
		else:
			acu = self.data[:self.size]
		for item in acu:
			user = item[0]
			date = item[1]
			text = item[2]
			#date = self.get_str_date(date_)
			self.temp_ansv.storage.update({"USER":user,"DATE":date,"POST":text})
			self.view = self.view + self.temp_ansv()
		self.temp.storage.update({"X":self.view})
		self.view = self.temp()


	def __call__(self):
		if not(self.view == ""):
			if self.update_status == False:
				pass
			else:
				self.rutina()
				self.update_status = False 
		else:
			self.rutina()
			self.update_status = False 
		return str(self.view)


	def import_data(self,data=None,path = ""):
		if not data == None:
			self.data = data
		if not path == "":
			self.data = self.worker.load_pickle(path)
		if (data == None and path == ""):	
			if "forum_data_"+self.name in (self.storage).keys():
				try:
					self.data = self.storage["forum_data_"+self.name]
				except:
					self.data = []
			else:
				self.data = []

		return None


	def export_data(self,path = ""):
		if path == "":
			self.storage["forum_data_"+self.name] = self.data
			return self.data
		else:
			self.worker.save_pickle(path,self.data)
		return self.data


	def check(self,date):
		if type(date) == type(list()):
			if len(date) == 3:
				return True		
		return False
	    

	def new_ansv(self,user,date,text):
		#print("start")		
		#if self.check(date) == False:
		#	print("yes")
		#	return None
		#else:		
		answ = [user,date,text]
		self.data.reverse()			
		self.data.append(answ)
		self.data.reverse()
		self.update_status = True
			#self.__call__()
		self.export_data()
		return None


	def style(self):
		stri = ""
		stri = stri + "forum {"
		stri = stri + "	border: solid black 2px;"
		stri = stri + "	border-radius: 10px;"
		stri = stri + "	background-color: rgba(254,254,216,0.85);"
		stri = stri + "	display: flex;"
		stri = stri + "  	width: 40%;"
		stri = stri + "  	/*height: 100%;*/"
		stri = stri + "	flex-direction: column;"
		stri = stri + "	align-items: start;"
		stri = stri + "	justify-content: center;"
		stri = stri + "	margin: 1%;"
		stri = stri + "	padding: 1%;}"
		stri = stri + "forum_row {"
		stri = stri + "	display: flex;"
		stri = stri + "  	width: 100%;"
		stri = stri + "	flex-direction: row;"
		stri = stri + "	align-items: center;}"
		return stri

	"""

	def forum_run_time(self,request):
		return self.__call__()
		

	def forum_button(self,request):
		user = ""
		text = ""
		if request.method == "POST":

			date = datetime.date.today()
			try:
				user = request.form["user"]
				text = request.form["text"]
			except:
				pass
		if user == "":
			return ""
		else:
			self.new_ansv(user,date,text)
		#return ""
		#return redirect(url_for("forum_run_time"))
		return redirect("/run_time")
	"""




class forum_2:
	#__USAGE:__
	#app = Flask(__name__)
	#dis = forum(app,[],5)
	#
	#@app.route("/")
	#def index():
	#	return redirect(url_for("forum_run_time"))
	#
	#@app.route("/forum_run_time", methods=["GET", ])
	#def forum_run_time():
	#	return dis.forum_run_time(request)	
	#
	#@app.route("/forum_button", methods=["POST"])
	#def forum_button():
	#	return dis.forum_button(request)
	
	#__forum_data_structure__
	#class for discuse forum.
	#data = [[user,date,text],[user,date,text],...]

	def __init__(self,storage,name,data=[],size = 100):
	#def __init__(self,app,data=[],size = 100):
		#setattr(forum,"app",app)
		self.storage = storage
		self.name = name
		interface = ""
		interface = interface + "<div class=\"col\">"
		interface = interface + "	<div class=\"form-group\">"
		interface = interface + "		<label>Enter user name, and your post text.</label>"
		interface = interface + "		<form method=\"POST\" action=\"/call_from_page\">"
		interface = interface + "			<input name=\"user\", id=\"forum\", placeholder=\"User\" >"
		interface = interface + "			<input name=\"text\", id=\"forum\", placeholder=\"Text\" >"
		interface = interface + "			<input type=\"submit\" >"
		interface = interface + "		</form>"
		interface = interface + "	</div>"
		interface = interface + "</div>"
		self.interface = interface
		#self.name = name
		self.data = data
		self.size = size	
		self.templ = "<forum><h3> Discuse Forum. </h3>" + self.interface + " <hr> {{X}}</forum>"
		self.temp = template("templ","",self.templ,dict())
		self.templ_ansv = "<forum_row><b> - User: {{user}}.</b>________<b>[ Date: {{date}} ].</b></forum_row><p>{{text}}</p><center>_______________________________</center>"
		self.temp_ansv = template("templ_ansv","",self.templ_ansv,dict())		
		#self.temp_ansv = template("templ_ansv","",templ_ansv,dict({"user":user,"date":date,"text":text}))
		self.view = ""
		self.update_status = False 
		self.worker = operator()
		#self.storage = storage 


		#__new__
		self.__temp_forum = self.storage["temp_forum"]
		self.__temp_forum_post = self.storage["temp_forum_post"]
		self.temp_forum = template("temp_forum","",self.__temp_forum,dict())
		self.temp_forum_post = template("temp_forum_post","",self.__temp_forum_post,dict())



	def get_str_date(self,date):
		return str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])


	def rutina(self):
		"""
		self.view = ""		
		#print(type(self.data))
		if self.size > len(self.data): 
			acu = self.data	
		else:
			acu = self.data[:self.size]
		for item in acu:
			user = item[0]
			date = item[1]
			text = item[2]
			#date = self.get_str_date(date_)
			self.temp_ansv.storage.update({"user":user,"date":date,"text":text})
			self.view = self.view + self.temp_ansv()
		self.temp.storage.update({"X":self.view})
		self.view = self.temp()
		"""
		#__new__
		self.view = ""		
		#print(type(self.data))
		if self.size > len(self.data): 
			acu = self.data	
		else:
			acu = self.data[:self.size]
		for item in acu:
			user = item[0]
			date = item[1]
			text = item[2]
			#date = self.get_str_date(date_)
			self.temp_forum_post.storage.update({"USER":user,"DATE":date,"POST":text})
			self.view = self.view + self.temp_forum_post()
		#print(self.__temp_forum)	
		self.temp_forum.storage.update({"X":self.view})
		self.view = self.temp_forum()
		print(self.view)





	def __call__(self):
		if not(self.view == ""):
			if self.update_status == False:
				pass
			else:
				self.rutina()
				self.update_status = False 
		else:
			self.rutina()
			self.update_status = False 
		return str(self.view)
		#return str("<center>"+self.view+"</center>")
		


	def import_data(self,data=None,path = ""):
		if not data == None:
			self.data = data
		if not path == "":
			self.data = self.worker.load_pickle(path)
		if (data == None and path == ""):	
			if "forum_data_"+self.name in (self.storage).keys():
				try:
					self.data = self.storage["forum_data_"+self.name]
				except:
					self.data = []
			else:
				self.data = []

		return None


	def export_data(self,path = ""):
		if path == "":
			self.storage["forum_data_"+self.name] = self.data
			return self.data
		else:
			self.worker.save_pickle(path,self.data)
		return self.data


	def check(self,date):
		if type(date) == type(list()):
			if len(date) == 3:
				return True		
		return False
	    

	def new_ansv(self,user,date,text):
		#print("start")		
		#if self.check(date) == False:
		#	print("yes")
		#	return None
		#else:		
		answ = [user,date,text]
		self.data.reverse()			
		self.data.append(answ)
		self.data.reverse()
		self.update_status = True
			#self.__call__()
		self.export_data()
		return None


	def style(self):
		stri = ""
		stri = stri + "forum {"
		stri = stri + "	border: solid black 2px;"
		stri = stri + "	border-radius: 10px;"
		stri = stri + "	background-color: rgba(254,254,216,0.85);"
		stri = stri + "	display: flex;"
		stri = stri + "  	width: 40%;"
		stri = stri + "  	/*height: 100%;*/"
		stri = stri + "	flex-direction: column;"
		stri = stri + "	align-items: start;"
		stri = stri + "	justify-content: center;"
		stri = stri + "	margin: 1%;"
		stri = stri + "	padding: 1%;}"
		stri = stri + "forum_row {"
		stri = stri + "	display: flex;"
		stri = stri + "  	width: 100%;"
		stri = stri + "	flex-direction: row;"
		stri = stri + "	align-items: center;}"
		return stri

	"""

	def forum_run_time(self,request):
		return self.__call__()
		

	def forum_button(self,request):
		user = ""
		text = ""
		if request.method == "POST":

			date = datetime.date.today()
			try:
				user = request.form["user"]
				text = request.form["text"]
			except:
				pass
		if user == "":
			return ""
		else:
			self.new_ansv(user,date,text)
		#return ""
		#return redirect(url_for("forum_run_time"))
		return redirect("/run_time")
	"""


class banner:
	def __init__(self,storage,name,ID,price,pcs,shipp_mess="",external_template=False):
		self.storage = storage
		self.name = name     		#[NAME]
		self.ID = ID 			#[ID]
		self.price = price		#[PRICE]
		self.pcs = pcs			#[PCS]
		self.shipp = shipp_mess		#[SHIPP]
		self.external_template = external_template
		self.tot_price = int(0)		#[TOT_PRICE]
		self.num = int(0) 		#[NUM] / aviable num.
		self.enable_banner = True	#Buying enabled.
		if external_template == True:
			self.temp = template("banner","",storage["temp_banner"],dict())
		else:
			self.temp = template("banner","",self.templ(),dict())			
		self.temp_disable = template("banner","",self.tampl_disable(),dict())
		self.view = ""
		self.p_1 = False
		self.m_1 = False

	
	def generate_hyperlink(self):	
		url = "/call_from_page?id=buy_{0}".format(self.name)
		stri = ""
		stri = stri + "<div class=\"banner_button\">"
		stri = stri + "<a href=\"{0}\"><center><b>  BUY  </b></center></a>".format(url)
		stri = stri + "</div>"
		return stri



	def __call__(self):
		#print("ss")
		self.temp = template("banner","",self.storage["temp_banner"],dict())
		self.temp.storage = dict({"NAME":self.name,"ID":self.ID,"PRICE":self.price,"PCS":self.num,"TOT_PRICE":self.tot_price,"BUY":self.generate_hyperlink(),"DOSAGE":self.storage["dosage_"+self.name]})                     
		self.view = self.temp()			
		return self.view
	
		"""
		if self.enable_banner == True:
			#self.temp.storage = dict({"NAME":self.name,"ID":self.ID,"PRICE":self.price,"SHIPP":self.shipp,"NUM":self.num,"TOT_PRICE":self.tot_price,"PCS":self.pcs})
			self.temp.storage = dict({"NAME":self.name,"ID":self.ID,"PRICE":self.price,"PCS":self.num,"TOT_PRICE":self.tot_price})
			self.view = self.temp()
			#return self.view
		else: 
			self.view = self.temp_disable
			#return self.view
		#print(self.view)
		return self.view		
		"""


	def calc(self):
		if self.p_1 == True:
			self.pcs = self.pcs + 1
		if self.m_1 == True: 
			self.pcs = self.pcs - 1 
		self.p_1 = False
		self.m_1 = False
		self.tot_price = float(int(self.pcs) * float(self.price)) 
		return None


	def load(self):
		try:
			self.ID = self.stroage["product_id_"+str(self.name)]
			self.shipp = self.stroage["default_shipp"]
		except:
			self.ID = "ID_"+str(self.name)
			self.shipp = "UPS (3, days!)"
		self.price = self.storage["price_"+str(self.name)]
		self.num = self.storage["num_"+str(self.name)]
		self.calc()
		return None


	def banner_row(self,txt):
		stri = ""		
		stri = stri + "<div class=\"banner_row\">"
		stri = stri + "	{0}".format(txt)		
		stri = stri + "</div>"
		return stri


	def banner_row_border(self,txt):
		stri = ""	
		#stri = stri + "	<div class=\"banner_row\">"
		stri = stri + "	<div class=\"banner_row_border\">"
		stri = stri + "	{0}".format(txt)		
		stri = stri + "	</div>"
		#stri = stri + "	</div>"
		return stri


	def templ(self):
		# {{NAME}}, {{ID}}, {{PRICE}}, {{TOT_PRICE}}, {{PCS}}, {{NUM}}
		# NUM -> Aviable.
		# PCS -> Buyed pcs.
		txt = ""	
		txt = txt + self.banner_row("name: {{NAME}}")
		txt = txt + self.banner_row("product_id: {{ID}}")
		txt = txt + self.banner_row("tot_price [1pcs]: {{PRICE}}")
		txt = txt + self.banner_row("aviable [pcs]: {{NUM}}")
		txt = txt + self.banner_row("ordered [pcs]: {{PCS}}")
		stri = ""
		stri = stri + "<form method=\"POST\" action=\"/call_from_page\">"
		stri = stri + "<input name=\"shipping\", id=\"shipping\", placeholder=\"Text\" >"
		stri = stri + "<input type=\"submit\" >"
		stri = stri + "</form>"
		txt = txt + self.banner_row(stri)
		stri = ""
		stri = stri + "<form method=\"POST\" action=\"/call_from_page\">"
		stri = stri + 	"<input name=\"num\", id=\"num\", placeholder=\"Text\" >"
		stri = stri + 	"<input type=\"submit\" >"
		stri = stri + "</form>"
		stri = stri + "<button> +1 </button>"
		stri = stri + "<button> -1 </button>"
		txt = txt + self.banner_row(stri)
		stri = ""
		stri = "{{TOT_PRICE}}"+"______"+"<button><b> BUY </b></button>"
		txt = txt + self.banner_row_border(stri)
		return "<div class=\"banner\">{0}</div>".format(txt)


	def tampl_disable(self):
		txt = ""
		stri = "This item is not aviable for buying"
		txt = txt + self.banner_row(stri)
		stri = "Name: "+str(self.name)
		txt = txt + self.banner_row(stri)
		stri = "Product_id: "+str(self.ID)
		txt = txt + self.banner_row(stri)
		return "<div class=\"banner\">{0}</div>".format(txt)
		

		
class page_wrapper:	

	def __init__(self,name,path,storage):
		self.mode = False
		self.banner = banner(storage, name, name, int(50), int(7))
		self.banner.load()
		self.wk = operator()
		self.name = name 
		self.path = path
		self.storage = storage
		self.img_format = ".jpg"
		self.img = "static/" + self.name + self.img_format
		try:
			self.temp = storage["temp_"+str(self.name)]		
		except: 
			self.temp = self.wk.load_text(self.path+self.name+".txt")
		try:
			self.label = storage["label_"+str(self.name)]
		except:
			self.label = self.name

		try:
			self.forum = forum(self.storage,self.name,self.storage["forum_data_"+self.name])
		except:
			self.forum = forum(self.storage,self.name)

		#try:
		#	self.forum.import_data()
		#except:
		#	try:
		#		self.forum.import_data(None,self.path)
		#	except:
		#		self.forum.import_data(list(),"")	


		if self.mode == False:
			temp_item_page = self.storage["temp_item_page"]
			self.page = template(self.name,"",temp_item_page,dict())
		else:
			self.page = template(self.name,"",self.page_templ(),dict())
		#---------------------------------------------
		self.fast_temp = str(self.page())
		self.view = ""
		self.full_render = True
	

	def text(self):
		#self.temp.storage = dict()
		#return str(self.temp())
		#print(self.temp)
		#print(self.temp())
		return self.temp
		



	def __call__(self):
		#print(self.banner())				
		self.banner.load()
		try:
			self.forum.import_data(self.storage["forum_data_"+self.name],"")
		except:
			pass
		self.full_render = True
		if self.full_render == True:
			#print("sss")
			self.view = self.render(self.banner(),self.text(),self.forum())
		else:
			self.fast_temp.storage = dict({"TEXT_1":TEXT_1,"TEXT_3":self.forum()})	
			self.view = str(self.fast_temp())		
		return self.view + "</div>"  #<<<<=========
#!!!!!!!!!!!!!!!!!!!!!!!!!!   CORECTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	def render(self,TEXT_1,TEXT_2,TEXT_3):
		#print("sssssss")
		self.page.storage = dict({"LABEL":self.label,"IMG":self.img,"TEXT_1":TEXT_1,"TEXT_2":TEXT_2,"TEXT_3":TEXT_3})
		return str(self.page())


	def export_forum_data(self):
		self.storage["forum_data_"+self.name] = self.forum.data
		self.storage.save_data(self.path+"data/storage.pickle")
		#print("-------------------")
		#print("forum_data_"+self.name)
		#print(self.forum.data)
		#print(self.storage["forum_data_"+self.name])
		return None


	def set_post(self,user,post):
		date = str(datetime.date.today())
		self.forum.new_ansv(str(user),date,str(post))
		self.export_forum_data()
		return None



	def img_resize(self,img):
		stri = ""	
		stri = stri + "<div class=\"img_container\">"
		stri = stri + "	   <div class=\"img_box\">"
		stri = stri + "		{0}".format(img)        
		stri = stri + "	   </div>"
		stri = stri + "</div>"
		return stri


	def page_templ(self):
		stri = ""
		stri = stri + "<div class=\"item_page\">"
		stri = stri + "	<div class=\"item_vertical_context\">"
		stri = stri + "		<div class=\"item_labbel\">"
		stri = stri + "			<center><h1>{{LABEL}}</h1></center>"
		stri = stri + "		</div>"
		stri = stri + "	</div>"
		stri = stri + "	<div class=\"item_vertical_context\">"
		stri = stri + "		<div class=\"item_horizontal_context\">"
		stri = stri + "				<div class=\"img_cont\">"
		stri = stri + "					{0}".format(self.img_resize("<img src=\"{{IMG}}\">"))		
		stri = stri + "				</div>"
		stri = stri + "				<div class=\"text_1_cont\">"
		stri = stri + "					{{TEXT_1}}"
		stri = stri + "				</div>"
		stri = stri + "		</div>"
		stri = stri + "	</div>"
		stri = stri + "	<div class=\"item_vertical_context\">"
		stri = stri + "		<div class=\"text_2_cont\">"
		stri = stri + "			{{TEXT_2}}"
		stri = stri + "		</div>"
		stri = stri + "	</div>"
		stri = stri + "	<div class=\"item_vertical_context\">"
		stri = stri + "		<div class=\"text_2_cont\">"
		stri = stri + "			{{TEXT_3}}"
		stri = stri + "		</div>"
		stri = stri + "	</div>"
		stri = stri + "</div>"
		return stri





class basket:
	#shitch = 1 ... review
	#switch = 2 ... set shipping and payment
	#switch = 3 ... payment
	#switch = 4 ... finish

	def __init__(self,path,uid,storage):
		self.path = path
		self.storage = storage
		self.data = dict()
		self.uid = uid
		self.switch = 0
		self.page = ""
		self.user_email = "user@google.com"
		self.pay = False
		self.gw_url = ""

		self.__wait = True
		self.vector = dict()

		temp_0 = self.storage["temp_basket"]
		self.temp_0 = template("basket_0","",temp_0,dict())
		temp_1 = self.storage["temp_shipping"]		
		self.temp_1 = template("basket_1","",temp_1,dict())
		#temp_2 = self.storage["temp_basket_payment"]
		#self.temp_2 = template("basket_2","",temp_2,dict())
		#---------------------------
		#temp_3 = self.storage["temp_basket_success"]
		#self.temp_3 = template("basket_2","",temp_3,dict())
		#self.temp_4 = self.storage["temp_basket_fail"]
		#self.temp_5 = self.storage["temp_basket_wait"]
		temp_2 = self.storage["temp_basket_choice"]
		self.temp_2 = template("temp_basket_choice","",temp_2,dict())

		temp_3 = self.storage["temp_basket_card_payment"]
		self.temp_3 = template("basket_3","",temp_3,dict())


		temp_4 = self.storage["temp_basket_btc_payment"]
		self.temp_4 = template("basket_4","",temp_4,dict())	

		temp_5 = self.storage["temp_basket_result"]
		self.temp_5 = template("basket_5","",temp_5,dict())


		temp_6 = self.storage["temp_basket_card_result"]
		self.temp_6 = template("basket_6","",temp_6,dict())

	



	def wait(self,wait = None):
		if wait == False:
			self.__wait = False
		return self.__wait



	def generate_hyperlink_base(self,button_id,button_text):	
		url = "/call_from_page?id={0}".format(button_id)
		stri = ""
		stri = stri + "<a href=\"{0}\"><button><center>  {1}  </center></button></a>".format(url,button_text)
		return stri





	def generate_hyperlink(self,button_id,button_text):	
		url = "/call_from_page?id={0}".format(button_id)
		stri = ""
		#stri = stri + "<div class=\"banner_convertor\">"
		stri = stri + 	"<div class=\"banner_button\"><center><a href=\"{0}\"><b>  {1}  </b></a></center></div>".format(url,button_text)
		#stri = stri + "</div>"
		return stri



	def tmp(self,var):
		stri = ""
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "        		{0}".format(var)
		stri = stri + "		</div>"
		return stri



	def pay_pannel(self):

		stri = ""
		stri = stri + "<div class=\"banner_row\">"
		stri = stri + self.tmp("")
		stri = stri + self.tmp("")
		stri = stri + self.tmp("")
		stri = stri + self.tmp("")
		stri = stri + self.tmp("")
		stri = stri + self.tmp("")
		stri = stri + self.tmp("")
		stri = stri + self.tmp("")
		stri = stri + self.tmp(".")		
		stri = stri + "</div>"
		empty = stri

		CONTEXT = ""
		for item in self.data.keys():
			name = item 
			price = str(self.storage["price_"+item])
			num = str(self.storage["num_"+item])
			psc = str(self.data[item])
			tot = str(int(int(psc)*float(price)))
			m1 = self.generate_hyperlink_base("basket_m1_"+item,"- 1")
			p1 = self.generate_hyperlink_base("basket_p1_"+item,"+ 1")
			#----------------------------------------------
			stri = ""
			#stri = stri + "<div class=\"banner_convertor\">"			
			stri = stri + "<form method=\"POST\" action=\"/call_from_page\">"       		
			stri = stri + "<input name=\"pcs_{0}\" id=\"basket_psc_{0}\" placeholder=\"0\">".format(item)
			#stri = stri + "</form>"
			#stri = stri + "</div>"
			inp = stri     
			#----------------------------------------------
			sub = ""
			#sub = sub + "<form method=\"POST\" action=\"/call_from_page\">"       		
			sub = sub + "<input type=\"submit\">"
			sub = sub + "</form>"
			#sub = "<button>submit</button>"#"<input type=\"submit\" id=\"basket_set_psc_{0}\">".format(item)

			stri = ""
			stri = stri + "<div class=\"banner_row\">"
			stri = stri + self.tmp(name)
			stri = stri + self.tmp(price)
			#stri = stri + self.tmp(num)
			stri = stri + self.tmp(psc)
			stri = stri + self.tmp(tot)
			stri = stri + self.tmp(m1)
			stri = stri + self.tmp(p1)
			stri = stri + self.tmp(inp)
			stri = stri + self.tmp(sub)		
			stri = stri + "</div>"
			CONTEXT = CONTEXT + stri + empty
		#----------------------------------------------
		head = ""
		head = head + "	<div class=\"banner_row\">"
		head = head + "		<div class=\"banner_box\">"
		head = head + "			BASKET:"
		head = head + "		</div>"
		head = head + "	</div>"
		#----------------------------------------------
		stri = ""
		stri = stri + "<div class=\"banner_row\">"
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "        		NAME:"
		stri = stri + "		</div>"
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "        		PRICE:"
		stri = stri + "		</div>"
		#stri = stri + "		<div class=\"banner_small_box\">"
		#stri = stri + "        		AVIALBE PSC:"
		#stri = stri + "		</div>"
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "        		SET PSC:"
		stri = stri + "		</div>"
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "        		TOTAL PRICE:"
		stri = stri + "		</div>"
		stri = stri + "		<div class=\"banner_small_box\">"   		
		stri = stri + "		</div>"
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "		</div>"
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "		</div>"
		stri = stri + "		<div class=\"banner_small_box\">"
		stri = stri + "		</div>"
		stri = stri + "</div>"
		LABEL = stri 
		#----------------------------------------------
		OUT = ""
		OUT = OUT + "	<div class=\"banner_row\">"
		OUT = OUT + "		<div class=\"banner_half_box\">"        	
		OUT = OUT + "		</div>"
		OUT = OUT + "		<div class=\"banner_half_box\">"
		OUT = OUT + "			<div class=\"banner_convertor\">"        		
		OUT = OUT + "				{0}".format(self.generate_hyperlink("basket_go_shipping"," <b> BUY </b>"))
		OUT = OUT + "			</div>"
		OUT = OUT + "		</div>"
		OUT = OUT + "	</div>"
		#----------------------------------------------

		return "<div class=\"banner_cont\">" + head + empty + LABEL + empty + CONTEXT + OUT +"</div>"
	#END
	#======================================================
	"""
	def action_temp(self,item):
		stri = ""
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp;{0} </td>".format(self.generate_hyperlink_base("basket_m1_"+str(item)," <b> -1 </b>"))
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp;{0} </td>".format(self.generate_hyperlink_base("basket_p1_"+str(item)," <b> +1 </b>"))
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp;<input type=\"text\" id=\"lname\" name=\"lname\"><input type=\"submit\" value=\"Submit\"></td>" # Text_field
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp;{0}</td>".format(self.generate_hyperlink_base("basket_go_shipping"," <b> BUY </b>")) #BUY
		return stri
	def pay_pannel(self,stat=None):
		if stat == None:
			stat = (self.calc())[1]
		stri = ""
		stri = stri + "<tr>"
		stri = stri + "<td>&nbsp;NAME</td>"
		stri = stri + "<td>&nbsp;PCS</td>"
		stri = stri + "<td>&nbsp;PRICE</td>"
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" #+1
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" #-!
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" # Text_field
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" #BUY
		stri = stri + "</tr>"
		cont = stri 

		stri = ""
		stri = stri + "<tr>"
		stri = stri + "<td>&nbsp; </td>"
		stri = stri + "<td>&nbsp; </td>"
		stri = stri + "<td>&nbsp; </td>"
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" #+1
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" #-!
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" # Text_field
		stri = stri + "<td>&nbsp; </td>" #empty
		stri = stri + "<td>&nbsp; </td>" #BUY
		stri = stri + "</tr>"
		empt = stri 
		for item in stat.keys():
			stri = ""
			stri = stri + "<tr>"
			stri = stri + "<td>&nbsp;{0}</td>".format(item)
			stri = stri + "<td>&nbsp;{0}</td>".format(self.data[item])
			stri = stri + "<td>&nbsp;{0}</td>".format(self.storage["price_"+item])
			if self.storage["num_"+item] == 0:
				stri = stri + "<td>&nbsp;{0}</td>".format("")
			else:
				stri = stri + "<td>&nbsp;{0}</td>".format(self.action_temp(item))
			stri = stri + "</tr>" + empt + "</tr>"
			cont = cont + stri
		table = "<table><tbody>"+str(cont)+"</tbody></table>"
		self.page = table
		return table
		"""


	def mess(self,messenge):
		stri = ""
		stri = stri + "<div class=\"basket_mess\">"
		stri = stri + "	<b>{0}</b>".format(messenge)
		stri = stri + "</div>"
		return stri


	def get_form(self,request):
		form = dict()
		return form


	def pay_table(self,stat):
		return self.pay_pannel()


	def __call__(self):
		#print("SWITCH  "+str(self.switch))
		#Review
		if self.switch == 0:
			self.vector = dict()
			self.temp_0.storage = dict({"X":self.pay_pannel()})
			self.view = self.temp_0()
			
		#Shipping
		if self.switch == 1:
			self.vector = dict()
			self.temp_1.storage = dict({"X":self.generate_hyperlink("basket_NEXT_SHIPP","NEXT")})
			self.view = self.temp_1()
			self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)
			#print(self.view)
			#self.view = self.temp_1()
			#print(self.view)
			#print("asdasdasdasdasdasdasd")

		#Choice of payment method
		if self.switch == 2:
			self.temp_2.storage = dict({"BUTTON_BTC":self.generate_hyperlink("basket_SET_BTC","BTC"),"BUTTON_CARD":self.generate_hyperlink("basket_SET_CARD","CARD")})
			self.view = self.temp_2()
			#self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)
			#out = self.calc()
			#self.temp_2.storage = 
			#self.data.update({"PAY_TABLE":self.pay_table(out[1])})
			#temp = self.storage["temp_baket_payment"]
			#self.temp = template("basket","",temp,self.data)

		#SET/CONFRIM_CARD
		if self.switch == 3:
			self.temp_3.storage = dict({"GENERATE_PAYGATE_CARD":self.generate_hyperlink("GENERATE_PAYGATE_CARD","PAYGATE"),"CONFRIM_CARD":self.generate_hyperlink("CONFRIM_CARD","PAY")})
			self.view = self.temp_3()
			self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)
	


		#SET/CONFRIM_CARD
		if self.switch == 4:
			self.temp_4.storage = dict({"EMAIL":self.user_email,"STATUS":self.vector["STATUS"],"PRICE":self.vector["PRICE"],"ADDRESS":self.vector["ADDRESS"],"CURRENCY":self.vector["BTC_currency"],"CONFRIM":self.generate_hyperlink("CONFRIM_BTC_PAY_REQUEST","LEAVE")})
			self.view = self.temp_4()
			self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)
			#print(">>>>>>>>>>")
			#print(self.vector)
			#print("<<<<<<<<<<<")

	

		#FINISF_BTC
		if self.switch == 5:
			self.view = self.temp_5()
			self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)
			#print(">>>>>>>>>>")
			#print(self.vector)
			#print("<<<<<<<<<<<")

	

		#FINISH_CARD
		if self.switch == 6:
			self.temp_4.storage = dict({"BASKET_BACK":self.generate_hyperlink("BASKET_BACK","HOME")})
			self.view = self.temp_6()
			self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)



		self.switch = 0	





		
		"""
		if self.switch == 2:
			self.temp_2.storage = dict({"X":self.generate_hyperlink("basket_CONFRIM","CONFRIM PAY")})
			self.view = self.temp_2()
			self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)
			#out = self.calc()
			#self.temp_2.storage = 
			#self.data.update({"PAY_TABLE":self.pay_table(out[1])})
			#temp = self.storage["temp_baket_payment"]
			#self.temp = template("basket","",temp,self.data)
		"""
		"""
		if self.switch == 4:
			#__V1___
				#temp = self.mess("Payment: Sucess... Transaction send to your email!")
				#self.temp = template("basket","",temp,dict())
				#self.data = dict()
				#self.switch = 
			#__V2__
			self.temp_3.storage = dict({"USER_EMAIL":self.user_email})
			self.view = self.temp_3()	
			self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)

			#__V3__
		"""	


		"""
		if self.switch == 3:
			self.view
		"""
		"""
		if self.switch == 5:
			self.view = str(self.temp_5)
		"""
		#--------------------
		#__RESTRICTOR__
		#self.view = "<basket_restrictor> {0} </basket_restrictor>".format(self.view)

		#--------------------
		return self.view


	def SET_PAY(self):
		if not(self.vector["TYPE"] == "BTC" or self.vector["TYPE"] == "BTC"):
			return None
		self.vector.update("")
		cand = []
		for key in self.data:
			if "price_"+key in self.storage.keys():
				cand.append(key)
		for cat in self.storage["category_dict"]:
			for key in self.storage["category_dict"][cat]:			
				if key in cand:
					self.vector.update({"item_"+key:self.data[key]})
		if self.vector["TYPE"] == "BTC":
			self.switch = 4	
			self.vector.update({"TYPE":"BTC"})		
		if self.vector["TYPE"] == "CARD":
			self.switch = 3
			self.vector.update({"TYPE":"CARD"})
		self.vector.update({"uid":self.uid})
		return None	



		"""
		self.vector = dict()
		self.vector = self.data
		if (_type == "BTC" or _type == "CARD"):
			for cat in self.storage["category_dict"]:
				for key in self.storage["category_dict"][cat]:			
					if key in self.data.keys():# and not("item_"+item in self.data.keys()):
						self.vector.update({"item_"+key:self.data[key]})
						self.vector.pop(key)
		

		
			item_data = dict()
			metadata = dict()			
			for key in self.data.keys():
				if "item_" in key:
					item_data.update({(key[5:]):self.data[key]})
				else:
					metadata.update({key:self.data[key]})
			#res_vector = self.__trans.set_transaction(_type,uid,item_data,metadata)
			res_vector = {**metadata,**item_data}
			
			#res_vector = self.data
			if _type == "BTC":
				self.switch = 4	
				self.vector.update({"TYPE":"BTC"})		
			if _type == "CARD":
				self.switch = 3
				self.vector.update({"TYPE":"CARD"})
			#res_vector = dict({"gw_url":"www.google.com/","STATUS":True,"KEY":"13235"})
			self.vector.update({"uid":self.uid})
			#self.vector = res_vector
			return None	

		"""

	def GET_PAY(self,finish = False):		
		if finish == True:
			try:
				status = self.vector["STATUS"]
				if status == True:
					STATUS = "CONFRIMED"				
				else:
					STATUS = "UNCONFRIMED"
			except:
				STATUS = "UNKNOW"
		else: 
			STATUS = "WAITING..."
		self.temp_5.storage = dict({"EMAIL":str(self.user_email),"STATUS":STATUS,"HOME":self.generate_hyperlink("RANDOM_WRONG_STRING","LEAVE")})
		self.switch = 5
		self.view = self.temp_5() 
		vector = self.vector
		#self.vector = dict()
		#self.data = dict()
		return vector
		





	def SHOW_PAY(self):	
		STATUS = "CONFRIMED"
		self.temp_5.storage = dict({"EMAIL":str(self.user_email),"STATUS":STATUS,"HOME":self.generate_hyperlink("RANDOM_WRONG_STRING","LEAVE")})
		self.switch = 5
		self.view = self.temp_5() 
		return None
		


			
	"""
	def GET_PAY(self,_type = "CARD",MODE = "INTERNAL",_implocite = dict()):
		if _type == "BTC":
			self.switch = 5
			self.view = str(_type) + "    " + str(MODE)



		if _type == "CARD":
			self.switch = 6
			if MODE == "EXTERNAL":
				self.view = str(_type) + "    " + str(MODE)
			if MODE == "INTERNAL":
				self.view = str(_type) + "    " + str(MODE)


			vector = _implicite
			try:
				KEY = vector["KEY"]
				vector.update({"STATUS":True}) #TESTING...
			except:
				KEY = "FAILED_TRANSACTIONS"
			res = self.__trans.get_transaction(KEY,vector)		



			self.switch = 3
			self.view = str(res+" RENDER......"+str(_type))
			return None
	"""
	


	"""
	def calc(self):
		stat = dict()
		for cat in self.storage["category_dict"]:
			for item in self.storage["category_dict"][cat]:	
				if item in self.data.keys():
					stat.update({item:[self.data[item],self.data[item]*float(self.storage["price_"+item])]})				
		tot = 0
		for key in stat.keys():
			tot = tot + (stat[key])[1]
		return(tot,stat)
	"""

	def inputs(self,button="",form=None):
		if not(form == None) and button == "":
			for key in form.keys():
				self.data.update({key:int(form[key])})
		else:	
			pass
		

		#if button == "buy":
		#	self.switch = 1

		#if button == "submit_setting":
		#	self.switch = 2
		#	for it in form.keys():
		#		self.data.update({it:form[it]})

		#if button == "submit_pay":
		#	self.switch = 3
		#	for it in form.keys():
		#		self.data.update({it:form[it]})
		#	#--------------------------------
		#	#call class transaction for pay...
		#	#--------------------------------
		#print("=====2==========>>>>>")
		#print(button)


		if (button == "card_pay") and not(form == None): 	
			for key in form.keys():
				self.vector.update({key:form[key]})
			




		if (button == "shipp") and not(form == None): 	
			#self.vector = dict()
			for key in form.keys():
				self.vector.update({key:form[key]})
			

		#print("==========>>>>")

		#print(self.data)


		if not(button == "") and form == None: 	
			
			for cat in self.storage["category_dict"]:
				for item in self.storage["category_dict"][cat]:			



					if button == "buy_"+item: 	
						if not(item in self.data.keys()):
							self.data.update({item:1})
						else:
							self.data[item] = self.data[item] + 1	
		
					#print("basket_"+"_p1_"+item)
					if button == "basket"+"_p1_"+item:
						#print("===============>>>>>")
						self.data[item] = self.data[item] + 1	
		

					if button == "basket"+"_m1_"+item:
						self.data[item] = self.data[item] - 1		
						if self.data[item] == 0: 
							self.data.pop(item)

					if button == "basket_submit_buy_"+item: 
						if not(item in self.data.keys()):
							self.data.update({item:form["pcs_"+item]})
						else:
							self.data[item] = form["pcs_"+item]	
		else:
			pass
		
		return None


	def pay_interface(self):
		#PROCES.......
		#.............
		self.pay=True
		#.............
		if self.pay == True:
			self.switch = 3
		else:
			self.switch = 4
		return None







class market:

	def __init__(self,path,storage,data=None):
		self.path = path 
		self.line_size = 4
		self.top = []
		self.data = []
		self.storage = storage	 
		#self.short_text_size = 50
		#self.font_size = [10,10,10]
		self.img_format = ".jpg"	
		#--------------------
		banner = self.storage["temp_market_banner"]
		row = self.storage["temp_market_row"]
		market = self.storage["temp_market"]
		self.temp_banner = template("banner","",banner,dict())
		self.temp_row = template("row","",row,dict())
		self.temp_market = template("row","",market,dict())
		self.temp_banner_empty = self.storage["temp_market_banner_empty"]


	def get_size(self,page):
		__JS = self.storage["js_get_screen_size"]
		_JS = template("JS","",__JS,dict({"ELEMENT_ID":"1"})) 
		JS = _JS()
		ind = page.rindex("</div>")
		UP = ">>>"
		DOWN = "<<<" 
		page[ind+6:] + UP + "<script>" + JS + "</script>" + DOWN + page[:ind+6]
		return page 


	def make_data(self):
		for key in (self.storage["category_dict"]).keys():
			for item in self.storage["category_dict"][key]:
				self.data.append([0,item,"static/"+item+self.img_format,self.storage["short_text_"+item],str(self.storage["price_"+item])])
		return None

	def sort_data(self,top_list = None):
		return None
	

	def get_market(self):
		num = len(self.data) 
		cont = ""
		sum_ = 0
		for j in range(0,num):
			if sum_ > num: break
			stri = ""
			for i in range(0,self.line_size):
				if sum_ < num: 
					self.temp_banner.storage = dict({"LABBEL":self.data[sum_][1],"IMG":self.data[sum_][2],"TEXT":self.data[sum_][3],"PRICE":self.data[sum_][4]})
					stri = stri + self.temp_banner()
				else:
					stri = stri + self.temp_banner_empty
				sum_ = sum_ + 1	
			self.temp_row.storage = dict({"X":stri})
			cont = cont + self.temp_row()
		self.temp_market.storage = dict({"X":cont})
		return self.temp_market()


	def wrapper(self):
		#print("JOHOH...")
		#print(self.get_market())
		#print(self.data[len(self.data)-1])
		self.storage.update({"temp_home":str(self.get_market())})
		return None















