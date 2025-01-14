#===(make_style.py)================
#==================================
import os 
import tools
#----------------------------------
def generate_style(new_stat=True,pr=True):
	try:
	#if True == True:
		path = os.getcwd()+"/"
		wk = tools.operator()
		files = wk.get_files(path+"style_templates/")
		#print(files)
		os.system("touch "+path+"style.css")
		data = list()
		for item in files:
			data.append(wk.load_text(path+"style_templates/"+str(item)))
		style = "<style>   "
		mez = "   "
		for item in data:
			style = style + mez +str(item) 
		style = style + "   </style>"	
		#print(style)
		#----------------------------------
		os.system("cp "+path+"static/style.css "+path+"static/style_old.css")
		#----------------------------------
		os.system("touch "+path+"style.css")	
		wk.save_text(style,"style", ".css")	
		#----------------------------------
		os.system("cp "+path+"style/style.css "+path+"style/style_old.css")
		#----------------------------------
		if new_stat == True:
			os.system("mv "+path+"style.css "+path+"static/style.css")
		else:
			pass
		#----------------------------------
		#os.system("rm "+path+"style.css")
		#----------------------------------
		if pr == True:
			print("   --> Style genrated:")
			print("      --> style_old.css = style.css")
			print("      --> style.css = generate_style()")
	except:
		if pr == True:
			print("   --> Style genrated ERROR.")
			print("      --> style_old.css = style.css")
			print("      --> style.css = style.css")
	return style
#----------------------------------
if __name__ == "__main__":
	generate_style()
	print("--> make_style() executed...")
#==================================