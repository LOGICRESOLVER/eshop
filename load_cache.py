import os
from cache import cache
from tools import operator



def update_indexs(item,cat,storage):
	try:
		category_dict = dict()
		category_list 
		if cat in (storage["category_dict"]).keys():
			for cat_ in storage["category_dict"].keys():
				if cat_ == cat:
					(storage["category_dict"]).update({cat:(storage["category_dict"][cat]).append(item)})		 
		else:
			(storage["category_dict"]).update({cat:[item]})
	except: 
		pass
	return storage	


def upload_new_data():
	print(" - Loading new data from ./PRODUCTS/...")
	#---------------------
	wk = operator()
	path = os.getcwd()+"/"
	products_list = wk.get_files(path+"PRODUCTS/")
	dr = []
	for item in products_list:
		if "." in item:
			dr.append(item)
	for item in dr:
		products_list.remove(item)
	#print(products_list)
	#---------------------
	storage = cache()
	storage.load_data(path+"data/storage.pickle")
	#---------------------
	cond = {"cat","price","dosage","num","short_text"}
	num_stat = {"price","dosage","num"}
	for item in products_list:
		#print("   --> ITEM LOAP; ITEM: "+str(item))
		if True == True:#try:
			metadata = wk.import_json_file(path,path+"PRODUCTS/"+str(item)+"/",item)
			for it in cond:
				if not(it in metadata):
					break	
				else:
					pass
					#NEXT_CODE_IS_OK_WITH_COND:
			#print("-------")
			#for key in metadata.keys():
			#	print(str(key)+" --- "+str(metadata[key]))
			#print("-------")
			cat = metadata["cat"]
			os.system("mkdir "+path+"data/items_data/")
			os.system("mkdir "+path+"data/items_data/"+str(cat))
			os.system("mkdir "+path+"data/items_data/"+str(cat)+"/"+str(item))
			os.system("mkdir "+path+"static/")
			dir_list = wk.get_files(path+"PRODUCTS/"+str(item)+"/")
			img = ""
			for item_ in dir_list:
				if ".jpg" in item_:
					os.system("cp "+path+"PRODUCTS/"+str(item)+"/"+item_+" "+path+"data/items_data/"+str(cat)+"/"+str(item)+"/"+str(item)+".jpg")
				if ".jpeg" in item_:
					os.system("cp "+path+"PRODUCTS/"+str(item)+"/"+item_+" "+path+"data/items_data/"+str(cat)+"/"+str(item)+"/"+str(item)+".jpg")
				if ".png" in item_:
					os.system("cp "+path+"PRODUCTS/"+str(item)+"/"+item_+" "+path+"data/items_data/"+str(cat)+"/"+str(item)+"/"+str(item)+".png")
				if ".jpg" in item_:
					os.system("cp "+path+"PRODUCTS/"+str(item)+"/"+item_+" "+path+"static/"+str(item)+".jpg")
				if ".jpeg" in item_:
					os.system("cp "+path+"PRODUCTS/"+str(item)+"/"+item_+" "+path+"static/"+str(item)+".jpg")
				if ".png" in item_:
					os.system("cp "+path+"PRODUCTS/"+str(item)+"/"+item_+" "+path+"static/"+str(item)+".png")
				img = item_
			storage.update({"img_"+str(item):"static/"+str(img)})
			for item_ in dir_list:
				if ".txt" in item_:
					os.system("cp "+path+"PRODUCTS/"+str(item)+"/"+item_+" "+path+"data/items_data/"+str(cat)+"/"+str(item)+"/"+str(item)+".txt")
					storage.update({"temp_"+str(item):wk.load_text(path+"PRODUCTS/"+str(item_))})
			for it in cond:
				if it in num_stat:
					storage.update({str(it)+"_"+str(item):int(metadata[it])})
				else: 
					storage.update({str(it)+"_"+str(item):str(metadata[it])})
			storage.update({"temp_"+str(item):wk.load_text(path+"data/items_data/"+str(cat)+"/"+str(item)+"/"+str(item)+".txt")})
			storage = update_indexs(item,cat,storage)
		else:#except:
			pass
	#---------------------
	storage.save_data(path+"data/storage.pickle")
	print("   --> Items from ./PRODUCTS/* success imported.")
	print("   --> data/storage.pickle uploaded.")
	return storage



class inst:
	def __init__(self,attributes,values):
		storage = cache()
		storage.get_class_constructor(inst,self,attributes,values)



def custome(attributes,values,worker,path):		
#========================
	attributes.append("temp_button")
	values.append(worker.load_text(path+"templates/"+"button.txt"))
	#------------------------
	attributes.append("temp_sub_button")
	values.append(worker.load_text(path+"templates/"+"sub_button.txt"))
	#------------------------
	attributes.append("temp_menu_cat")
	values.append(worker.load_text(path+"templates/"+"template_menu_cat.txt"))
	#------------------------
	attributes.append("temp_main_page")
	values.append(worker.load_text(path+"templates/"+"main.txt"))
	#------------------------
	attributes.append("temp_navbar")
	values.append(worker.load_text(path+"templates/"+"nav_bar.txt"))
	#------------------------
	attributes.append("temp_style")
	values.append(worker.load_text(path+"static/"+"style.css"))
	#------------------------
	attributes.append("temp_menu")
	values.append(worker.load_text(path+"templates/"+"menu.txt"))
	#------------------------
	attributes.append("temp_index")
	values.append(worker.load_text(path+"templates/"+"index.txt"))
	#------------------------
	attributes.append("temp_main")
	values.append(worker.load_text(path+"templates/"+"main.txt"))
	#------------------------
	cat_list = worker.get_files(path+"data/items_data/")
	attributes.append("category_list")
	values.append(cat_list)
	#------------------------
	cat_dict = dict()
	for cat in cat_list:
		cat_items = worker.get_files(path+"data/items_data/"+str(cat)+"/")
		for item in cat_items:
			if "." in cat_items:
				cat_items.remove(item)


		cat_dict.update({str(cat):cat_items})	
	attributes.append("category_dict")
	values.append(cat_dict)
	#------------------------
	for cat in cat_list:
		for item in cat_dict[cat]:
			attributes.append("path_"+str(item))
			values.append(path+"data/items_data/"+str(cat)+"/"+str(item)+"/")
			attributes.append("temp_"+str(item))
			values.append(worker.load_text(path+"data/items_data/"+str(cat)+"/"+str(item)+"/"+str(item)+".txt"))
	#------------------------
	for cat in cat_list:
		attributes.append("path_"+str(cat))
		values.append(path+"data/items_data/"+str(cat)+"/")
		attributes.append("temp_"+str(cat))
		values.append(worker.load_text(path+"data/items_data/"+str(cat)+"/"+str(cat)+".txt"))
	#------------------------
	cat_list = worker.get_files(path+"data/category_data/")
	for item in cat_list:
		attributes.append("temp_"+str(item))
		values.append(worker.load_text(path+"data/category_data/"+str(item)+"/"+str(item)+".txt"))
	#------------------------
	attributes.append("temp_nav_bar")
	values.append(worker.load_text(path+"templates/temp_nav_bar.txt"))
	#------------------------
	attributes.append("path_img_banner")
	values.append(worker.load_text("/data/images/path_img_banner.jpg"))
	#------------------------
	attributes.append("path_img_basket")
	values.append(worker.load_text("/data/images/path_img_basket.jpg"))
	#------------------------
	attributes.append("temp_out_menu")
	values.append(worker.load_text(path+"templates/temp_out_menu.txt"))
	#------------------------
	attributes.append("temp_basket")
	values.append(worker.load_text(path+"templates/temp_basket.txt"))
	#------------------------
	#========================
	return(attributes,values)




def read_stat(path,descriptor):
	if not(".csv" in descriptor):
		return None
	dt = dict()
	worker = operator()
	csv = worker.read_csv(path+descriptor)
	row = csv[0]
	label = csv[1]
	dt = dict()
	for item in csv[0]:
			for j in range(1,len(label)-1):
				#print(str(label[j])+"_"+str(item[0])+"    "+item[j])
				dt.update({label[j]+"_"+item[0]:item[j]})
	return dt
	


def init_storage_2():
	path = os.getcwd()+"/"
	storage = cache()
	storage.load_data(path+"data/storage.pickle")
	dt = read_stat(path,"data/stat.csv")
	for key in dt.keys():
		storage.update({key:dt[key]})
	storage.save_data(path+"data/storage.pickle")
	return storage


def init_storage():
	attributes = []
	values = []
	worker = operator()
	path = os.getcwd()+"/"
	attributes,values = custome(attributes,values,worker,path)
	x = "..."
	linker = inst(["x"],[x])
	storage = cache()
	storage.load_data(path+"data/storage.pickle")
	storage.import_data(attributes,values)
	storage.save_data(path+"data/storage.pickle")
	return storage



def load_all_templates():
	path = os.getcwd()+"/"
	storage = cache()
	storage.load_data(path+"data/storage.pickle")
	from tools import operator
	wk = operator()	
	files = wk.get_files(path+"templates/")
	name = ""
	txt = ""
	for item in files:
		if "temp_" in str(item):
			name = (str(item))[0:(str(item)).index(".")]
			txt = wk.load_text(path+"templates/"+item)
			storage.update({name:str(txt)})
	storage.save_data(path+"data/storage.pickle")
	print("   --> Templates success upload to cache.")
	return None


def load_javascript():
	print()
	try:
		path = os.getcwd()+"/"
		storage = cache()
		storage.load_data(path+"data/storage.pickle")
		os.system("cp -r " + path + "javascript/* " + path + "static/") 
		wk = operator()	
		files = wk.get_files(path+"javascript/")
		for item in files:
			if ".js" in item:
				js_txt = wk.load_text(path + "javascript/" + item)
				print("js_"+wk.get_name(item))
				storage.update({"js_"+wk.get_name(item):str(js_txt)})
			else:
				pass
		storage.save_data(path+"data/storage.pickle")
		print("   --> Javascript copy: ./javascript/* --> ./static/")
		print("   --> Javascript upload to storage (cache class).")
		return None
	except:
		pass



if __name__ == "__main__":
	print(" - init storage: ./data/storage.pickle")
	#print(storage["category_dict"])
	init_storage()
	storage = init_storage_2()
	upload_new_data()
	load_all_templates()
	load_javascript()
	#storage = upload_new_data()
	#print(storage["category_dict"])
	print("   -->storage loaded...")

