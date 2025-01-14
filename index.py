import os
path = os.getcwd()+"/"
try:
	os.system("python3 app.py")
except:	
	pass
try:
	os.system("python3 "+path+"app.py")
except:	
	pass
