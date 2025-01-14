import os


def get_setup():
	path = os.getcwd()+"/"
	os.system("rm "+path+"data/storage.pickle")
	from load_cache import init_storage, init_storage_2, upload_new_data, load_all_templates, load_javascript
	init_storage()
	storage = init_storage_2()
	upload_new_data()
	load_all_templates()
	load_javascript()
	#---------------------
	from cache import cache
	from make_style import generate_style
	_style_ = generate_style()
	storage = cache()
	storage.load_data(path + "data/storage.pickle")
	storage.update({"style":_style_})
	storage.save_data(path + "data/storage.pickle")	
	#---------------------
	from tools import load_images
	load_images(path)
	#---------------------
	return None


if __name__ == "__main__":
	print("__RUN SERVER SETUP APP__:")
	get_setup()