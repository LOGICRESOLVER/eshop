import os
import pickle
import re
import csv
import json


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
				try:
					temp = temp.replace("{{"+str(item)+"}}", str(data[item]))					
				except:
					temp = self.temp
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






class operator():
	#class for operation with files.





	def __init__(self): 
		self.pack_format = "tar.gz"		



	def repair_id(self,url_id):
		out = ""
		url_id = str(url_id)
		if url_id[0] == "/":
			out = url_id[1:]
		else:
			out = url_id
		return out




	def import_json_file(self,path,x_path,name):
		os.chdir(x_path)
		file_ = open(str(name)+".json")
		json_data = json.load(file_)
		data = dict(json_data)
		data = data["metadata"]
		os.chdir(path)
		return data 



	def read_csv(self,file_):
		rows = []
		with open(file_, 'r') as file:
			csvreader = csv.reader(file)
			header = next(csvreader)
			for row in csvreader:
				rows.append(row)
		return (rows,header)



	def get_zip(self,in_path,of_path,name):
		try:		
			#print("tar -czf "+str(of_path)+str(name)+" "+str(in_path)+"*")
			os.system("tar -czf "+str(of_path)+str(name)+" "+str(in_path)+"*")
			return True
		except:
			return False

	def make_backup(self,in_path = "", out_path = ""):
		in_path = in_path 
		of_path = out_path
		now = str(datetime.datetime.now())
		name = "backup_"+str(now)+".tar.gz"
		try:
			self.get_zip(in_path,out_path,name)
		except:
			print("   -->Error: make_backup()")
		return None



	def path_name(self,path):		
		if not(path[-1]=="/"):
			print("   -->Error path_name()")
			return ""
		else:
			ind = len(path)
		indx = list()
		for j in range(0,ind):
			if path[j] == "/":
				indx.append(int(j))
		name = path[indx[-2]+1:indx[-1]]
		return name



	@staticmethod
	def get_name(name,symb="."):
		if symb in name:
			name = name[0:name.index(symb)]
			return name
		else:
			return name


	@staticmethod
	def get_files(path):
		list_dir = os.listdir(str(path))
		return list_dir

	"""
	@staticmethod
	def save_text(text,file_,):		
		#lines = self.get_lines(text)			
		with open(str(file_), "w") as f:
			for sm in text:		
				f.write(str(sm))
		return True
	"""


	def save_text(self,text,file_,format_= ".txt"):
		with open(file_+format_, 'w') as f:
		    f.write(text)
		return(None)
	
	def load_text(self,file_path):
		try:	
			text = ""		
			with open(file_path, "r") as f:
				text = str(f.read())
			return text
		except:
			return ""

	"""
	def save_pickle(self,file_):
		try:		
			with open(str(file_), 'wb') as handle:
				pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)
		except Exception as ex:
			print("   -->ERROR: save pickle data, er_var: "+str(ex))
		return None
	"""


	def save_pickle(self,file_,data):
		try:		
			with open(str(file_), 'wb') as handle:
				pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
		except Exception as ex:
			print("   -->ERROR: save pickle data, er_var: "+str(ex))
		return None	
	"""
	def load_pickle(self,file_):
		try:
			with open(str(file_), 'rb') as handle:
				self.data = pickle.load(handle)
		except Exception as ex:
			print("   -->ERROR: load pickle data, er_var: "+str(ex))
		return None
	"""


	def load_pickle(self,file_):
		try:
			with open(str(file_), 'rb') as handle:
				data = pickle.load(handle)
		except Exception as ex:
			print("   -->ERROR: load pickle data, er_var: "+str(ex))
		return data


	def find_vars(self,temp):
		return self.find_between(temp, "{{", "}}")
		
	
	def find_between(self,s, first, last):		
		try:
			regex = rf'{first}(.*?){last}'
			return re.findall(regex, s)
		except ValueError:
			return -1



#___CLASS__Transmiter.___
	#================================================
import requests
from http.cookies import SimpleCookie
from flask import request

class Transmiter:

	#__slots__ = ("IN_URL","OUT_URL","secret_key")

	def __init__(self,IN_URL,OUT_URL,secret_key="",app=None,key_map = set(),HTTP_SELF = None):
		#GENERAL vars:
		#	IN_URL, OUT_URL, secret_key. 
		#FLASK vars:
		#	app, key_map.
		#HTTPD vars:
		#	HTTP_SELF.
		#...................
		self.IN_URL = IN_URL
		self.OUT_URL = OUT_URL
		self.secret_key = secret_key
		self.app = app
		self.key_map = key_map
		if HTTP_SELF == None:
			pass
		else:
			for key in HTTP_SELF.__dict__.keys():
				setattr(self,key,HTTP_SELF.__dict__[key])


	#__IN___
	#------------------------
	def IN(self,MODE = None):
		#MODE = True....-->...FLASK.
		#MODE = False...-->...HTTPD.
		if MODE == True:
			print("   -->Downloaded incoming data.")
			return self.flask_adapter			
		elif MODE == False:
			print("   -->Downloaded incoming data.")
			self.IN_HTTPD
		else:
			print("   --> Class Transmiter, self.IN(): Error: Not choice self.IN() mode.")
			self.__pass__

	def __pass__(self):
		return dict()
	#------------------------


		
	#__OUT__
	#------------------------
	def OUT(self,data,KEY = ""):
		print("   -->Uploaded data.")
		if KEY == "":
			KEY = str(data["KEY"]) 
		else:	
			pass
		ENDPOINT = self.OUT_URL + KEY       
		res = requests.get(url=ENDPOINT, cookies = data)
		return(res)
	#------------------------		                                                                                                                                                                                                                                               



	#__FLASK_IN__
	#------------------------
	#this code must be included in to main app.
	#@(self.app).route('/IN/<key>', methods=['POST',"GET"])
	def flask_adapter(self,key):
		KEY_FROM_URL = str(key)
		req = request
		return self.IN_FLASK(KEY_FROM_URL,req)

	def IN_FLASK(self,KEY_FROM_URL,req):		
		data = dict()
		for key in self.key_map:
			try:
				val = str(req.cookies.get(str(key)))
				data.update({str(key):str(val)})
			except: 
				pass
		if not "KEY" in data.keys():
			data.update({"KEY":KEY_FROM_URL})
		return(data)
	#------------------------



	#__HTTPD__		
	#------------------------
	#This code must be included to self.do_GET()
	def IN_HTTPD(self):
		if not(self.IN_URL in self.path):
			return dict()
		stack = dict()
		cookies = SimpleCookie(self.headers.get("Cookie"))
		keys_ = cookies.keys()
		for key in keys_:
			try:
				stack.update({key:str((cookies[key]).value)})
			except:
				pass
		stack_2 = dict()
		for key in stack.keys():
			try:
				stack_2.update({str(key):str(stack[key])})
			except:
				pass
		if not("KEY" in stack_2.keys()):
			stack_2.update({"KEY":(self.path)[((self.path).rindex("/IN/"))+4:]})
		return stack_2
	#------------------------



	#__SUPPORT_FUNCTIONS__
	#------------------------
	def encript(self,data):
		return data

	def deencript(self,data):
		return data
	#------------------------		
	#================================================







def load_images(path):
	#for img in operator.get_files(path+"data/images/"):
	#	app.send_static_file(path+"data/images/"+str(img))
	os.system("cp -r "+path+"data/images/* "+path+"static/")
	print("-->Images copy to static/*.")
	return None	



