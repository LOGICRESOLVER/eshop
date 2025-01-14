from cache import cache
storage = cache()
storage.load_data("data/storage.pickle")
print(" - Write storage key, for print storage[key]: ")
key = input("   --> Enter KEY: ")
try:
	print("   --> "+str(storage[str(key)]))
except:
	print("   --> Value for this key not-existed.")
print(type(storage["category_dict"]))