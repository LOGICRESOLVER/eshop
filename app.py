#__IMPORTS__
from flask import session as sess 
from flask import Flask, render_template, session
from flask import render_template, url_for, request, redirect, make_response
from server_tools import session
from cache import cache
import os
from tools import operator
import datetime
import time



#__CONFIG__
def get_config():
	hostname = "nootropic.noic.cz"
	port = 5001
	#---------------------------------
	#path = os.getcwd()+"/"
	#path = os.path.dirname(__file__) + "/"
	path = "./"
	print(path)
	config = dict()
	config.update({"path":path})
	config.update({"colector_size":10000})
	config.update({"hostname":hostname})
	config.update({"port":str(port)})
	static_cookie = dict()
	config.update({"cookies":static_cookie})
	#__SECRET_KEY__
	secret_key = "8df97sfs8fssdf6s9fsg7gs0f"
	config.update({"secret_key":secret_key})
	config.update({"run_setup":False})

	#_________________________________
	config.update({"currency":"EUR"})
	config.update({"lang":"EN"})	
	config.update({"url":"http://127.0.0.1:5001/"})
	config.update({"IN_URL":"http://127.0.0.1:5001/interface/"})	
	config.update({"GW_URL":"http://127.0.0.1:5001/user_return_call/"})
	config.update({"OUT_URL":"http://localhost:8080/register/create?id="})	
	address=["1Lbcfr7sAHTD9CgdQo3HTMTkV8LK4ZnX71",
		"a89sd09as8d0as08das90f8as09df8sd09",
		"as89d8as0d98as90d8a9s0d8as90d8asff",
		"as7d98as79a8sd7as89HTMTkV8LK4ZnX71"]
	config.update({"address":address})	
	return config

	




#__WEB_APP_SETUP__
#=================
from server_tools import sessions
global config
global server
config = get_config()
if config["run_setup"] == True:
	try:
		#os.system("rm "+path+"data/storage.pickle")
		os.system("python3 "+ config["path"] +"setup.py")
	except:
		pass
else: pass
server = sessions(config)
app = Flask(__name__)
app.secret_key = config["secret_key"]
#================


	

#__WEB_APP_IMPLEMENTATION__
#====================================================
@app.route('/')
def main():
	ses = server.ses()
	ses.context.page()
	ses.page = ses.storage["temp_index"]
	return ses.refresh()


@app.route('/menu')
def menu():
	ses = server.ses()
	name = str(request.args["id"])	
	print(name)
	if not(name in ses.context.content):
		pass		
	else:
		ses.click(name)
		ses.refresh()
	return ses.refresh()
   

def custome_test(ses):
	#cache_ = dict({"2FMA":5})
	#ses.basket.data = cache_
	return None




@app.route('/nav_bar')
def nav_bar():
	ses = server.ses()
	name = str(request.args["id"])	
	if name in ["basket","home","about_us","account"]:
		custome_test(ses)
		ses.click(name)	
	else:
   		pass
	return ses.refresh()
   

@app.route('/runtime', methods=['POST',"GET"])
def runtime():
	ses = server.ses()
	try:
		return ses.refresh()		
	except:
		redirect(url_for("/"))




@app.route('/interface/<IDENTITY>', methods=["POST","GET"])
def interface(IDENTITY):

	#__DOWNLOAD_DATA__
	vector = server.IN(request)
	print(vector)
	#print("JOHOHO")
	#__TASK_1__
	print(server.Transactions.GET(IDENTITY,vector))	
	try:
		pass
		#print("JOHOHO")
		#server.Transactions.GET(IDENTITY,vector)			
		#print("JOHOHO")
	except:
		pass
		print("   -->Error: Not posible run server.Transctions.GET(url,vector).")
	#__TASK_2__
	uid = ""
	ID = ""
	try:
		uid = str(vector["uid"])
	except:
		pass
	try:
		ID = str(vector["ID"])
	except:
		pass
	try:
		if (uid == "") and ( not(ID == "") ):
			uid = ID
		ses = server.get_ses(uid)
		ses.basket.wait(False)
		server.set_ses(uid,ses)
	except:
		pass
	return("SERVER IS LIVE!")



@app.route('/user_return_call/<key>', methods=['POST',"GET"])
def user_return_call(key):
	time.sleep(1)
	ses = server.ses()
	#return render_template("redirect.html"), {"Refresh": "5; url=www.google.com"}	
	#return redirect(server.url + "user_return_call_wait/" + str(key))
	if ses.basket.wait() == True:
		return redirect(server.url + "user_return_call_wait/" + str(key))	
	else:
		ses = server.ses()
		vector = ses.basket.vector
		ses.basket.GET_PAY(vector,True)
		#ses.basket.SHOW_PAY()
		ses.basket.wait(True)
		ses.page = ses.basket()	
		return redirect(url_for("runtime"))


@app.route('/user_return_call_wait/<key>', methods=['POST',"GET"])
def user_return_call_wait(key):
	default_wait = 8
	url = server.url + "user_return_call/" + str(key)
	ses = server.ses()
	return render_template("redirect.html"), {"Refresh": "{0}; url={1}".format(default_wait,url)}
	#return redirect(url)
	#return server.__redirect__("http:/"+url,default_wait)




def extract_form(request,__key_map):
	#print("=============>>>>")
	#print(request.form)
	if type(__key_map) == type("..."):
		key_map = [__key_map]
	else:
		key_map = __key_map
	#try:
	if True:
		form_ = dict()
		for item in request.form.keys():
			for key in key_map:
				#print(key)
				#print(item)
				if str(key) == str(item):
					form_.update({str(item):str(request.form[item])})
		return form_		
	else:
	#except:
		return dict()



#NOT IMPLEMENTED
@app.route('/call_from_page', methods=['POST',"GET"])
def call_from_page():
		"""
		try:
			for key in request.form.keys():
				print(request.form[key])
				print(key)
		except: 		
			pass

		"""
		#print(request.form)
		ses = server.ses()
		button_id = ""
		try:
			button_id = str(request.args["id"])
		except:
			pass
		try:		
			if button_id[0] == "/":
				button_id = button_id[1:] 
		except: 
			pass




		#__BASKET_SHIPPING__:
		try:
			form_ = extract_form(request,["full_name","street","city","zip","country"])
			print(form_)
			ses.basket.inputs("shipp",form_)
		except:
			pass
			
		
		#__BASKET_CARD__:
		try:
			form_ = extract_form(request,["card_number","card_expired","card_zip"])
			#print(form_)
			ses.basket.inputs("card_pay",form_)
		except:
			pass



		if button_id == "":	
			
		
			#__BASKET_BASE__:
			try:
				form_ = dict()
				for item in request.form.keys():
					if "pcs_" in item:
						form_.update({str(item[4:]):request.form[item]})
				#print(form_)
				ses.basket.inputs("",form_)
				ses.page = ses.basket()		
			except:
				pass





			"""
			#__BASKET_CARD__:
			try:
				form_ = extract_form(request,["card_number","expired_time","zip"])
				print(form_)
				ses.basket.inputs("",form_)
				ses.page = ses.basket()		
			except: 
				pass

			"""
			#__FORUM__
			try:
				if not(request.form['user'] == None) and not(request.form['text'] == None):
					#processing forum...
					user = ""
					text = ""
					try:
						user = request.form['user']
						text = request.form['text']
					except:
						pass
					
					name = ses.context.name
					page = ses.context.page(name)
					page.forum.import_data()
					page.set_post(user,text)
					ses.page = ses.context()
					return redirect(url_for("runtime"))
			except:
				pass



		else:
			if "basket_m1_" in button_id:
				print("johoho")
				ses.basket.inputs(button_id)
				ses.page = ses.basket()
				print("ok")
		
			if "basket_p1_" in button_id:
				print("dasdasdasd")
				ses.basket.inputs(button_id)
				ses.page = ses.basket()

			#processing touch button
			if "buy_" in button_id:
				ses.basket.inputs(button_id,None)
		
			if button_id == "basket_go_shipping":		
				ses.basket.switch = 1
				ses.page = ses.basket()


			if button_id == "basket_NEXT_SHIPP":		
				ses.basket.switch = 2
				ses.page = ses.basket()

			if button_id == "basket_CONFRIM":
				#ses.basket.pay_interface()
				ses.basket.switch = 3
				#ses.trans_task()
				ses.page = ses.basket()

			#__ALTERNATIVE_RUTINA_FOR_basket.confrim_pay(_type)
			#if button_id == "basket_SET_BTC":
			#	ses.basket.switch = 3
			#	ses.trans_task()
			#	ses.page = ses.basket()


			if button_id == "basket_SET_CARD":
				ses.basket.vector.update({"TYPE":"CARD"})
				ses.basket.SET_PAY()
				ses.basket.switch = 3
				ses.page = ses.basket()
				#print("JOHOHO")


			if button_id == "basket_SET_BTC":
				ses.basket.vector.update({"TYPE":"BTC"})
				ses.basket.SET_PAY()
				ses.basket.vector.update({"uid":str(ses.uid)})
				ses.basket.vector.update({"TYPE":"BTC"})
				ses.basket.vector = server.Transactions.SET(ses.basket.vector)
				ses.basket.GET_PAY(False)
				ses.basket.switch = 4	
				ses.page = ses.basket()
				ses.basket.vector = dict()
				ses.basket.data = dict()



			if button_id == "GENERATE_PAYGATE_CARD":
			
				ses.basket.vector.update({"uid":str(ses.uid)})
				ses.basket.vector.update({"TYPE":"CARD"})
				ses.basket.vector = server.Transactions.SET(ses.basket.vector)
				vector = ses.basket.GET_PAY(dict({"GW_URL":"http://127.0.0.1:5009/1111","STATUS":True,"KEY":"13235"}))
				if "GW_URL" in vector.keys():
					return redirect(vector["GW_URL"])
				else:
					return "ERROR_PAYGATE_GENERATING..."


			if button_id == "CONFRIM_CARD":
				
				ses.basket.vector.update({"uid":str(ses.uid)})
				ses.basket.vector.update({"TYPE":"CARD"})
				ses.basket.vector = server.Transactions.SET(ses.basket.vector)
				#vector = server.Transactions.GET(vector)
				ses.basket.GET_PAY(False)
				ses.page = ses.basket()


			if button_id == "CONFRIM_BTC_PAY_REQUEST":
				pass


		return redirect(url_for("runtime"))



"""
@app.route('/call_from_paygate', methods=['POST',"GET"])
def call_from_paygate():
	ses = server.ses()
	KEY = int(0)
	try:
		KEY = str(request.args["id"])
	except:
		return int(0) #<-- WRONG KEY.
	try:		
		if button_id[0] == "/":
			button_id = button_id[1:] 
	except: 
		pass
	try:		
		KEY = int(KEY) 
	except: 
		pass
	ses.basket.GET_PAY(KEY,finish = True)
	ses.page = ses.basket()
	return redirect(url_for("runtime"))
"""
		

"""

@app.route('/call_from_paygate', methods=['POST',"GET"])
def call_from_paygate():
	ses = server.ses()
	KEY = int(0)
	try:
		KEY = str(request.args["id"])
	except:
		return int(0) #<-- WRONG KEY.
	try:		
		if button_id[0] == "/":
			button_id = button_id[1:] 
	except: 
		pass
	try:		
		KEY = int(KEY) 
	except: 
		pass
	ses.basket.GET_PAY(KEY,finish = True)
	ses.page = ses.basket()
	return redirect(url_for("runtime"))
"""
		
				

#====================================================



#__RUN_WEB_APP_FROM_CALLING_app.py___
if __name__ == '__main__':
	app.run(threaded=True,host="0.0.0.0",port = config["port"])#, debug = True)





